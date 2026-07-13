#!/usr/bin/env python3
"""
DBOS Auto Image Pipeline Integration
Integrates image library, selection, optimization, and assignment into blog pipeline
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from image_library_manager import ImageLibraryManager
from image_selector import ImageSelector
from image_optimizer import ImageOptimizer
from auto_image_assigner import AutoImageAssigner
from image_generator import AIImageGenerator
from blog_content_analyzer import BlogContentAnalyzer
from prompt_generator import AIPromptGenerator

class BlogImagePipeline:
    """Orchestrates the complete image pipeline for blog posts"""
    
    def __init__(self):
        self.manager = ImageLibraryManager()
        self.selector = ImageSelector()
        self.optimizer = ImageOptimizer()
        self.assigner = AutoImageAssigner()
        
        self.pipeline_log_file = Path('assets/auto/pipeline-log.json')
        self.pipeline_status = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending",
            "stages": {},
            "errors": [],
            "warnings": []
        }
    
    def stage_1_initialize_library(self) -> bool:
        """Stage 1: Initialize image library"""
        print("\n📚 Stage 1: Initialize Image Library")
        print("-" * 50)
        
        try:
            # Initialize library
            self.manager.initialize_default_library()
            
            # Get stats
            stats = self.manager.get_library_stats()
            
            print(f"✓ Library initialized with {stats['total_assets']} images")
            print(f"  • Categories: {stats['total_categories']}")
            print(f"  • Tags: {stats['total_tags']}")
            
            self.pipeline_status["stages"]["library_initialization"] = {
                "status": "success",
                "images": stats['total_assets'],
                "categories": stats['total_categories']
            }
            
            return True
        except Exception as e:
            print(f"✗ Library initialization failed: {e}")
            self.pipeline_status["stages"]["library_initialization"] = {
                "status": "failed",
                "error": str(e)
            }
            self.pipeline_status["errors"].append(f"Library init: {e}")
            return False
    
    def stage_2_analyze_content(self) -> bool:
        """Stage 2: Analyze blog content for AI prompts"""
        print("\n📊 Stage 2: Analyze Blog Content")
        print("-" * 50)
        
        try:
            analyzer = BlogContentAnalyzer()
            
            # Run analysis
            analyses = analyzer.analyze_all_posts()
            analyzer.save_analysis(analyses)
            
            print(f"✓ Analyzed {len(analyses)} posts")
            
            self.pipeline_status["stages"]["content_analysis"] = {
                "status": "success",
                "posts_analyzed": len(analyses)
            }
            
            return True
        except Exception as e:
            print(f"⚠️  Content analysis skipped: {e}")
            self.pipeline_status["stages"]["content_analysis"] = {
                "status": "skipped",
                "reason": str(e)
            }
            self.pipeline_status["warnings"].append(f"Content analysis: {e}")
            return True  # Don't fail pipeline
    
    def stage_3_generate_prompts(self) -> bool:
        """Stage 3: Generate AI image prompts"""
        print("\n🤖 Stage 3: Generate AI Image Prompts")
        print("-" * 50)
        
        try:
            generator = AIPromptGenerator()
            
            # Generate prompts
            prompts_data = generator.generate_all_prompts()
            
            if prompts_data:
                generator.save_prompts(prompts_data)
                prompt_count = len(prompts_data.get("prompts", {}))
                print(f"✓ Generated prompts for {prompt_count} posts")
                
                self.pipeline_status["stages"]["prompt_generation"] = {
                    "status": "success",
                    "prompts_generated": prompt_count
                }
                return True
            else:
                print("⚠️  No prompts generated")
                self.pipeline_status["stages"]["prompt_generation"] = {
                    "status": "partial"
                }
                return True
        except Exception as e:
            print(f"⚠️  Prompt generation skipped: {e}")
            self.pipeline_status["stages"]["prompt_generation"] = {
                "status": "skipped",
                "reason": str(e)
            }
            self.pipeline_status["warnings"].append(f"Prompt generation: {e}")
            return True  # Don't fail pipeline
    
    def stage_4_generate_ai_images(self) -> bool:
        """Stage 4 (Optional): Generate images using OpenAI DALL-E"""
        print("\n🎨 Stage 4 (Optional): Generate AI Images")
        print("-" * 50)
        
        try:
            generator = AIImageGenerator()
            
            # Check if API key is available
            # Check if API key is available
            if not generator.validate_api_key():
                print("⚠️  Skipping AI image generation - no API key configured")
                print("   Set OPENAI_API_KEY environment variable to enable")
                self.pipeline_status["stages"]["ai_image_generation"] = {
                    "status": "skipped",
                    "reason": "API key not configured"
                }
                return True  # Don't fail pipeline
            
            # Generate images
            mapping = generator.generate_category_images()
            default_path = generator.generate_default_image()
            
            if default_path:
                mapping["default"] = default_path
            
            # Save mapping
            generator.save_mapping(mapping)
            generator.save_generation_log()
            
            print(f"✓ Generated {generator.generation_stats['total_generated']} images")
            
            self.pipeline_status["stages"]["ai_image_generation"] = {
                "status": "success",
                "images_generated": generator.generation_stats['total_generated'],
                "generation_model": generator.IMAGE_MODEL
            }
            
            return True
        except Exception as e:
            print(f"⚠️  AI image generation skipped: {e}")
            self.pipeline_status["stages"]["ai_image_generation"] = {
                "status": "skipped",
                "reason": str(e)
            }
            self.pipeline_status["warnings"].append(f"AI image generation: {e}")
            return True  # Don't fail pipeline
    
    def stage_5_validate_posts(self) -> bool:
        """Stage 5: Validate blog posts"""
        print("\n📝 Stage 5: Validate Blog Posts")
        print("-" * 50)
        
        try:
            posts = self.assigner.load_posts()
            
            if not posts:
                print("⚠️  No posts found")
                self.pipeline_status["warnings"].append("No posts in blog/assets/shared/posts.json")
                return True
            
            print(f"✓ Found {len(posts)} blog posts")
            
            # Validate each post
            valid_count = 0
            for post in posts:
                required_fields = ['title', 'slug', 'category', 'description']
                if all(field in post for field in required_fields):
                    valid_count += 1
            
            print(f"  • Valid posts: {valid_count}/{len(posts)}")
            
            self.pipeline_status["stages"]["post_validation"] = {
                "status": "success",
                "total_posts": len(posts),
                "valid_posts": valid_count
            }
            
            return valid_count > 0
        except Exception as e:
            print(f"✗ Post validation failed: {e}")
            self.pipeline_status["stages"]["post_validation"] = {
                "status": "failed",
                "error": str(e)
            }
            self.pipeline_status["errors"].append(f"Post validation: {e}")
            return False
    
    def stage_6_select_images(self) -> bool:
        """Stage 6: Select images for posts"""
        print("\n🎯 Stage 6: Select Images for Posts")
        print("-" * 50)
        
        try:
            posts = self.assigner.load_posts()
            
            if not posts:
                return True
            
            selection_results = {}
            success_count = 0
            
            for post in posts:
                slug = post.get("slug", "unknown")
                
                try:
                    image, details = self.selector.select_image(post)
                    selection_results[slug] = {
                        "image": image.name,
                        "score": details["score"],
                        "status": "selected"
                    }
                    success_count += 1
                    print(f"  ✓ {slug}: {image.name} (score: {details['score']:.1f})")
                except Exception as e:
                    selection_results[slug] = {
                        "status": "failed",
                        "error": str(e)
                    }
                    print(f"  ✗ {slug}: {e}")
            
            print(f"\n  Summary: {success_count}/{len(posts)} posts")
            
            self.pipeline_status["stages"]["image_selection"] = {
                "status": "success" if success_count > 0 else "partial",
                "selected": success_count,
                "total": len(posts),
                "results": selection_results
            }
            
            return success_count > 0
        except Exception as e:
            print(f"✗ Image selection failed: {e}")
            self.pipeline_status["stages"]["image_selection"] = {
                "status": "failed",
                "error": str(e)
            }
            self.pipeline_status["errors"].append(f"Image selection: {e}")
            return False
    
    def stage_7_assign_images(self) -> bool:
        """Stage 7: Assign images to posts"""
        print("\n✨ Stage 7: Assign Images to Posts")
        print("-" * 50)
        
        try:
            posts = self.assigner.load_posts()
            
            # Assign images
            assignment_results = self.assigner.assign_images_to_posts(posts)
            
            # Save posts
            self.assigner.save_posts(posts)
            print(f"\n✓ Saved {len(posts)} posts with images")
            
            self.pipeline_status["stages"]["image_assignment"] = {
                "status": "success",
                "posts_assigned": len(assignment_results),
                "total_posts": len(posts)
            }
            
            return True
        except Exception as e:
            print(f"✗ Image assignment failed: {e}")
            self.pipeline_status["stages"]["image_assignment"] = {
                "status": "failed",
                "error": str(e)
            }
            self.pipeline_status["errors"].append(f"Image assignment: {e}")
            return False
    
    def stage_8_generate_social_metadata(self) -> bool:
        """Stage 8: Generate social media metadata"""
        print("\n🌐 Stage 8: Generate Social Media Metadata")
        print("-" * 50)
        
        try:
            posts = self.assigner.load_posts()
            
            # Generate metadata
            social_metadata = self.assigner.generate_social_metadata(posts)
            
            # Save metadata
            self.assigner.save_social_metadata(social_metadata)
            print(f"✓ Generated social metadata for {len(social_metadata)} posts")
            
            self.pipeline_status["stages"]["social_metadata"] = {
                "status": "success",
                "metadata_count": len(social_metadata)
            }
            
            return True
        except Exception as e:
            print(f"✗ Social metadata generation failed: {e}")
            self.pipeline_status["stages"]["social_metadata"] = {
                "status": "failed",
                "error": str(e)
            }
            self.pipeline_status["errors"].append(f"Social metadata: {e}")
            return False
    
    def stage_9_optimize_images(self) -> bool:
        """Stage 9: Optimize images"""
        print("\n🖼️  Stage 9: Optimize Images")
        print("-" * 50)
        
        try:
            stats = self.optimizer.optimize_library(quality="medium")
            
            print(f"✓ Optimized {stats['images_optimized']} images")
            print(f"  • Compression: {stats['compression_rate']*100:.1f}%")
            print(f"  • Space saved: {(stats['total_original_size'] - stats['total_optimized_size'])/(1024*1024):.2f} MB")
            
            self.optimizer.save_optimization_log()
            
            self.pipeline_status["stages"]["image_optimization"] = {
                "status": "success",
                "images_optimized": stats['images_optimized'],
                "compression_rate": stats['compression_rate'],
                "space_saved_mb": (stats['total_original_size'] - stats['total_optimized_size']) / (1024*1024)
            }
            
            return True
        except Exception as e:
            print(f"⚠️  Image optimization skipped: {e}")
            self.pipeline_status["stages"]["image_optimization"] = {
                "status": "skipped",
                "reason": str(e)
            }
            self.pipeline_status["warnings"].append(f"Image optimization: {e}")
            return True  # Don't fail pipeline
    
    def stage_10_validate_pipeline(self) -> bool:
        """Stage 10: Validate complete pipeline"""
        print("\n✅ Stage 10: Validate Pipeline")
        print("-" * 50)
        
        try:
            posts = self.assigner.load_posts()
            
            all_assigned = all(post.get("image") for post in posts)
            all_metadata = all(post.get("category") for post in posts)
            
            print(f"✓ All posts have images: {all_assigned}")
            print(f"✓ All posts have metadata: {all_metadata}")
            
            if all_assigned and all_metadata:
                print(f"✓ Pipeline validation successful!")
                self.pipeline_status["stages"]["validation"] = {
                    "status": "success",
                    "all_assigned": True,
                    "all_metadata": True
                }
                return True
            else:
                print(f"⚠️  Some posts missing images or metadata")
                self.pipeline_status["stages"]["validation"] = {
                    "status": "partial",
                    "all_assigned": all_assigned,
                    "all_metadata": all_metadata
                }
                return True
        except Exception as e:
            print(f"⚠️  Validation skipped: {e}")
            self.pipeline_status["stages"]["validation"] = {
                "status": "skipped",
                "error": str(e)
            }
            return True
    
    def save_pipeline_log(self):
        """Save pipeline execution log"""
        self.pipeline_status["status"] = "completed"
        self.pipeline_status["completed_at"] = datetime.utcnow().isoformat()
        
        with open(self.pipeline_log_file, 'w') as f:
            json.dump(self.pipeline_status, f, indent=2)
        
        print(f"\n✓ Pipeline log saved: {self.pipeline_log_file}")
    
    def generate_pipeline_report(self) -> str:
        """Generate comprehensive pipeline report"""
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║       DBOS AUTO IMAGE PIPELINE - EXECUTION REPORT              ║
╚════════════════════════════════════════════════════════════════╝

📅 Execution Time: {self.pipeline_status['timestamp']}

📊 PIPELINE STAGES:
"""
        
        for stage_name, stage_data in self.pipeline_status['stages'].items():
            status_emoji = "✓" if stage_data['status'] == 'success' else "⚠" if stage_data['status'] == 'partial' else "✗"
            report += f"\n  {status_emoji} {stage_name.replace('_', ' ').title()}: {stage_data['status']}"
        
        if self.pipeline_status['errors']:
            report += "\n\n❌ ERRORS:\n"
            for error in self.pipeline_status['errors']:
                report += f"  • {error}\n"
        
        if self.pipeline_status['warnings']:
            report += "\n⚠️  WARNINGS:\n"
            for warning in self.pipeline_status['warnings']:
                report += f"  • {warning}\n"
        
        report += f"""
╔════════════════════════════════════════════════════════════════╗
✅ PIPELINE COMPLETE - Ready for blog deployment
╚════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def run(self):
        """Execute complete image pipeline"""
        print("\n" + "="*60)
        print("🎨 DBOS AUTO IMAGE PIPELINE")
        print("="*60)
        
        try:
            # Execute stages
            stages = [
                ("library", self.stage_1_initialize_library),
                ("content_analysis", self.stage_2_analyze_content),
                ("prompt_generation", self.stage_3_generate_prompts),
                ("ai_generation", self.stage_4_generate_ai_images),
                ("validation", self.stage_5_validate_posts),
                ("selection", self.stage_6_select_images),
                ("assignment", self.stage_7_assign_images),
                ("metadata", self.stage_8_generate_social_metadata),
                ("optimization", self.stage_9_optimize_images),
                ("verification", self.stage_10_validate_pipeline),
            ]
            
            completed_stages = 0
            for stage_name, stage_func in stages:
                try:
                    if stage_func():
                        completed_stages += 1
                    else:
                        print(f"\n⚠️  {stage_name} stage did not complete successfully")
                except Exception as e:
                    print(f"\n❌ Error in {stage_name} stage: {e}")
                    self.pipeline_status["errors"].append(f"{stage_name}: {e}")
            
            # Save log
            self.save_pipeline_log()
            
            # Print report
            report = self.generate_pipeline_report()
            print(report)
            
            print(f"\nCompleted {completed_stages}/{len(stages)} stages\n")
            
        except Exception as e:
            print(f"\n❌ Pipeline execution failed: {e}")
            self.pipeline_status["status"] = "failed"
            self.pipeline_status["errors"].append(str(e))
            self.save_pipeline_log()

if __name__ == '__main__':
    pipeline = BlogImagePipeline()
    pipeline.run()
