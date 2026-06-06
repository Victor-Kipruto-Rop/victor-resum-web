#!/usr/bin/env python3
"""
Topic Generator - Generates blog topics using AI and trend analysis
Combines user preferences, trending topics, and keyword research
"""

import json
import random
from datetime import datetime
from anthropic import Anthropic
from pathlib import Path


class TopicGenerator:
    """Generate blog topics using Claude AI and trend analysis"""

    def __init__(self, config_path="config.json", prompts_path="prompts.json"):
        """Initialize with configuration files"""
        self.config = self._load_json(config_path)
        self.prompts = self._load_json(prompts_path)
        self.client = Anthropic()
        self.topics_history = self._load_topics_history()

    def _load_json(self, filepath):
        """Load JSON configuration file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found")
            return {}

    def _load_topics_history(self):
        """Load previously generated topics to avoid duplicates"""
        history_file = Path("topics_history.json")
        if history_file.exists():
            with open(history_file, 'r') as f:
                return json.load(f)
        return {"topics": [], "used": []}

    def _save_topics_history(self):
        """Save generated topics to history"""
        with open("topics_history.json", 'w') as f:
            json.dump(self.topics_history, f, indent=2)

    def generate_topics_from_trends(self, trend_data: dict, count: int = 5) -> list:
        """Generate topics based on trending data"""
        conversation_history = []

        system_prompt = self.prompts.get("system_prompt", "You are a data engineering expert blogger")

        # First turn: analyze trends
        analysis_request = f"""
        Given these trending topics and keywords:
        
        {json.dumps(trend_data, indent=2)}
        
        Generate {count} relevant data engineering blog topics that:
        1. Align with current industry trends
        2. Are not in this list: {self.topics_history.get('used', [])}
        3. Have high search volume potential
        4. Are actionable and technical
        
        Format as JSON array with objects: {{"title": "", "description": "", "keywords": []}}
        """

        conversation_history.append({"role": "user", "content": analysis_request})

        response = self.client.messages.create(
            model=self.config.get("ai", {}).get("model", "claude-3-sonnet-20240229"),
            max_tokens=2000,
            system=system_prompt,
            messages=conversation_history
        )

        assistant_response = response.content[0].text
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # Second turn: refine and prioritize
        refinement_request = f"""
        Great topics! Now prioritize these topics by:
        1. Potential audience size
        2. Content depth (8-12 min read)
        3. Relevance to latest tech
        4. Unique perspective opportunity
        
        Return top {count} topics sorted by priority.
        """

        conversation_history.append({"role": "user", "content": refinement_request})

        refined_response = self.client.messages.create(
            model=self.config.get("ai", {}).get("model", "claude-3-sonnet-20240229"),
            max_tokens=2000,
            system=system_prompt,
            messages=conversation_history
        )

        refined_text = refined_response.content[0].text

        # Parse topics from response
        topics = self._parse_topics_json(refined_text)
        return topics

    def generate_topics_from_keywords(self, keywords: list, count: int = 5) -> list:
        """Generate topics from a list of keywords"""
        conversation_history = []

        system_prompt = self.prompts.get("system_prompt", "You are a data engineering expert blogger")

        # First turn: expand keywords
        expansion_request = f"""
        Expand these keywords into detailed blog topics:
        
        Keywords: {', '.join(keywords)}
        
        For each keyword, create a blog topic that:
        1. Goes deep into technical aspects
        2. Includes practical examples
        3. Solves real-world problems
        4. Includes code examples
        
        Return {count} topics as JSON array: {{"keyword": "", "title": "", "description": "", "code_examples": []}}
        """

        conversation_history.append({"role": "user", "content": expansion_request})

        response = self.client.messages.create(
            model=self.config.get("ai", {}).get("model", "claude-3-sonnet-20240229"),
            max_tokens=2000,
            system=system_prompt,
            messages=conversation_history
        )

        assistant_response = response.content[0].text
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # Second turn: add SEO metadata
        seo_request = """
        For each topic, add:
        1. SEO meta description (160 chars)
        2. Target keywords (3-5)
        3. Related topics (2-3)
        4. Internal link anchors
        
        Return complete topic objects with all metadata.
        """

        conversation_history.append({"role": "user", "content": seo_request})

        seo_response = self.client.messages.create(
            model=self.config.get("ai", {}).get("model", "claude-3-sonnet-20240229"),
            max_tokens=2000,
            system=system_prompt,
            messages=conversation_history
        )

        topics = self._parse_topics_json(seo_response.content[0].text)
        return topics

    def generate_related_topics(self, main_topic: str, count: int = 3) -> list:
        """Generate related topics for a main topic"""
        conversation_history = []

        system_prompt = self.prompts.get("system_prompt", "You are a data engineering expert blogger")

        request = f"""
        Generate {count} related blog topics for: "{main_topic}"
        
        Topics should:
        1. Build on the main topic
        2. Go deeper into specific aspects
        3. Provide complementary knowledge
        4. Encourage content series
        
        Return as JSON: {{"main_topic": "", "related": [{{"title": "", "description": "", "difficulty": ""}}]}}
        """

        conversation_history.append({"role": "user", "content": request})

        response = self.client.messages.create(
            model=self.config.get("ai", {}).get("model", "claude-3-sonnet-20240229"),
            max_tokens=1500,
            system=system_prompt,
            messages=conversation_history
        )

        related_text = response.content[0].text
        related_topics = self._parse_topics_json(related_text)
        return related_topics

    def _parse_topics_json(self, text: str) -> list:
        """Extract JSON array from AI response"""
        try:
            # Try to find JSON array in response
            start = text.find('[')
            end = text.rfind(']') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                topics = json.loads(json_str)
                if isinstance(topics, list):
                    return topics
        except (json.JSONDecodeError, ValueError):
            pass
        return []

    def save_topics(self, topics: list, filename: str = "generated_topics.json"):
        """Save generated topics to file"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "count": len(topics),
            "topics": topics
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved {len(topics)} topics to {filename}")

    def get_suggested_topic(self) -> dict:
        """Get a suggested topic from config"""
        topics = self.config.get("topics", [])
        if topics:
            return random.choice(topics)
        return {"title": "Data Engineering Fundamentals", "category": "general"}


