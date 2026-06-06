#!/usr/bin/env python3
"""
DBOS AI Image Generator
Generates category-specific images using OpenAI DALL-E API
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

@dataclass
class GeneratedImage:
    """Represents a generated image"""
    name: str
    category: str
    prompt: str
    filename: str
    path: str
    size: str
    model: str
    generated_at: str
    success: bool
    error: Optional[str] = None

class AIImageGenerator:
    """Generate images using OpenAI DALL-E API"""
    
    # OpenAI Configuration
    OPENAI_API_URL = "https://api.openai.com/v1/images/generations"
    IMAGE_MODEL = "dall-e-3"
    IMAGE_SIZE = "1024x1024"
    
    # Category Prompts - Tailored for each technical domain
    CATEGORY_PROMPTS = {
        "python": (
            "Modern Python programming environment: glowing code syntax with colorful brackets, "
            "nested function structures, elegant developer workspace with terminal windows, "
            "minimalist tech aesthetic, clean backgrounds, production-grade code editor interface"
        ),
        
        "data-engineering": (
            "Data engineering pipeline visualization: flowing data streams between databases, "
            "ETL workflow diagram with arrows and transformations, analytics dashboards with graphs, "
            "database clusters, modern data architecture, clean technical diagram style"
        ),
        
        "ai": (
            "Artificial intelligence neural networks: futuristic brain with glowing neural connections, "
            "interconnected nodes with flowing data, machine learning visualization, "
            "modern AI aesthetic with gradients and neon accents, abstract technical beauty"
        ),
        
        "cloud": (
            "Cloud computing infrastructure: distributed cloud services, connected servers, "
            "cloud architecture diagram, microservices mesh, serverless computing visualization, "
            "modern cloud-native design, clean technical illustration"
        ),
        
        "devops": (
            "CI/CD pipeline visualization: continuous integration and deployment workflow, "
            "Kubernetes container orchestration, automation pipelines, monitoring dashboards, "
            "DevOps tools ecosystem, modern infrastructure as code aesthetic"
        ),
        
        "sql": (
            "Database systems and SQL: relational database tables with structured data, "
            "SQL query results visualized, database schema diagrams, analytics tables, "
            "structured data organization, modern database design illustration"
        ),
        
        "api": (
            "API integration and microservices: REST API endpoints, connected systems communicating, "
            "API gateway architecture, microservices communication patterns, data exchange visualization, "
            "modern API design, technical integration diagram"
        ),
        
        "etl": (
            "ETL pipeline architecture: Extract-Transform-Load workflow visualization, "
            "data extraction from sources, transformation logic, loading into data warehouse, "
            "pipeline flow diagram, modern ETL design with interconnected stages"
        ),
        
        "airflow": (
            "Apache Airflow DAG orchestration: directed acyclic graph with tasks and dependencies, "
            "workflow orchestration visualization, scheduled pipeline execution, "
            "Airflow UI dashboard style, modern workflow automation aesthetic"
        ),
        
        "kubernetes": (
            "Kubernetes container orchestration: containerized microservices, pod deployments, "
            "k8s cluster architecture, container networking, orchestration dashboard, "
            "modern container infrastructure, scalable deployment visualization"
        ),
        
        "monitoring": (
            "System monitoring and observability: real-time dashboards with metrics and graphs, "
            "monitoring alerts and notifications, log aggregation visualization, "
            "performance metrics display, modern observability platform aesthetic"
        ),
        
        "testing": (
            "Software testing and quality assurance: automated test execution, test coverage metrics, "
            "quality gates visualization, testing framework integration, test results dashboard, "
            "modern QA automation aesthetic"
        )
    }
    
    DEFAULT_PROMPT = (
        "Modern abstract developer technology background: clean minimal tech aesthetic, "
        "futuristic design, glowing elements, productivity tools, development environment, "
        "professional software engineering workspace"
    )
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.output_dir = Path("assets/auto/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.generation_log_file = Path("assets/auto/generation-log.json")
        self.image_mapping_file = Path("assets/auto/generated-images.json")
        
        self.generation_stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "model": self.IMAGE_MODEL,
            "size": self.IMAGE_SIZE,
            "total_requested": 0,
            "total_generated": 0,
            "total_failed": 0,
            "images": {},
            "errors": []
        }
        
        self.generated_images: Dict[str, GeneratedImage] = {}
    
    def validate_api_key(self) -> bool:
        """Validate OpenAI API key is available"""
        if not self.api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            print("   Set it with: export OPENAI_API_KEY='your-key-here'")
            self.generation_stats["errors"].append("Missing OpenAI API key")
            return False
        
        if not self.api_key.startswith("sk-"):
            print("⚠️  API key format looks incorrect (should start with 'sk-')")
        
        return True
    
    def generate_image(self, category: str, prompt: str, filename: str) -> Optional[GeneratedImage]:
        """Generate single image via OpenAI API"""
        
        self.generation_stats["total_requested"] += 1
        
        try:
            print(f"🎨 Generating {category}...", end=" ")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.IMAGE_MODEL,
                "prompt": prompt,
                "size": self.IMAGE_SIZE,
                "quality": "standard",
                "n": 1
            }
            
            # Call OpenAI API
            response = requests.post(
                self.OPENAI_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                error_msg = f"API Error {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                self.generation_stats["total_failed"] += 1
                self.generation_stats["errors"].append(error_msg)
                
                return GeneratedImage(
                    name=category,
                    category=category,
                    prompt=prompt,
                    filename=filename,
                    path="",
                    size=self.IMAGE_SIZE,
                    model=self.IMAGE_MODEL,
                    generated_at=datetime.utcnow().isoformat(),
                    success=False,
                    error=error_msg
                )
            
            # Download image
            image_url = response.json()["data"][0]["url"]
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            # Save image
            file_path = self.output_dir / filename
            with open(file_path, "wb") as f:
                f.write(img_response.content)
            
            file_size_kb = file_path.stat().st_size / 1024
            
            print(f"✓ ({file_size_kb:.1f} KB)")
            
            self.generation_stats["total_generated"] += 1
            
            generated = GeneratedImage(
                name=category,
                category=category,
                prompt=prompt,
                filename=filename,
                path=f"assets/auto/generated/{filename}",
                size=self.IMAGE_SIZE,
                model=self.IMAGE_MODEL,
                generated_at=datetime.utcnow().isoformat(),
                success=True
            )
            
            return generated
            
        except requests.exceptions.Timeout:
            error_msg = "Request timeout"
            print(f"❌ {error_msg}")
            self.generation_stats["total_failed"] += 1
            self.generation_stats["errors"].append(error_msg)
            return None
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            print(f"❌ {error_msg}")
            self.generation_stats["total_failed"] += 1
            self.generation_stats["errors"].append(error_msg)
            return None
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ {error_msg}")
            self.generation_stats["total_failed"] += 1
            self.generation_stats["errors"].append(error_msg)
            return None
    
    def generate_category_images(self) -> Dict[str, str]:
        """Generate images for all categories"""
        
        print("\n🎨 GENERATING CATEGORY IMAGES\n")
        
        mapping = {}
        
        for category, prompt in self.CATEGORY_PROMPTS.items():
            filename = f"{category}.png"
            
            generated = self.generate_image(category, prompt, filename)
            
            if generated and generated.success:
                mapping[category] = generated.path
                self.generated_images[category] = generated
                self.generation_stats["images"][category] = {
                    "filename": generated.filename,
                    "path": generated.path,
                    "status": "success",
                    "generated_at": generated.generated_at
                }
            else:
                self.generation_stats["images"][category] = {
                    "status": "failed",
                    "error": generated.error if generated else "Unknown error"
                }
        
        return mapping
    
    def generate_default_image(self) -> Optional[str]:
        """Generate default fallback image"""
        
        print("\n🎯 GENERATING DEFAULT IMAGE\n")
        
        generated = self.generate_image("default", self.DEFAULT_PROMPT, "default-tech.png")
        
        if generated and generated.success:
            self.generated_images["default"] = generated
            self.generation_stats["images"]["default"] = {
                "filename": generated.filename,
                "path": generated.path,
                "status": "success",
                "generated_at": generated.generated_at
            }
            return generated.path
        else:
            self.generation_stats["images"]["default"] = {
                "status": "failed",
                "error": generated.error if generated else "Unknown error"
            }
            return None
    
    def save_mapping(self, mapping: Dict[str, str]):
        """Save image path mapping"""
        
        with open(self.image_mapping_file, 'w') as f:
            json.dump(mapping, f, indent=2)
        
        print(f"\n✓ Image mapping saved: {self.image_mapping_file}")
    
    def save_generation_log(self):
        """Save generation statistics and log"""
        
        with open(self.generation_log_file, 'w') as f:
            json.dump(self.generation_stats, f, indent=2)
        
        print(f"✓ Generation log saved: {self.generation_log_file}")
    
    def generate_generation_report(self) -> str:
        """Generate summary report"""
        
        stats = self.generation_stats
        
        report = f"""
