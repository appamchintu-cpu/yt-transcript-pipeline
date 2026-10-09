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

### Agent setup prompt (copy into your AI agent)

```text
Help me turn my local YouTube watch-history and transcript files into a private, searchable second brain, then create a custom reusable skill/command named “YouTube History” (or the closest supported equivalent in this agent).

First, inspect what capabilities this agent supports for local files, persistent knowledge/search, and creating skills. Explain the proposed files/data you will read and where you would write the skill. Ask for my approval before accessing private watch-history/transcript data or creating/modifying files. Never ask me to paste passwords, cookies, access tokens, or webhook secrets.

Use only the local history and transcript files I approve as evidence about what I watched. Do not infer viewing activity from general knowledge or silently browse the web to fill gaps. If a transcript is missing or incomplete, say so. Keep source references (video title, URL, watch date/time when available, and transcript filename/section) so answers can be traced back to the relevant item.

After approval, inspect the supplied records and transcripts. Discover recurring topics, categories, formats, and interests from the actual data instead of imposing a rigid taxonomy. Summarize the structure you found and ask me to correct it before encoding it into the skill. Do not assume that a category such as “useful,” “entertainment,” or “doom-scrolling” is objective; ask how I want those defined.

Create a concise custom skill/command that can:
1. Bootstrap or refresh its understanding of the local watch-history/transcript collection and adapt its organization as new data arrives.
2. Answer questions about videos I watched, topics covered, takeaways, and interests, grounding each answer in specific video/transcript references. If evidence is insufficient, clearly say so rather than guessing.
3. Optionally summarize viewing patterns (for example, Shorts versus long-form or topic distribution) only when the available metadata supports it, explaining assumptions and uncertainty.

The skill should prefer the approved local knowledge source for questions about my watch history. It may use outside sources only when I explicitly ask for broader research, and it must distinguish external information from transcript-grounded facts. Preserve privacy: keep data and skill local/private by default, do not transmit it to a webhook, Make.com, n8n, or any cloud service unless I separately approve the exact destination, payload, and handling. Do not modify or delete my original history/transcript files.

When finished, tell me exactly which files were read and created/changed, how to invoke the new skill, what data limitations remain, and whether any network access occurred. Do not claim the second brain is ready unless the agent can actually search the approved records and the new skill has been verified.
```

### Capabilities the resulting skill is intended to support

- **Bootstrap and pattern discovery:** infer useful groupings from the user's own history, review those patterns with the user, and encode the agreed approach into a personalized agent skill.
- **Query and interest mapping:** find relevant watched videos and answer questions using their transcripts and metadata, with traceable references and honest uncertainty.
- **Viewing-pattern summaries:** explore the mix of educational, entertainment, or Shorts content. Any classification should be transparent and based on real data; “doom-scroll” is only one possible user-defined lens.

These capabilities require an agent-side knowledge store/search layer in addition to this transcript fetcher; they are a prompt/specification for an agent to implement with user approval, not functionality currently built into this repository.

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