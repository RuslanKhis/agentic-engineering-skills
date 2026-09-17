#!/usr/bin/env python3
"""Add the artist-authorized hijaq. soundtrack; preserve earlier exports."""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'output' / 'action-cut'
MUSIC = ROOT / 'output' / 'music-hijaq'
SOURCE = MUSIC / 'just-turn-it-on-and-make-something-hijaq.mp3'
TARGET_LUFS = -18
CROSSFADE_SECONDS = 2
SPLICE_END_SECONDS = 86.43


def probe(path: Path) -> dict:
    return json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_streams','-show_format',
        '-show_chapters','-of','json',str(path)], text=True))


def run(args: list[str]) -> None:
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*args],check=True)


def video_hash(path: Path) -> str:
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
        '-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()


def main() -> None:
    silent=OUTPUT/'agentic-engineering-skills-action.mp4'
    info=probe(silent)
    duration=float(next(s for s in info['streams'] if s['codec_type']=='video')['duration'])
    # Decode first: MP3 container duration includes padding, while the WAV gives
    # the exact sample duration used for a repeat that preserves the outro.
    decoded=OUTPUT/'hijaq-decoded.wav'
    run(['-i',str(SOURCE),'-map','0:a:0','-ar','48000','-ac','2',
        '-c:a','pcm_s24le',str(decoded)])
    source_duration=float(probe(decoded)['format']['duration'])
    extension=duration-source_duration
    restart=SPLICE_END_SECONDS-extension-CROSSFADE_SECONDS
    if not (extension>0 and 0<restart<SPLICE_END_SECONDS<source_duration):
        raise ValueError('This arrangement expects a short film longer than this track.')
    arrangement=OUTPUT/'hijaq-arrangement.wav'
    repeat=(f'[0:a]asplit=2[first][second];'
        f'[first]atrim=end={SPLICE_END_SECONDS},asetpts=PTS-STARTPTS[a];'
        f'[second]atrim=start={restart:.6f},asetpts=PTS-STARTPTS[b];'
        f'[a][b]acrossfade=d={CROSSFADE_SECONDS}:c1=qsin:c2=qsin,'
        f'apad,atrim=duration={duration:.6f}[music]')
    run(['-i',str(decoded),'-filter_complex',repeat,'-map','[music]',
        '-c:a','pcm_s24le',str(arrangement)])
    # Measure the complete arrangement before applying the final playback level.
    measurement=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(arrangement),
        '-af',f'loudnorm=I={TARGET_LUFS}:TP=-2:LRA=11:print_format=json',
        '-f','null','-'],capture_output=True,text=True,check=True)
    values=json.loads(re.findall(r'\{[^{}]+\}',measurement.stderr)[-1])
    effect=(f'atrim=duration={duration:.6f},asetpts=PTS-STARTPTS,'
        f'loudnorm=I={TARGET_LUFS}:TP=-2:LRA=11:linear=true:'
        f'measured_I={values["input_i"]}:measured_TP={values["input_tp"]}:'
        f'measured_LRA={values["input_lra"]}:measured_thresh={values["input_thresh"]}:'
        f'offset={values["target_offset"]},aresample=48000,'
        'aformat=sample_fmts=fltp:channel_layouts=stereo,'
        f'afade=t=in:st=0:d=0.6,afade=t=out:st={duration-4:.6f}:d=4,'
        f'apad,atrim=duration={duration:.6f}')
    soundtrack=OUTPUT/'soundtrack-hijaq.wav'
    run(['-i',str(arrangement),'-af',effect,'-c:a','pcm_s24le',str(soundtrack)])
    final=OUTPUT/'agentic-engineering-skills-action-hijaq.mp4'
    credit=('Music: "just turn it on and make something." by hijaq. '
        'https://www.youtube.com/watch?v=Itn9lI0VK0U. '
        'Artist and published free-use permission: https://soundcloud.com/hijaqmusic. '
        'Download/support: https://hijaqmusic.bandcamp.com/track/just-turn-it-on-and-make-something. '
        'Used under the artist\'s published free-use permission. '
        'Looped and faded to fit this video; playback level adjusted. '
        'Animated worked example; local checks use an offline model double.')
    # Both inputs are already bounded to the same length. Avoid -t/-shortest:
    # a fractional MP4 end timestamp can otherwise discard the last B-frame.
    run(['-i',str(silent),'-i',str(soundtrack),'-map','0:v:0','-map','1:a:0',
        '-map_metadata','0','-map_chapters','0','-metadata',f'comment={credit}',
        '-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000',
        '-movflags','+faststart',str(final)])
    result=probe(final)
    v=next(s for s in result['streams'] if s['codec_type']=='video')
    a=next(s for s in result['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'])==(1920,1080)
    assert a['codec_name']=='aac'
    assert abs(float(a['duration'])-duration)<.05
    assert abs(float(v['duration'])-duration)<.04
    assert len(result['chapters'])==len(info['chapters'])
    original_hash=video_hash(silent)
    assert video_hash(final)==original_hash
    run(['-i',str(final),'-f','null','-'])
    report={'file':final.name,'video_duration':float(v['duration']),
        'audio_duration':float(a['duration']),'chapter_count':len(result['chapters']),
        'video_stream_matches_silent_master':True,'video_stream_sha256':original_hash,
        'track':SOURCE.name,'source_duration_seconds':source_duration,
        'extension_seconds':extension,'splice_end_seconds':SPLICE_END_SECONDS,
        'restart_seconds':restart,'crossfade_seconds':CROSSFADE_SECONDS,
        'target_lufs':TARGET_LUFS,
        'fade_in_seconds':.6,'fade_out_seconds':4,'measurement':values,'credit':credit}
    (OUTPUT/'mix-report-hijaq.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
