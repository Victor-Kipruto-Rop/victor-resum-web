#!/usr/bin/env python3
"""
Keyword Research - Analyze keywords for SEO and content planning
Provides keyword metrics and optimization recommendations
"""

import json
from datetime import datetime
from anthropic import Anthropic
from pathlib import Path


class KeywordResearcher:
    """Analyze and research keywords for blog content"""

    def __init__(self, config_path="config.json"):
        """Initialize keyword researcher"""
        self.config = self._load_json(config_path)
        self.client = Anthropic()
        self.keyword_data = {}

    def _load_json(self, filepath):
        """Load JSON configuration file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def analyze_keyword(self, keyword: str) -> dict:
        """Analyze a single keyword for SEO potential"""
        analysis = {
            "keyword": keyword,
            "metrics": self._estimate_metrics(keyword),
            "ai_insights": self._get_ai_insights(keyword),
            "optimization": self._get_optimization_tips(keyword),
            "related_keywords": self._find_related_keywords(keyword),
            "content_strategy": self._suggest_content_strategy(keyword)
        }
        return analysis

    def _estimate_metrics(self, keyword: str) -> dict:
        """Estimate keyword metrics"""
        # Simulated metrics based on keyword characteristics
        base_search_volume = len(keyword.split()) * 100
        difficulty = self._calculate_difficulty(keyword)

        metrics = {
            "estimated_monthly_searches": base_search_volume,
            "keyword_difficulty": difficulty,
            "search_intent": self._classify_intent(keyword),
            "cpc_estimate": "$2-5" if len(keyword) > 15 else "$5-15",
            "opportunity_score": max(0, 100 - difficulty),
            "competition_level": "high" if base_search_volume > 1000 else "medium" if base_search_volume > 100 else "low"
        }
        return metrics

    def _calculate_difficulty(self, keyword: str) -> int:
        """Calculate estimated keyword difficulty (0-100)"""
        # Simplified difficulty calculation
        factors = {
            "length": len(keyword.split()),
            "specificity": 1 if any(word in keyword.lower() for word in ["vs", "best", "how to"]) else 2,
            "competitiveness": 1 if any(brand in keyword.lower() for brand in ["airflow", "spark", "kafka"]) else 0
        }
        difficulty = min(100, (factors["length"] * 10) + (factors["specificity"] * 15) + (factors["competitiveness"] * 25))
        return difficulty

    def _classify_intent(self, keyword: str) -> str:
        """Classify search intent"""
        keyword_lower = keyword.lower()

        if any(word in keyword_lower for word in ["how to", "how do i", "tutorial", "guide"]):
            return "educational"
        elif any(word in keyword_lower for word in ["best", "top", "vs", "comparison"]):
            return "comparative"
        elif any(word in keyword_lower for word in ["install", "setup", "configure"]):
            return "instructional"
        elif any(word in keyword_lower for word in ["what is", "definition"]):
            return "informational"
        else:
            return "commercial"

    def _calculate_opportunity(self, keyword: str) -> int:
        """Calculate SEO opportunity score (0-100)"""
        difficulty = self._calculate_difficulty(keyword)
        # Lower difficulty = higher opportunity
        opportunity = max(0, 100 - difficulty)
        return opportunity

    def _get_ai_insights(self, keyword: str) -> dict:
        """Get AI-powered insights about keyword"""
        conversation_history = []

        system_prompt = """You are an expert SEO and content strategist specializing in data engineering, 
        data science, and analytics. Provide actionable insights for keyword optimization."""

        request = f"""
        Analyze this keyword for a technical data engineering blog:
        "{keyword}"
        
        Provide insights on:
        1. Content depth needed (beginner/intermediate/advanced)
        2. Target audience (data engineers/analysts/scientists)
        3. Why this keyword matters for technical audience
        4. Unique angles to cover
        5. Common questions users ask about this topic
        
        Return as JSON: {{"depth": "", "audience": "", "importance": "", "angles": [], "questions": []}}
        """

        conversation_history.append({"role": "user", "content": request})

        try:
            response = self.client.messages.create(
                model=self.config.get("ai", {}).get("model", "claude-3-sonnet-20240229"),
                max_tokens=1000,
                system=system_prompt,
                messages=conversation_history
            )

            insights_text = response.content[0].text

            # Extract JSON
            try:
                start = insights_text.find('{')
                end = insights_text.rfind('}') + 1
                if start != -1 and end > start:
                    insights = json.loads(insights_text[start:end])
                    return insights
            except (json.JSONDecodeError, ValueError):
                pass

        except Exception as e:
            print(f"AI insight error: {e}")

        return {"error": "Could not retrieve AI insights"}

    def _get_optimization_tips(self, keyword: str) -> list:
        """Get optimization tips for keyword"""
        tips = [
            f"Create comprehensive guide on '{keyword}'",
            f"Include code examples related to '{keyword}'",
            f"Add comparison table with alternatives",
            f"Link to related '{keyword}' articles",
            f"Optimize title with primary keyword",
            f"Use keyword in first 100 words",
            f"Create FAQ section about '{keyword}'",
            f"Add real-world scenarios for '{keyword}'"
        ]
        return tips

    def _find_related_keywords(self, keyword: str) -> list:
        """Find related keywords for content"""
        # Base related keywords
        base_keywords = [
            f"best {keyword}",
            f"{keyword} tutorial",
            f"{keyword} best practices",
            f"{keyword} vs alternatives",
            f"how to use {keyword}",
            f"{keyword} for beginners",
            f"advanced {keyword}",
            f"{keyword} tools"
        ]
        return base_keywords[:5]

    def _suggest_content_strategy(self, keyword: str) -> dict:
        """Suggest content strategy for keyword"""
        strategy = {
            "content_type": "comprehensive guide",
            "target_length": "8-12 minutes read time (2000-3000 words)",
            "sections": [
                "Introduction",
                "What is [Keyword]?",
                "Why [Keyword] Matters",
                "Getting Started",
                "Best Practices",
                "Real-World Examples",
                "Tools & Resources",
                "Conclusion"
            ],
            "media_types": ["code examples", "diagrams", "screenshots", "external links"],
            "internal_links": 3,
            "external_links": 5,
            "call_to_action": "Subscribe for more data engineering insights"
        }
        return strategy

    def analyze_keywords_batch(self, keywords: list) -> dict:
        """Analyze multiple keywords"""
        results = {
            "analyzed_keywords": [],
            "summary": {},
            "recommendations": [],
            "generated_at": datetime.now().isoformat()
        }

        for keyword in keywords:
            analysis = self.analyze_keyword(keyword)
            results["analyzed_keywords"].append(analysis)

        # Create summary
        results["summary"] = {
            "total_keywords": len(keywords),
            "high_opportunity": len([k for k in results["analyzed_keywords"]
                                     if k["metrics"]["opportunity_score"] > 70]),
            "low_difficulty": len([k for k in results["analyzed_keywords"]
                                   if k["metrics"]["keyword_difficulty"] < 30]),
            "avg_difficulty": sum([k["metrics"]["keyword_difficulty"]
                                   for k in results["analyzed_keywords"]]) / len(keywords) if keywords else 0
        }

        # Generate recommendations
        high_opportunity = sorted(
            results["analyzed_keywords"],
            key=lambda x: x["metrics"]["opportunity_score"],
            reverse=True
        )[:3]

        results["recommendations"] = [
            f"Focus on '{k['keyword']}' - High opportunity (score: {k['metrics']['opportunity_score']})"
            for k in high_opportunity
        ]

        return results

    def get_longtail_keywords(self, root_keyword: str) -> list:
        """Generate long-tail keyword variations"""
        prefixes = ["how to", "best", "learn", "advanced", "tutorial", "guide"]
        suffixes = ["tips", "guide", "best practices", "tutorial", "for beginners", "tools"]

        longtail = []

        # With prefixes
        for prefix in prefixes[:3]:
            longtail.append(f"{prefix} {root_keyword}")

        # With suffixes
        for suffix in suffixes[:3]:
            longtail.append(f"{root_keyword} {suffix}")

        # Question format
        longtail.append(f"What is {root_keyword}?")
        longtail.append(f"Why use {root_keyword}?")
        longtail.append(f"{root_keyword} vs alternatives?")

        return longtail

    def create_keyword_cluster(self, main_keyword: str) -> dict:
        """Create keyword cluster for topic cluster content"""
        cluster = {
            "main_keyword": main_keyword,
            "pillar_content": {
                "title": f"Complete Guide to {main_keyword}",
                "focus_keyword": main_keyword,
                "internal_links": 8
            },
            "cluster_content": [
                {
                    "title": f"How to Use {main_keyword}",
                    "focus_keyword": f"how to use {main_keyword}",
                    "backlink_to_pillar": True
                },
                {
                    "title": f"Best Practices for {main_keyword}",
                    "focus_keyword": f"{main_keyword} best practices",
                    "backlink_to_pillar": True
                },
                {
                    "title": f"{main_keyword} vs Alternatives",
                    "focus_keyword": f"{main_keyword} comparison",
                    "backlink_to_pillar": True
                }
            ]
        }
        return cluster

    def save_research(self, data: dict, filename: str = "keyword_research.json"):
        """Save keyword research to file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Keyword research saved to {filename}")


