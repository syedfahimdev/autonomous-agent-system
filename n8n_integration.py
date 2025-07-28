"""
n8n Integration Module for Autonomous Task Bot

This module provides comprehensive integration with n8n workflows,
including webhook notifications, task tracking, and automation triggers.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import config
from enum import Enum

class N8NEventType(Enum):
    """Enum for different n8n event types"""
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    AGENT_PROGRESS = "agent_progress"
    MEMORY_UPDATE = "memory_update"
    SYSTEM_HEALTH = "system_health"

class N8NIntegration:
    """Main n8n integration class"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or config.N8N_WEBHOOK_URL
        self.max_retries = 3
        self.retry_delay = 1
        self.timeout = 10
        
    def is_configured(self) -> bool:
        """Check if n8n is properly configured"""
        return bool(self.webhook_url)
    
    def send_event(self, event_type: N8NEventType, data: Dict[str, Any]) -> bool:
        """Send an event to n8n webhook"""
        if not self.is_configured():
            print("⚠️ N8N_WEBHOOK_URL not configured, skipping n8n notification")
            return False
        
        payload = {
            "event_type": event_type.value,
            "timestamp": datetime.now().isoformat(),
            "source": "autonomous-task-bot",
            "version": "1.0.0",
            "data": data
        }
        
        return self._send_with_retry(payload)
    
    def send_task_started(self, task_id: str, prompt: str, task_type: str = "general") -> bool:
        """Send task started event"""
        data = {
            "task_id": task_id,
            "prompt": prompt,
            "task_type": task_type,
            "status": "started"
        }
        return self.send_event(N8NEventType.TASK_STARTED, data)
    
    def send_task_completed(self, task_id: str, result: str, task_type: str = "general", 
                           execution_time: Optional[float] = None) -> bool:
        """Send task completed event"""
        data = {
            "task_id": task_id,
            "result": result,
            "task_type": task_type,
            "status": "completed",
            "execution_time": execution_time
        }
        return self.send_event(N8NEventType.TASK_COMPLETED, data)
    
    def send_task_failed(self, task_id: str, error: str, task_type: str = "general") -> bool:
        """Send task failed event"""
        data = {
            "task_id": task_id,
            "error": error,
            "task_type": task_type,
            "status": "failed"
        }
        return self.send_event(N8NEventType.TASK_FAILED, data)
    
    def send_agent_progress(self, task_id: str, agent_name: str, progress: str, 
                           step: int, total_steps: int) -> bool:
        """Send agent progress update"""
        data = {
            "task_id": task_id,
            "agent_name": agent_name,
            "progress": progress,
            "step": step,
            "total_steps": total_steps,
            "percentage": (step / total_steps) * 100
        }
        return self.send_event(N8NEventType.AGENT_PROGRESS, data)
    
    def send_memory_update(self, task_id: str, memory_type: str, action: str, 
                          content: str) -> bool:
        """Send memory update event"""
        data = {
            "task_id": task_id,
            "memory_type": memory_type,
            "action": action,
            "content": content
        }
        return self.send_event(N8NEventType.MEMORY_UPDATE, data)
    
    def send_system_health(self, status: str, details: Dict[str, Any]) -> bool:
        """Send system health check"""
        data = {
            "status": status,
            "details": details
        }
        return self.send_event(N8NEventType.SYSTEM_HEALTH, data)
    
    def _send_with_retry(self, payload: Dict[str, Any]) -> bool:
        """Send payload to n8n with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.webhook_url,
                    json=payload,
                    timeout=self.timeout,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    print(f"✅ Event sent to n8n successfully (attempt {attempt + 1})")
                    return True
                else:
                    print(f"⚠️ Failed to send to n8n: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Network error sending to n8n (attempt {attempt + 1}): {e}")
                
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
                self.retry_delay *= 2  # Exponential backoff
                
        print(f"❌ Failed to send to n8n after {self.max_retries} attempts")
        return False

# Global n8n integration instance
n8n = N8NIntegration()

def get_n8n_status() -> Dict[str, Any]:
    """Get n8n integration status"""
    return {
        "configured": n8n.is_configured(),
        "webhook_url": n8n.webhook_url if n8n.is_configured() else None,
        "max_retries": n8n.max_retries,
        "timeout": n8n.timeout
    }

def test_n8n_connection() -> bool:
    """Test n8n webhook connection"""
    if not n8n.is_configured():
        return False
    
    test_data = {
        "test": True,
        "message": "Testing n8n connection",
        "timestamp": datetime.now().isoformat()
    }
    
    return n8n.send_event(N8NEventType.SYSTEM_HEALTH, test_data) 