#!/usr/bin/env python3
"""
DBOS Auto Image Library Manager
Manages and assigns images to blog posts automatically
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ImageAsset:
    """Represents an image asset in the library"""
    name: str
    path: str
    category: str
    tags: List[str]
    width: int
    height: int
    size_kb: float
    format: str
    generated: bool = False

class ImageLibraryManager:
    """Manages the auto image library"""
    
    def __init__(self):
        self.library_path = Path('assets/auto')
        self.library_config_file = Path('assets/auto/library-config.json')
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.library = self.load_library()
    
    def load_library(self) -> Dict[str, ImageAsset]:
        """Load image library configuration"""
        if self.library_config_file.exists():
            with open(self.library_config_file) as f:
                data = json.load(f)
                return {
                    name: ImageAsset(**asset) 
                    for name, asset in data.get('assets', {}).items()
                }
        return {}
    
    def save_library(self):
        """Save library configuration"""
        config = {
            "library": {
                "name": "DBOS Auto Image Library",
                "version": "1.0.0",
                "description": "Automatically assigned images for blog posts",
                "last_updated": datetime.utcnow().isoformat(),
                "total_assets": len(self.library),
                "categories": list(set(img.category for img in self.library.values())),
                "tags": list(set(tag for img in self.library.values() for tag in img.tags))
            },
            "assets": {name: asdict(asset) for name, asset in self.library.items()}
        }
        
        with open(self.library_config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def register_image(self, name: str, path: str, category: str, 
                      tags: List[str], width: int = 1200, height: int = 675,
                      size_kb: float = 0, format: str = "png", 
                      generated: bool = False) -> ImageAsset:
        """Register a new image in the library"""
        asset = ImageAsset(
            name=name,
            path=path,
            category=category,
            tags=tags,
            width=width,
            height=height,
            size_kb=size_kb,
            format=format,
            generated=generated
        )
        self.library[name] = asset
        self.save_library()
        return asset
    
    def get_default_library(self) -> Dict[str, ImageAsset]:
        """Get default library structure"""
        defaults = {
            # Technology domains
            "python": ImageAsset("python", "assets/auto/python.png", "Python", 
                               ["python", "backend"], 1200, 675, 0, "png"),
            
            "data-engineering": ImageAsset("data-engineering", 
                                          "assets/auto/data-engineering.png", 
                                          "Data Engineering", 
                                          ["data", "etl", "pipelines", "engineering"], 
                                          1200, 675, 0, "png"),
            
            "airflow": ImageAsset("airflow", "assets/auto/airflow.png", 
                                 "Data Engineering", 
                                 ["airflow", "orchestration", "etl"], 
                                 1200, 675, 0, "png"),
            
            "dbt": ImageAsset("dbt", "assets/auto/dbt.png", 
                             "Data Transformation", 
                             ["dbt", "transformation", "sql", "analytics"], 
                             1200, 675, 0, "png"),
            
            "sql": ImageAsset("sql", "assets/auto/sql.png", 
                             "Databases", 
                             ["sql", "database", "queries", "postgres"], 
                             1200, 675, 0, "png"),
            
            "kubernetes": ImageAsset("kubernetes", "assets/auto/kubernetes.png", 
                                    "Infrastructure", 
                                    ["kubernetes", "k8s", "containers", "devops"], 
                                    1200, 675, 0, "png"),
            
            "cloud-computing": ImageAsset("cloud-computing", 
                                         "assets/auto/cloud-computing.png", 
                                         "Cloud", 
                                         ["cloud", "aws", "gcp", "azure", "infrastructure"], 
                                         1200, 675, 0, "png"),
            
            "ai-ml": ImageAsset("ai-ml", "assets/auto/ai-ml.png", 
                               "AI & Machine Learning", 
                               ["ai", "ml", "machine-learning", "deep-learning"], 
                               1200, 675, 0, "png"),
            
            "api": ImageAsset("api", "assets/auto/api.png", 
                             "APIs", 
                             ["api", "rest", "graphql", "integration"], 
                             1200, 675, 0, "png"),
            
            "testing": ImageAsset("testing", "assets/auto/testing.png", 
                                 "Testing & QA", 
                                 ["testing", "qa", "quality", "pytest"], 
                                 1200, 675, 0, "png"),
            
            "monitoring": ImageAsset("monitoring", "assets/auto/monitoring.png", 
                                    "Monitoring & Observability", 
                                    ["monitoring", "observability", "logging", "metrics"], 
                                    1200, 675, 0, "png"),
            
            "git": ImageAsset("git", "assets/auto/git.png", 
                             "DevOps & Git", 
                             ["git", "github", "gitlab", "devops", "ci-cd"], 
                             1200, 675, 0, "png"),
            
            "default-tech": ImageAsset("default-tech", "assets/auto/default-tech.png", 
                                      "Technology", 
                                      ["default", "technology", "development"], 
                                      1200, 675, 0, "png"),
        }
        
        return defaults
    
    def initialize_default_library(self):
        """Initialize library with default images"""
        defaults = self.get_default_library()
        
        for name, asset in defaults.items():
            if name not in self.library:
                self.library[name] = asset
        
        self.save_library()
        print(f"✓ Initialized {len(self.library)} default images")
    
    def get_library_stats(self) -> Dict:
        """Get library statistics"""
        categories = {}
        tags_count = {}
        
        for asset in self.library.values():
            cat = asset.category
            categories[cat] = categories.get(cat, 0) + 1
            
            for tag in asset.tags:
                tags_count[tag] = tags_count.get(tag, 0) + 1
        
        return {
            "total_images": len(self.library),
            "categories": categories,
            "total_tags": len(tags_count),
            "most_common_tags": sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10],
            "categories_covered": list(categories.keys())
        }
    
    def get_images_by_category(self, category: str) -> List[ImageAsset]:
        """Get all images in a category"""
        return [img for img in self.library.values() if img.category == category]
    
    def get_images_by_tag(self, tag: str) -> List[ImageAsset]:
        """Get all images with a specific tag"""
        return [img for img in self.library.values() if tag in img.tags]
    
    def get_library_summary(self) -> Dict:
        """Get library summary for dashboard"""
        stats = self.get_library_stats()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "library_size": len(self.library),
            "categories": len(stats["categories"]),
            "stats": stats,
            "categories_breakdown": [
                {
                    "category": cat,
                    "count": count,
                    "images": [img.name for img in self.get_images_by_category(cat)]
                }
                for cat, count in sorted(stats["categories"].items(), key=lambda x: x[1], reverse=True)
            ]
        }
    
    def run(self):
        """Initialize library"""
        print("\n🎨 DBOS Image Library Manager\n")
        
        self.initialize_default_library()
        
        stats = self.get_library_stats()
        print(f"✓ Total Images: {stats['total_images']}")
        print(f"✓ Categories: {len(stats['categories'])}")
        print(f"✓ Tags: {stats['total_tags']}")
        
        print("\nCategories:")
        for cat, count in sorted(stats["categories"].items(), key=lambda x: x[1], reverse=True):
            print(f"  • {cat}: {count} images")
        
        print(f"\n✅ Image Library initialized!\n")

if __name__ == '__main__':
    manager = ImageLibraryManager()
    manager.run()
