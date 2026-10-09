#!/usr/bin/env python3
"""Fetch YouTube captions with yt-dlp and display/save transcript text only."""
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path


def extract_video_url(url):
    """Normalize supported YouTube URLs and remove extra query parameters."""
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        query = urllib.parse.parse_qs(parsed.query)
        video_id = query.get("v", [""])[0]
        if not video_id and parsed.path.startswith(("/shorts/", "/live/")):
            parts = parsed.path.split("/")
            video_id = parts[2] if len(parts) > 2 else ""
    else:
        return url
    return f"https://www.youtube.com/watch?v={video_id}" if video_id else url


def parse_vtt_text(vtt):
    """Convert WebVTT caption cues into readable, deduplicated text."""
    lines, seen = [], set()
    for raw_line in vtt.splitlines():
        line = raw_line.strip()
        if not line or line == "WEBVTT" or line.startswith(("NOTE", "Kind:", "Language:")) or "-->" in line or line.isdigit():
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return " ".join(lines)


def fetch_transcript_ytdlp(url, language="en.*,en,hi,te,es,fr,de"):
    """Fetch subtitle files only; never download audio or video."""
    try:
        with tempfile.TemporaryDirectory(prefix="yt-captions-") as temp_dir:
            template = str(Path(temp_dir) / "%(id)s")
            result = subprocess.run(
                ["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
                 "--sub-langs", language, "--sub-format", "vtt", "--output", template,
                 "--no-warnings", extract_video_url(url)],
                capture_output=True, text=True, timeout=90, check=False,
            )
            files = sorted(Path(temp_dir).glob("*.vtt"))
            for caption_file in files:
                text = parse_vtt_text(caption_file.read_text(encoding="utf-8"))
                if text:
                    return text, None
            return None, result.stderr.strip()[-500:] or "No captions were available."
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)


def main():
    history_file = Path("youtube_history_today.json")
    output_file = Path("youtube_transcripts_today.md")
    if not history_file.exists():
        print(f"ERROR: {history_file} not found. Provide a JSON array of YouTube history items.", file=sys.stderr)
        return 1
    try:
        items = json.loads(history_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: Could not read history JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(items, list):
        print("ERROR: History JSON must contain a list of video entries.", file=sys.stderr)
        return 1
    videos = [item for item in items if isinstance(item, dict) and "/shorts/" not in item.get("url", "")]
    report = ["# YouTube Watch History — Transcripts", "", f"Processed videos: {len(videos)}", ""]
    for index, item in enumerate(videos, 1):
        title, url = item.get("title") or "Untitled", item.get("url", "")
        print(f"[{index}/{len(videos)}] {title} — fetching captions")
        transcript, error = fetch_transcript_ytdlp(url)
        report.extend([f"## {index}. {title}", f"- **Channel:** {item.get('channel') or 'Unknown Channel'}",
                       f"- **URL:** {url}", f"- **Section:** {item.get('section', 'Today')}", ""])
        if transcript:
            report.extend(["### Transcript", "", transcript, ""])
            print("\n" + transcript + "\n")
        else:
            report.extend([f"_Transcript unavailable: {error}_", ""])
            print(f"Transcript unavailable: {error}", file=sys.stderr)
        report.extend(["---", ""])
    output_file.write_text("\n".join(report), encoding="utf-8")
    print(f"Transcripts saved to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
