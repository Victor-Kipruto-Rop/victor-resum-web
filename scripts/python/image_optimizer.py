#!/usr/bin/env python3
"""
DBOS Image Optimizer
Optimizes images for web: compression, format conversion, responsive sizing
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import mimetypes
import os

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("⚠️  Pillow not installed. Install with: pip install Pillow")

class ImageOptimizer:
    """Optimize images for web delivery"""
    
    # Configuration
    TARGET_SIZE_KB = 100  # Target file size for web
    QUALITY_LEVELS = {
        "high": 85,
        "medium": 75,
        "low": 65
    }
    
    # Responsive breakpoints
    BREAKPOINTS = {
        "desktop": 1200,
        "tablet": 600,
        "mobile": 400
    }
    
    # Output formats
    FORMATS = {
        "webp": {"quality": 85, "method": 6},
        "jpeg": {"quality": 80},
        "png": {"optimize": True, "compress_level": 9}
    }
    
    def __init__(self):
        self.library_dir = Path('assets/auto')
        self.optimized_dir = self.library_dir / 'optimized'
        self.optimized_dir.mkdir(parents=True, exist_ok=True)
        self.optimization_log_file = self.library_dir / 'optimization-log.json'
        self.optimization_stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "images_processed": 0,
            "images_optimized": 0,
            "total_original_size": 0,
            "total_optimized_size": 0,
            "compression_rate": 0.0,
            "details": []
        }
    
    def detect_format(self, image_path: str) -> str:
        """Detect optimal format based on content"""
        if not PILLOW_AVAILABLE:
            return "jpeg"
        
        try:
            with Image.open(image_path) as img:
                # Use WebP for modern browsers, PNG for transparency
                if img.mode in ('RGBA', 'LA', 'P'):
                    return "png"  # Preserve transparency
                else:
                    return "webp"  # Modern format with better compression
        except Exception as e:
            print(f"⚠️  Error detecting format for {image_path}: {e}")
            return "jpeg"
    
    def compress_image(self, input_path: Path, quality: str = "medium") -> Optional[bytes]:
        """Compress image to target size"""
        if not PILLOW_AVAILABLE:
            return None
        
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                
                # Get quality level
                quality_val = self.QUALITY_LEVELS.get(quality, self.QUALITY_LEVELS["medium"])
                
                # Save to bytes
                output = None
                format_to_use = self.detect_format(str(input_path))
                
                if format_to_use == "webp":
                    output = self._save_webp(img, quality_val)
                elif format_to_use == "png":
                    output = self._save_png(img)
                else:
                    output = self._save_jpeg(img, quality_val)
                
                return output
        except Exception as e:
            print(f"⚠️  Error compressing {input_path}: {e}")
            return None
    
    def _save_webp(self, img: 'Image.Image', quality: int) -> bytes:
        """Save image as WebP"""
        from io import BytesIO
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality, method=6)
        return output.getvalue()
    
    def _save_png(self, img: 'Image.Image') -> bytes:
        """Save image as PNG"""
        from io import BytesIO
        output = BytesIO()
        img.save(output, format='PNG', optimize=True, compress_level=9)
        return output.getvalue()
    
    def _save_jpeg(self, img: 'Image.Image', quality: int) -> bytes:
        """Save image as JPEG"""
        from io import BytesIO
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
    
    def generate_responsive_sizes(self, input_path: Path) -> Dict[str, Path]:
        """Generate responsive versions of image"""
        if not PILLOW_AVAILABLE:
            return {}
        
        results = {}
        
        try:
            with Image.open(input_path) as img:
                original_width, original_height = img.size
                
                # Calculate aspect ratio
                aspect_ratio = original_width / original_height if original_height > 0 else 1.0
                
                for breakpoint, width in self.BREAKPOINTS.items():
                    # Skip if original is smaller
                    if width > original_width:
                        continue
                    
                    height = int(width / aspect_ratio)
                    
                    # Resize
                    resized = img.resize((width, height), Image.Resampling.LANCZOS)
                    
                    # Save
                    stem = input_path.stem
                    ext = input_path.suffix.lower()
                    output_filename = f"{stem}-{breakpoint}{ext}"
                    output_path = self.optimized_dir / output_filename
                    
                    resized.save(output_path, quality=85, optimize=True)
                    results[breakpoint] = output_path
        except Exception as e:
            print(f"⚠️  Error generating responsive sizes for {input_path}: {e}")
        
        return results
    
    def strip_metadata(self, input_path: Path) -> Optional[Path]:
        """Strip EXIF and metadata from image"""
        if not PILLOW_AVAILABLE:
            return input_path
        
        try:
            with Image.open(input_path) as img:
                # Create new image without metadata
                data = list(img.getdata())
                img_without_exif = Image.new(img.mode, img.size)
                img_without_exif.putdata(data)
                
                # Save
                output_path = self.optimized_dir / input_path.name
                img_without_exif.save(output_path, optimize=True)
                
                return output_path
        except Exception as e:
            print(f"⚠️  Error stripping metadata from {input_path}: {e}")
            return None
    
    def optimize_image(self, input_path: Path, quality: str = "medium") -> Dict:
        """Complete optimization pipeline for single image"""
        result = {
            "name": input_path.name,
            "status": "failed",
            "original_size": 0,
            "optimized_size": 0,
            "compression_rate": 0.0,
            "format": "unknown",
            "versions": {},
            "metadata": {}
        }
        
        if not input_path.exists():
            result["error"] = f"File not found: {input_path}"
            return result
        
        try:
            original_size = input_path.stat().st_size
            result["original_size"] = original_size
            
            # Detect format
            detected_format = self.detect_format(str(input_path))
            result["format"] = detected_format
            
            # Compress main image
            compressed_data = self.compress_image(input_path, quality)
            
            if compressed_data:
                # Save optimized version
                output_path = self.optimized_dir / input_path.name
                with open(output_path, 'wb') as f:
                    f.write(compressed_data)
                
                optimized_size = len(compressed_data)
                result["optimized_size"] = optimized_size
                result["compression_rate"] = 1.0 - (optimized_size / original_size)
                result["versions"]["full"] = str(output_path)
                result["status"] = "optimized"
                
                # Generate responsive versions
                responsive_versions = self.generate_responsive_sizes(input_path)
                for breakpoint, path in responsive_versions.items():
                    result["versions"][breakpoint] = str(path)
                
                result["metadata"] = {
                    "target_size_kb": self.TARGET_SIZE_KB,
                    "quality": quality,
                    "breakpoints": list(self.BREAKPOINTS.keys()),
                    "format": detected_format
                }
            else:
                result["status"] = "compression_failed"
        
        except Exception as e:
            result["error"] = str(e)
            result["status"] = "error"
        
        return result
    
    def optimize_library(self, quality: str = "medium") -> Dict:
        """Optimize all library images"""
        print("🖼️  Optimizing image library...\n")
        
        # Load library config
        library_config_file = self.library_dir / 'library-config.json'
        
        if not library_config_file.exists():
            print("⚠️  Library config not found. Run image_library_manager.py first.")
            return self.optimization_stats
        
        with open(library_config_file) as f:
            library_config = json.load(f)
        
        # Optimize each image
        for asset_name, asset_info in library_config.get('assets', {}).items():
            image_path = Path(asset_info.get('path'))
            
            if not image_path.is_absolute():
                image_path = Path.cwd() / image_path
            
            if not image_path.exists():
                print(f"⊘ {asset_name}: File not found at {image_path}")
                continue
            
            print(f"📦 Optimizing {asset_name}...")
            
            # Optimize
            result = self.optimize_image(image_path, quality)
            
            # Display result
            if result["status"] == "optimized":
                compression_pct = result["compression_rate"] * 100
                print(f"   ✓ {result['name']}")
                print(f"     • Original: {result['original_size'] / 1024:.1f} KB")
                print(f"     • Optimized: {result['optimized_size'] / 1024:.1f} KB")
                print(f"     • Compression: {compression_pct:.1f}%")
                print(f"     • Format: {result['format']}")
                print(f"     • Versions: {list(result['versions'].keys())}")
                
                self.optimization_stats["images_optimized"] += 1
                self.optimization_stats["total_original_size"] += result["original_size"]
                self.optimization_stats["total_optimized_size"] += result["optimized_size"]
            else:
                print(f"   ✗ {result['name']}: {result.get('error', result['status'])}")
            
            self.optimization_stats["images_processed"] += 1
            self.optimization_stats["details"].append(result)
        
        # Calculate overall compression rate
        if self.optimization_stats["total_original_size"] > 0:
            self.optimization_stats["compression_rate"] = 1.0 - (
                self.optimization_stats["total_optimized_size"] /
                self.optimization_stats["total_original_size"]
            )
        
        return self.optimization_stats
    
    def save_optimization_log(self):
        """Save optimization results"""
        with open(self.optimization_log_file, 'w') as f:
            json.dump(self.optimization_stats, f, indent=2)
        
        print(f"\n✓ Optimization log saved: {self.optimization_log_file}")
    
    def generate_optimization_report(self) -> str:
        """Generate optimization report"""
        stats = self.optimization_stats
        
        report = f"""
