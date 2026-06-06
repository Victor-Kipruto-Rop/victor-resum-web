#!/usr/bin/env python3
"""
DBOS Blog Content Analyzer
Analyzes blog posts to extract technical metadata for AI image generation
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ContentAnalysis:
    """Analysis result for a blog post"""
    title: str
    slug: str
    category: str
    tags: List[str]
    keywords: Set[str]
    primary_topic: str
    secondary_topics: List[str]
    technical_stack: List[str]
    visual_style: str
    tone: str
    target_audience: str

class BlogContentAnalyzer:
    """Analyzes blog content to extract technical metadata for image generation"""
    
    # Domain-specific keyword mappings
    TECHNOLOGY_KEYWORDS = {
        # Data Engineering
        "data": ["data engineering", "etl", "pipelines", "warehouse", "lakes", "streaming"],
        "airflow": ["apache airflow", "dag", "orchestration", "workflows", "scheduling"],
        "etl": ["extract", "transform", "load", "etl", "elt", "pipeline"],
        "sql": ["sql", "database", "query", "relational", "postgres", "mysql", "snowflake"],
        "spark": ["apache spark", "pyspark", "distributed", "spark streaming"],
        "dbt": ["dbt", "data build tool", "transformation", "analytics engineering"],
        
        # Python & Backend
        "python": ["python", "django", "flask", "fastapi", "async", "concurrency"],
        "backend": ["backend", "server", "api", "microservices", "rest"],
        "async": ["asyncio", "concurrent", "parallel", "threading", "multiprocessing"],
        
        # Infrastructure & DevOps
        "kubernetes": ["kubernetes", "k8s", "container", "docker", "orchestration", "pod"],
        "devops": ["ci/cd", "devops", "deployment", "infrastructure", "terraform", "ansible"],
        "cloud": ["aws", "gcp", "azure", "cloud", "serverless", "lambda", "functions"],
        "docker": ["docker", "container", "containerization", "image", "registry"],
        
        # AI & Machine Learning
        "ai": ["artificial intelligence", "ai", "machine learning", "ml", "neural", "model"],
        "nlp": ["nlp", "natural language", "text processing", "transformers"],
        "deep-learning": ["deep learning", "neural network", "pytorch", "tensorflow"],
        
        # Testing & Quality
        "testing": ["testing", "unit test", "integration test", "pytest", "test-driven"],
        "quality": ["quality", "validation", "expectations", "soda", "data quality"],
        
        # APIs & Integration
        "api": ["api", "rest", "graphql", "grpc", "webhook", "integration"],
        "integration": ["integration", "connector", "sync", "replication"],
        
        # Monitoring & Observability
        "monitoring": ["monitoring", "observability", "metrics", "logs", "tracing", "datadog"],
        "performance": ["performance", "optimization", "profiling", "benchmarking"],
    }
    
    # Category to visual style mappings
    VISUAL_STYLE_MAPPING = {
        "Infrastructure": "architecture-diagrams",
        "Data Engineering": "pipeline-flows",
        "Data Transformation": "transformation-flows",
        "Data Quality": "quality-dashboards",
        "Python": "code-editor",
        "DevOps": "infrastructure-mesh",
        "AI/ML": "neural-networks",
        "Cloud": "distributed-systems"
    }
    
    # Tone detection patterns
    TONE_PATTERNS = {
        "technical": ["implement", "architecture", "design", "system", "framework", "pattern"],
        "tutorial": ["build", "create", "setup", "guide", "step", "beginner", "learn"],
        "comparison": ["vs", "comparison", "alternative", "difference", "choose"],
        "best-practices": ["best practice", "pattern", "principle", "standard", "convention"],
        "deep-dive": ["deep dive", "comprehensive", "advanced", "expert", "mastery"]
    }
    
    def __init__(self):
        self.posts_file = Path("blog/posts.json")
        self.analysis_file = Path("assets/auto/content-analysis.json")
        self.analysis_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_posts(self) -> List[Dict]:
        """Load blog posts"""
        if self.posts_file.exists():
            with open(self.posts_file) as f:
                return json.load(f)
        return []
    
    def extract_keywords(self, text: str) -> Set[str]:
        """Extract technical keywords from text"""
        keywords = set()
        text_lower = text.lower()
        
        for tech_area, keywords_list in self.TECHNOLOGY_KEYWORDS.items():
            for keyword in keywords_list:
                if keyword in text_lower:
                    keywords.add(tech_area)
        
        return keywords
    
    def detect_primary_topic(self, category: str, keywords: Set[str], tags: List[str]) -> str:
        """Detect primary topic"""
        # Category takes priority
        if category:
            return category
        
        # Map keywords to topics
        keyword_to_topic = {
            "data": "Data Engineering",
            "airflow": "Data Engineering",
            "etl": "Data Engineering",
            "dbt": "Data Transformation",
            "python": "Python",
            "kubernetes": "Infrastructure",
            "devops": "DevOps",
            "ai": "AI/ML",
            "testing": "Testing & QA",
            "monitoring": "Monitoring"
        }
        
        for keyword in keywords:
            if keyword in keyword_to_topic:
                return keyword_to_topic[keyword]
        
        return "Technology"
    
    def detect_secondary_topics(self, keywords: Set[str], primary: str) -> List[str]:
        """Detect secondary topics"""
        secondary = list(keywords - {self._topic_to_keyword(primary)})
        return secondary[:3]  # Top 3
    
    def _topic_to_keyword(self, topic: str) -> str:
        """Map topic to keyword"""
        mapping = {
            "Data Engineering": "data",
            "Data Transformation": "dbt",
            "Python": "python",
            "Infrastructure": "kubernetes",
            "DevOps": "devops",
            "AI/ML": "ai",
            "Testing & QA": "testing",
            "Monitoring": "monitoring"
        }
        return mapping.get(topic, topic.lower())
    
    def extract_technical_stack(self, text: str, tags: List[str]) -> List[str]:
        """Extract technical stack from text and tags"""
        stack = []
        
        # Add tags (they're already technical)
        stack.extend(tags[:5])  # Top 5 tags
        
        # Extract specific technologies
        technologies = [
            "Python", "Airflow", "dbt", "SQL", "Kubernetes", "Docker",
            "Spark", "Postgres", "AWS", "GCP", "Azure", "Terraform",
            "GitHub", "GitLab", "Django", "FastAPI", "PostgreSQL"
        ]
        
        text_lower = text.lower()
        for tech in technologies:
            if tech.lower() in text_lower:
                stack.append(tech)
        
        return list(set(stack))[:6]  # Return unique, top 6
    
    def detect_tone(self, title: str, description: str) -> str:
        """Detect post tone/style"""
        text = (title + " " + description).lower()
        
        tone_scores = {}
        for tone, patterns in self.TONE_PATTERNS.items():
            score = sum(text.count(pattern) for pattern in patterns)
            tone_scores[tone] = score
        
        if not tone_scores:
            return "technical"
        
        return max(tone_scores, key=tone_scores.get)
    
    def detect_audience(self, category: str, tags: List[str]) -> str:
        """Detect target audience"""
        beginner_indicators = ["beginner", "introduction", "guide", "tutorial", "basics"]
        advanced_indicators = ["advanced", "expert", "optimization", "patterns", "architecture"]
        
        # Check tags
        all_text = (category + " " + " ".join(tags)).lower()
        
        for indicator in beginner_indicators:
            if indicator in all_text:
                return "Beginners & Learners"
        
        for indicator in advanced_indicators:
            if indicator in all_text:
                return "Advanced Engineers"
        
        return "Mid-Level Professionals"
    
    def get_visual_style(self, category: str) -> str:
        """Get visual style recommendation"""
        return self.VISUAL_STYLE_MAPPING.get(
            category,
            "technical-illustration"
        )
    
    def analyze_post(self, post: Dict) -> ContentAnalysis:
        """Analyze single blog post"""
        title = post.get("title", "")
        slug = post.get("slug", "")
        category = post.get("category", "")
        tags = post.get("tags", [])
        description = post.get("description", "")
        
        # Extract keywords
        full_text = f"{title} {description} {' '.join(tags)}"
        keywords = self.extract_keywords(full_text)
        
        # Detect topics
        primary = self.detect_primary_topic(category, keywords, tags)
        secondary = self.detect_secondary_topics(keywords, primary)
        
        # Extract technical stack
        stack = self.extract_technical_stack(full_text, tags)
        
        # Detect tone and audience
        tone = self.detect_tone(title, description)
        audience = self.detect_audience(category, tags)
        
        # Get visual style
        visual_style = self.get_visual_style(category)
        
        return ContentAnalysis(
            title=title,
            slug=slug,
            category=category,
            tags=tags,
            keywords=keywords,
            primary_topic=primary,
            secondary_topics=secondary,
            technical_stack=stack,
            visual_style=visual_style,
            tone=tone,
            target_audience=audience
        )
    
    def analyze_all_posts(self) -> Dict[str, ContentAnalysis]:
        """Analyze all blog posts"""
        posts = self.load_posts()
        analyses = {}
        
        print("📊 ANALYZING BLOG CONTENT\n")
        
        for post in posts:
            slug = post.get("slug", "unknown")
            analysis = self.analyze_post(post)
            analyses[slug] = analysis
            
            print(f"✓ {slug}")
            print(f"  → Primary: {analysis.primary_topic}")
            print(f"  → Keywords: {', '.join(list(analysis.keywords)[:3])}")
            print(f"  → Stack: {', '.join(analysis.technical_stack[:3])}")
        
        return analyses
    
    def save_analysis(self, analyses: Dict[str, ContentAnalysis]):
        """Save analysis results"""
        # Convert dataclass to dict
        analyses_dict = {}
        for slug, analysis in analyses.items():
            analyses_dict[slug] = {
                "title": analysis.title,
                "category": analysis.category,
                "tags": analysis.tags,
                "keywords": list(analysis.keywords),
                "primary_topic": analysis.primary_topic,
                "secondary_topics": analysis.secondary_topics,
                "technical_stack": analysis.technical_stack,
                "visual_style": analysis.visual_style,
                "tone": analysis.tone,
                "target_audience": analysis.target_audience
            }
        
        with open(self.analysis_file, 'w') as f:
            json.dump(analyses_dict, f, indent=2)
        
        print(f"\n✓ Analysis saved: {self.analysis_file}")
    
    def generate_analysis_report(self, analyses: Dict[str, ContentAnalysis]) -> str:
        """Generate analysis report"""
        report = f"""
