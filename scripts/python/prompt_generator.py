#!/usr/bin/env python3
"""
DBOS AI Prompt Generator
Converts blog metadata into optimized AI image generation prompts
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class PromptResult:
    """AI image generation prompt"""
    blog_prompt: str
    social_prompt: str
    thumbnail_prompt: str
    style_keywords: List[str]
    composition: str

class AIPromptGenerator:
    """Generates AI-optimized prompts for image generation"""
    
    # Visual style templates
    VISUAL_STYLES = {
        "architecture-diagrams": {
            "base": "Clean architectural diagram style, technical schematic, blueprint aesthetic",
            "elements": ["nodes", "connections", "layers", "data flow", "system design"],
            "mood": "professional, technical, structured"
        },
        "pipeline-flows": {
            "base": "Data pipeline visualization, ETL workflow diagram, connected processes",
            "elements": ["arrows", "stages", "transformations", "data movement", "sequence"],
            "mood": "dynamic, flowing, organized"
        },
        "transformation-flows": {
            "base": "Data transformation visualization, before-after contrast, analytics",
            "elements": ["input", "process", "output", "metrics", "results"],
            "mood": "insightful, analytical, clean"
        },
        "quality-dashboards": {
            "base": "Data quality metrics dashboard, monitoring interface, real-time metrics",
            "elements": ["gauges", "charts", "metrics", "status indicators", "alerts"],
            "mood": "professional, clear, actionable"
        },
        "code-editor": {
            "base": "Modern code editor interface, syntax highlighting, programming environment",
            "elements": ["code", "terminal", "syntax colors", "file tree", "debugging"],
            "mood": "productive, technical, modern"
        },
        "infrastructure-mesh": {
            "base": "Infrastructure mesh architecture, microservices, connected systems",
            "elements": ["services", "connections", "clusters", "networking", "deployment"],
            "mood": "interconnected, scalable, robust"
        },
        "neural-networks": {
            "base": "Neural network visualization, AI/ML concepts, interconnected nodes",
            "elements": ["nodes", "synapses", "layers", "data flow", "learning"],
            "mood": "futuristic, intelligent, dynamic"
        },
        "distributed-systems": {
            "base": "Distributed cloud architecture, global systems, scalable infrastructure",
            "elements": ["servers", "regions", "connectivity", "distribution", "redundancy"],
            "mood": "scalable, reliable, modern"
        },
        "technical-illustration": {
            "base": "Technical illustration, abstract tech aesthetic, professional design",
            "elements": ["abstract", "tech elements", "modern", "clean", "minimal"],
            "mood": "professional, innovative, contemporary"
        }
    }
    
    # Design parameters by audience
    AUDIENCE_DESIGN = {
        "Beginners & Learners": {
            "complexity": "simple, clear, easy to understand",
            "style": "friendly, approachable, educational",
            "colors": "bright, welcoming, encouraging"
        },
        "Mid-Level Professionals": {
            "complexity": "balanced, professional, detailed",
            "style": "modern, practical, direct",
            "colors": "professional, refined, corporate"
        },
        "Advanced Engineers": {
            "complexity": "technical, sophisticated, in-depth",
            "style": "minimalist, precise, expert-level",
            "colors": "dark, technical, professional"
        }
    }
    
    # Composition patterns
    COMPOSITION_PATTERNS = {
        "centered": "centered composition, symmetric balance, focal point in center",
        "flow": "directional flow, left to right progression, movement through image",
        "layered": "layered design, depth, foreground-background separation",
        "abstract": "abstract representation, artistic interpretation, conceptual",
        "technical": "technical accuracy, schematic style, diagram-like representation"
    }
    
    # Color schemes by topic
    COLOR_SCHEMES = {
        "Data Engineering": "dark blues, greens, oranges - data flow colors",
        "Data Transformation": "purples, teals, golds - transformation energy",
        "Python": "blue, yellow, green - Python brand colors",
        "Infrastructure": "red, gray, blacks - industrial colors",
        "DevOps": "orange, blacks, white - DevOps aesthetic",
        "AI/ML": "electric blues, purples, bright accents - futuristic",
        "Cloud": "light blues, white, silver - cloud/sky aesthetic",
        "Monitoring": "greens, reds, yellows - status/health colors"
    }
    
    def __init__(self):
        self.analysis_file = Path("assets/auto/content-analysis.json")
        self.prompts_file = Path("assets/auto/generated-prompts.json")
        self.prompts_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_analysis(self) -> Dict:
        """Load content analysis"""
        if self.analysis_file.exists():
            with open(self.analysis_file) as f:
                return json.load(f)
        return {}
    
    def get_visual_style(self, style_name: str) -> Dict:
        """Get visual style template"""
        return self.VISUAL_STYLES.get(style_name, self.VISUAL_STYLES["technical-illustration"])
    
    def get_design_params(self, audience: str) -> Dict:
        """Get design parameters for audience"""
        return self.AUDIENCE_DESIGN.get(audience, self.AUDIENCE_DESIGN["Mid-Level Professionals"])
    
    def get_color_scheme(self, topic: str) -> str:
        """Get color scheme for topic"""
        return self.COLOR_SCHEMES.get(topic, "professional teals and grays")
    
    def generate_prompt(self, analysis: Dict) -> PromptResult:
        """Generate comprehensive AI prompt"""
        
        title = analysis.get("title", "")
        category = analysis.get("category", "")
        tags = analysis.get("tags", [])
        technical_stack = analysis.get("technical_stack", [])
        visual_style = analysis.get("visual_style", "technical-illustration")
        tone = analysis.get("tone", "technical")
        audience = analysis.get("target_audience", "Mid-Level Professionals")
        
        # Get design parameters
        style_template = self.get_visual_style(visual_style)
        design_params = self.get_design_params(audience)
        color_scheme = self.get_color_scheme(category)
        
        # Build elements list
        elements = style_template["elements"]
        technical_elements = technical_stack[:3]
        all_elements = elements + technical_elements
        
        # Select composition
        if visual_style == "pipeline-flows":
            composition = self.COMPOSITION_PATTERNS["flow"]
        elif visual_style == "neural-networks":
            composition = self.COMPOSITION_PATTERNS["abstract"]
        elif visual_style == "architecture-diagrams":
            composition = self.COMPOSITION_PATTERNS["technical"]
        else:
            composition = self.COMPOSITION_PATTERNS["balanced"]
        
        # Generate blog cover image prompt
        blog_prompt = f"""
