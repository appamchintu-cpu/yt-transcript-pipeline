#!/usr/bin/env python3
"""
Cloud transcript fetcher.
Reads youtube_history_today.json, fetches transcripts for each URL,
and writes youtube_transcripts_today.md as output.
"""
import json
import re
import sys
import os

def extract_video_id(url):
    patterns = [
        r'(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def format_timestamp(seconds):
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def fetch_transcript(video_id):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id)
        segments = [{"text": seg.text, "start": seg.start, "duration": seg.duration} for seg in result]
        full_text = " ".join(seg["text"] for seg in segments)
        return full_text, None
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

    print(f"Processing {len(items)} items from today's YouTube history...")

    md = "# Today's YouTube Watch History — Transcripts\n\n"
    md += f"Total items: {len(items)}\n\n---\n\n"

    for idx, item in enumerate(items, 1):
        title = item.get("title") or "Untitled"
        url = item.get("url", "")
        channel = item.get("channel") or "Unknown Channel"
        item_type = "Short" if "/shorts/" in url else "Video"

        print(f"[{idx}/{len(items)}] [{item_type}] {title} — {url}")

        md += f"## {idx}. {title}\n"
        md += f"- **Type:** {item_type}\n"
        md += f"- **Channel:** {channel}\n"
        md += f"- **URL:** {url}\n\n"

        video_id = extract_video_id(url)
        if not video_id:
            md += "_Could not extract video ID from URL._\n\n---\n\n"
            continue

        transcript, error = fetch_transcript(video_id)
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
