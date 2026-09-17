"""Action-led editorial walkthrough; build.py renders the separate action cut.

The editor and chat are animated worked examples grounded in demo/ evidence.
They are not a recording of a live coding client or a live model invocation.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from manim import *
from manimpango import list_fonts

ROOT = Path(__file__).resolve().parent
PAPER, LIGHT, INK = '#F4F1EA', '#FBF8F2', '#1C1C1C'
ACCENT, MUTED, GUIDE, SHADOW = '#8B2635', '#766F66', '#C8C1B5', '#D7D0C4'
SERIF = os.environ.get('ADK_VIDEO_SERIF', 'Georgia')
MONO = os.environ.get('ADK_VIDEO_MONO', 'Menlo')
PREVIEW = os.environ.get('ADK_VIDEO_PREVIEW') == '1'
OUTPUT = Path(os.environ.get('ADK_VIDEO_OUTPUT', ROOT / 'output' / 'action-cut'))
config.background_color = PAPER
config.frame_width, config.frame_height = 16, 9
config.max_files_cached = 1000


class SkillsWalkthrough(MovingCameraScene):
    def construct(self):
        for font in (SERIF, MONO):
            if font not in set(list_fonts()):
                raise RuntimeError(f'Missing font: {font}')
        self.camera.background_color = PAPER
        self.pages = json.loads((ROOT / 'storyboard.json').read_text())
        self.evidence = json.loads((ROOT / 'demo' / 'video-evidence.json').read_text())
        self.records, self.layout_checks = [], []
        OUTPUT.mkdir(parents=True, exist_ok=True)
        (OUTPUT / 'frames').mkdir(exist_ok=True)
        for index, page in enumerate(self.pages, 1):
            self.page_index = index
            self.start_time = self.time
            self.heading(page)
            getattr(self, page['layout'])(page)
            self.finish_page(page)
        (OUTPUT / 'timeline.json').write_text(json.dumps(self.records, indent=2) + '\n')
        (OUTPUT / 'layout-checks.json').write_text(json.dumps(self.layout_checks, indent=2) + '\n')

    def text(self, value, size=30, color=INK, mono=False, width=14.3):
        obj = Text(value, font=MONO if mono else SERIF, font_size=size,
                   color=color, line_spacing=.85, disable_ligatures=mono)
        effective = size
        if obj.width > width:
            effective *= width / obj.width
            obj.scale(width / obj.width)
        if effective < 19.8:
            raise ValueError(f'Text too small: {effective:.1f}, {value!r}')
        self.layout_checks.append({'scene': self.page_index, 'text': value,
                                   'font_size': round(effective, 2), 'width': round(obj.width, 3)})
        return obj

    def act(self, *animations, duration=.55):
        seconds=min(duration,.10) if PREVIEW else duration
        seconds=max(1,round(seconds*config.frame_rate))/config.frame_rate
        self.play(*animations,run_time=seconds)

    def at(self, seconds):
        gap = seconds - (self.time-self.start_time)
        if gap > 0:
            seconds=.10 if PREVIEW else gap
            seconds=max(1,round(seconds*config.frame_rate))/config.frame_rate
            self.wait(seconds,frozen_frame=True)

    def heading(self, page):
        self.top = self.text(page['chapter'].upper(), 20, ACCENT).to_edge(LEFT, buff=.7).set_y(4.0)
        self.title = self.text(page['title'], 43).to_edge(LEFT, buff=.7).set_y(3.12)
        rule = Line([-7.3,3.63,0], [7.3,3.63,0], color=GUIDE, stroke_width=1)
        self.act(FadeIn(self.top), FadeIn(self.title), Create(rule), duration=.35)

    def badge(self, label='WORKED EXAMPLE', y=4.0):
        obj = self.text(label, 20, MUTED, width=7).to_edge(RIGHT, buff=.7).set_y(y)
        self.act(FadeIn(obj), duration=.25)
        return obj

    def window(self, label, width=14.4, height=5.9, center=(0,-.5,0)):
        shadow = Rectangle(width=width, height=height, stroke_width=0,
            fill_color=SHADOW, fill_opacity=.4).move_to(center).shift(RIGHT*.055+DOWN*.055)
        box = Rectangle(width=width, height=height, stroke_width=1.4,
            stroke_color=INK, fill_color=LIGHT, fill_opacity=1).move_to(center)
        title = self.text(label, 21, ACCENT, mono=True, width=width-.7)
        title.move_to(box.get_top()+DOWN*.38).align_to(box,LEFT).shift(RIGHT*.35)
        rule = Line(box.get_corner(UL)+DOWN*.78,box.get_corner(UR)+DOWN*.78,color=GUIDE,stroke_width=1)
        return VGroup(shadow,box,title,rule)

    def chip(self, label, width=4.0, accent=False, size=27):
        box = Rectangle(width=width,height=.83,stroke_width=1,
            stroke_color=ACCENT if accent else GUIDE,fill_color=LIGHT,fill_opacity=1)
        txt = self.text(label,size,ACCENT if accent else INK,width=width-.3).move_to(box)
        return VGroup(box,txt)

    def type_lines(self, lines, point, size=27, width=13.1, time=3.2, spacing=.57):
        group = VGroup()
        for index, line in enumerate(lines):
            indent = len(line)-len(line.lstrip())
            advance = Text('MM',font=MONO,font_size=size).width-Text('M',font=MONO,font_size=size).width
            obj = self.text(line.lstrip() or ' ',size,mono=True,width=width-indent*advance)
            obj.move_to([point[0]+indent*advance,point[1]-index*spacing,0],aligned_edge=LEFT)
            if index == 0 and line.startswith(('/', '$')):
                obj.set_color(ACCENT)
            group.add(obj)
        duration = time / max(1,len(lines))
        for obj in group:
            self.act(AddTextLetterByLetter(obj), duration=duration)
        return group

    def bubble(self, value, width=10.8, height=1.1, accent=False, size=30):
        box = Rectangle(width=width,height=height,stroke_color=ACCENT if accent else GUIDE,
                        stroke_width=1,fill_color=PAPER if accent else LIGHT,fill_opacity=1)
        words = self.text(value,size,ACCENT if accent else INK,width=width-.6).move_to(box)
        return VGroup(box,words)

    def install(self, page):
        win = self.window('TERMINAL  /  your-agent/',height=5.35,center=(0,-.25,0))
        self.act(FadeIn(win,shift=UP*.08))
        self.type_lines(page['command'].splitlines(),[-6.7,1.16],size=30,time=2.9,spacing=.66)
        self.at(5.2)
        choose = self.chip('Choose your coding client in the installer',width=12.0,size=29).move_to([0,-1.75,0])
        self.act(FadeIn(choose,shift=UP*.10))
        self.at(8)
        mark = self.chip('Open the same project in your coding agent',width=12.0,size=29).move_to(choose)
        self.act(ReplacementTransform(choose,mark))

    def frontend_before(self, page):
        agent = self.window('agent.py',width=5.4,height=3.1,center=(-4.4,.15,0))
        works = self.text('Your ADK agent\nalready works.',35,width=4.6).move_to([-4.4,-.1,0])
        browser = self.window('React chat',width=5.4,height=3.1,center=(4.4,.15,0))
        waiting = self.text('Waiting for\na connection…',33,width=4.6).move_to([4.4,-.1,0])
        self.act(FadeIn(agent),FadeIn(works),FadeIn(browser),FadeIn(waiting))
        left = DashedLine([-1.6,.05,0],[-.40,.05,0],color=GUIDE)
        right = DashedLine([.4,.05,0],[1.6,.05,0],color=GUIDE)
        q = self.text('?',44,ACCENT).move_to([0,.05,0])
        self.act(Create(left),Create(right),FadeIn(q))
        thoughts=VGroup(*[self.chip(s,width=4.2) for s in ['Sessions?', 'Streaming?', 'Login?']]).arrange(RIGHT,buff=.35).set_y(-2.6)
        self.at(2.8)
        self.act(LaggedStart(*[FadeIn(x,shift=UP*.13) for x in thoughts],lag_ratio=.35),duration=1.0)
        self.at(5.5)
        self.act(Indicate(q,color=ACCENT,scale_factor=1.2))

    def request(self, page, context):
        win = self.window('CODING-AGENT CHAT  /  Claude Code syntax',height=5.85,center=(0,-.5,0))
        self.act(FadeIn(win))
        context_obj=self.text(context,29,MUTED,width=13.1).move_to([-6.7,1.15,0],aligned_edge=LEFT)
        self.act(FadeIn(context_obj))
        self.type_lines(page['prompt'].splitlines(),[-6.7,.25],size=28,time=3.7,spacing=.65)
        button=self.chip('Send request  ↵',width=3.9,accent=True).move_to([4.65,-2.73,0])
        self.at(9.8)
        self.act(FadeIn(button))
        self.at(11.7)
        self.act(Indicate(button,color=ACCENT,scale_factor=1.04),duration=.4)

    def frontend_prompt(self,page):
        self.request(page,'“How do I connect this to my frontend?”')

    def memory_prompt(self,page):
        self.request(page,'“Can it remember Spanish in the next conversation?”')

    def read_project(self,page):
        self.badge()
        files = self.window('YOUR PROJECT',width=6.7,height=3.5,center=(-3.75,.15,0))
        project = self.text('agent.py\nweb/Chat.jsx\nauth/  ·  tests/',29,mono=True,width=5.9).move_to([-3.75,-.10,0])
        skill = self.window('THE SKILL',width=6.7,height=3.5,center=(3.75,.15,0))
        instructions=self.text('SKILL.md\nEngineering instructions\n+ implementation recipes',29,width=5.9).move_to([3.75,-.10,0])
        self.act(FadeIn(files),FadeIn(project))
        self.act(FadeIn(skill),FadeIn(instructions))
        task = self.chip('Apply the guidance to your code',width=9.8,accent=True,size=30).set_y(-2.6)
        arrows=VGroup(*[Arrow([x,-1.65,0],[x*.55,-2.15,0],color=INK,stroke_width=1.4,buff=.04,tip_length=.12) for x in [-3.75,3.75]])
        self.at(3)
        self.act(Create(arrows),FadeIn(task))
        packets=VGroup(*[Square(side_length=.12,fill_color=ACCENT,fill_opacity=1,stroke_width=0).move_to(a.get_start()) for a in arrows])
        self.add(packets)
        self.act(*[MoveAlongPath(p,a) for p,a in zip(packets,arrows)],duration=1.0)
        self.remove(packets)

    def excerpt(self,key,center=(0,-.28,0),width=14.4):
        value=self.evidence[key]
        lines=value['lines']
        if len(lines)>8:
            raise ValueError(f'Too many lines for video excerpt {key}')
        win=self.window(value['file']+'  /  excerpt',width=width,height=5.6,center=center)
        self.act(FadeIn(win))
        group=VGroup()
        for i,line in enumerate(lines):
            indent=len(line)-len(line.lstrip())
            advance=Text('MM',font=MONO,font_size=27).width-Text('M',font=MONO,font_size=27).width
            obj=self.text(line.lstrip() or ' ',27,mono=True,width=width-.85-indent*advance)
            obj.move_to([center[0]-width/2+.43+indent*advance,center[1]+1.24-i*.51,0],aligned_edge=LEFT)
            group.add(obj)
        self.act(LaggedStart(*[FadeIn(o,shift=UP*.045) for o in group],lag_ratio=.16),duration=1.2)
        self.renderer.update_frame(self)
        self.camera.get_image().save(OUTPUT/'frames'/f'{self.page_index:02d}-{key}-excerpt.png')
        return win,group

    def frontend_code(self,page):
        self.badge('WORKED EXAMPLE  /  CODE EXCERPTS')
        win,code=self.excerpt('backend')
        self.at(3.1)
        self.act(*[o.animate.set_color(ACCENT) for o in code[-3:]],duration=.45)
        self.at(6.3)
        self.act(FadeOut(win),FadeOut(code),duration=.35)
        win,code=self.excerpt('frontend')
        self.at(10)
        self.act(*[code[i].animate.set_color(ACCENT) for i in [1,3,5]],duration=.45)

    def frontend_after(self,page):
        self.badge('WORKED EXAMPLE  /  MODEL DOUBLE')
        win=self.window('Support chat',height=5.9,center=(0,-.48,0))
        self.act(FadeIn(win))
        question=self.bubble(self.evidence['replay']['question'],width=10.5,height=.92,accent=True).move_to([1,1.02,0])
        self.act(FadeIn(question,shift=UP*.1))
        status=self.chip(self.evidence['replay']['progress'],width=10.5,size=27).move_to([-1,-.24,0])
        self.at(2.0);self.act(FadeIn(status))
        answer_box=Rectangle(width=12.3,height=1.2,stroke_color=GUIDE,stroke_width=1,fill_color=LIGHT,fill_opacity=1).move_to([-.40,-1.65,0])
        answer=self.text(self.evidence['replay']['answer'],32,width=11.7).move_to(answer_box)
        self.at(4.0);self.act(FadeIn(answer_box))
        self.act(AddTextLetterByLetter(answer),duration=2.0)
        done=self.chip('Reply complete',width=10.5,size=27,accent=True).move_to(status)
        self.at(7.7);self.act(ReplacementTransform(status,done))

    def memory_code(self,page):
        self.badge('WORKED EXAMPLE  /  CODE EXCERPTS')
        win,code=self.excerpt('memory_save')
        self.at(3)
        self.act(code[1].animate.set_color(ACCENT),duration=.4)
        self.at(5.9)
        self.act(FadeOut(win),FadeOut(code),duration=.35)
        win,code=self.excerpt('memory_load')
        self.at(9.0)
        self.act(code[4].animate.set_color(ACCENT),duration=.4)

    def memory_after(self,page):
        self.badge('WORKED EXAMPLE  /  MODEL DOUBLE')
        win=self.window('Support chat  /  conversation 1',height=5.9,center=(0,-.48,0))
        self.act(FadeIn(win))
        ask=self.bubble('Remember Spanish for future conversations?',width=12.0,height=1.1,size=31).move_to([0,.9,0])
        save=self.chip('Yes, remember it',width=5.2,accent=True).move_to([0,-.6,0])
        self.act(FadeIn(ask),FadeIn(save))
        self.at(2.2);self.act(Indicate(save,color=ACCENT,scale_factor=1.07))
        saved=self.chip('Saved to this user’s profile',width=9.0,accent=True).move_to([0,-.6,0])
        self.act(ReplacementTransform(save,saved))
        self.at(4.8)
        newtitle=self.text('Support chat  /  new conversation',21,ACCENT,mono=True,width=13.7).move_to(win[2],aligned_edge=LEFT)
        self.act(ReplacementTransform(win[2],newtitle),FadeOut(ask),FadeOut(saved))
        question=self.bubble(self.evidence['replay']['question'],width=10.5,height=.92,accent=True).move_to([1,1.02,0])
        self.act(FadeIn(question))
        answer=self.bubble(self.evidence['replay']['spanish_answer'],width=12.0,height=1.3,size=33).move_to([-.4,-.60,0])
        self.act(FadeIn(answer[0]),AddTextLetterByLetter(answer[1]),duration=1.5)
        forget=self.chip('Change it  ·  Forget it',width=8.0,size=26).move_to([0,-2.46,0])
        self.at(9.3);self.act(FadeIn(forget))

    def checks(self,page):
        self.badge('ACTUAL LOCAL TEST RESULTS')
        result=self.text(f"{self.evidence['tests']['passed']} checks passed.",57,ACCENT).set_y(1.13)
        scope=self.text('19 HTTP/Python + 6 stream-helper checks\nOffline model double',29,MUTED).set_y(-.05)
        items=VGroup(*[self.chip(s,width=6.7,size=28) for s in ['Session ownership','Stream completion & errors','Consent & user isolation','New chat & forgetting']]).arrange_in_grid(rows=2,cols=2,buff=(.4,.35)).set_y(-2.22)
        self.act(FadeIn(result),FadeIn(scope))
        self.at(2);self.act(LaggedStart(*[FadeIn(x) for x in items],lag_ratio=.2),duration=1.0)

    def clients(self,page):
        rows=VGroup()
        for label,value in page['items']:
            win=self.window(label,width=14.4,height=1.55,center=(0,0,0))
            # Compact rows use a single header band and command beneath it.
            win[2].set_y(.4);win[3].set_y(.05)
            command=self.text(value,27,mono=True,width=13.7).move_to([-6.8,-.35,0],aligned_edge=LEFT)
            rows.add(VGroup(win,command))
        rows.arrange(DOWN,buff=.25).set_y(-.48)
        for row in rows:
            self.act(FadeIn(row,shift=UP*.1),duration=.6)
            self.at(2.5*(len([m for m in rows if m in self.mobjects])))
        self.at(7)

    def closing(self,page):
        words=VGroup(*[self.text(s,48,ACCENT if i==1 else INK) for i,s in enumerate(['Install.','Ask.','Review.'])]).arrange(RIGHT,buff=.85).set_y(1.55)
        self.act(LaggedStart(*[FadeIn(x,shift=UP*.12) for x in words],lag_ratio=.35),duration=1.2)
        repo=self.window('GET THE SKILLS',height=2.45,center=(0,-.45,0))
        url=self.text('github.com/RuslanKhis/\nagentic-engineering-skills',32,mono=True,width=13.2).move_to([0,-.73,0])
        self.at(2.5);self.act(FadeIn(repo),FadeIn(url))
        book=self.text('The skills companion to Agentic Engineering',29).set_y(-2.6)
        author=self.text('By Ruslan Khissamiyev',25,MUTED).set_y(-3.27)
        self.at(5);self.act(FadeIn(book),FadeIn(author))

    def finish_page(self,page):
        self.renderer.update_frame(self)
        self.camera.get_image().save(OUTPUT/'frames'/f'{self.page_index:02d}-{page["id"]}.png')
        for mob in self.mobjects:
            if mob.width and mob.height:
                assert mob.get_left()[0]>=-7.95 and mob.get_right()[0]<=7.95, (page['id'],'horizontal overflow')
                assert mob.get_bottom()[1]>=-4.48 and mob.get_top()[1]<=4.48, (page['id'],'vertical overflow')
        if not PREVIEW and self.time-self.start_time>page['duration']-.3:
            raise ValueError(f'Animation exceeds scene reading budget: {page["id"]}')
        self.at(page['duration']-.3)
        self.act(FadeOut(Group(*self.mobjects)),duration=.3)
        self.clear()
        self.records.append({'scene':self.page_index,'id':page['id'],'title':page['title'],
                             'start':round(self.start_time,3),'end':round(self.time,3),
                             'planned_duration':page['duration']})
