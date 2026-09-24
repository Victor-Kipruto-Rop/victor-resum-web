#!/usr/bin/env python3
"""
Dashboard HTML Enhancement Script
Automatically adds missing theme toggle buttons to dashboard files
"""

import os
import re
from pathlib import Path

class HTMLEnhancer:
    def __init__(self, dashboard_path: str):
        self.dashboard_path = Path(dashboard_path)
        self.enhanced_count = 0
        self.skipped_count = 0
        
    def enhance_files(self) -> None:
        """Enhance all HTML files that need theme toggles"""
        html_files = sorted(self.dashboard_path.glob('*.html'))
        
        print("=" * 80)
        print("🔧 DASHBOARD HTML FILES ENHANCEMENT")
        print("=" * 80)
        print(f"\nProcessing: {self.dashboard_path}\n")
        
        for html_file in html_files:
            self.enhance_file(html_file)
        
        self.print_summary()
    
    def enhance_file(self, file_path: Path) -> None:
        """Add theme toggle to individual file if needed"""
        filename = file_path.name
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if file already has theme toggle
        if self._has_theme_toggle(content):
            print(f"✅ {filename:<40} Already has theme toggle")
            self.skipped_count += 1
            return
        
        # Check if file has navigation (our marker for enhanced files)
        if not self._has_navigation(content):
            print(f"⏭️  {filename:<40} No navigation found, skipping")
            self.skipped_count += 1
            return
        
        # Add theme toggle
        try:
            updated_content = self._add_theme_toggle(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✨ {filename:<40} Theme toggle added successfully")
            self.enhanced_count += 1
        except Exception as e:
            print(f"❌ {filename:<40} Error: {str(e)}")
            self.skipped_count += 1
    
    def _has_theme_toggle(self, content: str) -> bool:
        """Check if file already has theme toggle"""
        toggle_patterns = [
            r'theme-toggle|themeToggle|toggleTheme',
            r'localStorage.*theme',
        ]
        return sum(1 for pattern in toggle_patterns if re.search(pattern, content)) >= 1
    
    def _has_navigation(self, content: str) -> bool:
        """Check if file has navigation bar"""
        return bool(re.search(r'<nav', content, re.IGNORECASE))
    
    def _add_theme_toggle(self, content: str) -> str:
        """Add theme toggle script to file"""
        # Find the closing </body> tag
        body_close_match = re.search(r'</body>', content, re.IGNORECASE)
        
        if not body_close_match:
            raise Exception("Could not find </body> tag")
        
        # Theme toggle script
        theme_script = '''
    <script>
        // Theme Toggle Logic
        const themeToggle = document.querySelector('[id*="theme-toggle"], [id*="themeToggle"]');
        const body = document.body;
        
        if (themeToggle) {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                body.classList.add('dark-mode');
            }
            
            themeToggle.addEventListener('click', () => {
                body.classList.toggle('dark-mode');
                const theme = body.classList.contains('dark-mode') ? 'dark' : 'light';
                localStorage.setItem('theme', theme);
            });
        }
    </script>
'''
        
        # Insert before </body>
        insert_position = body_close_match.start()
        new_content = content[:insert_position] + theme_script + content[insert_position:]
        
        return new_content
    
    def print_summary(self) -> None:
        """Print enhancement summary"""
        print("\n" + "=" * 80)
        print("📊 ENHANCEMENT SUMMARY")
        print("=" * 80)
        print(f"Files Enhanced:  {self.enhanced_count}")
        print(f"Files Skipped:   {self.skipped_count}")
        print(f"Total Processed: {self.enhanced_count + self.skipped_count}")
        print("=" * 80)

def main():
    dashboard_path = '/home/kipruto/Desktop/resume/dashboard'
    
    if not os.path.exists(dashboard_path):
        print(f"❌ Dashboard path not found: {dashboard_path}")
        return
    
    enhancer = HTMLEnhancer(dashboard_path)
    enhancer.enhance_files()

if __name__ == '__main__':
    main()
