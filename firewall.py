#!/usr/bin/env python3
"""LEVITICAL FIREWALL - Advanced Filtering with AHAZAZEAL"""
import logging, json, hashlib
from typing import Dict, Any, List
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    CLEAN = "CLEAN"
    SUSPICIOUS = "SUSPICIOUS"
    DANGEROUS = "DANGEROUS"
    CRITICAL = "CRITICAL"

class LeviticalFirewall:
    def __init__(self):
        self.rules: List[Dict[str, Any]] = []
        self.blocked_entities: List[Dict[str, Any]] = []
        self.allowed_entities: List[Dict[str, Any]] = []
        logger.info("[FIREWALL] Levitical Firewall initialized")
    
    def add_rule(self, rule_name: str, pattern: str, action: str) -> Dict[str, Any]:
        """Add firewall rule"""
        rule = {
            "rule_id": hashlib.sha256(rule_name.encode()).hexdigest()[:8],
            "name": rule_name,
            "pattern": pattern,
            "action": action,
            "created_at": datetime.utcnow().isoformat()
        }
        self.rules.append(rule)
        logger.info(f"[FIREWALL] Rule added: {rule_name}")
        return rule
    
    def evaluate_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate entity against firewall rules"""
        entity_str = json.dumps(entity).lower()
        threat_level = ThreatLevel.CLEAN
        
        for rule in self.rules:
            if rule["pattern"].lower() in entity_str:
                if rule["action"] == "BLOCK":
                    threat_level = ThreatLevel.CRITICAL
                    self.blocked_entities.append(entity)
                    logger.warning(f"[FIREWALL] Entity BLOCKED by rule: {rule['name']}")
                    return {"status": "BLOCKED", "threat_level": threat_level.value}
        
        self.allowed_entities.append(entity)
        return {"status": "ALLOWED", "threat_level": threat_level.value}
    
    def get_firewall_status(self) -> Dict[str, Any]:
        return {
            "firewall_name": "LEVITICAL_FIREWALL",
            "rules_active": len(self.rules),
            "entities_blocked": len(self.blocked_entities),
            "entities_allowed": len(self.allowed_entities),
            "status": "OPERATIONAL"
        }

if __name__ == "__main__":
    fw = LeviticalFirewall()
    fw.add_rule("Block Trackers", "tracker", "BLOCK")
    fw.add_rule("Block Vipers", "viper", "BLOCK")
    fw.add_rule("Block Spam", "spam", "BLOCK")
    
    fw.evaluate_entity({"type": "safe_data"})
    fw.evaluate_entity({"type": "tracker_viper"})
    
    print(json.dumps(fw.get_firewall_status(), indent=2))
