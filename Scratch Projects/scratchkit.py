"""Shared toolkit for the weekly Scratch projects.

Each week's build.py imports this, draws its own art, writes its own missions,
and calls write_pair() to produce a Starter (no code, instructions in notes)
and a Solution (the finished game).
"""

import hashlib
import io
import json
import math
import struct
import wave
import zipfile
from pathlib import Path

RATE = 22050
WEBSITE = Path(__file__).resolve().parent.parent / "docs" / "scratch"  # the website's Scratch tab links here


# ---------------------------------------------------------------- art

def svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>'
    )


# ---------------------------------------------------------------- sound

def tone(freq, dur, vol=0.5, decay=6.0, shape="sine", slide_to=None):
    n = int(RATE * dur)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / RATE
        f = freq if slide_to is None else freq + (slide_to - freq) * (i / n)
        phase += 2 * math.pi * f / RATE
        if shape == "sine":
            s = math.sin(phase) + 0.3 * math.sin(2 * phase)
        else:
            s = 1.0 if math.sin(phase) >= 0 else -1.0
        attack = min(1.0, i / (RATE * 0.005))
        release = min(1.0, (n - i) / (RATE * 0.01))
        out.append(s * vol * attack * release * math.exp(-decay * t))
    return out


def wav(samples):
    peak = max(1e-9, max(abs(s) for s in samples))
    scale = min(1.0, 0.9 / peak)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(s * scale * 32767)) for s in samples))
    return buf.getvalue(), len(samples)


# ---------------------------------------------------------------- assets

class Assets:
    def __init__(self):
        self.files = {}

    def _store(self, data, ext):
        md5 = hashlib.md5(data).hexdigest()
        self.files[f"{md5}.{ext}"] = data
        return md5

    def costume(self, name, svg_text, cx, cy):
        md5 = self._store(svg_text.encode(), "svg")
        return {"name": name, "bitmapResolution": 1, "dataFormat": "svg", "assetId": md5,
                "md5ext": f"{md5}.svg", "rotationCenterX": cx, "rotationCenterY": cy}

    def sound(self, name, made):
        data, count = made
        md5 = self._store(data, "wav")
        return {"name": name, "assetId": md5, "dataFormat": "wav", "format": "", "rate": RATE,
                "sampleCount": count, "md5ext": f"{md5}.wav"}


# ---------------------------------------------------------------- blocks

def uid(prefix, n=[0]):
    n[0] += 1
    return f"{prefix}{n[0]:03d}"


class Var:
    def __init__(self, name):
        self.name = name
        self.id = uid("var-")


class Msg:
    def __init__(self, name):
        self.name = name
        self.id = uid("msg-")


class B:
    """A block. Inputs may be numbers, strings, Vars, other Bs, or lists of Bs (stacks)."""

    def __init__(self, opcode, inputs=None, fields=None, mutation=None):
        self.opcode = opcode
        self.inputs = inputs or {}
        self.fields = fields or {}
        self.mutation = mutation


NUMBER_KINDS = {"math_number": 4, "math_positive_number": 5, "math_angle": 8, "color": 9, "text": 10}


def emit(target_blocks, stack, parent=None, x=None, y=None):
    """Writes a list of Bs into target_blocks as a linked stack and returns the first id."""
    ids = [uid("b-") for _ in stack]
    for i, (bid, blk) in enumerate(zip(ids, stack)):
        entry = {
            "opcode": blk.opcode,
            "next": ids[i + 1] if i + 1 < len(ids) else None,
            "parent": parent if i == 0 else ids[i - 1],
            "inputs": {},
            "fields": blk.fields,
            "shadow": False,
            "topLevel": i == 0 and parent is None,
        }
        if entry["topLevel"]:
            entry["x"], entry["y"] = x, y
        if blk.mutation:
            entry["mutation"] = blk.mutation
        target_blocks[bid] = entry
        for name, value in blk.inputs.items():
            entry["inputs"][name] = input_for(target_blocks, bid, value)
    return ids[0]


