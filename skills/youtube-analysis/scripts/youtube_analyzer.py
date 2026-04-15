#!/usr/bin/env python3
"""
YouTube Video Analyzer for Ábaco
Extracts transcripts and analyzes YouTube videos for insights
"""

import subprocess
import sys
import json
import re
from pathlib import Path

def extract_transcript(video_url, output_dir="/tmp"):
    """Extract transcript using yt-dlp"""
    output_file = f"{output_dir}/transcript_{hash(video_url)}"
    
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--skip-download",
        "--convert-subs", "srt",
        "--output", output_file,
        video_url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def extract_transcript_txt(video_url):
    """Extract transcript as plain text using yt-dlp"""
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--skip-download",
        "--convert-subs", "vtt",
        "-o", "/tmp/transcript_%(id)s",
        video_url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # Find the vtt file and convert to text
        vtt_files = list(Path("/tmp").glob("transcript_*.vtt"))
        if vtt_files:
            vtt_file = vtt_files[0]
            with open(vtt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Parse VTT to plain text
            lines = content.split('\n')
            text_lines = [l for l in lines if l and not l.startswith('-->') and not l.isdigit() and not l.startswith('WEBVTT')]
            return True, '\n'.join(text_lines)
        
        return False, "No transcript found"
    except Exception as e:
        return False, str(e)

def analyze_with_claude(transcript, analysis_type="comprehensive"):
    """Analyze transcript using Claude via direct API"""
    import requests
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return None, "No API key found"
    
    prompt = f"""Analyze this YouTube video transcript and provide:
    
1. **Resumen Ejecutivo** (3-5 bullet points)
2. **Insights Clave** (datos numéricos, conceptos importantes)
3. **Action Items** (próximos pasos mencionados)
4. **Relevancia para Presupuesto Inmobiliario** (si aplica)

Transcript:
{transcript[:5000]}

Format response as JSON with keys: resumen, insights, action_items, relevance
"""
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "x-api-key": api_key
            },
            json={
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_analyzer.py <youtube_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"🎬 Analyzing: {url}")
    
    success, result = extract_transcript_txt(url)
    if success:
        print(f"✅ Transcript extracted ({len(result)} chars)")
        print(f"\n--- TRANSCRIPT ---")
        print(result[:2000])
    else:
        print(f"❌ Error: {result}")