Professional blog cover image: {title}

Visual Style: {style_template['base']}
Theme: {category}
Technical Stack: {', '.join(technical_elements)}

Composition: {composition}
Color Palette: {color_scheme}
Mood: {style_template['mood']}, {design_params['style']}
Complexity: {design_params['complexity']}

Elements: {', '.join(all_elements)}

Design Requirements:
- 16:9 aspect ratio
- Professional, polished quality
- High resolution (1024x1024 or higher)
- Consistent tech aesthetic
- Dark modern background preferred
- No text overlays
- Clean, minimal design
- Production-ready quality

Technical Style: modern, contemporary, refined, professional SaaS illustration
""".strip()
        
        # Generate social media OG image prompt (1.91:1 ratio, text overlay space)
        social_prompt = f"""
Social media Open Graph image for LinkedIn, Twitter, Facebook:
Title: {title}

Base: Professional tech background
Style: {design_params['style']}, {design_params['complexity']}
Colors: {color_scheme}
Theme: {category}

Elements: {', '.join(all_elements[:5])}
Composition: {composition}, with top text overlay space

Requirements:
- 1.91:1 aspect ratio (1200x630px scaled)
- Bold, clear visual
- Text overlay friendly (top/bottom margins)
- High contrast
- Social media optimized
- Professional quality
- Shareable design
- Eye-catching but professional
""".strip()
        
        # Generate thumbnail prompt (1:1 ratio)
        thumbnail_prompt = f"""
