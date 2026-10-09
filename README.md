# Watch History Agent

Turn the YouTube videos you watch into a personal library of transcripts—and, over time, a searchable second brain for your AI agent.

**Right now:** give the script a JSON file of video links. It uses yt-dlp to fetch available captions, prints the transcript, and saves a Markdown report. It does not download video/audio, read your browser history automatically, or send anything to a webhook.

> The second-brain and custom-agent-skill features described below are a vision and setup prompt. They are not built into the current script yet.

## Try it out

You need Python 3 and yt-dlp. Install the dependency:

```bash
python3 -m pip install -r requirements.txt
```

Create `youtube_history_today.json` in the project directory:

```json
[
  {
    "title": "Example video",
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "channel": "Example channel"
  }
]
```

Then run:

```bash
python3 fetch_transcripts.py
```

You’ll see progress and any retrieved transcript text in the terminal. The full report is saved as `youtube_transcripts_today.md`. The sample above is only a format example; replace it with your own video information.

## What to expect

- The script processes links you provide; it does not sign in to YouTube or collect your watch history for you.
- It asks yt-dlp for subtitles only (`--skip-download`), never video or audio.
- Captions may be missing, unavailable in the requested languages, or rate-limited by YouTube.
- Your history file and generated transcript report are excluded from Git by default. Keep them private unless you choose to share them.
- There is no webhook, Make.com/n8n connection, or AI memory integration in the current code.

## The longer-term idea

With an agent that can access your local transcript files, you could ask it to build a custom “YouTube History” skill. The agent would discover themes in your actual watch history, help organize the material, and let you ask later what a video covered or what you’ve been watching. See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for a ready-to-copy setup prompt and the full vision. That requires agent-side setup; this repository currently only fetches and displays transcripts.

A future version could also connect to Make.com or n8n for automation, but no webhook is implemented here today.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The tests are offline and do not contact YouTube.

## GitHub Actions

An optional manual workflow can process history JSON in GitHub Actions and save the transcript report as an artifact. This sends the supplied data to GitHub’s cloud environment; use it only if you are comfortable with that. It does not send a webhook.

## Project guide

See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for the agent setup prompt, second-brain concept, privacy notes, and future ideas.

## License

No license has been specified.