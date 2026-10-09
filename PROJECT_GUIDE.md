# Project guide: a second brain for your YouTube history

## What this project does today

Give the script a list of YouTube links. It asks yt-dlp for captions, prints any transcript it can retrieve, and saves a Markdown report. It does not sign in to your account, collect watch history from your browser, or send anything to a webhook.

The code only asks for subtitle files. It uses yt-dlp's `--skip-download` option, so it does not download video or audio.

## Try it locally

Install yt-dlp:

```sh
python3 -m pip install -r requirements.txt
```

In the project folder, create `youtube_history_today.json` with the videos you want to process:

```json
[
  {"title": "Example video", "url": "https://www.youtube.com/watch?v=VIDEO_ID", "channel": "Example channel"}
]
```

Run the script:

```sh
python3 fetch_transcripts.py
```

You’ll see progress and retrieved transcript text in the terminal. The complete report is written to `youtube_transcripts_today.md`. Some videos don’t have captions, and YouTube may limit requests. When that happens, the report notes that no transcript was available.

## The second-brain idea

I’d like to be able to ask an AI agent about a video I watched last week and get an answer from that video’s transcript, not a plausible-sounding guess. A collection of transcripts can give an agent something concrete to search when you want to remember a detail or find videos you’ve watched about a topic.

This repo doesn’t build that agent integration yet. It fetches and displays transcripts. The prompt below is for an AI agent that can read local files and create skills. Give it to the agent you want to use with your transcripts, then review what it proposes before letting it read or change anything.

### Prompt for your AI agent

```text
I want to make a private “YouTube History” skill for this AI agent. It should help me search and ask questions about YouTube videos I’ve watched, using the transcripts and history files I choose to provide.

Before you access any files or create anything, tell me which files you propose to read and where you would save the skill or any search index. Wait for my approval. Don’t ask me for passwords, browser cookies, API keys, or webhook secrets.

Once I approve, use only the history and transcript files I approved to determine what I watched. Don’t fill gaps with guesses or silently search the web. If a transcript is missing or unclear, tell me. Keep the video title and URL with each useful answer so I can check the source; include the watch date if the file has one.

Read through the approved material and look for themes and categories that actually fit it. Don’t start with a fixed list of categories. Show me the patterns you notice and let me correct them before you build the skill. Ask me what I mean by subjective labels such as “useful” or “doom-scrolling” instead of deciding for me.

Then create a reusable skill or command, ideally called “YouTube History”, that can:
- Find videos I watched about a topic and answer questions from their transcripts.
- Explain what a particular video covered and help me revisit its ideas.
- Cite the relevant video title and URL, and say when the available material doesn’t support an answer.
- If I ask, summarize patterns in my viewing, such as recurring topics or Shorts versus longer videos. Explain what data you used and where the result is uncertain.

For questions about my watch history, use the approved local collection first. Only use outside sources when I explicitly ask for broader research, and keep outside information separate from transcript-based answers. Keep my files and the skill private and local by default. Don’t send anything to a webhook, Make.com, n8n, or another service unless I separately approve exactly what will be sent and where. Don’t change or delete my original history or transcript files.

When you finish, tell me how to use the skill, which files you read or created, what it can and can’t answer, and whether you accessed the network. Don’t say it’s ready until you’ve checked that it can find and cite an item from my approved collection.
```

That prompt is a starting point, not a magic switch. Your agent needs permission to read the transcript files and must support creating a custom skill or command. If your collection is large, it may also need a local search index or another way to find the right transcript quickly.

### What you could use the skill for

You might ask, “Which videos I watched talked about local AI?” or “What did that video say about memory?” The agent should point you to the transcript it used and be upfront if the transcript doesn’t answer the question.

If you want, the skill could also look for patterns in your viewing: recurring topics, video formats, or how much of a day’s watch history was Shorts. Those summaries depend on what information your files contain. Labels like “useful” and “doom-scrolling” are personal judgments, so the agent should use your definitions rather than invent its own.

## Make.com and n8n

You could extend the project to send transcript data to Make.com or n8n and use those tools to organize or process it. That connection is not implemented here: this repository currently sends no webhooks. Before adding one, decide what data should leave your computer, where it should go, and how its credentials and retention will be handled.

## Privacy

Watch history can be personal. The input file and generated transcript report are ignored by Git to help prevent accidental commits, but still check `git status` before pushing changes. Don’t upload transcripts or history to an AI service, GitHub Actions, Make.com, n8n, or another provider unless you’re comfortable with how that service handles them.

The optional GitHub Actions workflow runs in GitHub’s cloud. It takes the history JSON you provide and makes the transcript report available as an artifact. That is not local-only processing.

## Tests

Run:

```sh
python3 -m unittest discover -s tests -v
```

The tests mock yt-dlp and don’t make network requests.

## License

This repository doesn’t have a license yet.

## One privacy caveat

The current version no longer contains the sample history and transcript output, but those files appeared in earlier public commits. Removing them from the latest version does not remove them from Git history. Anyone who may have accessed the repository earlier could still have copies.