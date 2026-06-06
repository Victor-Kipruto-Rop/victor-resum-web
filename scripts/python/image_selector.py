#!/usr/bin/env python3
"""
DBOS Image Selection Engine
Intelligent image selection using multi-layer scoring algorithm
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from image_library_manager import ImageLibraryManager, ImageAsset

@dataclass
class SelectionCandidate:
    """Candidate image with scoring"""
    image: ImageAsset
    score: float
    matches: List[str]
    layers: Dict[str, float]

class ImageSelector:
    """Selects best image for blog post using multi-layer algorithm"""
    
    def __init__(self):
        self.manager = ImageLibraryManager()
        self.manager.initialize_default_library()
        self.library = self.manager.library
        
        # Keywords mapping for Layer 3
        self.keyword_mapping = {
            # Python & Backend
            "python": ["python"],
            "django": ["python"],
            "flask": ["python"],
            "fastapi": ["python"],
            "backend": ["python"],
            
            # Data Engineering & ETL
            "data-engineering": ["data", "engineering", "etl"],
            "airflow": ["airflow", "orchestration", "dag"],
            "etl": ["etl", "pipeline", "extraction"],
            "pipeline": ["etl", "pipeline", "airflow"],
            
            # Data Transformation
            "dbt": ["dbt", "transformation", "sql", "analytics"],
            "sql": ["sql", "query", "postgres", "mysql"],
            "analytics": ["analytics", "dbt", "sql"],
            
            # Databases
            "database": ["sql", "database", "postgres"],
            "sql": ["sql", "database", "query"],
            "nosql": ["api", "database"],
            
            # Kubernetes & Infrastructure
            "kubernetes": ["kubernetes", "k8s", "containers"],
            "k8s": ["kubernetes", "k8s", "containers"],
            "docker": ["kubernetes", "containers"],
            "container": ["kubernetes", "containers"],
            "infrastructure": ["kubernetes", "cloud"],
            
            # Cloud
            "cloud": ["cloud", "aws", "gcp", "azure"],
            "aws": ["cloud", "aws"],
            "gcp": ["cloud", "gcp"],
            "azure": ["cloud", "azure"],
            
            # AI & ML
            "ai": ["ai-ml", "machine-learning"],
            "ml": ["ai-ml", "machine-learning"],
            "machine-learning": ["ai-ml", "machine-learning"],
            "deep-learning": ["ai-ml"],
            "neural": ["ai-ml"],
            "nlp": ["ai-ml"],
            
            # API & Integration
            "api": ["api", "rest", "integration"],
            "rest": ["api", "rest"],
            "graphql": ["api"],
            
            # Testing & Quality
            "testing": ["testing", "qa"],
            "test": ["testing", "qa"],
            "qa": ["testing", "qa"],
            "pytest": ["testing", "python"],
            "unit": ["testing"],
            
            # Monitoring
            "monitoring": ["monitoring", "observability"],
            "logging": ["monitoring"],
            "observability": ["monitoring"],
            "metrics": ["monitoring"],
            
            # DevOps & Git
            "devops": ["git", "devops"],
            "github": ["git", "devops"],
            "gitlab": ["git", "devops"],
            "git": ["git", "devops"],
            "ci-cd": ["git", "devops"],
        }
    
    def select_image(self, post_data: Dict) -> Tuple[ImageAsset, Dict]:
        """
        Select best image for post using 4-layer algorithm
        Returns: (selected_image, selection_details)
        """
        
        candidates = []
        
        # Layer 1: Category-based matching
        category_candidates = self._layer_category(post_data.get("category"))
        candidates.extend(category_candidates)
        
        # Layer 2: Tag-based matching
        tag_candidates = self._layer_tags(post_data.get("tags", []))
        candidates.extend(tag_candidates)
        
        # Layer 3: Title keyword matching
        title_candidates = self._layer_title(post_data.get("title", ""))
        candidates.extend(title_candidates)
        
        # Remove duplicates and merge scores
        merged_candidates = self._merge_candidates(candidates)
        
        # Layer 4: Fallback
        if not merged_candidates:
            default = self.library.get("default-tech")
            merged_candidates = [
                SelectionCandidate(
                    image=default,
                    score=1.0,
                    matches=["default"],
                    layers={"fallback": 1.0}
                )
            ]
        
        # Select best candidate
        best = max(merged_candidates, key=lambda x: x.score)
        
        details = {
            "selected_image": best.image.name,
            "path": best.image.path,
            "score": best.score,
            "matches": best.matches,
            "layer_scores": best.layers,
            "all_candidates": len(merged_candidates)
        }
        
        return best.image, details
    
    def _layer_category(self, category: str) -> List[SelectionCandidate]:
        """Layer 1: Category-based image selection (highest priority)"""
        if not category:
            return []
        
        candidates = []
        category_lower = category.lower()
        
        for name, asset in self.library.items():
            if asset.category.lower() == category_lower:
                candidates.append(SelectionCandidate(
                    image=asset,
                    score=50,  # Category match = 50 points
                    matches=["category"],
                    layers={"category": 50}
                ))
        
        return candidates
    
    def _layer_tags(self, tags: List[str]) -> List[SelectionCandidate]:
        """Layer 2: Tag-based image selection (medium priority)"""
        if not tags:
            return []
        
        candidates = []
        tags_lower = [tag.lower() for tag in tags]
        
        for name, asset in self.library.items():
            asset_tags_lower = [tag.lower() for tag in asset.tags]
            
            matching_tags = [tag for tag in tags_lower if tag in asset_tags_lower]
            
            if matching_tags:
                score = len(matching_tags) * 30  # 30 points per matching tag
                candidates.append(SelectionCandidate(
                    image=asset,
                    score=score,
                    matches=matching_tags,
                    layers={"tags": float(score)}
                ))
        
        return candidates
    
    def _layer_title(self, title: str) -> List[SelectionCandidate]:
        """Layer 3: Title keyword matching (lower priority)"""
        if not title:
            return []
        
        # Extract keywords from title
        keywords = self._extract_keywords(title)
        
        candidates = []
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Check keyword mapping
            mapped_keywords = self.keyword_mapping.get(keyword_lower, [])
            
            if mapped_keywords:
                for name, asset in self.library.items():
                    asset_tags_lower = [tag.lower() for tag in asset.tags]
                    
                    matching_mapped = [k for k in mapped_keywords if k in asset_tags_lower]
                    
                    if matching_mapped:
                        candidates.append(SelectionCandidate(
                            image=asset,
                            score=20,  # 20 points per keyword match
                            matches=[keyword],
                            layers={"title": 20}
                        ))
        
        return candidates
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential keywords from text"""
        # Convert to lowercase and split
        words = re.findall(r'\b[a-z][a-z\-]*[a-z]\b', text.lower())
        
        # Filter out common words
        common_words = {'the', 'and', 'for', 'with', 'from', 'your', 'how', 'to', 'a', 'of', 'in', 'on', 'is', 'are'}
        
        keywords = [w for w in words if w not in common_words and len(w) > 2]
        
        return keywords[:5]  # Limit to top 5 keywords
    
    def _merge_candidates(self, candidates: List[SelectionCandidate]) -> List[SelectionCandidate]:
        """Merge duplicate candidates and combine scores"""
        if not candidates:
            return []
        
        merged = {}
        
        for candidate in candidates:
            image_name = candidate.image.name
            
            if image_name not in merged:
                merged[image_name] = SelectionCandidate(
                    image=candidate.image,
                    score=0,
                    matches=[],
                    layers={}
                )
            
            # Accumulate scores
            merged[image_name].score += candidate.score
            merged[image_name].matches.extend(candidate.matches)
            merged[image_name].layers.update(candidate.layers)
        
        # Remove duplicates from matches
        for candidate in merged.values():
            candidate.matches = list(set(candidate.matches))
        
        return list(merged.values())
    
    def explain_selection(self, post_data: Dict) -> str:
        """Generate human-readable explanation of image selection"""
        image, details = self.select_image(post_data)
        
        explanation = f"""
📊 IMAGE SELECTION DETAILS

Post Title: {post_data.get('title')}
Category: {post_data.get('category')}
Tags: {', '.join(post_data.get('tags', []))}

Selected Image: {details['selected_image']}
Path: {details['path']}
Score: {details['score']:.1f}

Matching Layers:
"""
        
        for layer, score in details['layer_scores'].items():
            explanation += f"  • {layer}: +{score}\n"
        
        explanation += f"\nMatched on: {', '.join(details['matches'])}\n"
        explanation += f"Candidates evaluated: {details['all_candidates']}\n"
        
        return explanation
    
    def batch_select_images(self, posts: List[Dict]) -> Dict[str, Tuple[str, Dict]]:
        """Select images for multiple posts"""
        results = {}
        
        for post in posts:
            slug = post.get("slug")
            if slug:
                image, details = self.select_image(post)
                results[slug] = (image.path, details)
        
        return results
    
    def run(self):
        """Test image selection"""
        print("\n🎨 DBOS Image Selection Engine\n")
        
        # Test posts
        test_posts = [
            {
                "title": "Advanced Kubernetes Patterns for Data Engineers",
                "category": "Infrastructure",
                "tags": ["kubernetes", "data-engineering", "devops", "containers"]
            },
            {
                "title": "Building Data Pipelines with Apache Airflow",
                "category": "Data Engineering",
                "tags": ["airflow", "etl", "data-pipelines", "python"]
            },
            {
                "title": "dbt Best Practices: Structuring Your Data Models",
                "category": "Data Transformation",
                "tags": ["dbt", "sql", "analytics-engineering", "data-modeling"]
            }
        ]
        
        print("Testing Image Selection:\n")
        
        for post in test_posts:
            image, details = self.select_image(post)
            print(f"✓ {post['title']}")
            print(f"  → Selected: {image.name}")
            print(f"  → Path: {image.path}")
            print(f"  → Score: {details['score']:.1f}\n")
        
        print("✅ Image selection complete!\n")

if __name__ == '__main__':
    selector = ImageSelector()
    selector.run()