def input_for(target_blocks, parent, value):
    kind = "math_number"
    if isinstance(value, tuple):
        kind, value = value
    if isinstance(value, list):
        return [2, emit(target_blocks, value, parent)]
    if isinstance(value, Var):
        return [3, [12, value.name, value.id], [NUMBER_KINDS[kind], ""]]
    if isinstance(value, Msg):
        return [1, [11, value.name, value.id]]
    if isinstance(value, B):
        child = emit(target_blocks, [value], parent)
        if value.opcode.endswith("_menu") or value.opcode in SHADOW_MENUS:
            target_blocks[child]["shadow"] = True
            return [1, child]
        if kind == "bool":
            return [2, child]
        return [3, child, [NUMBER_KINDS[kind], ""]]
    return [1, [NUMBER_KINDS[kind], str(value)]]


SHADOW_MENUS = {"sensing_touchingobjectmenu", "sound_sounds_menu", "looks_costume"}


# block helpers, named after the palette

def when_flag():
    return B("event_whenflagclicked")


def when_key(key):
    return B("event_whenkeypressed", fields={"KEY_OPTION": [key, None]})


def when_receive(msg):
    return B("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": [msg.name, msg.id]})


def broadcast(msg):
    return B("event_broadcast", {"BROADCAST_INPUT": msg})


def forever(*stack):
    return B("control_forever", {"SUBSTACK": list(stack)})


def if_(cond, *stack):
    return B("control_if", {"CONDITION": ("bool", cond), "SUBSTACK": list(stack)})


def repeat_until(cond, *stack):
    return B("control_repeat_until", {"CONDITION": ("bool", cond), "SUBSTACK": list(stack)})


def wait(secs):
    return B("control_wait", {"DURATION": ("math_positive_number", secs)})


def stop_all():
    return B("control_stop", fields={"STOP_OPTION": ["all", None]},
             mutation={"tagName": "mutation", "children": [], "hasnext": "false"})


def stop_other_scripts():
    return B("control_stop", fields={"STOP_OPTION": ["other scripts in sprite", None]},
             mutation={"tagName": "mutation", "children": [], "hasnext": "true"})


def go_to_xy(x, y):
    return B("motion_gotoxy", {"X": x, "Y": y})


def change_x(dx):
    return B("motion_changexby", {"DX": dx})


def change_y(dy):
    return B("motion_changeyby", {"DY": dy})


def y_position():
    return B("motion_yposition")


def point_in_direction(degrees):
    return B("motion_pointindirection", {"DIRECTION": ("math_angle", degrees)})


def glide_to_xy(secs, x, y):
    return B("motion_glidesecstoxy", {"SECS": secs, "X": x, "Y": y})


def say_for(text, secs):
    return B("looks_sayforsecs", {"MESSAGE": ("text", text), "SECS": secs})


def show():
    return B("looks_show")


def hide():
    return B("looks_hide")


def next_costume():
    return B("looks_nextcostume")


def switch_costume(name):
    return B("looks_switchcostumeto", {"COSTUME": B("looks_costume", fields={"COSTUME": [name, None]})})


def change_effect(effect, by):
    """effect is COLOR, FISHEYE, WHIRL, PIXELATE, MOSAIC, BRIGHTNESS or GHOST."""
    return B("looks_changeeffectby", {"CHANGE": by}, {"EFFECT": [effect, None]})


