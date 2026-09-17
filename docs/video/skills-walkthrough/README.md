# Agentic Engineering Skills — the action cut

*Install. Ask. Review.*

A **2 minute 20 second** walkthrough for someone who already has a Google ADK
agent. It opens with the installation command, then shows two practical requests:

1. Connect an existing React chat: name the frontend skill, inspect code excerpts,
   and watch a reply stream into the interface.
2. Remember a preferred language: name the memory skill, save with consent, and
   carry the preference into a new conversation.

There is **no voice-over**. Animated typing, code excerpts, interface changes and
short central labels tell the story. The warm paper, serif type and brick-red
accent follow the supplied editorial style. The soundtrack is
“just turn it on and make something.” by hijaq.

## What the example demonstrates

The editor and interface are animated **worked examples**, grounded in the
[runnable local demo](demo/README.md). Its HTTP endpoint, browser stream handling,
SQLite preferences, consent and ownership checks are real. Its model/event source
and sign-in identities are explicit offline doubles. The React file is an
integration excerpt, not a claim that an existing React application was built.

The film does not record a live coding-client session. It demonstrates the
request → implementation → review workflow, with exact code excerpts and actual
local test results. No cloud deployment is performed.

The previous 5:58 silent and music editions remain in `output/`. The new cut has
its own `output/action-cut/` directory, which also retains the earlier
“Life of Riley” export.

## Build locally

Use Python 3.12, Manim, Cairo/Pango and FFmpeg:

```bash
brew install python@3.12 cairo pango pkg-config ffmpeg
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The default fonts are **Georgia** and **Menlo**. You can override them with
`ADK_VIDEO_SERIF` and `ADK_VIDEO_MONO` using installed fonts.

From this directory, first generate the demo evidence as described in
[its README](demo/README.md), then render:

```bash
# Quick layout/motion preview; compresses reading holds.
.venv/bin/python build.py --preview

# Full 1920 × 1080, 30 fps cut with reading time.
.venv/bin/python build.py

# Add the downloaded track to a separate export.
python3 add_music.py
```

`build.py --skip-render` repeats packaging without rendering again. The preview
uses `output/action-cut/preview/`; full output uses `output/action-cut/`.

### Soundtrack source

Download **“just turn it on and make something.” by hijaq.** from the
[official Bandcamp track page](https://hijaqmusic.bandcamp.com/track/just-turn-it-on-and-make-something).
Choose **Buy Digital Track**, enter **0**, then use **download to your computer**
and **Download Now**. Save the MP3 as
`output/music-hijaq/just-turn-it-on-and-make-something-hijaq.mp3` before running
`add_music.py`. Bandcamp also lets you pay to support the artist.

This edition uses the artist's published free-use permission on
[SoundCloud](https://soundcloud.com/hijaqmusic), also confirmed in the
[artist's FAQ](https://docs.google.com/document/d/1lfkvGJJ3mN4bo0tguU4oWIpVdwTAC_HdWL0Isv8aIKo/edit?usp=sharing).
The track remains credited to hijaq.; no Creative Commons licence is asserted.

The script preserves the opening and outro, repeats an interior passage with a
two-second crossfade to cover the full film, and normalizes to −18 LUFS before
opening and closing fades. It copies the video and chapters unchanged and verifies
stream duration, video identity and decoding. Paste the
[plain-text music credit](youtube-music-credit.txt) into the YouTube description;
the [publishing notes](publishing.md#music-credits) include the same credit.

## Outputs

| File in `output/action-cut/` | Purpose |
| --- | --- |
| `agentic-engineering-skills-action-hijaq.mp4` | Finished video with hijaq. soundtrack |
| `agentic-engineering-skills-action-with-music.mp4` | Earlier “Life of Riley” edition |
| `agentic-engineering-skills-action.mp4` | Silent master |
| `contact-sheet.jpg` | Complete frames from all twelve scenes |
| `transcript.md` | Copyable screen text and requests |
| `timeline.json` | Actual scene times |
| `build-report.json` | Resolution, duration and chapter checks |
| `mix-report-hijaq.json` | Current soundtrack edits and validation |
| `layout-checks.json` | Text size and width evidence |
| `frames/` | Full-resolution scene frames |

Generated outputs, music downloads and local environments are ignored by Git.

## Copy the requests

Run this in the terminal inside your application's project directory:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*'
```

Choose your coding client in the installer. Use the same project in that client;
start a new session if newly installed skills do not appear. Installation needs
Git and Node.js 22.20+ with npm. Full setup is in the [repository README](../../../README.md).

Then send a request in the coding-agent chat:

```text
/adk-frontend-integration
Connect our React chat to this ADK agent.
Reuse our login. Stream replies and tool progress.
Check session ownership. Add tests.
```

```text
/adk-memory-architecture
Remember my language between conversations.
Reuse our login and database. Ask before saving.
Let me change or forget it. Add tests.
```

Claude Code uses `/skill-name`; Codex uses `$skill-name`. In Google clients,
write “Use the adk-engineer skill to…”. When you have not chosen a specialist,
start with `adk-engineer` and describe the change. See the
[Google client guide](../../integrations/google-coding-agents.md) for account
requirements and installation details.

## Editing

- [storyboard.json](storyboard.json): twelve beats and their reading time.
- [walkthrough.py](walkthrough.py): animated terminal, prompts, code and chat.
- [demo/](demo/README.md): tested source, excerpts and replay evidence.
- [build.py](build.py): render, package, chapters, transcript and contact sheet.
- [add_music.py](add_music.py): soundtrack normalization and muxing.
- [publishing.md](publishing.md): title, description, timestamps and attribution.

Keep code excerpts short and legible. Keep explanatory copy attached to the
current action; do not reintroduce paragraphs across the lower screen. Review
both the contact sheet and the final animation after edits.
