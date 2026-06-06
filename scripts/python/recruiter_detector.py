#!/usr/bin/env python3
"""
DBOS Recruiter Intelligence System
Detects and tracks recruiter/high-value visitor activity
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import re

class RecruiterDetector:
    """Detect recruiter and high-value visitor activity"""
    
    # Major tech company domains
    RECRUITER_DOMAINS = {
        "google.com": {"company": "Google", "score": 0.95, "tier": "FAANG"},
        "amazon.com": {"company": "Amazon", "score": 0.95, "tier": "FAANG"},
        "apple.com": {"company": "Apple", "score": 0.95, "tier": "FAANG"},
        "meta.com": {"company": "Meta", "score": 0.95, "tier": "FAANG"},
        "microsoft.com": {"company": "Microsoft", "score": 0.95, "tier": "FAANG"},
        "netflix.com": {"company": "Netflix", "score": 0.90, "tier": "Unicorn"},
        "airbnb.com": {"company": "Airbnb", "score": 0.90, "tier": "Unicorn"},
        "stripe.com": {"company": "Stripe", "score": 0.90, "tier": "Unicorn"},
        "uber.com": {"company": "Uber", "score": 0.90, "tier": "Unicorn"},
        "slack.com": {"company": "Slack", "score": 0.85, "tier": "VC-backed"},
        "databricks.com": {"company": "Databricks", "score": 0.90, "tier": "Unicorn"},
        "confluent.com": {"company": "Confluent", "score": 0.85, "tier": "VC-backed"},
        "elastic.co": {"company": "Elastic", "score": 0.85, "tier": "Public"},
        "hashicorp.com": {"company": "HashiCorp", "score": 0.85, "tier": "VC-backed"},
        "jetbrains.com": {"company": "JetBrains", "score": 0.80, "tier": "Public"},
        "github.com": {"company": "GitHub (Microsoft)", "score": 0.88, "tier": "FAANG"},
    }
    
    # LinkedIn referrer patterns
    LINKEDIN_PATTERNS = [
        r"linkedin\.com",
        r"in\.linkedin\.com",
    ]
    
    # Corporate IP ranges (sample - IPs from major tech companies)
    CORPORATE_IP_RANGES = {
        "8.8.0.0/16": "Google",
        "1.1.1.0/24": "Cloudflare",
        "52.0.0.0/8": "Amazon AWS",
    }
    
    def __init__(self):
        self.history_file = Path('analytics/recruiter-history.json')
        self.visitor_file = Path('analytics/visitor-activity.json')
        self.recruiter_history = self.load_recruiter_history()
        self.visitor_activity = self.load_visitor_activity()
    
    def load_recruiter_history(self) -> Dict:
        """Load recruiter detection history"""
        if self.history_file.exists():
            with open(self.history_file) as f:
                return json.load(f)
        return {
            "detections": [],
            "returning_recruiters": [],
            "high_value_visitors": [],
            "company_stats": {}
        }
    
    def load_visitor_activity(self) -> Dict:
        """Load visitor activity data"""
        if self.visitor_file.exists():
            with open(self.visitor_file) as f:
                return json.load(f)
        return {"visitors": [], "sessions": []}
    
    def save_recruiter_history(self):
        """Save recruiter detection history"""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.recruiter_history, f, indent=2)
    
    def save_visitor_activity(self):
        """Save visitor activity"""
        self.visitor_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.visitor_file, 'w') as f:
            json.dump(self.visitor_activity, f, indent=2)
    
    def detect_recruiter(self, visitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visitor data for recruiter characteristics"""
        detection = {
            "visitor_id": visitor_data.get("visitor_id", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "company": None,
            "recruiter_score": 0.0,
            "indicators": [],
            "is_recruiter": False,
            "returning": False,
            "tier": None,
            "high_value": False
        }
        
        # Check domain
        domain = visitor_data.get("domain", "")
        if domain:
            detection = self._check_domain(detection, domain)
        
        # Check referrer
        referrer = visitor_data.get("referrer", "")
        if self._is_linkedin_referrer(referrer):
            detection["indicators"].append("LinkedIn referrer")
            detection["recruiter_score"] += 0.3
        
        # Check IP (optional)
        ip = visitor_data.get("ip_address", "")
        if ip:
            detection = self._check_ip(detection, ip)
        
        # Check user agent
        user_agent = visitor_data.get("user_agent", "")
        if self._is_bot_user_agent(user_agent):
            detection["indicators"].append("Bot detection")
            detection["recruiter_score"] += 0.2
        
        # Check behavior
        pages_visited = visitor_data.get("pages_visited", [])
        time_on_site = visitor_data.get("time_on_site_seconds", 0)
        
        # Recruiters often visit portfolio/CV pages
        if any("cv" in page.lower() or "resume" in page.lower() for page in pages_visited):
            detection["indicators"].append("Viewed resume/CV")
            detection["recruiter_score"] += 0.25
        
        # Recruiters typically spend more time
        if time_on_site > 300:  # 5+ minutes
            detection["indicators"].append("Long session (5+ min)")
            detection["recruiter_score"] += 0.15
        
        # Check return visits
        if self._is_returning_visitor(visitor_data.get("visitor_id")):
            detection["returning"] = True
            detection["indicators"].append("Returning visitor")
            detection["recruiter_score"] += 0.2
        
        # Determine if recruiter
        detection["is_recruiter"] = detection["recruiter_score"] > 0.5
        detection["high_value"] = detection["recruiter_score"] > 0.7
        
        # Cap score at 1.0
        detection["recruiter_score"] = min(detection["recruiter_score"], 1.0)
        
        return detection
    
    def _check_domain(self, detection: Dict, domain: str) -> Dict:
        """Check domain against known recruiter companies"""
        domain_lower = domain.lower()
        
        for recruiter_domain, info in self.RECRUITER_DOMAINS.items():
            if recruiter_domain in domain_lower:
                detection["company"] = info["company"]
                detection["recruiter_score"] += info["score"]
                detection["tier"] = info["tier"]
                detection["indicators"].append(f"Domain: {info['company']}")
                break
        
        return detection
    
    def _check_ip(self, detection: Dict, ip: str) -> Dict:
        """Check IP address against known corporate ranges"""
        for ip_range, company in self.CORPORATE_IP_RANGES.items():
            if self._ip_in_range(ip, ip_range):
                detection["company"] = company
                detection["recruiter_score"] += 0.15
                detection["indicators"].append(f"Corporate IP: {company}")
                break
        
        return detection
    
    def _ip_in_range(self, ip: str, cidr_range: str) -> bool:
        """Check if IP is in CIDR range"""
        try:
            import ipaddress
            return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr_range)
        except:
            return False
    
    def _is_linkedin_referrer(self, referrer: str) -> bool:
        """Check if referrer is LinkedIn"""
        return any(re.search(pattern, referrer, re.IGNORECASE) for pattern in self.LINKEDIN_PATTERNS)
    
    def _is_bot_user_agent(self, user_agent: str) -> bool:
        """Check if user agent indicates bot"""
        bot_patterns = ["bot", "crawler", "spider", "scraper", "curl", "wget"]
        return any(pattern in user_agent.lower() for pattern in bot_patterns)
    
    def _is_returning_visitor(self, visitor_id: str) -> bool:
        """Check if visitor is returning"""
        for prev_detection in self.recruiter_history.get("detections", []):
            if prev_detection.get("visitor_id") == visitor_id:
                return True
        return False
    
    def process_visitors(self, visitors: List[Dict]) -> Dict[str, Any]:
        """Process visitor data for recruiter detection"""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_visitors": len(visitors),
            "recruiters_detected": [],
            "returning_recruiters": [],
            "high_value_leads": [],
            "company_breakdown": {},
            "alerts": []
        }
        
        for visitor in visitors:
            detection = self.detect_recruiter(visitor)
            
            if detection["is_recruiter"]:
                results["recruiters_detected"].append(detection)
                
                if detection["returning"]:
                    results["returning_recruiters"].append(detection)
                    results["alerts"].append({
                        "type": "recruiter_returning",
                        "company": detection["company"],
                        "score": detection["recruiter_score"],
                        "timestamp": detection["timestamp"]
                    })
                else:
                    results["alerts"].append({
                        "type": "recruiter_detected",
                        "company": detection["company"],
                        "score": detection["recruiter_score"],
                        "timestamp": detection["timestamp"]
                    })
                
                if detection["high_value"]:
                    results["high_value_leads"].append(detection)
                
                # Track company stats
                company = detection.get("company", "Unknown")
                if company not in results["company_breakdown"]:
                    results["company_breakdown"][company] = 0
                results["company_breakdown"][company] += 1
        
        # Update history
        self.recruiter_history["detections"].extend(results["recruiters_detected"])
        self.recruiter_history["returning_recruiters"].extend(results["returning_recruiters"])
        self.recruiter_history["high_value_visitors"].extend(results["high_value_leads"])
        
        # Update company stats
        for company, count in results["company_breakdown"].items():
            if company not in self.recruiter_history["company_stats"]:
                self.recruiter_history["company_stats"][company] = 0
            self.recruiter_history["company_stats"][company] += count
        
        self.save_recruiter_history()
        
        return results
    
    def get_recruiter_metrics(self) -> Dict[str, Any]:
        """Get recruiter detection metrics"""
        detections = self.recruiter_history.get("detections", [])
        
        return {
            "total_detections": len(detections),
            "unique_companies": len(self.recruiter_history.get("company_stats", {})),
            "returning_recruiters": len(self.recruiter_history.get("returning_recruiters", [])),
            "high_value_leads": len(self.recruiter_history.get("high_value_visitors", [])),
            "top_companies": sorted(
                self.recruiter_history.get("company_stats", {}).items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "average_recruiter_score": sum(d.get("recruiter_score", 0) for d in detections) / len(detections) if detections else 0
        }
    
    def generate_recruiter_report(self) -> Dict[str, Any]:
        """Generate comprehensive recruiter intelligence report"""
        metrics = self.get_recruiter_metrics()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "title": "Recruiter Intelligence Report",
            "summary": metrics,
            "top_companies": dict(metrics["top_companies"]),
            "recent_detections": self.recruiter_history.get("detections", [])[-10:],
            "returning_recruiters": self.recruiter_history.get("returning_recruiters", [])[-5:],
            "high_value_leads": self.recruiter_history.get("high_value_visitors", [])[-5:],
            "recommendations": self._generate_recommendations(metrics)
        }
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on recruiter data"""
        recommendations = []
        
        if metrics["high_value_leads"] > 0:
            recommendations.append(f"💼 {metrics['high_value_leads']} high-value leads detected - Consider updating portfolio highlights")
        
        if metrics["unique_companies"] > 10:
            recommendations.append("🌟 Strong recruiter interest - Consider public speaking or content marketing")
        
        if metrics["returning_recruiters"] > 3:
            recommendations.append("🔄 Multiple returning recruiters - May indicate serious interest")
        
        top_companies = dict(metrics["top_companies"])
        if top_companies:
            top_company = list(top_companies.keys())[0]
            recommendations.append(f"🎯 Most interested company: {top_company} - Consider targeted interview prep")
        
        return recommendations
    
    def run(self):
        """Execute recruiter detection"""
        print("\n🚀 DBOS Recruiter Intelligence System\n")
        
        # Sample visitor data for demonstration
        sample_visitors = [
            {
                "visitor_id": "visitor_001",
                "domain": "google.com",
                "referrer": "",
                "user_agent": "Mozilla/5.0",
                "pages_visited": ["/", "/cv", "/projects"],
                "time_on_site_seconds": 450
            },
            {
                "visitor_id": "visitor_002",
                "domain": "amazon.com",
                "referrer": "https://linkedin.com",
                "user_agent": "Mozilla/5.0",
                "pages_visited": ["/", "/resume"],
                "time_on_site_seconds": 320
            }
        ]
        
        results = self.process_visitors(sample_visitors)
        
        print(f"✓ Analyzed {results['total_visitors']} visitors")
        print(f"✓ Detected {len(results['recruiters_detected'])} recruiters")
        print(f"✓ Found {len(results['high_value_leads'])} high-value leads")
        print(f"✓ Found {len(results['returning_recruiters'])} returning recruiters")
        
        # Save results
        output_file = Path('analytics/recruiter-analysis.json')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Generate report
        report = self.generate_recruiter_report()
        report_file = Path('analytics/recruiter-report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Saved recruiter analysis: {output_file}")
        print(f"✓ Saved recruiter report: {report_file}")
        print("\n✅ Recruiter detection complete!\n")

if __name__ == '__main__':
    detector = RecruiterDetector()
    detector.run()