def main():
    """CLI interface for topic generator"""
    import sys

    generator = TopicGenerator()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--trends":
            # Example trend data
            trends = {
                "trending_keywords": ["RAG", "Vector Database", "LLM Fine-tuning"],
                "popular_tools": ["Apache Airflow", "Kafka", "Spark"],
                "github_trending": ["data-pipeline", "analytics-engineering"]
            }
            topics = generator.generate_topics_from_trends(trends, count=5)
            generator.save_topics(topics, "trends_topics.json")
            print(f"Generated {len(topics)} topics from trends")

        elif sys.argv[1] == "--keywords":
            keywords = sys.argv[2:] if len(sys.argv) > 2 else ["Kafka", "Airflow", "Data Pipeline"]
            topics = generator.generate_topics_from_keywords(keywords, count=5)
            generator.save_topics(topics, "keyword_topics.json")
            print(f"Generated {len(topics)} topics from keywords")

        elif sys.argv[1] == "--related":
            main_topic = sys.argv[2] if len(sys.argv) > 2 else "Apache Airflow"
            topics = generator.generate_related_topics(main_topic, count=3)
            generator.save_topics(topics, "related_topics.json")
            print(f"Generated related topics for: {main_topic}")

        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage: python3 topic_generator.py [--trends|--keywords|--related]")

    else:
        # Generate suggested topic
        topic = generator.get_suggested_topic()
        print(f"📝 Suggested Topic: {topic.get('title', 'N/A')}")


if __name__ == "__main__":
    main()
