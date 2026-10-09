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

Imagine being able to ask your AI agent, “What was that video I watched about local AI?” and get an answer from the actual video transcript—not a guess. That’s the goal of the second-brain idea: build a searchable library from the videos you watch, then let your agent use it to answer questions and notice patterns that matter to you.

The transcript-fetching script in this repository is the first step. The agent integration and custom “YouTube History” skill are not built yet. If your AI agent supports local files and custom skills, give it the prompt below to help set them up.

### Setup prompt for your AI agent

Copy the text below into the AI agent you want to use with your transcript collection:

```text
I want to create a private, searchable “YouTube History” second brain from my own watch-history and transcript files. Help me set it up as a reusable skill or command in this AI agent, if supported.

Before doing anything, explain what files you propose to inspect and where you would create the skill or index. Ask me to approve access to my files and creation or modification of files. Do not ask me for passwords, browser cookies, API keys, or webhook secrets.

After I approve, use only the history and transcript files I specifically approve to determine what I watched. Do not guess from general knowledge, and do not search the web to fill gaps unless I explicitly ask for outside research. If a transcript is missing, incomplete, or unclear, tell me.

Look through the approved records and discover recurring topics, interests, and useful categories from the actual content. Do not force a preset category system. Show me the patterns you found and let me correct them before creating the skill. Ask me how I want subjective labels such as “useful” or “doom-scrolling” defined; do not treat those labels as objective facts.

Then create a reusable skill/command, preferably called “YouTube History”, that lets me:
- Ask what a watched video covered, find videos about a topic, and explore themes in my viewing.
- Get answers grounded in specific transcripts, with the video title and URL (and watch date/time when available) cited as sources.
- See when the available transcripts do not contain enough information, instead of receiving a guessed answer.
- Optionally request viewing-pattern summaries, such as topics or Shorts versus long-form, only when the records contain enough evidence; explain assumptions and uncertainty.

Keep the skill and data local/private by default. Do not send them to a webhook, Make.com, n8n, or another cloud service unless I separately approve the exact destination and data to be sent. Do not alter or delete my original history or transcript files.

When done, explain how I invoke the skill, which files you read and created, what the skill can and cannot answer, and whether you used any network access. Do not say setup is complete unless you verified the skill can find and cite entries from my approved transcript collection.
```

### What the custom skill should help you do

- **Build itself around your data:** notice recurring topics and create an organization that fits the videos you actually watch, rather than imposing fixed categories.
- **Ask questions about your viewing:** find relevant videos and answer from their transcripts, citing the source and acknowledging gaps.
- **Explore viewing habits:** optionally summarize topics, formats, or Shorts versus long-form. Treat subjective labels as your choice and explain any assumptions.

This is a guide for an AI agent to perform a setup with your approval—not an automatic feature of the transcript script. The agent may need its own local search/index or knowledge store to make a large transcript collection searchable.

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