📊 BLOG CONTENT ANALYSIS REPORT

Analysis Date: {datetime.utcnow().isoformat()}

Summary:
  • Total Posts: {len(analyses)}

Content Breakdown:
"""
        
        # Aggregate by topic
        topic_counts = {}
        for analysis in analyses.values():
            topic = analysis.primary_topic
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"  • {topic}: {count}\n"
        
        # Aggregate by tone
        report += f"\nTone Distribution:\n"
        tone_counts = {}
        for analysis in analyses.values():
            tone = analysis.tone
            tone_counts[tone] = tone_counts.get(tone, 0) + 1
        
        for tone, count in sorted(tone_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"  • {tone}: {count}\n"
        
        # Top technical stack
        report += f"\nTop Technical Stack:\n"
        stack_counts = {}
        for analysis in analyses.values():
            for tech in analysis.technical_stack:
                stack_counts[tech] = stack_counts.get(tech, 0) + 1
        
        for tech, count in sorted(stack_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"  • {tech}: {count} posts\n"
        
        return report
    
    def run(self):
        """Execute content analysis"""
        print("\n" + "="*60)
        print("📊 DBOS BLOG CONTENT ANALYZER")
        print("="*60 + "\n")
        
        # Analyze all posts
        analyses = self.analyze_all_posts()
        
        # Save analysis
        self.save_analysis(analyses)
        
        # Generate report
        report = self.generate_analysis_report(analyses)
        print(report)
        
        print("\n✅ Content analysis complete!\n")

if __name__ == '__main__':
    analyzer = BlogContentAnalyzer()
    analyzer.run()
