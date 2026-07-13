#!/usr/bin/env python3
"""
Verify GitHub Actions Setup - Complete System Check
Validates all workflows, scripts, and configurations
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime

class GitHubSetupVerifier:
    def __init__(self, root_path="."):
        self.root = Path(root_path)
        self.workflows_path = self.root / ".github" / "workflows"
        self.scripts_path = self.root / "scripts" / "python"
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def run_all_checks(self):
        """Run all verification checks"""
        print("=" * 80)
        print("🔍 GITHUB ACTIONS SETUP VERIFICATION")
        print("=" * 80)
        print()
        
        self.check_workflows_exist()
        self.check_workflow_syntax()
        self.check_script_references()
        self.check_env_variables()
        self.check_requirements_txt()
        self.check_secrets_configuration()
        
        self.print_results()
    
    def check_workflows_exist(self):
        """Verify all workflow files exist"""
        print("📋 Checking workflow files...")
        if not self.workflows_path.exists():
            self.errors.append("Workflows directory not found!")
            return
        
        workflow_files = list(self.workflows_path.glob("*.yml"))
        if not workflow_files:
            self.errors.append("No workflow files found!")
            return
        
        for wf in sorted(workflow_files):
            self.passed.append(f"✅ Workflow exists: {wf.name}")
        
        print(f"   Found {len(workflow_files)} workflows")
    
    def check_workflow_syntax(self):
        """Validate YAML syntax in workflows"""
        print("🔧 Checking workflow syntax...")
        
        for wf in self.workflows_path.glob("*.yml"):
            try:
                with open(wf, 'r') as f:
                    yaml.safe_load(f)
                self.passed.append(f"✅ Valid YAML: {wf.name}")
            except yaml.YAMLError as e:
                self.errors.append(f"❌ YAML Error in {wf.name}: {str(e)[:100]}")
            except Exception as e:
                self.errors.append(f"❌ Error in {wf.name}: {str(e)[:100]}")
    
    def check_script_references(self):
        """Verify all scripts referenced in workflows exist"""
        print("🐍 Checking Python script references...")
        
        required_scripts = {
            # Core generation scripts
            'scripts/python/generate_blog.py',
            'scripts/python/generate_rss.py',
            'scripts/python/generate_sitemap.py',
            'scripts/python/generate_seo.py',
            'scripts/python/generate_performance_scores.py',
            'scripts/python/generate_content_strategy.py',
            'scripts/python/generate_distribution.py',
            
            # Image processing
            'scripts/python/auto_image_assigner.py',
            'scripts/python/image_library_manager.py',
            'scripts/python/image_selector.py',
            
            # Notifications
            'scripts/python/notify_telegram.py',
            'scripts/python/notify_email.py',
            'scripts/python/notify_recruiter.py',
            'scripts/python/notify_seo.py',
            'scripts/python/notify_viral.py',
            
            # Detection & Analysis
            'scripts/python/parse_blog_changes.py',
            'scripts/python/recruiter_detector.py',
            'scripts/python/viral_detector.py',
            'scripts/python/event_detection.py',
            'scripts/python/subscriber_segmentation.py',
            
            # Logging
            'scripts/python/log_notification.py',
            
            # Automation
            'automation/notifier.py',
        }
        
        missing_scripts = []
        for script in sorted(required_scripts):
            script_path = self.root / script
            if script_path.exists():
                self.passed.append(f"✅ Script exists: {script}")
            else:
                missing_scripts.append(script)
                self.errors.append(f"❌ Missing script: {script}")
        
        if missing_scripts:
            print(f"   ⚠️  {len(missing_scripts)} scripts missing")
        else:
            print(f"   ✅ All {len(required_scripts)} required scripts found")
    
    def check_env_variables(self):
        """Verify .env file contains required variables"""
        print("🔐 Checking environment variables...")
        
        env_file = self.root / ".env"
        if not env_file.exists():
            self.errors.append("❌ .env file not found!")
            return
        
        required_vars = [
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID',
            'GITHUB_TOKEN',
            'DASHBOARD_HUB_PASSWORD',
            'DEVTO_API_KEY',
            'MEDIUM_ACCESS_TOKEN',
            'LINKEDIN_CLIENT_ID',
            'RESEND_API_KEY',
        ]
        
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        missing_vars = []
        for var in required_vars:
            if var in env_content:
                self.passed.append(f"✅ Env var defined: {var}")
            else:
                missing_vars.append(var)
                self.warnings.append(f"⚠️  Missing .env variable: {var}")
        
        if missing_vars:
            print(f"   ⚠️  {len(missing_vars)} variables potentially missing")
        else:
            print(f"   ✅ All {len(required_vars)} required variables found")
    
    def check_requirements_txt(self):
        """Verify requirements.txt contains necessary dependencies"""
        print("📦 Checking Python dependencies...")
        
        req_file = self.scripts_path / "requirements.txt"
        if not req_file.exists():
            self.errors.append("❌ requirements.txt not found!")
            return
        
        required_packages = [
            'requests',
            'python-dotenv',
            'Pillow',
            'tweepy',
            'python-telegram-bot',
            'feedparser',
        ]
        
        with open(req_file, 'r') as f:
            req_content = f.read()
        
        missing_packages = []
        for pkg in required_packages:
            if pkg.lower() in req_content.lower():
                self.passed.append(f"✅ Dependency defined: {pkg}")
            else:
                missing_packages.append(pkg)
                self.warnings.append(f"⚠️  Missing dependency: {pkg}")
    
    def check_secrets_configuration(self):
        """Verify GitHub secrets are properly referenced"""
        print("🔒 Checking GitHub secrets references...")
        
        secrets_needed = [
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID',
            'TWITTER_API_KEY',
            'LINKEDIN_API_KEY',
            'DEVTO_API_KEY',
            'MEDIUM_ACCESS_TOKEN',
        ]
        
        workflows_with_secrets = 0
        for wf in self.workflows_path.glob("*.yml"):
            with open(wf, 'r') as f:
                content = f.read()
                if any(f'secrets.{s}' in content for s in secrets_needed):
                    workflows_with_secrets += 1
        
        if workflows_with_secrets > 0:
            self.passed.append(f"✅ {workflows_with_secrets} workflows reference secrets")
        else:
            self.warnings.append("⚠️  No workflows reference secrets")
    
    def print_results(self):
        """Print verification results"""
        print()
        print("=" * 80)
        print("📊 VERIFICATION RESULTS")
        print("=" * 80)
        print()
        
        if self.passed:
            print(f"✅ PASSED ({len(self.passed)} checks):")
            for msg in self.passed[:10]:  # Show first 10
                print(f"   {msg}")
            if len(self.passed) > 10:
                print(f"   ... and {len(self.passed) - 10} more")
            print()
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)} issues):")
            for msg in self.warnings:
                print(f"   {msg}")
            print()
        
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)} critical issues):")
            for msg in self.errors:
                print(f"   {msg}")
            print()
        
        # Summary
        total = len(self.passed) + len(self.warnings) + len(self.errors)
        status = "🟢 READY" if not self.errors else "🔴 NEEDS FIXES"
        
        print("=" * 80)
        print(f"{status} - GitHub Actions Setup: {len(self.passed)}/{total} checks passed")
        print("=" * 80)
        print()
        
        # Recommendations
        if self.errors or self.warnings:
            print("📋 RECOMMENDATIONS:")
            if self.errors:
                print("1. Fix critical errors listed above")
            if self.warnings:
                print("2. Review warnings and add missing configurations if needed")
            print("3. Test workflows manually in GitHub Actions")
            print("4. Monitor first few runs for any issues")
            print()

if __name__ == "__main__":
    verifier = GitHubSetupVerifier()
    verifier.run_all_checks()
