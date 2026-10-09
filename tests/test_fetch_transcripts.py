import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fetch_transcripts import extract_video_url, parse_vtt_text, fetch_transcript_ytdlp


class TranscriptFetcherTests(unittest.TestCase):
    def test_normalizes_youtube_url(self):
        self.assertEqual(extract_video_url("https://youtu.be/abc123?t=20"), "https://www.youtube.com/watch?v=abc123")

    def test_parses_vtt_and_deduplicates_caption_cues(self):
        vtt = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n<c>Hello there</c>\n\n00:00:02.000 --> 00:00:03.000\n<c>Hello there</c>\n"
        self.assertEqual(parse_vtt_text(vtt), "Hello there")

    @patch("fetch_transcripts.subprocess.run")
    def test_uses_caption_only_flags_and_returns_transcript(self, run):
        def fake_run(command, **kwargs):
            template = command[command.index("--output") + 1]
            outdir = Path(template.replace("%(id)s", "abc123")).parent
            (outdir / "abc123.en.vtt").write_text("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nHello from captions\n", encoding="utf-8")
            return type("Completed", (), {"stdout": "", "stderr": "", "returncode": 0})()

        run.side_effect = fake_run
        text, error = fetch_transcript_ytdlp("https://youtu.be/abc123")
        self.assertEqual(text, "Hello from captions")
        self.assertIsNone(error)
        command = run.call_args.args[0]
        self.assertIn("--skip-download", command)
        self.assertIn("--write-auto-subs", command)
        self.assertIn("--write-subs", command)
        self.assertNotIn("--extract-audio", command)
        self.assertNotIn("--format", command)


if __name__ == "__main__":
    unittest.main()

# Run with: python3 -m unittest discover -s tests -v
