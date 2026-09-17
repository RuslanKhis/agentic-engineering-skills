#!/usr/bin/env python3
"""Render and package the silent Agentic Engineering Skills walkthrough."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASENAME = "agentic-engineering-skills"


def run(arguments: list[str], *, env: dict[str, str] | None = None) -> None:
    print("Running:", " ".join(arguments), flush=True)
    subprocess.run(arguments, cwd=ROOT, env=env, check=True)


def timestamp(seconds: float) -> str:
    whole = round(seconds)
    minutes, seconds = divmod(whole, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"


def metadata_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("=", "\\=").replace(";", "\\;").replace("#", "\\#").replace("\n", " ")


def chapter_metadata(timeline: list[dict], output: Path) -> Path:
    lines = [";FFMETADATA1", "title=Agentic Engineering Skills — a practical introduction", "comment=Silent illustrated walkthrough; application changes and checks are illustrative."]
    previous_end = 0.0
    for record in timeline:
        start, end = float(record["start"]), float(record["end"])
        if not math.isfinite(start) or not math.isfinite(end) or start < previous_end - .01 or end <= start:
            raise ValueError(f"Invalid or overlapping timeline interval: {record!r}")
        title = metadata_escape(f"{record['scene']:02d} · {record['title']}")
        lines.extend(["[CHAPTER]", "TIMEBASE=1/1000", f"START={round(start * 1000)}", f"END={round(end * 1000)}", f"title={title}"])
        previous_end = end
    path = output / "chapters.ffmetadata"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def additional_diagram_text(page: dict, scene: int, layout_checks: list[dict]) -> list[str]:
    """Find rendered labels not already represented in this page's source text."""
    def strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for child in value.values():
                yield from strings(child)
        elif isinstance(value, (list, tuple)):
            for child in value:
                yield from strings(child)

    def normalized(value: str) -> str:
        return " ".join(value.split()).casefold()

    represented = {normalized(value) for value in strings(page)}
    represented.update({"agentic engineering / the skills companion", "silent walkthrough"})
    extra = []
    for record in layout_checks:
        if record.get("scene") != scene:
            continue
        value = record.get("text", "")
        key = normalized(value)
        if not key or key in represented or re.fullmatch(r"\d+\s*/\s*\d+", key):
            continue
        represented.add(key)
        extra.append(value)
    return extra


def write_transcript(pages: list[dict], output: Path) -> None:
    layout_path = output / "layout-checks.json"
    layout_checks = json.loads(layout_path.read_text(encoding="utf-8")) if layout_path.is_file() else []
    lines = ["# Agentic Engineering Skills — screen transcript", "", "A silent, illustrated walkthrough. These are the source cards, explanatory notes and additional rendered diagram labels, not a record of generated code or passing tests. Timings below describe the full-length cut; the preview compresses the holds.", ""]
    elapsed = 0.0
    for index, page in enumerate(pages, 1):
        end = elapsed + float(page["duration"])
        lines.extend([f"## {index:02d} · {page['title']}", "", f"**{timestamp(elapsed)}–{timestamp(end)} · {page['chapter']} · {page['duration']} seconds**", ""])
        if page.get("context"):
            lines.extend([page["context"], ""])
        for key, language in (("command", "bash"), ("prompt", "text")):
            if page.get(key):
                lines.extend([f"```{language}", page[key], "```", ""])
        for card in page.get("cards", []):
            lines.extend([f"**{card['label']}**", "", card["text"], ""])
        if page.get("items"):
            for item in page["items"]:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    label, detail = item
                    lines.append(f"- **{label}:** {str(detail).replace(chr(10), ' ')}")
                else:
                    lines.append(f"- {item}")
            lines.append("")
        if page.get("notes"):
            lines.extend(["### On-screen explanations", ""])
            lines.extend(f"{i}. {note}" for i, note in enumerate(page["notes"], 1))
            lines.append("")
        known = {"id", "title", "chapter", "duration", "layout", "context", "command", "prompt", "cards", "items", "notes"}
        for key, value in page.items():
            if key not in known and isinstance(value, str):
                lines.extend([f"**{key.replace('_', ' ').capitalize()}:** {value}", ""])
        extras = additional_diagram_text(page, index, layout_checks)
        if extras:
            lines.extend(["### Additional diagram text", ""])
            for value in extras:
                # Preserve code records and folder trees. A visually wrapped URL
                # should remain copyable as one address in the transcript.
                if value.startswith("github.com/"):
                    lines.extend([f"- `{''.join(value.split())}`", ""])
                elif "\n" in value and (value.startswith("user_id:") or "\n  " in value):
                    lines.extend(["```text", value, "```", ""])
                else:
                    lines.append(f"- {' '.join(value.split())}")
            lines.append("")
        elapsed = end
    lines.extend(["## Resources", "", "- [Repository and installation instructions](https://github.com/RuslanKhis/agentic-engineering-skills)", "- [Google coding-client setup and account guidance](https://github.com/RuslanKhis/agentic-engineering-skills/blob/main/docs/integrations/google-coding-agents.md)", "", "Companion to *Agentic Engineering: Building Production-Grade Multi-Agent Systems with Google ADK on GCP*, by Ruslan Khissamiyev. The skills can be used without the book.", ""])
    (output / "transcript.md").write_text("\n".join(lines), encoding="utf-8")


