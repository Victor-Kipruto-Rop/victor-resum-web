#!/usr/bin/env python3
"""
Generate placeholder blog post images using PIL (Pillow)
Creates attractive placeholder images for all blog posts in blog/assets/shared/posts.json
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
import hashlib

# Setup paths
BLOG_DIR = Path(__file__).parent
POSTS_JSON = BLOG_DIR / "assets/shared/posts.json"
IMAGES_DIR = Path(__file__).parent.parent / "assets" / "images"

# Ensure images directory exists
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Color palette for different categories
COLORS = {
    "Data Engineering": "#ff6b6b",
    "Infrastructure": "#4ecdc4",
    "Data Transformation": "#45b7d1",
    "DevOps": "#f7b731",
    "Python": "#5f27cd",
    "Analytics": "#00d2d3",
    "Streaming": "#ff6348",
    "Database": "#a29bfe",
    "Cloud": "#fab1a0",
    "Other": "#6c5ce7"
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_image(post_id, title, category, image_path):
    """Generate a placeholder image for a blog post"""
    
    # Image dimensions
    width, height = 1200, 630
    
    # Get color based on category
    color_hex = COLORS.get(category, COLORS["Other"])
    bg_color = hex_to_rgb(color_hex)
    
    # Create image with gradient effect
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Add semi-transparent overlay for better text contrast
    overlay_color = (0, 0, 0, 100)
    draw.rectangle([(0, 0), (width, height)], fill=overlay_color)
    
    # Add diagonal accent
    accent_color = (*hex_to_rgb(color_hex), 200)
    points = [(0, 0), (width, 0), (width//2, height), (0, height)]
    draw.polygon(points[:2] + [points[2], (0, height//2)], fill=accent_color)
    
    # Try to use a nice font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        category_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        category_font = ImageFont.load_default()
    
    # Add category badge
    badge_x = 50
    badge_y = 50
    badge_padding = 15
    
    # Draw category background
    category_bbox = draw.textbbox((badge_x, badge_y), category, font=category_font)
    category_width = category_bbox[2] - category_bbox[0] + (badge_padding * 2)
    category_height = category_bbox[3] - category_bbox[1] + (badge_padding * 2)
    
    draw.rectangle(
        [(badge_x, badge_y), (badge_x + category_width, badge_y + category_height)],
        fill=(255, 255, 255, 220)
    )
    draw.text(
        (badge_x + badge_padding, badge_y + badge_padding),
        category,
        font=category_font,
        fill=bg_color
    )
    
    # Wrap and center title
    max_chars = 40
    wrapped_lines = textwrap.wrap(title, width=max_chars)
    
    # Calculate total text height
    line_height = 70
    total_text_height = len(wrapped_lines) * line_height
    start_y = (height - total_text_height) // 2
    
    # Draw title
    for i, line in enumerate(wrapped_lines):
        y_position = start_y + (i * line_height)
        
        # Draw text with shadow effect
        shadow_offset = 3
        draw.text(
            (50 + shadow_offset, y_position + shadow_offset),
            line,
            font=title_font,
            fill=(0, 0, 0, 100)
        )
        
        # Draw main text
        draw.text(
            (50, y_position),
            line,
            font=title_font,
            fill=(255, 255, 255, 255)
        )
    
    # Add decorative elements
    accent_circle_x = width - 100
    accent_circle_y = height - 100
    accent_radius = 60
    
    draw.ellipse(
        [(accent_circle_x - accent_radius, accent_circle_y - accent_radius),
         (accent_circle_x + accent_radius, accent_circle_y + accent_radius)],
        fill=(*hex_to_rgb(color_hex), 150),
        outline=(255, 255, 255, 100),
        width=3
    )
    
    # Add corner text
    try:
        footer_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        footer_font = ImageFont.load_default()
    
    draw.text(
        (50, height - 60),
        "VICTOR KIPRUTO'S BLOG",
        font=footer_font,
        fill=(255, 255, 255, 180)
    )
    
    # Save image
    img.save(image_path, quality=90)
    return True


def main():
    """Main function to generate all blog post images"""
    
    print("📸 Blog Post Image Generator")
    print("=" * 50)
    
    try:
        with open(POSTS_JSON, 'r') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print(f"❌ assets/shared/posts.json not found at {POSTS_JSON}")
        return 1
    except json.JSONDecodeError:
        print(f"❌ assets/shared/posts.json is invalid JSON")
        return 1
    
    if not isinstance(posts, list):
        print("❌ assets/shared/posts.json should contain an array of posts")
        return 1
    
    generated_count = 0
    skipped_count = 0
    
    for post in posts:
        post_id = post.get('slug', post.get('id', 'unknown'))
        title = post.get('title', 'Untitled')
        category = post.get('category', 'Data Engineering')
        
        # Skip posts that already have custom images in assets/images
        if post.get('image'):
            image_ref = post['image']
            
            # Extract filename from image path
            if '/' in image_ref:
                filename = image_ref.split('/')[-1]
            else:
                filename = image_ref
            
            image_path = IMAGES_DIR / filename
            
            # Check if image already exists
            if image_path.exists():
                print(f"✓ {title:<50} (already exists)")
                skipped_count += 1
                continue
            
            # Generate image for posts with placeholder images
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                try:
                    generate_image(post_id, title, category, image_path)
                    print(f"✓ {title:<50} → {filename}")
                    generated_count += 1
                except Exception as e:
                    print(f"✗ {title:<50} ERROR: {e}")
    
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"   Generated: {generated_count} images")
    print(f"   Skipped:   {skipped_count} images (already exist)")
    print(f"   Location:  {IMAGES_DIR}")
    
    if generated_count > 0:
        print(f"\n✅ Successfully generated {generated_count} blog post images!")
    else:
        print(f"\n⚠️  No new images generated (all exist or no posts to process)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
