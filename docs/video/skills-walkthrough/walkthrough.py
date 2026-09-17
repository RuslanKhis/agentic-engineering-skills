"""Silent editorial walkthrough. Run build.py for preview or full production.

All application diagrams and changes are illustrations, not a live client capture.
The palette and camera conventions follow the author's supplied style guide.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from manim import *
from manimpango import list_fonts

ROOT = Path(__file__).resolve().parent
PAPER = '#F4F1EA'
LIGHT = '#FBF8F2'
INK = '#1C1C1C'
MUTED = '#766F66'
GUIDE = '#C8C1B5'
SHADOW = '#D7D0C4'
ACCENT = '#8B2635'
SERIF = os.environ.get('ADK_VIDEO_SERIF', 'Georgia')
MONO = os.environ.get('ADK_VIDEO_MONO', 'Menlo')
PREVIEW = os.environ.get('ADK_VIDEO_PREVIEW') == '1'
OUTPUT = Path(os.environ.get('ADK_VIDEO_OUTPUT', ROOT / 'output'))
SELECT = os.environ.get('ADK_VIDEO_SCENES', '')

config.background_color = PAPER
config.frame_width = 16
config.frame_height = 9
# Keep this film's 167 segments so a later text edit can reuse other scenes.
config.max_files_cached = 1000


class SkillsWalkthrough(MovingCameraScene):
    def construct(self):
        available = set(list_fonts())
        for font in (SERIF, MONO):
            if font not in available:
                raise RuntimeError(f'Missing font {font!r}; install it or set ADK_VIDEO_SERIF / ADK_VIDEO_MONO.')
        self.camera.background_color = PAPER
        self.pages = json.loads((ROOT / 'storyboard.json').read_text())
        self.records = []
        self.layout_checks = []
        self.caption = None
        self.overlay = []
        self.selected = {int(i) for i in SELECT.split(',') if i} if SELECT else set()
        OUTPUT.mkdir(parents=True, exist_ok=True)
        (OUTPUT / 'frames').mkdir(exist_ok=True)
        for index, page in enumerate(self.pages, 1):
            if self.selected and index not in self.selected:
                continue
            self.page_index = index
            self.page = page
            self.start_time = self.time
            self.camera.frame.move_to(ORIGIN)
            self.begin_page(page, index)
            getattr(self, page['layout'])(page)
            self.finish_page(page, index)
        (OUTPUT / 'timeline.json').write_text(json.dumps(self.records, indent=2) + '\n')
        (OUTPUT / 'layout-checks.json').write_text(json.dumps(self.layout_checks, indent=2) + '\n')

    def text(self, value, size=27, color=INK, mono=False, width=None, weight=NORMAL):
        result = Text(value, font=MONO if mono else SERIF, font_size=size,
                      color=color, weight=weight, line_spacing=0.85,
                      disable_ligatures=mono)
        if width and result.width > width:
            ratio = width / result.width
            result.scale(ratio)
            effective = size * ratio
        else:
            effective = size
        self.layout_checks.append({'scene': self.page_index, 'text': value,
                                   'font_size': round(effective, 2), 'width': round(result.width, 3)})
        if effective < 17.5:
            raise ValueError(f'Text too small ({effective:.1f}): {value!r}')
        return result

    def act(self, *animations, duration=0.7):
        self.play(*animations, run_time=min(duration, 0.12) if PREVIEW else duration)

    def hold(self, duration):
        if duration > 0:
            self.wait(0.12 if PREVIEW else duration, frozen_frame=True)

    def at(self, seconds):
        if not PREVIEW:
            self.hold(max(0, seconds - (self.time - self.start_time)))

    def begin_page(self, page, index):
        self.caption = None
        self.overlay = []
        label = self.text(page['chapter'].upper(), 18, ACCENT)
        label.to_edge(LEFT, buff=0.7).set_y(4.1)
        folio = self.text(f'{index:02d} / {len(self.pages):02d}', 18, MUTED)
        folio.to_edge(RIGHT, buff=0.7).set_y(4.1)
        rule = Line([-7.3, 3.83, 0], [7.3, 3.83, 0], color=GUIDE, stroke_width=1)
        title = self.text(page['title'], 43, width=14.3)
        title.to_edge(LEFT, buff=0.7).set_y(3.18)
        bottom_rule = Line([-7.3, -4.02, 0], [7.3, -4.02, 0], color=GUIDE, stroke_width=1)
        progress = Line([-7.3, -4.02, 0], [-7.3 + 14.6 * index / len(self.pages), -4.02, 0],
                        color=ACCENT, stroke_width=2)
        footer = self.text('AGENTIC ENGINEERING  /  THE SKILLS COMPANION', 18, MUTED)
        footer.to_edge(LEFT, buff=0.7).set_y(-4.22)
        hint = self.text('Silent walkthrough', 18, MUTED).to_edge(RIGHT, buff=0.7).set_y(-4.22)
        self.act(FadeIn(VGroup(label, folio, title, footer, hint)), Create(rule), Create(bottom_rule), Create(progress))

    def note(self, value):
        label = self.text(value, 25, width=14.1)
        label.move_to([0, -3.24, 0])
        label.add_background_rectangle(color=PAPER, opacity=1, buff=0.13)
        label.set_z_index(90)
        if self.caption is None:
            self.act(FadeIn(label, shift=UP * 0.06), duration=0.5)
        else:
            self.act(FadeOut(self.caption), FadeIn(label), duration=0.4)
        self.caption = label

    def panel(self, eyebrow, lines, width=6.7, height=3.6, mono=False, size=27, accent=False):
        shadow = Rectangle(width=width, height=height, stroke_width=0,
                           fill_color=SHADOW, fill_opacity=0.45).shift(RIGHT * .055 + DOWN * .055)
        box = Rectangle(width=width, height=height, stroke_color=ACCENT if accent else INK,
                        stroke_width=1.5 if accent else 1, fill_color=LIGHT, fill_opacity=1)
        head = self.text(eyebrow.upper(), 19, ACCENT if accent else MUTED, width=width-.6)
        head.move_to(box.get_top() + DOWN * .4).align_to(box, LEFT).shift(RIGHT * .3)
        content = self.text(lines, size, mono=mono, width=width-.6)
        content.move_to(box.get_center() + DOWN * .20).align_to(box, LEFT).shift(RIGHT * .3)
        if content.height > height - 1.1:
            raise ValueError(f'Panel overflow: {eyebrow}: {content.height:.2f} > {height-1.1:.2f}')
        return VGroup(shadow, box, head, content)

    def tag(self, title, detail='', width=3.5, height=1.3, accent=False):
        box = Rectangle(width=width, height=height, stroke_width=1.4 if accent else 1,
                        stroke_color=ACCENT if accent else INK, fill_color=LIGHT, fill_opacity=1)
        title_text = self.text(title, 26, color=ACCENT if accent else INK, width=width-.35)
        if detail:
            subtitle = self.text(detail, 20, MUTED, width=width-.35)
            words = VGroup(title_text, subtitle).arrange(DOWN, buff=.17)
        else:
            words = VGroup(title_text)
        words.move_to(box)
        return VGroup(box, words)

    def link(self, source, target, label='', reverse=False):
        begin, end = (source.get_right(), target.get_left())
        if reverse:
            begin, end = end, begin
        arrow = Arrow(begin, end, buff=.05, color=INK, stroke_width=1.2,
                      max_tip_length_to_length_ratio=.35, tip_length=.12)
        self.act(GrowArrow(arrow), duration=.6)
        if label:
            text = self.text(label, 20, width=4).next_to(arrow, UP, buff=.12)
            text.add_background_rectangle(color=PAPER, opacity=1, buff=.06)
            self.act(FadeIn(text), duration=.4)
        packet = Square(side_length=.10, stroke_width=0, fill_color=ACCENT, fill_opacity=1)
        packet.move_to(arrow.get_start())
        self.add(packet)
        self.act(MoveAlongPath(packet, arrow), duration=1.2)
        self.remove(packet)
        return arrow

    def cards(self, page):
        cards = [self.panel(item['label'], item['text'], width=6.85, height=4.05,
                            mono=item.get('mono', False), size=item.get('size', 28), accent=i == 1)
                 for i, item in enumerate(page['cards'])]
        if len(cards) == 2:
            cards[0].move_to([-3.75, .35, 0]); cards[1].move_to([3.75, .35, 0])
        else:
            raise ValueError('cards layout needs two cards')
        self.act(FadeIn(cards[0], shift=UP*.12))
        self.note(page['notes'][0])
        self.at(page['duration'] * .40)
        self.act(FadeIn(cards[1], shift=UP*.12))
        self.note(page['notes'][-1])

    def title_page(self, page):
        subtitle = self.text('Install once. Ask for the next useful change.', 32)
        subtitle.move_to([0, 1.95, 0])
        self.act(FadeIn(subtitle))
        cards = VGroup(self.tag('Existing agent', 'your project', 3.5),
                       self.tag('Engineering skills', 'guidance for your coding agent', 5, accent=True),
                       self.tag('Useful changes', 'memory · interface · tests', 3.5)).arrange(RIGHT, buff=.7).set_y(.0)
        self.act(LaggedStart(*[FadeIn(card, shift=UP*.1) for card in cards], lag_ratio=.3), duration=1.3)
        self.link(cards[0], cards[1]); self.link(cards[1], cards[2])
        author = self.text('By Ruslan Khissamiyev', 24, MUTED).set_y(-1.7)
        self.act(FadeIn(author))
        self.note(page['notes'][0])

    def folder(self, page):
        left = self.panel('A skill is a folder', 'adk-memory-architecture/\n  SKILL.md\n  references/\n  scripts/\n  tests/', width=7.1, height=4.2, mono=True, size=25)
        left.move_to([-3.6, .1, 0])
        right = VGroup(*[self.tag(item[0], item[1], 6.6, 1.05, accent=i == 0)
                         for i, item in enumerate(page['items'])]).arrange(DOWN, buff=.23).move_to([3.85, .1, 0])
        self.act(FadeIn(left)); self.note(page['notes'][0])
        self.at(6)
        self.act(LaggedStart(*[FadeIn(item) for item in right], lag_ratio=.3), duration=1.2)
        self.at(11); self.note(page['notes'][-1])

    def router(self, page):
        router = self.tag('adk-engineer', 'describe the outcome', 5.2, 1.2, accent=True).move_to([0, 1.65, 0])
        self.act(FadeIn(router))
        self.note(page['notes'][0])
        nodes = VGroup(*[self.tag(item[0], item[1], 4.6, 1.35) for item in page['items']]).arrange(RIGHT, buff=.35).set_y(-.75)
        for node in nodes:
            arrow = Arrow(router.get_bottom(), node.get_top(), buff=.12, color=INK, stroke_width=1.2, tip_length=.12)
            self.act(GrowArrow(arrow), FadeIn(node), duration=.65)
        self.at(9); self.note(page['notes'][-1])

    def terminal(self, page):
        panel = self.panel('TERMINAL  /  inside your application project', page['command'],
                           width=14.4, height=3.1, mono=True, size=27, accent=True).set_y(.85)
        self.act(FadeIn(panel[:3]))
        self.act(AddTextLetterByLetter(panel[3]), duration=2.5)
        self.note(page['notes'][0])
        options = VGroup(*[self.tag(item[0], item[1], 4.5, 1.10) for item in page['items']]).arrange(RIGHT, buff=.4).set_y(-1.75)
        self.at(9)
        self.act(LaggedStart(*[FadeIn(item) for item in options], lag_ratio=.25), duration=1.1)
        self.at(15); self.note(page['notes'][-1])

    def clients(self, page):
        rows = VGroup()
        for index, item in enumerate(page['items']):
            box = Rectangle(width=14.3, height=1.16, stroke_color=INK,
                            stroke_width=1, fill_color=LIGHT, fill_opacity=1)
            name = self.text(item[0], 26, ACCENT, width=3.6).move_to([-5, 0, 0])
            command = self.text(item[1], 26, mono=True, width=9.1)
            command.align_to(box, LEFT).shift(RIGHT*4.55)
            rows.add(VGroup(box, name, command))
        rows.arrange(DOWN, buff=.21).set_y(.3)
        self.act(LaggedStart(*[FadeIn(row) for row in rows], lag_ratio=.3), duration=1.6)
        self.note(page['notes'][0])
        self.at(11); self.note(page['notes'][-1])

    def prompt(self, page):
        context = self.text(page['context'], 25, MUTED, width=14.2).set_y(2.24)
        panel = self.panel('CODING-AGENT CHAT  /  Claude Code example', page['prompt'],
                           width=14.4, height=3.55, mono=True, size=25, accent=True).set_y(-.10)
        self.act(FadeIn(context), FadeIn(panel[:3]))
        self.act(FadeIn(panel[3], shift=UP*.07), duration=.8)
        self.note(page['notes'][0])
        self.at(13)
        self.note(page['notes'][-1])

    def memory_flow(self, page):
        columns = VGroup(self.tag('Signed-in user', 'verified identity', 3.8),
                         self.tag('Application', 'consent + ownership', 4.1, accent=True),
                         self.tag('Existing database', 'user-scoped preference', 4.1)).arrange(RIGHT, buff=.9).set_y(1.3)
        self.act(LaggedStart(*[FadeIn(node) for node in columns], lag_ratio=.2), duration=1)
        self.link(columns[0], columns[1]); self.link(columns[1], columns[2])
        stored = self.panel('ILLUSTRATIVE RECORD', 'user_id: 42\npreferred_language: "Spanish"', width=6.7, height=2.15, mono=True, size=25).move_to([3.6, -1.12, 0])
        later = self.panel('NEXT SESSION', 'Load this user’s preference.\nLet them change or forget it.', width=6.7, height=2.15, size=27).move_to([-3.6, -1.12, 0])
        self.act(FadeIn(stored)); self.note(page['notes'][0])
        self.at(11); self.act(FadeIn(later)); self.note(page['notes'][-1])

    def sequence(self, page):
        xs = [-5.6, -1.9, 1.9, 5.6]
        headers = VGroup(*[self.tag(label, detail, 3.3, .93, accent=i==1)
                          for i, (label, detail) in enumerate(page['items'])])
        for x, node in zip(xs, headers):
            node.move_to([x, 1.87, 0]); node.set_z_index(20)
        lines = VGroup(*[DashedLine([x,1.35,0], [x,-3.2,0], color=GUIDE, stroke_width=1, dash_length=.09) for x in xs])
        self.act(FadeIn(headers), Create(lines), duration=1)
        # Sticky diagram headers follow the camera; their colour is never animated.
        for node in headers:
            offset = node.get_center().copy()
            node.add_updater(lambda m, off=offset: m.move_to(self.camera.frame.get_center() + off))
        self.note(page['notes'][0])
        events = [(0,1,.70,'Send message + session ID'),
                  (1,2,-.18,'Check ownership, then run'),
                  (2,3,-1.06,'Invoke the ADK agent'),
                  (3,0,-2.15,'Events return through runner and API')]
        for index, (source, target, y, label) in enumerate(events):
            self.at(3 + index*3.2)
            arrow = Arrow([xs[source],y,0], [xs[target],y,0], buff=.12, color=INK, stroke_width=1.2, tip_length=.12)
            text = self.text(label, 22, width=6.5).move_to([(xs[source]+xs[target])/2,y+.35,0])
            text.add_background_rectangle(color=PAPER, opacity=1, buff=.08)
            if index == 3:
                # Draw the return through every backend participant explicitly.
                segments = VGroup(*[Arrow([xs[i],y,0], [xs[i-1],y,0], buff=.12,
                    color=INK, stroke_width=1.2, tip_length=.12) for i in (3,2,1)])
                self.act(LaggedStart(*[GrowArrow(part) for part in segments], lag_ratio=.25), FadeIn(text), duration=.6)
            else:
                self.act(GrowArrow(arrow), FadeIn(text), duration=.6)
            packet = Square(side_length=.11, fill_color=ACCENT, fill_opacity=1, stroke_width=0).move_to(arrow.get_start())
            self.add(packet)
            headers[target][0].set_stroke(color=ACCENT, width=2)
            self.act(MoveAlongPath(packet, arrow), duration=.9)
            headers[target][0].set_stroke(color=INK, width=1)
            self.remove(packet)
        # Keep the viewport fixed for text readability; MovingCameraScene permits
        # later extensions without detaching the pinned diagram headers.
        self.at(16); self.note(page['notes'][-1])

    def endings(self, page):
        browser = self.panel('REACT CHAT  /  illustrative interface', 'You: Where is my order?', width=8, height=3.9, size=27).move_to([-3.2,.25,0])
        browser[3].set_y(1)
        tool = self.tag('Tool progress: looking up the order', width=7.2, height=.7).move_to([-3.2, .08, 0])
        reply = self.text('Agent: …', 26, width=7.2).move_to([-3.2,-.98,0]).align_to(browser[3],LEFT)
        self.act(FadeIn(browser), FadeIn(tool), FadeIn(reply)); self.note(page['notes'][0])
        paths = VGroup(self.tag('Complete', 'show the final answer once', 5.4, 1.05, accent=True),
                       self.tag('Interrupted', 'mark the answer incomplete', 5.4, 1.05),
                       self.tag('Rejected', 'show a clear error', 5.4, 1.05)).arrange(DOWN,buff=.25).move_to([4.25,.25,0])
        self.at(5)
        self.act(LaggedStart(*[FadeIn(row) for row in paths], lag_ratio=.3), duration=1.3)
        self.at(9)
        done = self.tag('Tool progress: lookup complete', width=7.2, height=.7, accent=True).move_to(tool)
        answer = self.text('Agent: Your order arrives on Friday.', 25, width=7.2).move_to(reply).align_to(browser[3],LEFT)
        self.act(FadeTransform(tool, done), FadeTransform(reply, answer), duration=.7)
        self.at(12); self.note(page['notes'][-1])

    def closing(self, page):
        line = self.text('One project. One useful change. Start there.', 36, width=14.2).set_y(1.9)
        repo = self.panel('INSTALLATION, COMMANDS & THREE EXAMPLES PER SKILL',
                          'github.com/RuslanKhis/\nagentic-engineering-skills', width=12.9, height=2.3,
                          mono=True, size=32, accent=True).set_y(-.05)
        book = self.text('The companion to Agentic Engineering\nBuilding Production-Grade Multi-Agent Systems with Google ADK on GCP',
                         23, width=14.0).set_y(-2)
        self.act(FadeIn(line), FadeIn(repo), FadeIn(book), duration=1)
        self.note(page['notes'][0])

    def finish_page(self, page, index):
        self.renderer.update_frame(self)
        self.camera.get_image().save(OUTPUT / 'frames' / f'{index:02d}-{page["id"]}.png')
        # Verify each complete frame stays inside the video safe area.
        for mob in self.mobjects:
            if mob.width and mob.height:
                assert mob.get_left()[0] >= -7.95 and mob.get_right()[0] <= 7.95, (page['id'], 'horizontal overflow')
                assert mob.get_bottom()[1] >= -4.48 and mob.get_top()[1] <= 4.48, (page['id'], 'vertical overflow')
        self.at(page['duration'] - .6)
        for mob in self.mobjects:
            mob.clear_updaters(recursive=True)
        self.act(FadeOut(Group(*self.mobjects)), duration=.6)
        self.clear()
        self.records.append({'scene': index, 'id': page['id'], 'title': page['title'],
                             'start': round(self.start_time, 3), 'end': round(self.time, 3),
                             'planned_duration': page['duration']})
