# Agentic Engineering Skills — the video walkthrough

*A short introduction, from installation to the next useful change.*

This **5 minute 58 second silent video** explains what coding-agent skills are,
shows how to install this collection, and walks through two requests against an existing
Python Google ADK application:

1. Remember a user's preferred language using the existing database and login.
2. Connect an existing React chat with private conversations and streamed replies.

The diagrams explain the changes to ask for and the checks to review. They are
**illustrations, not recordings of generated code or passing tests**. No cloud
deployment is performed. All explanation appears on screen; there is no
narration or soundtrack.

## Build locally

Use **Python 3.12** in an isolated virtual environment. Manim needs native Cairo
and Pango libraries; the export step needs **FFmpeg**, including `ffprobe`.
On macOS with Homebrew, install the native dependencies:

```bash
brew install python@3.12 cairo pango pkg-config ffmpeg
```

From this directory:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

The renderer defaults to **Georgia** for prose and **Menlo** for commands. It
checks that both fonts are installed before rendering. On another platform,
install those fonts or choose available serif and monospace fonts explicitly:

```bash
ADK_VIDEO_SERIF="Liberation Serif" ADK_VIDEO_MONO="DejaVu Sans Mono" \
  .venv/bin/python build.py --preview
```

Preview the layout and animation with compressed reading holds at
**960 × 540, 15 fps**:

```bash
.venv/bin/python build.py --preview
```

Build the complete **1920 × 1080, 30 fps** video with full reading time:

```bash
.venv/bin/python build.py
```

The build uses the same Python interpreter for Manim. It renders a silent video,
then exports H.264 with `yuv420p` pixels, chapter metadata, and MP4 fast-start for
playback. It checks the exported resolution, duration and absence of an audio
stream. The preview is shorter than the final video because it compresses holds.

To repeat only packaging after a successful render:

```bash
.venv/bin/python build.py --skip-render
# Or repackage the preview:
.venv/bin/python build.py --preview --skip-render
```

## Outputs

The full build writes to `output/`; the preview writes to `output/preview/`.
Both directories contain:

| File | Purpose |
| --- | --- |
| `agentic-engineering-skills.mp4` | The final silent video |
| `contact-sheet.jpg` | Numbered frames for reviewing all scenes together |
| `transcript.md` | Copyable screen text, commands and example requests |
| `timeline.json` | Actual scene start/end times from the renderer |
| `chapters.ffmetadata` | Chapter markers embedded in the video |
| `build-report.json` | Export properties and duration checks |
| `layout-checks.json` | Renderer font sizes and text widths for review |
| `frames/` | One complete frame per scene |
| `media/` | Manim render files and intermediate video |

Generated outputs and the local virtual environment are ignored by Git.
Review the full export before publishing it. There is no public video URL until
a reviewed version is uploaded.

## Copy the examples

### Install in your application's project directory

Run this in the **terminal**, not the coding-agent chat:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*'
```

Choose your client when prompted. The installer requires Git and Node.js
**22.20 or later** with npm. Open the same project in your coding agent afterward;
start a fresh session if the skills do not appear.

### Add memory

Send this in the **coding-agent chat**:

```text
/adk-engineer Add memory so our support agent remembers
preferred language between conversations. Reuse our
database and login. Ask before saving; support changes
and forgetting. Add tests for consent and user isolation.
```

### Connect the frontend

```text
/adk-frontend-integration Connect our React chat to
this ADK agent through an API. Reuse our login.
Stream replies and tool progress. Enforce conversation
ownership. Add API tests and check one browser flow.
```

These examples use Claude Code's slash form. In Codex, replace the leading `/`
with `$`. In Google clients, use “Use the adk-engineer skill to…” or “Use the
adk-frontend-integration skill to…”. For Google consumer accounts, use
Antigravity; see the [Google setup guide](../../integrations/google-coding-agents.md)
for Gemini CLI's supported account routes and installation details.

## Editing the video

- [storyboard.json](storyboard.json) contains the page order, planned durations,
  cards, prompts and explanatory text.
- [walkthrough.py](walkthrough.py) draws and animates the scenes in Manim.
- [build.py](build.py) renders, exports, writes chapters and produces the review
  contact sheet and transcript.
- [publishing.md](publishing.md) provides a suggested title, description and
  chapter timestamps for the finished cut.

The intended full duration is **358 seconds across 18 scenes**. Keep the
installation command and both prompts readable long enough to pause and copy.
After changing text, review the contact sheet for clipping and the full video
for reading time; a passing layout assertion alone does not establish clarity.

### Editorial style

The supplied style guide defines warm paper (`#F4F1EA`), charcoal ink (`#1C1C1C`)
and one brick-red accent (`#8B2635`). Use classic serif typography, fine lines,
square data packets, restrained motion and subtle paper shadows. Code and
commands use monospace. Avoid dark terminal backgrounds, neon and glow.

Keep the distinction between the **coding agent** that reads a skill and the
**ADK application** whose code it changes. Skill installation does not deploy
an application or automatically load skill instructions into its runtime.
Never present illustrative checklists as actual test results.

For publishing, include the [repository](https://github.com/RuslanKhis/agentic-engineering-skills)
and the copyable transcript in the description. The skills accompany Ruslan
Khissamiyev's *Agentic Engineering: Building Production-Grade Multi-Agent Systems
with Google ADK on GCP*. Add a book purchase or preorder link only when a real
customer-facing URL is available.
