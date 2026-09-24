#!/usr/bin/env python3
"""
DBOS Master Orchestrator
Runs all 15 DBOS systems in correct order
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

class DBOSOrchestrator:
    """Master orchestrator for all DBOS systems"""
    
    PHASES = {
        "phase_1": [
            ("generate_blog.py", "Blog Rendering Engine"),
            ("generate_rss.py", "RSS Feed Generator"),
            ("generate_sitemap.py", "Sitemap Generator"),
        ],
        "phase_2": [
            ("generate_seo.py", "SEO Engine"),
        ],
        "phase_3": [
            ("generate_performance_scores.py", "Performance Scoring Engine"),
        ],
        "phase_4": [
            ("generate_content_strategy.py", "AI Content Strategist"),
            ("generate_distribution.py", "Social Distribution Engine"),
        ],
        "phase_5": [
            # GitHub Actions workflows (external)
        ],
        "phase_6": [
            ("generate_security.py", "Security Layer"),
        ]
    }
    
    def __init__(self):
        self.script_dir = Path("scripts/python")
        self.results = {
            "timestamp": datetime.utcnow().isoformat(),
            "phases": {}
        }
    
    def run_generator(self, script_name: str, display_name: str) -> bool:
        """Run a single generator script"""
        script_path = self.script_dir / script_name
        
        if not script_path.exists():
            print(f"❌ {display_name}: Script not found ({script_path})")
            return False
        
        try:
            print(f"\n▶️  Running {display_name}...")
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.script_dir.parent,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"✅ {display_name}: Complete")
                return True
            else:
                print(f"❌ {display_name}: Failed")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}")
                return False
        except subprocess.TimeoutExpired:
            print(f"⏱️  {display_name}: Timeout (>5 minutes)")
            return False
        except Exception as e:
            print(f"❌ {display_name}: Exception - {str(e)}")
            return False
    
    def run_phase(self, phase_name: str, generators: list) -> dict:
        """Run all generators in a phase"""
        phase_results = {
            "name": phase_name.replace("_", " ").upper(),
            "status": "running",
            "generators": {},
            "start_time": datetime.utcnow().isoformat()
        }
        
        print(f"\n{'='*60}")
        print(f"🚀 {phase_results['name']}")
        print(f"{'='*60}")
        
        success_count = 0
        for script_name, display_name in generators:
            if self.run_generator(script_name, display_name):
                phase_results["generators"][display_name] = "success"
                success_count += 1
            else:
                phase_results["generators"][display_name] = "failed"
        
        phase_results["status"] = "complete"
        phase_results["end_time"] = datetime.utcnow().isoformat()
        phase_results["success_count"] = success_count
        phase_results["total_count"] = len(generators)
        
        return phase_results
    
    def run_all(self, phases_to_run: list = None):
        """Run all DBOS systems"""
        if phases_to_run is None:
            phases_to_run = list(self.PHASES.keys())
        
        print("\n" + "="*60)
        print("🎯 DBOS COMPLETE SYSTEM ORCHESTRATOR")
        print("="*60)
        print(f"📅 {datetime.utcnow().isoformat()}")
        print(f"📋 Phases to run: {', '.join(phases_to_run)}")
        print("="*60)
        
        total_generators = 0
        total_success = 0
        
        for phase in phases_to_run:
            if phase not in self.PHASES:
                print(f"⚠️  Unknown phase: {phase}")
                continue
            
            generators = self.PHASES[phase]
            if not generators:
                print(f"\n⏭️  {phase.upper()}: No generators (external workflows)")
                continue
            
            phase_results = self.run_phase(phase, generators)
            self.results["phases"][phase] = phase_results
            
            total_generators += phase_results["total_count"]
            total_success += phase_results["success_count"]
        
        # Print summary
        self.print_summary(total_generators, total_success)
        
        # Save results
        self.save_results()
    
    def print_summary(self, total: int, success: int):
        """Print execution summary"""
        print("\n" + "="*60)
        print("📊 EXECUTION SUMMARY")
        print("="*60)
        
        for phase_name, phase_data in self.results["phases"].items():
            status_icon = "✅" if phase_data["status"] == "complete" else "⏳"
            print(f"\n{status_icon} {phase_data['name']}")
            for generator, result in phase_data["generators"].items():
                result_icon = "✅" if result == "success" else "❌"
                print(f"   {result_icon} {generator}")
        
        print("\n" + "="*60)
        print(f"🎉 Total: {success}/{total} generators successful")
        
        if success == total and total > 0:
            print("✨ ALL SYSTEMS OPERATIONAL ✨")
        elif success > 0:
            print(f"⚠️  {total - success} generator(s) failed")
        else:
            print("❌ No generators ran successfully")
        
        print("="*60 + "\n")
    
    def save_results(self):
        """Save execution results"""
        results_file = Path("execution-results.json")
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📁 Results saved to {results_file}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="DBOS Master Orchestrator")
    parser.add_argument("--phases", nargs="+", 
                       choices=["phase_1", "phase_2", "phase_3", "phase_4", "phase_5", "phase_6"],
                       default=["phase_1", "phase_2", "phase_3", "phase_4", "phase_6"],
                       help="Phases to run")
    parser.add_argument("--all", action="store_true", help="Run all phases")
    
    args = parser.parse_args()
    
    phases = list(DBOSOrchestrator.PHASES.keys()) if args.all else args.phases
    
    orchestrator = DBOSOrchestrator()
    orchestrator.run_all(phases)

if __name__ == '__main__':
    main()
