#!/usr/bin/env python3
"""
n8n Integration Setup Script

This script helps you set up n8n integration for your autonomous task bot.
"""

import os
import requests
import json
from datetime import datetime
from n8n_integration import test_n8n_connection, get_n8n_status

def setup_n8n_integration():
    """Interactive setup for n8n integration"""
    
    print("🚀 n8n Integration Setup for Autonomous Task Bot")
    print("=" * 50)
    
    # Check current configuration
    status = get_n8n_status()
    print(f"\n📊 Current Status:")
    print(f"   Configured: {status['configured']}")
    print(f"   Webhook URL: {status['webhook_url'] or 'Not set'}")
    
    if status['configured']:
        print("\n✅ n8n is already configured!")
        test_connection = input("Would you like to test the connection? (y/n): ").lower()
        if test_connection == 'y':
            if test_n8n_connection():
                print("✅ Connection test successful!")
            else:
                print("❌ Connection test failed!")
        return
    
    print("\n🔧 Setting up n8n integration...")
    
    # Get webhook URL
    webhook_url = input("\nEnter your n8n webhook URL: ").strip()
    
    if not webhook_url:
        print("❌ Webhook URL is required!")
        return
    
    # Test the webhook
    print(f"\n🧪 Testing webhook: {webhook_url}")
    
    try:
        test_payload = {
            "event_type": "system_health",
            "timestamp": datetime.now().isoformat(),
            "source": "autonomous-task-bot",
            "version": "1.0.0",
            "data": {
                "test": True,
                "message": "Testing n8n webhook connection"
            }
        }
        
        response = requests.post(webhook_url, json=test_payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print(f"⚠️ Webhook test returned status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return
    
    # Update environment file
    env_file = ".env"
    env_content = ""
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Add or update N8N_WEBHOOK_URL
    if "N8N_WEBHOOK_URL" in env_content:
        # Update existing
        lines = env_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("N8N_WEBHOOK_URL="):
                lines[i] = f"N8N_WEBHOOK_URL={webhook_url}"
                break
        env_content = '\n'.join(lines)
    else:
        # Add new
        env_content += f"\nN8N_WEBHOOK_URL={webhook_url}\n"
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ n8n webhook URL saved to {env_file}")
    
    # Test final connection
    print("\n🧪 Testing final connection...")
    if test_n8n_connection():
        print("✅ n8n integration setup complete!")
    else:
        print("❌ Final connection test failed. Please check your webhook URL.")

def show_n8n_workflow_instructions():
    """Show instructions for setting up n8n workflow"""
    
    print("\n📋 n8n Workflow Setup Instructions")
    print("=" * 40)
    
    print("""
1. Open your n8n instance
2. Create a new workflow
3. Add a 'Webhook' trigger node
4. Configure the webhook with:
   - Method: POST
   - Path: /webhook (or your preferred path)
   - Save the webhook URL

5. Add conditional nodes to handle different event types:
   - task_started
   - task_completed  
   - task_failed
   - agent_progress
   - memory_update
   - system_health

6. Add action nodes for notifications:
   - Slack notifications
   - Email alerts
   - Database logging (Notion, Airtable, etc.)
   - SMS notifications
   - Discord webhooks

7. Import the sample workflow:
   - Use the provided n8n_workflow_example.json
   - Modify it according to your needs

8. Test the workflow with the test endpoint:
   POST /api/n8n/test
""")

def main():
    """Main setup function"""
    
    print("🤖 Autonomous Task Bot - n8n Integration Setup")
    print("=" * 55)
    
    while True:
        print("\nOptions:")
        print("1. Setup n8n webhook integration")
        print("2. Show workflow setup instructions")
        print("3. Test current connection")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            setup_n8n_integration()
        elif choice == "2":
            show_n8n_workflow_instructions()
        elif choice == "3":
            if test_n8n_connection():
                print("✅ Connection test successful!")
            else:
                print("❌ Connection test failed!")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main() 