Thumbnail image (1:1 square): {title}

Style: Bold, compact, icon-like
Technical Theme: {category}
Primary Elements: {', '.join(all_elements[:3])}

Requirements:
- 1:1 square aspect ratio (512x512)
- High contrast
- Recognizable icon-like quality
- Professional tech aesthetic
- Clear at small sizes
- Distinctive visual
""".strip()
        
        # Style keywords for filtering
        style_keywords = [
            visual_style,
            tone,
            category.lower().replace(" ", "-"),
            design_params['style'],
            "professional",
            "tech"
        ] + tags[:3]
        
        return PromptResult(
            blog_prompt=blog_prompt,
            social_prompt=social_prompt,
            thumbnail_prompt=thumbnail_prompt,
            style_keywords=style_keywords,
            composition=composition
        )
    
    def generate_all_prompts(self) -> Dict[str, Dict]:
        """Generate prompts for all analyzed posts"""
        
        analysis_data = self.load_analysis()
        
        if not analysis_data:
            print("⚠️  No content analysis found")
            return {}
        
        prompts_data = {
            "generated_at": Path("assets/auto/generated-prompts.json").stem,
            "total_posts": len(analysis_data),
            "prompts": {}
        }
        
        print("🤖 GENERATING AI IMAGE PROMPTS\n")
        
        for slug, analysis in analysis_data.items():
            prompt_result = self.generate_prompt(analysis)
            
            prompts_data["prompts"][slug] = {
                "title": analysis.get("title"),
                "category": analysis.get("category"),
                "blog_cover_prompt": prompt_result.blog_prompt,
                "social_og_prompt": prompt_result.social_prompt,
                "thumbnail_prompt": prompt_result.thumbnail_prompt,
                "style_keywords": prompt_result.style_keywords,
                "composition": prompt_result.composition,
                "visual_style": analysis.get("visual_style"),
                "tone": analysis.get("tone"),
                "audience": analysis.get("target_audience")
            }
            
            print(f"✓ {slug}")
            print(f"  → Style: {analysis.get('visual_style')}")
            print(f"  → Tone: {analysis.get('tone')}")
            print(f"  → Keywords: {', '.join(prompt_result.style_keywords[:3])}")
        
        return prompts_data
    
    def save_prompts(self, prompts_data: Dict):
        """Save generated prompts"""
        with open(self.prompts_file, 'w') as f:
            json.dump(prompts_data, f, indent=2)
        
        print(f"\n✓ Prompts saved: {self.prompts_file}")
    
    def generate_prompts_report(self, prompts_data: Dict) -> str:
        """Generate report of generated prompts"""
        
        report = f"""
🤖 AI PROMPT GENERATION REPORT

Total Posts: {prompts_data.get('total_posts', 0)}

Sample Prompts Generated:
"""
        
        for slug, prompt_info in list(prompts_data.get("prompts", {}).items())[:3]:
            report += f"\n📝 {slug}:"
            report += f"\n   Category: {prompt_info.get('category')}"
            report += f"\n   Tone: {prompt_info.get('tone')}"
            report += f"\n   Visual Style: {prompt_info.get('visual_style')}"
            report += f"\n   Keywords: {', '.join(prompt_info.get('style_keywords', [])[:3])}"
        
        return report
    
    def run(self):
        """Execute prompt generation"""
        
        print("\n" + "="*60)
        print("🤖 DBOS AI PROMPT GENERATOR")
        print("="*60 + "\n")
        
        # Generate prompts
        prompts_data = self.generate_all_prompts()
        
        if prompts_data:
            # Save prompts
            self.save_prompts(prompts_data)
            
            # Generate report
            report = self.generate_prompts_report(prompts_data)
            print(report)
            
            print("\n✅ Prompt generation complete!\n")
        else:
            print("\n❌ No prompts generated\n")

if __name__ == '__main__':
    generator = AIPromptGenerator()
    generator.run()
