#!/usr/bin/env python3
"""
Cloud transcript fetcher using yt-dlp to extract auto-subtitles/transcripts.
Filters out Shorts and processes only regular YouTube videos.
"""
import json
import os
import re
import subprocess
import sys

def parse_vtt(vtt_path):
    """Parse a WebVTT subtitle file into clean plain text."""
    if not os.path.exists(vtt_path):
        return ""
    
    lines = []
    seen = set()
    with open(vtt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("WEBVTT") or "-->" in line or line.isdigit():
                continue
            line = re.sub(r'<[^>]+>', '', line)
            if line not in seen:
                seen.add(line)
                lines.append(line)
    return " ".join(lines)

def fetch_transcript_ytdlp(url, output_dir):
    """Use yt-dlp to download auto-subtitles for a YouTube video."""
    try:
        cmd = [
            "yt-dlp",
            "--write-auto-subs",
            "--write-subs",
            "--sub-lang", "en,hi,te,es,fr,de",
            "--skip-download",
            "--sub-format", "vtt",
            "--output", os.path.join(output_dir, "%(id)s"),
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        vtt_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".vtt")]
        if not vtt_files:
            return None, "This video does not have closed captions or auto-generated subtitles available on YouTube."
        
        vtt_path = vtt_files[0]
        text = parse_vtt(vtt_path)
        
        for f in vtt_files:
            try:
                os.remove(f)
            except:
                pass
                
        if not text:
            return None, "Subtitle file was empty."
        return text, None
        
    except Exception as e:
        return None, str(e)

def main():
    history_file = "youtube_history_today.json"
    output_file = "youtube_transcripts_today.md"

    if not os.path.exists(history_file):
        print(f"ERROR: {history_file} not found.")
        sys.exit(1)

    with open(history_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Filter out Shorts
    filtered_items = [item for item in items if "/shorts/" not in item.get("url", "")]
    print(f"Total items in history: {len(items)}. Filtered out Shorts, processing {len(filtered_items)} regular videos...")

    md = "# Today's YouTube Watch History — Transcripts (Cloud via yt-dlp)\n\n"
    md += f"Processed videos: {len(filtered_items)}\n\n---\n\n"

    for idx, item in enumerate(filtered_items, 1):
        title = item.get("title") or "Untitled"
        url = item.get("url", "")
        channel = item.get("channel") or "Unknown Channel"
        item_section = item.get("section", "Today")

        print(f"[{idx}/{len(filtered_items)}] Processing: {title} ({url})")

        md += f"## {idx}. {title}\n"
        md += f"- **Channel:** {channel}\n"
        md += f"- **URL:** {url}\n"
        md += f"- **Section:** {item_section}\n\n"

        temp_dir = f"temp_subs_{idx}"
        os.makedirs(temp_dir, exist_ok=True)
        
        transcript, error = fetch_transcript_ytdlp(url, temp_dir)
        
        try:
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)
        except:
            pass

        if transcript:
            md += "### Transcript\n\n"
            md += f"{transcript}\n\n"
        else:
            md += f"_Transcript unavailable: {error}_\n\n"

        md += "---\n\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\nDone! Transcripts saved to {output_file}")

if __name__ == "__main__":
    main()