def go_to_front():
    return B("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]})


def play(sound):
    return B("sound_play", {"SOUND_MENU": B("sound_sounds_menu", fields={"SOUND_MENU": [sound, None]})})


def play_until_done(sound):
    return B("sound_playuntildone", {"SOUND_MENU": B("sound_sounds_menu", fields={"SOUND_MENU": [sound, None]})})


def key_pressed(key):
    return B("sensing_keypressed", {"KEY_OPTION": B("sensing_keypressed_menu", fields={"KEY_OPTION": [key, None]})})


def touching(sprite):
    """sprite is a sprite name, or "_edge_" for the edge of the stage."""
    return B("sensing_touchingobject", {
        "TOUCHINGOBJECTMENU": B("sensing_touchingobjectmenu", fields={"TOUCHINGOBJECTMENU": [sprite, None]})})


def touching_color(hex_color):
    return B("sensing_touchingcolor", {"COLOR": ("color", hex_color)})


def random(lo, hi):
    return B("operator_random", {"FROM": lo, "TO": hi})


def minus(a, b):
    return B("operator_subtract", {"NUM1": a, "NUM2": b})


def less_than(a, b):
    return B("operator_lt", {"OPERAND1": ("text", a), "OPERAND2": ("text", b)})


def greater_than(a, b):
    return B("operator_gt", {"OPERAND1": ("text", a), "OPERAND2": ("text", b)})


def equals(a, b):
    return B("operator_equals", {"OPERAND1": ("text", a), "OPERAND2": ("text", b)})


def set_var(var, value):
    return B("data_setvariableto", {"VALUE": ("text", value)}, {"VARIABLE": [var.name, var.id]})


def change_var(var, by):
    return B("data_changevariableby", {"VALUE": by}, {"VARIABLE": [var.name, var.id]})


# ---------------------------------------------------------------- project

def note(text, x, y, w=480, h=None):
    """A yellow workspace note, tall enough for its text when h is left out.

    Scratch notes don't grow, and students won't scroll inside one."""
    text = text.strip()
    return {"blockId": None, "x": x, "y": y, "width": w, "height": h or note_height(text, w),
            "minimized": False, "text": text}


def note_height(text, w=480):
    """Measured in the editor on a Mac: at width 480 a line holds about 66 characters
    and is 19 units tall, and the title bar and padding take 68. Chromebooks and
    Windows use a wider font, so this assumes 12% fewer characters and adds 30."""
    per_line = int(66 * (w - 24) / 456 * 0.88)
    rows = 0
    for line in text.split("\n"):
        used, rows = 0, rows + 1
        for word in line.split(" "):
            if used and used + 1 + len(word) > per_line:
                rows, used = rows + 1, len(word)
            else:
                used += len(word) + (1 if used else 0)
    return rows * 19 + 68 + 30


def _target(name, costumes, sounds, **extra):
    t = {"isStage": name == "Stage", "name": name, "variables": {}, "lists": {}, "broadcasts": {},
         "blocks": {}, "comments": {}, "currentCostume": 0, "costumes": costumes,
         "sounds": list(sounds), "volume": 100}
    t.update(extra)
    return t


def new_stage(costumes, sounds=()):
    return _target("Stage", costumes, sounds, layerOrder=0, tempo=60, videoTransparency=50,
                   videoState="on", textToSpeechLanguage=None)


def new_sprite(name, costumes, sounds, layer, x, y, visible=True, rotation="all around"):
    """rotation is "all around", "left-right" or "don't rotate"."""
    return _target(name, costumes, sounds, layerOrder=layer, visible=visible, x=x, y=y, size=100,
                   direction=90, draggable=False, rotationStyle=rotation)


def monitor(var, x, y):
    """A variable readout on the stage, for a variable that belongs to the Stage."""
    return {"id": var.id, "mode": "default", "opcode": "data_variable",
            "params": {"VARIABLE": var.name}, "spriteName": None, "value": 0,
            "width": 0, "height": 0, "x": x, "y": y, "visible": True,
            "sliderMin": 0, "sliderMax": 100, "isDiscrete": True}


def package(targets, assets, monitors):
    project = {"targets": targets, "monitors": monitors, "extensions": [],
               "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "WISE Academy scratchkit"}}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        files = [("project.json", json.dumps(project, separators=(",", ":")).encode())] + sorted(assets.files.items())
        for name, data in files:
            # A fixed date keeps rebuilds byte-identical, so Git only sees real changes.
            z.writestr(zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0)), data, zipfile.ZIP_DEFLATED)
    return buf.getvalue()


def write_pair(folder, title, build):
    """build(with_code) returns sb3 bytes. Writes '<title> - Starter.sb3' and '<title> - Solution.sb3',
    and copies the Starter to docs/scratch/<title-in-kebab-case>.sb3 for the website to link to."""
    for label, with_code in (("Starter", False), ("Solution", True)):
        out = folder / f"{title} - {label}.sb3"
        out.write_bytes(build(with_code))
        print(f"wrote {out.name}  ({out.stat().st_size // 1024} KB)")
    site = WEBSITE / (title.lower().replace(" ", "-") + ".sb3")
    site.write_bytes((folder / f"{title} - Starter.sb3").read_bytes())
    print(f"copied the Starter to docs/scratch/{site.name}")
