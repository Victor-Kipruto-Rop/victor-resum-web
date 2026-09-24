#!/usr/bin/env python3
"""
DBOS PHASE 6: Security Layer
Token-based authentication and session management
"""

import json
import hashlib
import hmac
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

class SecurityLayer:
    """Manage authentication, authorization, and security"""
    
    def __init__(self):
        self.tokens_file = Path('security/tokens.json')
        self.tokens_file.parent.mkdir(parents=True, exist_ok=True)
        self.secret_key = self.load_or_create_secret_key()
        self.tokens = self.load_tokens()
    
    def load_or_create_secret_key(self) -> str:
        """Load or create the master secret key"""
        key_file = Path('security/secret.key')
        
        if key_file.exists():
            with open(key_file, 'r') as f:
                return f.read().strip()
        else:
            # Generate new secret key
            key = secrets.token_hex(32)
            with open(key_file, 'w') as f:
                f.write(key)
            return key
    
    def load_tokens(self) -> Dict:
        """Load active tokens"""
        if self.tokens_file.exists():
            with open(self.tokens_file) as f:
                return json.load(f)
        return {"tokens": [], "sessions": []}
    
    def save_tokens(self):
        """Save tokens to file"""
        with open(self.tokens_file, 'w') as f:
            json.dump(self.tokens, f, indent=2)
    
    def generate_token(self, user_email: str, duration_hours: int = 8) -> Dict:
        """Generate a new authentication token"""
        token_id = secrets.token_urlsafe(32)
        token_value = secrets.token_urlsafe(64)
        
        # Hash the token for storage
        token_hash = hashlib.sha256(token_value.encode()).hexdigest()
        
        expires_at = datetime.utcnow() + timedelta(hours=duration_hours)
        
        token_data = {
            "id": token_id,
            "hash": token_hash,
            "email": user_email,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at.isoformat(),
            "last_used": datetime.utcnow().isoformat(),
            "ip_address": "0.0.0.0",  # Set by API
            "user_agent": "",  # Set by API
            "revoked": False
        }
        
        self.tokens["tokens"].append(token_data)
        self.save_tokens()
        
        return {
            "token": token_value,
            "token_id": token_id,
            "expires_at": expires_at.isoformat(),
            "type": "Bearer"
        }
    
    def verify_token(self, token_value: str) -> Tuple[bool, Optional[Dict]]:
        """Verify a token is valid and not expired"""
        try:
            token_hash = hashlib.sha256(token_value.encode()).hexdigest()
            
            for token in self.tokens["tokens"]:
                if token["hash"] == token_hash:
                    # Check expiration
                    expires_at = datetime.fromisoformat(token["expires_at"])
                    if datetime.utcnow() > expires_at:
                        return False, {"error": "Token expired"}
                    
                    # Check revocation
                    if token.get("revoked"):
                        return False, {"error": "Token revoked"}
                    
                    # Update last used
                    token["last_used"] = datetime.utcnow().isoformat()
                    self.save_tokens()
                    
                    return True, token
            
            return False, {"error": "Invalid token"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def revoke_token(self, token_id: str) -> bool:
        """Revoke a token"""
        for token in self.tokens["tokens"]:
            if token["id"] == token_id:
                token["revoked"] = True
                self.save_tokens()
                return True
        return False
    
    def revoke_all_user_tokens(self, user_email: str) -> int:
        """Revoke all tokens for a user"""
        count = 0
        for token in self.tokens["tokens"]:
            if token["email"] == user_email and not token.get("revoked"):
                token["revoked"] = True
                count += 1
        self.save_tokens()
        return count
    
    def create_session(self, token_id: str, ip_address: str, user_agent: str) -> Dict:
        """Create a session for a token"""
        session_id = secrets.token_urlsafe(32)
        
        session_data = {
            "session_id": session_id,
            "token_id": token_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "active": True
        }
        
        self.tokens["sessions"].append(session_data)
        self.save_tokens()
        
        return session_data
    
    def validate_session(self, session_id: str, ip_address: str) -> Tuple[bool, Optional[Dict]]:
        """Validate a session"""
        for session in self.tokens["sessions"]:
            if session["session_id"] == session_id:
                # Check if active
                if not session["active"]:
                    return False, {"error": "Session inactive"}
                
                # Check IP (optional, can be disabled)
                # if session["ip_address"] != ip_address:
                #     return False, {"error": "IP mismatch"}
                
                # Check last activity (8 hour timeout)
                last_activity = datetime.fromisoformat(session["last_activity"])
                if datetime.utcnow() - last_activity > timedelta(hours=8):
                    session["active"] = False
                    self.save_tokens()
                    return False, {"error": "Session expired"}
                
                # Update last activity
                session["last_activity"] = datetime.utcnow().isoformat()
                self.save_tokens()
                
                return True, session
        
        return False, {"error": "Invalid session"}
    
    def end_session(self, session_id: str) -> bool:
        """End a session"""
        for session in self.tokens["sessions"]:
            if session["session_id"] == session_id:
                session["active"] = False
                self.save_tokens()
                return True
        return False
    
    def get_user_sessions(self, user_email: str) -> list:
        """Get all active sessions for a user"""
        active_sessions = []
        
        for session in self.tokens["sessions"]:
            if session["active"]:
                # Find token
                for token in self.tokens["tokens"]:
                    if token["id"] == session["token_id"] and token["email"] == user_email:
                        active_sessions.append(session)
                        break
        
        return active_sessions
    
    def generate_audit_log(self) -> Dict:
        """Generate security audit log"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_tokens": len(self.tokens["tokens"]),
            "active_tokens": len([t for t in self.tokens["tokens"] if not t.get("revoked")]),
            "revoked_tokens": len([t for t in self.tokens["tokens"] if t.get("revoked")]),
            "total_sessions": len(self.tokens["sessions"]),
            "active_sessions": len([s for s in self.tokens["sessions"] if s.get("active")]),
            "expired_tokens": len([t for t in self.tokens["tokens"] 
                                  if datetime.utcnow() > datetime.fromisoformat(t["expires_at"])]),
            "token_summary": {
                "by_user": self._count_tokens_by_user()
            }
        }
    
    def _count_tokens_by_user(self) -> Dict:
        """Count tokens by user"""
        user_counts = {}
        for token in self.tokens["tokens"]:
            email = token["email"]
            user_counts[email] = user_counts.get(email, 0) + 1
        return user_counts
    
    def export_security_config(self) -> Dict:
        """Export security configuration"""
        return {
            "name": "DBOS Security Configuration",
            "version": "1.0",
            "created": datetime.utcnow().isoformat(),
            "security_policies": {
                "token_expiry_hours": 8,
                "session_timeout_hours": 8,
                "max_tokens_per_user": 5,
                "password_min_length": 8,
                "require_https": True,
                "rate_limit_requests": 100,
                "rate_limit_window_seconds": 60
            },
            "audit_log": self.generate_audit_log(),
            "features": {
                "token_based_auth": True,
                "session_management": True,
                "ip_tracking": True,
                "user_agent_tracking": True,
                "token_revocation": True,
                "audit_logging": True
            }
        }
    
    def run(self):
        """Execute security setup"""
        print("\n🚀 DBOS PHASE 6: Security Layer\n")
        
        # Generate demo tokens for testing
        admin_token = self.generate_token('admin@dbos.local')
        user_token = self.generate_token('user@dbos.local')
        
        print("✓ Token system initialized")
        print(f"  - Admin token generated")
        print(f"  - User token generated")
        
        # Export security config
        config = self.export_security_config()
        config_file = Path('security/config.json')
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Security configuration exported to {config_file}")
        
        # Print audit log
        audit_log = self.generate_audit_log()
        print(f"\n📊 Security Audit Log:")
        print(f"  - Active Tokens: {audit_log['active_tokens']}")
        print(f"  - Active Sessions: {audit_log['active_sessions']}")
        print(f"  - Total Users: {len(audit_log['token_summary']['by_user'])}")
        
        print("\n✅ Security layer setup complete!\n")

if __name__ == '__main__':
    security = SecurityLayer()
    security.run()