def make_contact_sheet(timeline: list[dict], output: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    columns, thumb_width, thumb_height = 3, 640, 360
    margin, label_height = 24, 74
    rows = math.ceil(len(timeline) / columns)
    sheet = Image.new("RGB", (columns * (thumb_width + margin) + margin, rows * (thumb_height + label_height + margin) + margin), "#F4F1EA")
    draw = ImageDraw.Draw(sheet)
    font = None
    for name in ("/System/Library/Fonts/Supplemental/Georgia.ttf", "DejaVuSerif.ttf"):
        try:
            font = ImageFont.truetype(name, 22)
            break
        except OSError:
            pass
    if font is None:
        font = ImageFont.load_default(size=22)
    for cell, record in enumerate(timeline):
        frame = output / "frames" / f"{record['scene']:02d}-{record['id']}.png"
        if not frame.is_file():
            raise FileNotFoundError(f"Missing rendered scene frame: {frame}")
        x = margin + (cell % columns) * (thumb_width + margin)
        y = margin + (cell // columns) * (thumb_height + label_height + margin)
        with Image.open(frame) as source:
            thumb = source.convert("RGB")
            thumb.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x + (thumb_width - thumb.width) // 2, y))
        draw.rectangle((x, y, x + thumb_width, y + thumb_height), outline="#C8C1B5", width=1)
        label = f"{record['scene']:02d} · {timestamp(record['start'])}–{timestamp(record['end'])} · {record['title']}"
        label_lines, current = [], ""
        for word in label.split():
            candidate = f"{current} {word}".strip()
            if current and draw.textlength(candidate, font=font) > thumb_width:
                label_lines.append(current)
                current = word
            else:
                current = candidate
        label_lines.append(current)
        draw.multiline_text((x, y + thumb_height + 10), "\n".join(label_lines), font=font, fill="#1C1C1C", spacing=5)
    sheet.save(output / "contact-sheet.jpg", quality=93)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Render a quick 960×540 / 15 fps preview with compressed holds.")
    parser.add_argument("--skip-render", action="store_true", help="Repackage the existing render in the selected output directory.")
    args = parser.parse_args()
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        parser.error("ffmpeg and ffprobe are required on PATH; see README.md for setup.")
    output = ROOT / "output"
    if args.preview:
        output /= "preview"
    output.mkdir(parents=True, exist_ok=True)
    pages = json.loads((ROOT / "storyboard.json").read_text(encoding="utf-8"))
    width, height, fps = (960, 540, 15) if args.preview else (1920, 1080, 30)
    media = output / "media"
    if not args.skip_render:
        env = os.environ.copy()
        env["ADK_VIDEO_OUTPUT"] = str(output)
        env["ADK_VIDEO_PREVIEW"] = "1" if args.preview else "0"
        env.pop("ADK_VIDEO_SCENES", None)
        run([sys.executable, "-m", "manim", "--renderer", "cairo", "--resolution", f"{width},{height}", "--fps", str(fps), "--media_dir", str(media), "--format", "mp4", "--output_file", "SkillsWalkthrough.mp4", "walkthrough.py", "SkillsWalkthrough"], env=env)
    movies = sorted(media.glob("videos/walkthrough/*/SkillsWalkthrough.mp4"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not movies:
        raise FileNotFoundError(f"No completed Manim video found below {media}; partial render chunks are not usable.")
    timeline = json.loads((output / "timeline.json").read_text(encoding="utf-8"))
    if not timeline:
        raise ValueError("The renderer wrote an empty timeline.")
    if [record["id"] for record in timeline] != [page["id"] for page in pages]:
        raise ValueError("The render must contain every storyboard scene in order.")
    # Manim can round a static hold down by one frame per scene.
    if not args.preview and abs(float(timeline[-1]["end"]) - sum(page["duration"] for page in pages)) > max(.2, len(pages) / fps):
        raise ValueError("The full render differs from the planned reading time.")
    chapters = chapter_metadata(timeline, output)
    final = output / f"{BASENAME}.mp4"
    run([ffmpeg, "-y", "-hide_banner", "-loglevel", "warning", "-i", str(movies[0]), "-f", "ffmetadata", "-i", str(chapters), "-map", "0:v:0", "-map_metadata", "1", "-map_chapters", "1", "-an", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(final)])
    write_transcript(pages, output)
    make_contact_sheet(timeline, output)
    probe = json.loads(subprocess.check_output([ffprobe, "-v", "error", "-show_streams", "-show_format", "-show_chapters", "-of", "json", str(final)], text=True))
    video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
    if any(stream["codec_type"] == "audio" for stream in probe["streams"]):
        raise ValueError("Unexpected audio stream in the silent export.")
    if (video["width"], video["height"]) != (width, height):
        raise ValueError("The render resolution differs from the selected build mode.")
    if video["codec_name"] != "h264" or video["pix_fmt"] != "yuv420p":
        raise ValueError("Expected a broadly playable H.264 / yuv420p export.")
    if len(probe.get("chapters", [])) != len(timeline):
        raise ValueError("The export is missing scene chapter markers.")
    actual_seconds = float(video.get("duration", probe["format"]["duration"]))
    timeline_seconds = float(timeline[-1]["end"])
    if abs(actual_seconds - timeline_seconds) > max(.2, 2 / fps):
        raise ValueError(f"Video duration {actual_seconds:.3f}s differs from timeline {timeline_seconds:.3f}s.")
    report = {"mode": "preview" if args.preview else "full", "video": final.name, "resolution": [width, height], "fps": video["avg_frame_rate"], "codec": video["codec_name"], "pixel_format": video["pix_fmt"], "audio_streams": 0, "duration_seconds": actual_seconds, "timeline_seconds": timeline_seconds, "planned_full_seconds": sum(float(page["duration"]) for page in pages), "rendered_scenes": len(timeline), "chapter_count": len(probe.get("chapters", []))}
    (output / "build-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
    print(f"\nVideo: {final}\nContact sheet: {output / 'contact-sheet.jpg'}\nTranscript: {output / 'transcript.md'}", flush=True)


if __name__ == "__main__":
    main()