📊 IMAGE OPTIMIZATION REPORT

Timestamp: {stats['timestamp']}

Summary:
  • Images Processed: {stats['images_processed']}
  • Images Optimized: {stats['images_optimized']}
  • Overall Compression: {stats['compression_rate'] * 100:.1f}%

Storage Impact:
  • Original Size: {stats['total_original_size'] / (1024*1024):.2f} MB
  • Optimized Size: {stats['total_optimized_size'] / (1024*1024):.2f} MB
  • Space Saved: {(stats['total_original_size'] - stats['total_optimized_size']) / (1024*1024):.2f} MB

Optimization Details:
"""
        for detail in stats['details'][:10]:  # Show first 10
            report += f"\n  {detail['name']}:\n"
            report += f"    • Status: {detail['status']}\n"
            if detail['status'] == 'optimized':
                report += f"    • Compression: {detail['compression_rate']*100:.1f}%\n"
                report += f"    • Format: {detail['format']}\n"
                report += f"    • Versions: {', '.join(detail['versions'].keys())}\n"
        
        return report
    
    def run(self):
        """Execute image optimization"""
        print("\n🎨 DBOS Image Optimizer\n")
        
        if not PILLOW_AVAILABLE:
            print("❌ Pillow library not available")
            print("Install with: pip install Pillow")
            return
        
        # Optimize library
        stats = self.optimize_library(quality="medium")
        
        # Save log
        self.save_optimization_log()
        
        # Generate report
        report = self.generate_optimization_report()
        print(report)
        
        print("\n✅ Image optimization complete!\n")

if __name__ == '__main__':
    optimizer = ImageOptimizer()
    optimizer.run()
