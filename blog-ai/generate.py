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
import markdown
from typing import Dict, Tuple
from dotenv import load_dotenv
from anthropic import Anthropic
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from keyword_research import KeywordResearcher

# Load environment variables
load_dotenv()

# Initialize AI clients
client_anthropic = None
client_openai = None
client_gemini = None

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if anthropic_key:
    client_anthropic = Anthropic(api_key=anthropic_key)

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key and HAS_OPENAI:
    client_openai = OpenAI(api_key=openai_key)

gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key and HAS_GEMINI:
    genai.configure(api_key=gemini_key)
    client_gemini = genai.GenerativeModel('gemini-flash-latest')

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
        self.researcher = KeywordResearcher()
        
        # Determine which AI service to use
        if client_gemini:
            self.ai_service = "gemini"
            self.model = "gemini-flash-latest"
            print("🤖 Using Google Gemini")
        elif client_anthropic:
            self.ai_service = "anthropic"
            self.model = self.config["ai"].get("model", "claude-3-sonnet-20240229")
            print("🤖 Using Anthropic Claude")
        elif client_openai:
            self.ai_service = "openai"
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
            print(f"🤖 Using OpenAI {self.model}")
        else:
            raise Exception("No AI API keys found in .env file (checked GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY)")

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
        """Generate a blog post topic using AI"""
        topics = self.config.get("topics", [])
        focus_areas = self.prompts.get("topics_generation", {}).get("focus_areas", [])
        
        selected_topic = random.choice(topics)
        selected_focus = random.choice(focus_areas)

        prompt = f"""Generate ONE catchy, technical blog post title for a data engineer's blog.

Topic: {selected_topic}
Content Pillar: {selected_focus}
Target Audience: Intermediate to advanced data engineers

Requirements:
- Make it actionable and specific
- Include numbers or power words where appropriate
- Make it SEO-friendly
- Between 60-80 characters

        Return ONLY the title, nothing else."""

        if self.ai_service == "gemini":
            response = client_gemini.generate_content(prompt)
            return response.text.strip()
        elif self.ai_service == "anthropic":
            message = client_anthropic.messages.create(

                model=self.model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
        else:
            response = client_openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            return response.choices[0].message.content.strip()

    def generate_post(self, title: str = None) -> Tuple[str, str, str]:
        """Generate a complete blog post"""
        if not title:
            title = self.generate_topic()

        # SEO Optimization: Analyze title keywords
        print(f"🔍 Optimizing for SEO...")
        keyword_analysis = self.researcher.analyze_keyword(title)
        primary_keyword = keyword_analysis.get('keyword', title)
        related_keywords = keyword_analysis.get('related_keywords', [])

        print(f"📝 Generating post: '{title}'...")

        # Create conversation for multi-turn generation
        conversation = []
        
        outline_prompt = f"""Create a detailed outline for this technical blog post:

Title: {title}
Primary Keyword: {primary_keyword}
Secondary Keywords: {', '.join(related_keywords)}

Author persona: {json.dumps(self.config['author'], indent=2)}

Writing guidelines:
{json.dumps(self.prompts['post_instructions'], indent=2)}

Create a 5-6 section outline with brief descriptions. Be specific about code examples and real-world scenarios."""

        # First turn: Generate outline
        if self.ai_service == "gemini":
            chat = client_gemini.start_chat(history=[])
            response = chat.send_message(f"SYSTEM: {self.prompts['system_prompt']}\n\n{outline_prompt}")
            outline = response.text
        elif self.ai_service == "anthropic":
            conversation.append({"role": "user", "content": outline_prompt})
            outline_response = client_anthropic.messages.create(
                model=self.model,
                max_tokens=1000,
                system=self.prompts["system_prompt"],
                messages=conversation
            )
            outline = outline_response.content[0].text
        else:
            conversation.append({"role": "system", "content": self.prompts["system_prompt"]})
            conversation.append({"role": "user", "content": outline_prompt})
            outline_response = client_openai.chat.completions.create(
                model=self.model,
                messages=conversation,
                max_tokens=1000
            )
            outline = outline_response.choices[0].message.content

        conversation.append({"role": "assistant", "content": outline})

        # Second turn: Generate full content
        content_prompt = f"""Now write the complete blog post based on this outline.

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

        if self.ai_service == "gemini":
            response = chat.send_message(content_prompt)
            content = response.text
        elif self.ai_service == "anthropic":
            conversation.append({"role": "user", "content": content_prompt})
            content_response = client_anthropic.messages.create(
                model=self.model,
                max_tokens=3000,
                system=self.prompts["system_prompt"],
                messages=conversation
            )
            content = content_response.content[0].text
        else:
            conversation.append({"role": "user", "content": content_prompt})
            content_response = client_openai.chat.completions.create(
                model=self.model,
                messages=conversation,
                max_tokens=3000
            )
            content = content_response.choices[0].message.content

        conversation.append({"role": "assistant", "content": content})

        # Third turn: Extract metadata
        metadata_prompt = f"""Extract metadata for this blog post. Respond ONLY with valid JSON in this exact format:

{{
  "title": "{title}",
  "read_time": <number 5-20>,
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "tldr": "<2-3 sentence summary>",
  "excerpt": "<1-2 sentence hook for blog listing>",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}

Do not include any markdown or additional text."""

        if self.ai_service == "gemini":
            response = chat.send_message(metadata_prompt)
            metadata_text = response.text.strip()
        elif self.ai_service == "anthropic":
            conversation.append({"role": "user", "content": metadata_prompt})
            metadata_response = client_anthropic.messages.create(
                model=self.model,
                max_tokens=500,
                system="You are a JSON generator. Respond ONLY with valid JSON.",
                messages=conversation
            )
            metadata_text = metadata_response.content[0].text.strip()
        else:
            conversation.append({"role": "user", "content": metadata_prompt})
            metadata_response = client_openai.chat.completions.create(
                model=self.model,
                messages=conversation,
                max_tokens=500
            )
            metadata_text = metadata_response.choices[0].message.content.strip()

        try:
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
        """Format generated post for assets/shared/posts.js"""
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

    def _markdown_to_html(self, md_content: str) -> str:
        """Convert markdown to high-quality HTML using markdown library"""
        extensions = [
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'attr_list',
            'md_in_html'
        ]
        
        # Add extra spacing for readability
        content = md_content.replace("\n", "\n\n")
        
        html = markdown.markdown(md_content, extensions=extensions)
        
        # Clean up some common issues
        html = html.replace('<code>', '<code class="language-python">') # Default to python
        
        return html

    def generate_multiple(self, count: int = 1) -> list:
        """Generate multiple blog posts"""
        posts = []
        
        for i in range(count):
            print(f"\n📚 Generating post {i+1}/{count}...")
            try:
                title, content, metadata = self.generate_post()
                md_file, meta_file = self.save_post(title, content, metadata)
                
                # Format for assets/shared/posts.js
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
    parser.add_argument("--output", type=str, default="assets/shared/posts.json", help="Output file for posts")
    
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
