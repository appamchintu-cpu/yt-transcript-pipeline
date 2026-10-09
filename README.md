# Watch History Agent

Turn YouTube watch history into readable transcripts—and, eventually, a structured knowledge base your AI agent can query. Today this project uses **yt-dlp to fetch captions only**: it does not download video or audio, and it does not send webhooks.

## What it does today

- Reads video entries from a local `youtube_history_today.json` file.
- Skips YouTube Shorts.
- Fetches available subtitle tracks with yt-dlp and `--skip-download`.
- Prints transcript text in the terminal and saves a Markdown report to `youtube_transcripts_today.md`.
- Reports when captions cannot be retrieved.

It does not automatically access your browser's watch history, send data to Make.com/n8n, or build an AI-agent memory/skill. See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for the second-brain vision and future integration ideas.

## Quick start

Requirements: Python 3 and yt-dlp. Install yt-dlp:

```bash
python3 -m pip install -r requirements.txt
```

Create `youtube_history_today.json` in the project folder:

```json
[
  {
    "title": "Example video",
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "channel": "Example channel",
    "section": "Today"
  }
]
```

Run the script:

```bash
python3 fetch_transcripts.py
```

The transcript appears in your terminal and is saved to `youtube_transcripts_today.md`. The input and generated output are ignored by Git by default to help avoid publishing personal watch data.

## Notes

- A video must have captions available in one of the selected languages; YouTube may also rate-limit requests.
- yt-dlp is called with `--skip-download` and subtitle-only options. No audio or video is downloaded.
- The script processes only the JSON you provide. It does not log in to YouTube or read browser profiles.
- Watch history and transcripts can be sensitive. Review the data before sharing it with any service.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The tests are offline and mock yt-dlp; they do not contact YouTube.

## GitHub Actions

A manual workflow is available under Actions. It accepts history JSON as a base64 input and uploads the transcript report as an artifact. GitHub Actions is a cloud environment—not local-only processing—so only submit data you are comfortable processing there. No webhook is sent.

## License

No license is specified yet.

## Files

- `fetch_transcripts.py` — transcript-only fetcher and display/output script
- `requirements.txt` — Python dependency
- `PROJECT_GUIDE.md` — current behavior, future integrations, and second-brain concept
- `.github/workflows/transcribe.yml` — optional manual Actions workflow
- `tests/` — offline tests
