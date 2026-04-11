#!/usr/bin/env python3
"""
Magnum Progress Reporter - Sends status updates to Telegram every 3 minutes
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
TELEGRAM_BOT_TOKEN = "8562696632:AAEkhgiHhZBoOabjlh6Gw9AkbQHWtSx0mec"  # Bot de Magnum
TELEGRAM_CHAT_ID = "7666543493"  # Chat ID de Jose en Telegram

# Paperclip config
PAPERCLIP_API_KEY = "pcp_f3e1b628f753a66f03f15a1b9d6c0d98e4b14e5f8581edc5"
PAPERCLIP_API_URL = "http://31.97.214.129:65158"
AGENT_ID = "1a6961f7-1c5c-479a-ad40-bb86c613f22e"
COMPANY_ID = "44a2bc4e-bfce-420a-ba86-bf3424f43366"
TASK_TITLE = "Configurar Ollama como provider de modelos"

def get_run_status():
    """Get current run status from Paperclip"""
    try:
        # Get agent status first
        agent_response = requests.get(
            f"{PAPERCLIP_API_URL}/api/agents/{AGENT_ID}",
            headers={"Authorization": f"Bearer {PAPERCLIP_API_KEY}"},
            timeout=10
        )
        
        if agent_response.status_code != 200:
            return {"status": "error", "error": f"Agent API failed: {agent_response.status_code}"}
        
        agent = agent_response.json()
        
        # Get latest heartbeat run
        runs_response = requests.get(
            f"{PAPERCLIP_API_URL}/api/companies/{COMPANY_ID}/heartbeat-runs?agentId={AGENT_ID}",
            headers={"Authorization": f"Bearer {PAPERCLIP_API_KEY}"},
            timeout=10
        )
        
        latest_run = {}
        if runs_response.status_code == 200:
            runs = runs_response.json()
            if isinstance(runs, list) and len(runs) > 0:
                latest_run = runs[0]
        
        return {
            "status": agent.get("status", "unknown"),
            "lastHeartbeatAt": agent.get("lastHeartbeatAt", "Never"),
            "lastError": agent.get("lastError", ""),
            "exitCode": latest_run.get("exitCode", "N/A"),
            "stdoutExcerpt": latest_run.get("stdoutExcerpt", "")[:500] if latest_run.get("stdoutExcerpt") else "",
            "stderrExcerpt": latest_run.get("stderrExcerpt", "")[:500] if latest_run.get("stderrExcerpt") else ""
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def send_telegram_message(message):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,  # 7666543493
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

def main():
    """Main function"""
    run = get_run_status()
    
    status = run.get("status", "unknown")
    started_at = run.get("startedAt", "pending")
    finished_at = run.get("finishedAt", "running...")
    exit_code = run.get("exitCode", "en ejecución")
    
    # Build status message
    message = f"""
🤖 *Magnum Progress Report*
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 *Status:* `{status}`
🕐 *Last Heartbeat:* {run.get('lastHeartbeatAt', 'Never')}
🔧 *Task:* {TASK_TITLE}

"""
    
    # Add agent status explanation
    if status == 'idle':
        message += "✅ *Magnum está IDLE* (disponible, sin hacer nada)\n"
    elif status == 'error':
        message += "❌ *Magnum tuvo un ERROR*\n"
    elif status == 'running':
        message += "🔄 *Magnum está EJECUTANDO*\n"
    
    # Add error details if any
    if run.get('lastError'):
        error_text = run['lastError']
        if len(error_text) > 800:
            error_text = error_text[:800] + '...'
        message += f"\n❌ *Error:*\n```{error_text}```"
    
    # Add stdout/stderr if available
    if run.get('stdoutExcerpt'):
        excerpt = run['stdoutExcerpt'][:500]
        message += f"\n📄 *Output:*\n```{excerpt}...```"
    
    if run.get('stderrExcerpt'):
        excerpt = run['stderrExcerpt'][:500]
        message += f"\n📄 *Error Log:*\n```{excerpt}...```"
    
    message += "\n_This is an automated update every 3 minutes_"
    
    # Send to Telegram
    success = send_telegram_message(message)
    
    if success:
        print("✅ Telegram message sent successfully")
    else:
        print("❌ Failed to send Telegram message")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