def main():
    """CLI interface for keyword research"""
    import sys

    researcher = KeywordResearcher()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--analyze":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "Apache Airflow"
            analysis = researcher.analyze_keyword(keyword)
            researcher.save_research(analysis, f"analysis_{keyword.replace(' ', '_')}.json")
            print(f"✅ Analyzed keyword: {keyword}")
            print(f"   Opportunity Score: {analysis['metrics']['opportunity_score']}")
            print(f"   Difficulty: {analysis['metrics']['keyword_difficulty']}")

        elif sys.argv[1] == "--batch":
            keywords = sys.argv[2:] if len(sys.argv) > 2 else [
                "Apache Airflow",
                "Data Pipeline",
                "ETL",
                "Data Warehouse"
            ]
            results = researcher.analyze_keywords_batch(keywords)
            researcher.save_research(results, "batch_keyword_research.json")
            print(f"✅ Analyzed {len(keywords)} keywords")
            print(f"   High opportunity: {results['summary']['high_opportunity']}")

        elif sys.argv[1] == "--longtail":
            root_keyword = sys.argv[2] if len(sys.argv) > 2 else "Data Engineering"
            longtail = researcher.get_longtail_keywords(root_keyword)
            data = {"root_keyword": root_keyword, "longtail_keywords": longtail}
            researcher.save_research(data, f"longtail_{root_keyword.replace(' ', '_')}.json")
            print(f"✅ Generated {len(longtail)} long-tail keywords for '{root_keyword}'")

        elif sys.argv[1] == "--cluster":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "Apache Airflow"
            cluster = researcher.create_keyword_cluster(keyword)
            researcher.save_research(cluster, f"cluster_{keyword.replace(' ', '_')}.json")
            print(f"✅ Created keyword cluster for '{keyword}'")

        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage: python3 keyword_research.py [--analyze|--batch|--longtail|--cluster]")

    else:
        print("Keyword Research Tool")
        print("Usage: python3 keyword_research.py [--analyze|--batch|--longtail|--cluster] [keywords...]")


if __name__ == "__main__":
    main()
