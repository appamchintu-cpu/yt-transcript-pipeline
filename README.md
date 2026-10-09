# Watch History Agent

I wanted a simple way to keep the useful parts of the YouTube videos I watch: the words, not another pile of downloaded video files. This project takes a list of YouTube links, fetches captions with yt-dlp, and gives you the transcript in your terminal and in a Markdown file.

That transcript collection could later become a searchable second brain for an AI agent. The agent could help you find a video you half-remember, revisit an idea, or spot topics that keep showing up in your watch history. That part still needs to be set up in an agent; this repo currently fetches and displays transcripts.

## Run it locally

You’ll need Python 3 and yt-dlp. Install the dependency from the project folder:

```bash
python3 -m pip install -r requirements.txt
```

Create a file called `youtube_history_today.json` beside the script. Add the videos you want to process:

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

The script prints each transcript as it retrieves it and saves a copy to `youtube_transcripts_today.md`. If a video has no accessible captions, it says so in the report.

## A few things to know

- You provide the video list. The script doesn’t sign in to YouTube or collect your watch history from the browser.
- yt-dlp fetches subtitle files only. The command includes `--skip-download`, so it does not download video or audio.
- Captions aren’t available for every video. YouTube can also limit requests, and language availability varies.
- Your history and transcript files are ignored by Git so they’re less likely to end up in a commit by accident. Still, treat them as private and check before sharing them.
- There’s no webhook or Make.com/n8n connection in the code today.

## Turning it into a second brain

The longer-term idea is to give an AI agent access to your transcript library and ask it to make a personal “YouTube History” skill. That skill could help you find videos by topic and answer questions from the transcripts you actually watched, rather than guessing. The setup prompt and more detail are in [PROJECT_GUIDE.md](PROJECT_GUIDE.md). The agent integration isn’t included in the current script.

You could also build an automation with Make.com or n8n later. Nothing is sent to those services by this project now.

## Tests

Run the offline tests with:

```bash
python3 -m unittest discover -s tests -v
```

They use a mocked yt-dlp call, so they don’t contact YouTube.

## GitHub Actions

There’s also a manual GitHub Actions workflow. It runs in GitHub’s cloud, takes the history JSON you provide, and makes the transcript report available as an artifact. That means your submitted history is processed outside your computer; only use the workflow if you’re comfortable with that.

## License

This repository doesn’t have a license yet.

## More detail

See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for the second-brain setup prompt, privacy notes, and ideas for what an agent skill could do.