# Project Guide: YouTube Watch History as an AI Second Brain

## Current implementation

The script reads a local JSON list of video entries, skips Shorts, and uses yt-dlp with media downloading disabled to fetch available caption files. It displays transcript text in the terminal and writes a Markdown report. It does not log in to YouTube, inspect browser profiles, obtain your account history by itself, send webhooks, or create an AI knowledge base.

### Local use

Install yt-dlp:

```sh
python3 -m pip install -r requirements.txt
```

Create `youtube_history_today.json` in the project root, for example:

```json
[
  {"title": "Example video", "url": "https://www.youtube.com/watch?v=VIDEO_ID", "channel": "Example channel"}
]
```

Then run:

```sh
python3 fetch_transcripts.py
```

Transcript text is printed and saved to `youtube_transcripts_today.md`. If captions are missing or unavailable, the report says so. Caption availability, language, and rate limits affect results. The script downloads no media.

## Optional automation: Make.com or n8n (future work)

A future extension could send structured transcript records to Make.com or n8n for categorization, summarization, storage, or other automation. **This repository currently has no webhook sender and does not connect to either service.** Any integration should be implemented separately, with endpoints and secrets configured securely, and with a privacy review before sending personal watch data to a third party.

## The second-brain idea

A second brain for an AI agent means feeding it the videos and transcript content you watch each day, so it can consult that personal knowledge later. Instead of guessing from general knowledge, the agent could retrieve the relevant video and use its transcript to answer questions about something you watched—giving a precise response grounded in your viewing material and tailored to your expectations.

One possible future bootstrap step is for the agent to examine accumulated watch history, discover themes and categories that fit the actual content (rather than relying on a fixed taxonomy), and create a personalized query skill or command. Later, you could ask about a topic from a video and have the agent answer from your stored transcript collection. This is a product vision, not a capability implemented by the current script.

Possible future directions:

- **Bootstrap and pattern discovery:** infer useful groupings from the user's own history and help generate a personalized agent skill.
- **Query and interest mapping:** find relevant watched videos and answer questions using their transcripts and metadata.
- **Viewing-pattern summaries:** explore the mix of educational, entertainment, or Shorts content. Any classification should be transparent and based on real data; “doom-scroll” is only one possible user-defined lens.

These ideas would need an agent-side knowledge store/search layer in addition to this transcript fetcher.

## Privacy and security

Watch history and transcripts can reveal personal interests. Keep generated files private unless you intentionally choose to share them. `.gitignore` excludes the local history input and transcript output to reduce the chance of accidental publication. Before sending data to an AI service, Make.com, n8n, or GitHub Actions, review what is being sent and how long that service retains it.

## GitHub Actions note

An existing manually triggered workflow accepts the history JSON as a base64 input and uploads its transcript report as a downloadable artifact. That runs in GitHub's cloud environment, not on your local machine. Workflow inputs, logs, and artifacts may be retained; submit watch data only if you are comfortable with that exposure. It does not send a webhook.

## Tests

Run `python3 -m unittest discover -s tests -v`. The tests mock yt-dlp subprocess execution and do not make live network requests.

## Files

- `fetch_transcripts.py` — transcript-only fetcher and display/output script
- `requirements.txt` — yt-dlp dependency
- `README.md` — overview and quick start
- `.github/workflows/transcribe.yml` — optional manual Actions workflow
- `tests/` — offline tests

No license is specified yet.

## Local output files

`youtube_history_today.json` and `youtube_transcripts_today.md` are local input/output files and are intentionally ignored by Git. Do not commit private watch history or transcript data.

---

## Important privacy note

History and transcript files present in previous commits may remain accessible in the public Git history after removal from the current version. Their current-tree removal does not erase prior commits.