📊 IMAGE GENERATION REPORT

Timestamp: {stats['timestamp']}
Model: {stats['model']}
Size: {stats['size']}

Summary:
  • Requested: {stats['total_requested']}
  • Generated: {stats['total_generated']}
  • Failed: {stats['total_failed']}
  • Success Rate: {stats['total_generated']/max(stats['total_requested'], 1)*100:.1f}%

Generated Images:
"""
        
        for category, image_info in stats['images'].items():
            status = image_info.get('status', 'unknown')
            if status == 'success':
                report += f"  ✓ {category}: {image_info['path']}\n"
            else:
                error = image_info.get('error', 'Unknown error')
                report += f"  ✗ {category}: {error}\n"
        
        if stats['errors']:
            report += f"\nErrors:\n"
            for error in stats['errors']:
                report += f"  • {error}\n"
        
        return report
    
    def run(self):
        """Execute image generation pipeline"""
        
        print("\n" + "="*60)
        print("🎨 DBOS AI IMAGE GENERATOR")
        print("="*60)
        
        # Validate API key
        if not self.validate_api_key():
            print("\n❌ Image generation skipped - API key not configured")
            return
        
        try:
            # Generate category images
            mapping = self.generate_category_images()
            
            # Generate default image
            default_path = self.generate_default_image()
            
            if default_path:
                mapping["default"] = default_path
            
            # Save mapping
            self.save_mapping(mapping)
            
            # Save log
            self.save_generation_log()
            
            # Print report
            report = self.generate_generation_report()
            print(report)
            
            print(f"\n✅ Image generation complete!")
            print(f"   Generated: {self.generation_stats['total_generated']} images")
            print(f"   Location: {self.output_dir}")
            print(f"   Mapping: {self.image_mapping_file}\n")
            
        except Exception as e:
            print(f"\n❌ Generation pipeline failed: {e}")
            self.generation_stats["errors"].append(str(e))
            self.save_generation_log()

if __name__ == '__main__':
    generator = AIImageGenerator()
    generator.run()
