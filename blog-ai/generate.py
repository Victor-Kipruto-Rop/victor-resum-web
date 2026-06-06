#!/usr/bin/env python3
"""
AI Blog Post Generator
Generates technical blog posts using Claude API
"""

import os
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import random
import re
from typing import Dict, Tuple
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic()

CONFIG_PATH = Path(__file__).parent / "config.json"
PROMPTS_PATH = Path(__file__).parent / "prompts.json"
TEMPLATE_PATH = Path(__file__).parent / "template.md"
OUTPUT_DIR = Path(__file__).parent.parent / "blog-ai-posts"

class BlogPostGenerator:
    def __init__(self):
        """Initialize the blog post generator"""
        self.config = self._load_config()
        self.prompts = self._load_prompts()
        self.template = self._load_template()
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)

    def _load_config(self) -> Dict:
        """Load configuration from config.json"""
        with open(CONFIG_PATH) as f:
            return json.load(f)

    def _load_prompts(self) -> Dict:
        """Load prompts from prompts.json"""
        with open(PROMPTS_PATH) as f:
            return json.load(f)

    def _load_template(self) -> str:
        """Load template from template.md"""
        with open(TEMPLATE_PATH) as f:
            return f.read()

    def generate_topic(self) -> str:
        """Generate a blog post topic using Claude"""
        topics = self.config.get("topics", [])
        focus_areas = self.prompts.get("topics_generation", {}).get("focus_areas", [])
        
        selected_topic = random.choice(topics)
        selected_focus = random.choice(focus_areas)

        message = client.messages.create(
            model=self.config["ai"]["model"],
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"""Generate ONE catchy, technical blog post title for a data engineer's blog.

Topic: {selected_topic}
Content Pillar: {selected_focus}
Target Audience: Intermediate to advanced data engineers

Requirements:
- Make it actionable and specific
- Include numbers or power words where appropriate
- Make it SEO-friendly
- Between 60-80 characters

Return ONLY the title, nothing else."""
                }
            ]
        )
        
        return message.content[0].text.strip()

    def generate_post(self, title: str = None) -> Tuple[str, str, str]:
        """Generate a complete blog post"""
        if not title:
            title = self.generate_topic()

        print(f"📝 Generating post: '{title}'...")

        # Create conversation for multi-turn generation
        conversation = []

        # First turn: Generate outline
        conversation.append({
            "role": "user",
            "content": f"""Create a detailed outline for this technical blog post:

Title: {title}

Author persona: {json.dumps(self.config['author'], indent=2)}

Writing guidelines:
{json.dumps(self.prompts['post_instructions'], indent=2)}

Create a 5-6 section outline with brief descriptions. Be specific about code examples and real-world scenarios."""
        })

        outline_response = client.messages.create(
            model=self.config["ai"]["model"],
            max_tokens=1000,
            system=self.prompts["system_prompt"],
            messages=conversation
        )

        outline = outline_response.content[0].text
        conversation.append({
            "role": "assistant",
            "content": outline
        })

        # Second turn: Generate full content
        conversation.append({
            "role": "user",
            "content": f"""Now write the complete blog post based on this outline.

Title: {title}

Requirements from prompts:
{json.dumps(self.prompts['content_rules'], indent=2)}

Write in markdown format. Include:
1. Compelling hook/introduction
2. Real problem statement
3. 3-4 detailed sections with code examples
4. Pro tips and best practices
5. Real-world scenario
6. Key takeaways
7. Resources and further reading

Target length: {self.prompts['post_instructions']['length']}
Tone: {self.prompts['post_instructions']['tone']}
Code language: {self.prompts['post_instructions']['code_examples']['language']}

Write engaging, practical content that provides immediate value."""
        })

        content_response = client.messages.create(
            model=self.config["ai"]["model"],
            max_tokens=3000,
            system=self.prompts["system_prompt"],
            messages=conversation
        )

        content = content_response.content[0].text
        conversation.append({
            "role": "assistant",
            "content": content
        })

        # Third turn: Extract metadata
        conversation.append({
            "role": "user",
            "content": f"""Extract metadata for this blog post. Respond ONLY with valid JSON in this exact format:

{{
  "title": "{title}",
  "read_time": <number 5-20>,
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "tldr": "<2-3 sentence summary>",
  "excerpt": "<1-2 sentence hook for blog listing>",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}

Do not include any markdown or additional text."""
        })

        metadata_response = client.messages.create(
            model=self.config["ai"]["model"],
            max_tokens=500,
            system="You are a JSON generator. Respond ONLY with valid JSON.",
            messages=conversation
        )

        try:
            metadata_text = metadata_response.content[0].text.strip()
            # Try to extract JSON from the response
            json_match = re.search(r'\{[\s\S]*\}', metadata_text)
            if json_match:
                metadata = json.loads(json_match.group())
            else:
                metadata = json.loads(metadata_text)
        except json.JSONDecodeError:
            print(f"⚠️  Failed to parse metadata JSON, using defaults")
            metadata = {
                "title": title,
                "read_time": 10,
                "tags": random.sample(self.config["topics"], 5),
                "tldr": "An insightful technical deep-dive.",
                "excerpt": "Read on to learn more.",
                "keywords": []
            }

        return title, content, json.dumps(metadata, indent=2)

    def save_post(self, title: str, content: str, metadata: str) -> Tuple[str, str]:
        """Save generated post to file"""
        # Generate post ID from title
        post_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        
        # Save markdown content
        md_file = self.output_dir / f"{post_id}.md"
        with open(md_file, 'w') as f:
            f.write(content)

        # Save metadata
        metadata_file = self.output_dir / f"{post_id}.meta.json"
        with open(metadata_file, 'w') as f:
            f.write(metadata)

        print(f"✅ Post saved: {md_file}")
        print(f"✅ Metadata saved: {metadata_file}")

        return str(md_file), str(metadata_file)

    def format_for_posts_js(self, title: str, content: str, metadata_str: str) -> Dict:
        """Format generated post for posts.js"""
        metadata = json.loads(metadata_str)
        
        # Convert markdown to HTML (basic conversion)
        html_content = self._markdown_to_html(content)
        
        return {
            "title": metadata.get("title", title),
            "date": datetime.now().strftime("%B %d, %Y"),
            "readTime": metadata.get("read_time", 10),
            "tags": metadata.get("tags", []),
            "isDraft": False,
            "excerpt": metadata.get("excerpt", ""),
            "content": html_content,
            "keywords": metadata.get("keywords", []),
            "tldr": metadata.get("tldr", "")
        }

    def _markdown_to_html(self, markdown: str) -> str:
        """Simple markdown to HTML conversion"""
        import re
        
        html = markdown
        
        # Headers
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
        
        # Code blocks
        html = re.sub(
            r'```python\n(.*?)\n```',
            r'<pre><code class="language-python">\1</code></pre>',
            html,
            flags=re.DOTALL
        )
        html = re.sub(r'```\n(.*?)\n```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        
        # Inline code
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        
        # Links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        
        # Lists
        html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.+</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
        
        # Paragraphs
        html = re.sub(r'\n\n+', '</p><p>', html)
        html = '<p>' + html + '</p>'
        
        # Line breaks
        html = html.replace('\n', '<br>')
        
        return html

    def generate_multiple(self, count: int = 1) -> list:
        """Generate multiple blog posts"""
        posts = []
        
        for i in range(count):
            print(f"\n📚 Generating post {i+1}/{count}...")
            try:
                title, content, metadata = self.generate_post()
                md_file, meta_file = self.save_post(title, content, metadata)
                
                # Format for posts.js
                post_entry = self.format_for_posts_js(title, content, metadata)
                posts.append({
                    "id": re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-'),
                    **post_entry
                })
                
                print(f"✅ Post {i+1} complete: {title}")
            except Exception as e:
                print(f"❌ Error generating post {i+1}: {e}")
                continue
        
        return posts

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI blog posts")
    parser.add_argument("--count", type=int, default=1, help="Number of posts to generate")
    parser.add_argument("--title", type=str, help="Specific title for the post")
    parser.add_argument("--output", type=str, default="posts.json", help="Output file for posts")
    
    args = parser.parse_args()
    
    print("🚀 Starting AI Blog Post Generator\n")
    
    generator = BlogPostGenerator()
    
    if args.title:
        print(f"📝 Generating specific post: {args.title}")
        title, content, metadata = generator.generate_post(args.title)
        md_file, meta_file = generator.save_post(title, content, metadata)
        print(f"\n✅ Post generated successfully!")
    else:
        posts = generator.generate_multiple(args.count)
        
        # Save posts to JSON
        output_file = Path(args.output)
        with open(output_file, 'w') as f:
            json.dump(posts, f, indent=2)
        
        print(f"\n✅ Generated {len(posts)} posts")
        print(f"📁 Posts saved to: {output_file}")

if __name__ == "__main__":
    main()
