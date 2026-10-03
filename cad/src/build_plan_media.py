"""CharCube prototype build plan pictures (CCB-BLD-001, STANDARDS section 18).

Run from the repo root (one group per process keeps memory low):
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CCB-DWG-101 to 116        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as m  # noqa: E402
from model import PARAMS as P, levels, tripod_geometry  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
L = levels()
T = tripod_geometry()
_C = None


def comps():
    global _C
    if _C is None:
        _C = m.build_components()
    return _C


def S(*keys):
    """The named components as one compound (no boolean fuse, which can fail on touching parts)."""
    import build123d as b
    if len(keys) == 1:
        return comps()[keys[0]].shape
    return b.Compound(children=[comps()[k].shape for k in keys])


COL = {"blocks": "#9CA3AF", "pan": "#57534E", "drum": "#4B5563", "dampers": "#D97706", "guides": "#92400E",
       "blanket": "#E7E5E4", "bricks": "#B45309", "retort": "#9A3412", "rlid": "#7C2D12", "handles": "#111827",
       "lid": "#374151", "collar": "#0EA5E9", "throat": "#C2410C", "shroud": "#0284C7", "band": "#1D4ED8",
       "lblanket": "#F5F5F4", "jacket": "#0F766E", "fins": "#64748B", "jlid": "#14B8A6", "vent": "#1F2937",
       "tap": "#D4A017", "jblanket": "#FDE68A", "leg": "#A16207", "cleat": "#713F12", "pad": "#44403C",
       "bolt": "#111827", "tri_leg": "#A16207", "tri_cleat": "#713F12", "tri_pad": "#44403C", "tri_bolts": "#111827", "flue": "#6B7280", "clips": "#7C3AED", "cap_legs": "#6D28D9", "cap": "#374151",
       "baffle": "#78716C", "rod": "#DC2626", "probes": "#7C3AED", "logger": "#6D28D9",
       "board": "#FDE7C4", "btc": "#DC2626", "labels": "#F2C230", "footing": "#A8A29E", "gsleeve": "#57534E",
       "post": "#334155", "arm": "#475569", "brace": "#94A3B8", "aid_bolts": "#111827", "pulleys": "#0EA5E9",
       "winch": "#B91C1C", "rope": "#1F2937", "hook": "#111827", "bar": "#DC2626"}
AID_POST = ("footing", "gsleeve", "post")
AID_ARM = ("arm", "brace", "aid_bolts", "pulleys", "winch", "rope", "hook")


def aid_part(name, keys, arm_deg, color=None, explode=(0, 0, 0)):
    """Lifting-aid parts with the arm turned to arm_deg (the model has it parked)."""
    import build123d as b
    loc = m.lifting_aid_local()
    sh = b.Compound(children=[m.aid_place(P, loc[k][1], arm_deg=arm_deg) for k in keys])
    return Part(name, sh, color or COL[keys[0]], None, tuple(explode), 1.0)


def part(name, keys, color=None, explode=(0, 0, 0), alpha=1.0):
    keys = (keys,) if isinstance(keys, str) else keys
    return Part(name, S(*keys), color or COL[keys[0]], None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of a shape inside a box, solid by solid (a boolean on a whole compound is not reliable)."""
    import build123d as b
    box = b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)
    out = None
    for so in shape.solids():
        bb = so.bounding_box()
        if bb.max.X < x0 or bb.min.X > x1 or bb.max.Y < y0 or bb.min.Y > y1 or bb.max.Z < z0 or bb.min.Z > z1:
            continue
        try:
            r = so & box
        except ValueError:          # a box face exactly on a model face can defeat the boolean: nudge it
            nb = b.Pos((x0 + x1) / 2 + 0.013, (y0 + y1) / 2 + 0.011, (z0 + z1) / 2 + 0.017) * b.Box(x1 - x0, y1 - y0, z1 - z0)
            r = so & nb
        if r is None:
            continue
        for s2 in r.solids():
            if s2.volume > 1e-3:
                out = s2 if out is None else out + s2
    return out


def wpart(name, keys, box, color=None):
    keys = (keys,) if isinstance(keys, str) else keys
    return Part(name, win(S(*keys), *box), color or COL[keys[0]], None, (0, 0, 0), 1.0)


def qpart(name, keys, r, z0, z1, color=None):
    """Three-quarter cutaway: the part inside a square of half-side r, with the front left quarter
    (toward a camera at azimuth -135) removed, so the section shows and the part stays in view."""
    keys = (keys,) if isinstance(keys, str) else keys
    sh = S(*keys)
    a_, b_ = win(sh, 0, r, -r, r, z0, z1), win(sh, -r, 0, 0, r, z0, z1)
    out = a_ if b_ is None else (b_ if a_ is None else a_ + b_)
    return Part(name, out, color or COL[keys[0]], None, (0, 0, 0), 1.0)


# ----------------------------------------------------------------- named groups, in build order
def groups():
    return [
        ("Concrete blocks (4)", ("blocks",)),
        ("Block thermocouple", ("btc",)),
        ("Fibre board", ("board",)),
        ("Ash pan", ("pan",)),
        ("Outer drum, cut", ("drum",)),
        ("Port dampers and guides", ("dampers", "guides")),
        ("Drum blanket", ("blanket",)),
        ("Firebrick standoffs (3)", ("bricks",)),
        ("Retort, lid and handles", ("retort", "rlid", "handles")),
        ("Outer lid, cut", ("lid",)),
        ("Throat collar", ("collar",)),
        ("Burner throat", ("throat",)),
        ("Air shroud and band damper", ("shroud", "band")),
        ("Lid blanket", ("lblanket",)),
        ("Water jacket with fins", ("jacket", "fins")),
        ("Tap", ("tap",)),
        ("Jacket lid and vent nipple", ("jlid", "vent")),
        ("Jacket blanket", ("jblanket",)),
        ("Tripod legs (3)", ("tri_leg",)),
        ("Foot cleats and pads (3)", ("tri_cleat", "tri_pad")),
        ("Lifting aid: footing, sleeve and post", AID_POST),
        ("Lifting aid: arm, brace, pulleys, winch, rope", AID_ARM),
        ("Flue with clips and rain cap", ("flue", "clips", "cap_legs", "cap")),
        ("Spiral baffle and rod", ("baffle", "rod")),
        ("Logger and probes", ("logger", "probes")),
        ("Hot-surface labels (2)", ("labels",)),
    ]


# ----------------------------------------------------------------- overview
def overview():
    off = {   # three columns: blankets on the left, the kiln stack in the middle, loose parts on the right
        "Concrete blocks (4)": (0, 0, -650), "Block thermocouple": (1000, 0, -600), "Fibre board": (0, 0, -450),
        "Ash pan": (0, 0, -250), "Outer drum, cut": (0, 0, 0),
        "Port dampers and guides": (-600, -1100, 300), "Drum blanket": (-1100, 0, 0), "Firebrick standoffs (3)": (1000, 0, -150),
        "Retort, lid and handles": (1000, 0, 150), "Outer lid, cut": (0, 0, 450), "Throat collar": (0, 0, 600),
        "Burner throat": (0, 0, 800), "Air shroud and band damper": (1000, 0, 750), "Lid blanket": (-1100, 0, 450),
        "Water jacket with fins": (0, 0, 1050), "Tap": (1000, 0, 1050), "Jacket lid and vent nipple": (0, 0, 1350),
        "Jacket blanket": (-1100, 0, 1050), "Tripod legs (3)": (2100, 0, 0), "Foot cleats and pads (3)": (2100, 0, -250),
        "Flue with clips and rain cap": (0, 0, 1650), "Spiral baffle and rod": (1000, 0, 1350), "Logger and probes": (2100, 0, 1900),
        "Hot-surface labels (2)": (-1100, -400, 300),
        "Lifting aid: footing, sleeve and post": (3500, -1200, -400), "Lifting aid: arm, brace, pulleys, winch, rope": (3500, -1200, 0),
    }
    parts = [part(n, k, explode=off[n]) for n, k in groups()]
    return bv.overview(parts, OUT / "overview.png", "CharCube prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above", elev=16, azim=-62,
                       size=(12, 10), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def _sheet(n, key_part, neighbours, title, material, notes, view_shape=None, inset=(20, -60)):
    return bv.component_sheet(key_part, neighbours, project="CharCube", dwg_no=f"CCB-DWG-{n}", title=title,
                              material=material, notes=notes, date=DATE, view_shape=view_shape, inset_view=inset,
                              out_dir=str(DWG))


def sheets(which=None):
    import build123d as b
    zl = L["z_lid"]
    grey = lambda name, keys: part(name, keys, "#D1D5DB")   # noqa: E731
    cg = m.cap_geometry()
    TAB_UP = cg["under"](P["FLUE_D"] / 2 + 30)
    LEG_CAP = TAB_UP + 60 + 30
    sh = {}

    sh[101] = lambda: _sheet(101, part("Ash pan, fibre board and block thermocouple", ("pan", "board", "btc"), "#57534E"),
        [grey("Blocks", "blocks"), grey("Drum", "drum")],
        "CharCube plinth: ash pan and fibre board: making sketch", "Mild steel plate 3 mm; ceramic fibre board 25 mm",
        ["Pan: cut 760 x 600 mm from 3 mm mild steel plate; grind the edges",
         "  and round the corners to about 10 mm. Mark a 572 mm circle in",
         "  the middle with a centre line each way: the drum stands on it.",
         "Board: cut a 600 x 600 mm square from a 25 mm ceramic fibre board",
         "  sheet (1260 deg C grade) with a fine saw; wear a dust mask.",
         "  Cut a groove 4 wide x 4 deep in its underside, from 150 mm",
         "  behind the centre, 50 mm left of it, straight out to the back edge.",
         "Block thermocouple: lay its tip on the back block in line with the",
         "  groove, 150 mm behind the centre; the lead runs out at the back.",
         "Fit: blocks, then board centred on them, then the pan on the board.",
         "Check: the pan rests flat without rocking; the lead is not pinched."], inset=(25, -60))

    sh[102] = lambda: _sheet(102, part("Outer drum, cut", "drum"), [grey("Pan", "pan"), grey("Blocks", "blocks")],
        "CharCube outer drum (200 L): cutting sketch", "Used 200 L open-head steel drum, 1.2 mm",
        ["A clean 200 L open-head drum, 572 mm across, 851 mm tall, that held",
         "  only a non-flammable, non-toxic product. Burn off paint outdoors first.",
         "Air ports: four, 40 wide x 110 tall, bottom edge 20 mm above the floor,",
         "  on the four diagonals (front left, front right, back left, back",
         "  right; the tap is on the right). Drill the corners 6 mm, cut",
         "  between with an angle grinder and thin disc, file the edges.",
         "Probe hole: one 10 mm hole at the back, 361 mm above the floor.",
         "Damper guide rivet holes: 4.9 mm, two above and two below each port",
         "  (see the damper sketch CCB-DWG-103).",
         "Deburr every edge; fold or file any sharp lip.",
         "Check: the lid and locking ring still close on the rim."], inset=(20, -55))

    def _ang(so):
        c = so.center()
        return math.degrees(math.atan2(c.Y, c.X))
    one = [so for so in S("dampers", "guides").solids() if abs(_ang(so) - 52) < 20]   # the back right set
    a0 = 45 + math.degrees(P["DAMPER_OPEN"] / 2 / (P["OUT_D"] / 2))
    flat_d = b.Rot(0, 0, -90 - a0) * b.Compound(children=one)   # turned to face the front view
    sh[103] = lambda: _sheet(103, Part("Port damper and guides", S("dampers", "guides"), COL["dampers"], None, (0, 0, 0), 1),
        [grey("Drum", "drum")],
        "CharCube port damper and guide strips (make 4 sets): making sketch", "Mild steel sheet 1.2 mm and strip 1.5 mm",
        ["Damper: cut four 60 x 122 mm plates from 1.2 mm sheet; roll each to",
         "  the drum's curve (286 mm radius) by hand over a pipe.",
         "Guides: eight strips 10 mm wide x about 135 mm long from 1.5 mm",
         "  strip. Joggle 10 mm at each end by 1.2 mm so the ends sit on the",
         "  drum and the middle stands off it by the damper's thickness.",
         "Fit: one guide just below each port (its top edge 6 mm over the",
         "  damper's lower edge), one just above. Two 4.8 mm rivets per guide,",
         "  through the joggled ends, which sit beyond the damper's travel.",
         "The damper slides sideways 55 mm: closed it covers the port with",
         "  6 mm to spare all round; open it clears the port.",
         "Check: the damper slides by hand and stays where it is put."],
        view_shape=flat_d, inset=(10, -30))

    sh[104] = lambda: _sheet(104, part("Retort, lid and handles", ("retort", "rlid", "handles")),
        [grey("Bricks", "bricks"), grey("Drum", "drum")],
        "CharCube retort (114 L): cutting sketch", "Used 114 L open-head steel drum with bolt-ring lid, 1.0 mm",
        ["A clean 114 L open-head drum, 463 mm across, 737 mm tall, with its",
         "  bolt-ring lid. Same rules for past contents and paint as the outer drum.",
         "Gas holes: eight 20 mm holes in the base on a 300 mm circle, 45",
         "  degrees apart, one on the line of the probe slot. Step drill.",
         "Probe slot: 10 wide x 40 tall in the side, centred 300 mm above",
         "  the base (the middle of the 600 mm fill). Drill and file.",
         "Handles: two M8 U-bolts, legs 80 mm apart, through four 9 mm holes",
         "  in the lid, 130 mm each side of centre; nuts and large washers",
         "  under the lid. Mark the slot's position on the lid rim.",
         "Fit: stands on the three bricks; the base holes stay clear of them.",
         "Check: the lid seals on its gasket when the ring is bolted."], inset=(20, -60))

    sh[105] = lambda: _sheet(105, part("Outer lid and collar", ("lid", "collar")),
        [grey("Drum", "drum"), grey("Throat", "throat")],
        "CharCube outer lid and throat collar: making sketch", "Drum lid (item 1); collar from 1.5 mm sheet",
        ["Lid: the outer drum's own lid. Cut a 150 mm hole in the middle",
         "  (jigsaw with a metal blade, file to a scribed circle).",
         "Collar: a strip of 1.5 mm sheet 40 mm wide plus six tabs 15 wide x",
         "  20 long along one edge. Roll it round a piece of the 160 mm throat",
         "  pipe so it fits the pipe snugly, and rivet the overlap.",
         "Fold the six tabs out flat. Stand the collar on the lid centred on",
         "  the hole, drill through each tab and the lid 4.9 mm, rivet.",
         "The throat stands on the 5 mm ring of lid inside the collar.",
         "Glue ceramic gasket rope in the lid's rim channel with sealant.",
         "Check: a 160 mm pipe slides into the collar by hand, with no gap",
         "  wider than 1 mm, and sits flat on the lid."], inset=(30, -60))

    sh[106] = lambda: _sheet(106, part("Burner throat", "throat"), [grey("Lid", ("lid", "collar")), grey("Shroud", "shroud")],
        "CharCube burner throat: making sketch", "Plain steel pipe 160 x 2 mm (not galvanized)",
        ["Cut 400 mm of 160 x 2 mm plain steel pipe; square the ends.",
         "Air holes: two rings of fifteen 12 mm holes (24 degrees apart),",
         "  95 and 135 mm above the bottom end; the upper ring turned 12",
         "  degrees from the lower. Wrap a paper template round the pipe.",
         "Probe hole: one 8 mm hole at the back, 330 mm above the bottom end.",
         "Fixing: four 4.9 mm rivet holes 20 mm above the bottom end, drilled",
         "  through the collar once the throat stands in it.",
         "Shroud tab holes: six, 200 mm above the bottom end (drill with",
         "  the shroud in place, CCB-DWG-107).",
         "Check: stands square on a flat plate; holes deburred inside."], inset=(25, -60))

    sh[107] = lambda: _sheet(107, part("Air shroud and band damper", ("shroud", "band")), [grey("Throat", "throat"), grey("Lid", ("lid", "collar"))],
        "CharCube air shroud and band damper: making sketch", "Mild steel sheet 1.5 mm; band from 3 mm strip",
        ["Sleeve: a 150 mm wide strip of 1.5 mm sheet rolled to 230 mm",
         "  outside diameter, overlap riveted.",
         "Top ring: a 230 mm disc with a 160 mm hole; cut six tabs 15 mm wide",
         "  into the hole edge (before cutting it to size) and fold them up",
         "  20 mm. Fold or rivet the ring onto the sleeve top.",
         "Fit: slide over the throat, bottom edge 40 mm above the lid (a",
         "  40 mm block under it while drilling); rivet the six tabs to the",
         "  throat. The air holes sit inside, 55 and 95 mm above its bottom.",
         "Band damper: a 60 mm wide band of 3 mm strip rolled to fit round",
         "  the sleeve, with a riveted nut and an M6 wing screw. Open: up on",
         "  the sleeve; closed: slid down to the lid.",
         "Check: the band slides and the wing screw holds it."], inset=(25, -60))

    sh[108] = lambda: _sheet(108, part("Water jacket with fins", ("jacket", "fins")), [grey("Throat", "throat"), grey("Legs", "tri_leg")],
        "CharCube water jacket: fabrication sketch (the one welded part)", "Mild steel sheet 2 mm, pipe 168 x 2 mm, plate 6 mm",
        ["For a welder. Sleeve: 700 mm of 168 x 2 mm pipe. Shell: 2 mm sheet",
         "  rolled to 420 mm outside, 600 mm tall. Bottom: 2 mm ring, 420 mm",
         "  outside, 168 mm hole. Weld water-tight; the sleeve stands 50 mm",
         "  out of the top and the bottom (the two sockets). Flare the bottom",
         "  20 mm of the sleeve to about 190 mm across (a cone) so it guides",
         "  itself onto the throat. Two 18 mm holes across the top socket,",
         "  35 mm above the shell top, for the lift bar. The sleeve weld",
         "  carries the whole unit when it is lifted: weld it all round.",
         "Fins: three 6 mm plates 85 x 140 mm, welded radially to the shell,",
         "  one at the front, one back right, one back left (120 degrees",
         "  apart), 60 mm up the shell and 80 mm below it.",
         "  Two 11 mm holes per fin: 245 mm from the axis, 15 mm above the",
         "  jacket's underside; 267 mm from the axis, 52 mm below it.",
         "Tap socket: 1/2 in socket welded 40 mm above the bottom, on the",
         "  right side. Open top: no lid welded, nothing sealed.",
         "Leak test with water before painting. High-temperature paint outside.",
         "Check: holds water overnight; the sleeve slides over a 160 mm pipe."], inset=(20, -60))

    sh[109] = lambda: _sheet(109, part("Jacket lid and vent nipple", ("jlid", "vent")), [grey("Jacket", ("jacket", "fins"))],
        "CharCube jacket loose lid: making sketch", "Mild steel sheet 1.5 mm; 3/4 in steel nipple",
        ["Cut a 420 mm disc from 1.5 mm sheet with a 210 mm hole in the middle",
         "  (the hole clears the flue and its stop clips).",
         "Locating tabs: three 20 x 15 mm tabs riveted under the lid, folded",
         "  down, 2 mm inside the shell, 120 degrees apart.",
         "Vent: a 27 mm hole 170 mm from the centre; a 3/4 in steel nipple",
         "  80 mm long through it, held by a locknut each side.",
         "Fit: rests loose on the shell rim. It is never fixed, sealed or",
         "  weighted: the jacket must stay open to the air.",
         "Check: lifts off by hand; the vent is clear."], inset=(35, -60))

    leg1 = S("tri_leg").solids()
    leg0 = b.Rot(0, 0, -P["LEG_ANGLES"][0]) * leg1[0]
    d = T["d"]
    flat = b.Plane(origin=(T["g"][0], 0, 0), x_dir=(T["n"][0], 0, T["n"][1]), z_dir=(d[0], 0, d[1])).to_local_coords(leg0)
    tg = T["s"]
    leg_long = flat.bounding_box().size.Z
    sh[110] = lambda: _sheet(110, Part("Tripod leg", leg1[0], COL["leg"], None, (0, 0, 0), 1),
        [grey("Jacket", ("jacket", "fins")), grey("Cleat", ("tri_cleat", "tri_pad"))],
        "CharCube tripod leg (make 3): making sketch", "Steel equal angle 40 x 40 x 4 mm",
        [f"Cut three lengths of 40 x 40 x 4 angle, {leg_long:.0f} mm on the longest",
         "  edge (drawn upright). Cut the lower end 18 degrees off square so",
         "  it stands level when the leg leans 18 degrees in; the upper end",
         "  is cut square.",
         "Three 11 mm holes in one face of the angle (the flat face), 18 mm",
         "  from its free edge, measured along the leg from the lower end:",
         f"  foot pin {P['FOOT_BOLT_Z'] / d[1] - tg['bot']:.0f} mm; "
         f"fin bolts {tg['b2'] - tg['bot']:.0f} and {tg['b1'] - tg['bot']:.0f} mm.",
         "Drill the three legs clamped together so the holes match.",
         "Fit: the flat face lies on a jacket fin (two M10 bolts) and on a",
         "  foot cleat (one M10 bolt, a pin). The other face points away",
         "  from the jacket.",
         "Check: hole centres within 1 mm of the figures."], view_shape=flat, inset=(15, -40))

    sh[111] = lambda: _sheet(111, part("Foot cleat and pad", ("tri_cleat", "tri_pad")), [grey("Legs", "tri_leg")],
        "CharCube foot cleat and pad (make 3 sets): making sketch", "Steel angle 40 x 40 x 4 mm; plate 6 mm",
        ["Cleat: a 60 mm length of 40 x 40 x 4 angle.",
         "  Upright face: one 11 mm hole at mid-length, 24 mm up from the",
         "  underside of the flat face (the leg's pin).",
         "  Flat face: two 9 mm holes, 18 mm each side of the middle,",
         "  22 mm in from the heel.",
         "Pad: a 100 x 100 mm square of 6 mm plate; two 9 mm holes to",
         "  match the cleat, countersunk from below.",
         "Fit: M8 countersunk screws up through the pad, nyloc nuts on the",
         "  cleat. The leg's flat face lies on the cleat's upright face,",
         "  outside it; one M10 bolt, nyloc nut, snug (the leg can pivot).",
         "Check: the pad sits flat with the screw heads flush."], inset=(25, -50))

    sh[112] = lambda: _sheet(112, part("Flue with stop clips", ("flue", "clips")), [grey("Jacket", ("jacket", "fins")), grey("Cap", ("cap", "cap_legs"))],
        "CharCube flue pipe and stop clips: making sketch", "Plain steel pipe 160 x 2 mm; angle 20 x 20 x 3 mm",
        ["Cut 650 mm of 160 x 2 mm plain steel pipe; square the ends.",
         "Rod holes: two 11 mm holes opposite each other, 15 mm above the",
         "  bottom end (the foot).",
         "Stop clips: three 20 mm lengths of 20 x 20 x 3 mm angle, each",
         "  riveted (two 4.8 mm rivets) by its upright leg to the pipe, 120",
         "  degrees apart, with the flat leg's underside 50 mm above the foot.",
         "Fit: the foot slides 50 mm into the jacket sleeve; the clips rest",
         "  on the sleeve rim and carry the flue and the baffle.",
         "Cap leg rivet holes: see CCB-DWG-113.",
         "Check: drops into a 164 mm bore to the clips without forcing."], inset=(20, -60))

    sh[113] = lambda: _sheet(113, part("Rain cap and legs", ("cap", "cap_legs")), [grey("Flue", ("flue", "clips"))],
        "CharCube conical rain cap and its legs: making sketch", "Mild steel sheet 1.5 mm; flat bar 20 x 3 mm",
        ["Cap: cut a 300 mm disc from 1.5 mm sheet (150 mm radius). Cut out",
         "  a 48 degree wedge to the centre, roll the rest into a cone 260 mm",
         "  across with a 30 degree slope, and rivet the overlap (three rivets).",
         f"Legs: three {LEG_CAP:.0f} mm lengths of 20 x 3 mm flat bar, each bent",
         "  90 degrees 30 mm from one end to make a foot.",
         "Fit: rivet each leg's long part to the outside of the flue top,",
         "  120 degrees apart, two 4.8 mm rivets, so the bent feet stand",
         f"  {TAB_UP:.0f} mm above the flue's top edge. Rivet the cap to the feet.",
         "The shortest gap from the flue's top edge to the cap is 60 mm:",
         "  never less, or it chokes the draft.",
         "Check: the gap under the cap is the same all round."], inset=(25, -60))

    sh[114] = lambda: _sheet(114, part("Spiral baffle and rod", ("baffle", "rod")), [grey("Flue", ("flue", "clips")), grey("Jacket", "jacket")],
        "CharCube spiral baffle insert and hanger rod: making sketch", "Plain steel strip 150 x 1.5 mm; round bar 10 mm",
        ["Strip: 615 mm of 150 x 1.5 mm plain steel strip.",
         "Drill an 11 mm hole on the centre line 10 mm from one end (the top).",
         "Twist: clamp the top end in a vice and turn the bottom end with",
         "  a long spanner on a clamped bar, half a turn per 300 mm: just",
         "  over one full turn in all. Keep the edges straight.",
         "Rod: 160 mm of 10 mm round bar; file the ends square.",
         "Fit: hold the strip inside the flue foot, push the rod through",
         "  one flue hole, the strip's hole and the other flue hole. The",
         "  strip hangs 10 mm above the throat top with 3 mm clear of the",
         "  sleeve; it lifts out with the flue.",
         "Check: the twisted strip passes through a 160 mm ring."], inset=(15, -60))

    loc = m.lifting_aid_local()
    za = L["z_arm"]
    ab = P["ARM_ANG"][0]
    sh[115] = lambda: _sheet(115, Part("Post, ground sleeve and footing", b.Compound(children=[loc[k][1] for k in AID_POST]),
                                       COL["post"], None, (0, 0, 0), 1),
        [Part("Arm and brace", b.Compound(children=[loc[k][1] for k in ("arm", "brace")]), "#D1D5DB", None, (0, 0, 0), 1)],
        "CharCube lifting aid: post, ground sleeve and footing", "Steel tube 88.9 x 3.2 and 101.6 x 3.6 mm; concrete",
        ["Footing: dig a hole 600 x 600 x 750 deep, 1.2 m straight behind the",
         "  kiln's centre. Ground sleeve: 730 mm of 101.6 x 3.6 tube with a",
         "  6 mm plate in its bottom end (a welder tacks it, or a bolt across",
         "  the tube holds a loose plate). Stand it 30 mm proud and plumb;",
         "  fill with concrete; wait at least three days.",
         f"Post: {(za + 37 + 694) / 1000:.2f} m of 88.9 x 3.2 tube; a 3 mm cap plate",
         "  in the top end. Two 17 mm holes across it: 20 mm and",
         f"  {P['BRACE_DZ'] - ab / 2 + 40:.0f} mm below the post's top end (CCB-DWG-116).",
         "Fit: two people stand the post in the sleeve; it turns by hand.",
         "Check: plumb both ways; the post turns freely through 90 degrees."], inset=(20, -60))
    arm_set = b.Compound(children=[loc[k][1] for k in ("arm", "brace", "aid_bolts", "pulleys", "rope", "hook")])
    sh[116] = lambda: _sheet(116, Part("Arm, brace, pulleys and rope", arm_set, COL["arm"], None, (0, 0, 0), 1),
        [Part("Post (top)", win(loc["post"][1], -120, 120, -120, 120, za - P["BRACE_DZ"] - 100, za + 100), "#D1D5DB", None, (0, 0, 0), 1)],
        "CharCube lifting aid: arm, brace and pulleys (bolted)", "Steel angle 50 x 50 x 5 and 40 x 40 x 4 mm; bolts",
        [f"Arm: two {P['ARM_L'] + P['ARM_TAIL']:.0f} mm lengths of 50 x 50 x 5 angle, one each side of",
         "  the post, upright faces on the post, flat faces on top, outward.",
         f"  A 17 mm hole {P['ARM_TAIL']:.0f} mm from the back end, 20 mm up: M16 bolt",
         "  through both angles and the post. Holes 13 mm,",
         f"  25 mm up, at {P['ARM_TAIL'] - 100:.0f}, {P['ARM_TAIL'] + P['BRACE_X']:.0f} and "
         f"{P['ARM_TAIL'] + P['POST_R'] - 52:.0f} mm: back pulley, brace, tip pulley.",
         "Brace: two 990 mm lengths of 40 x 40 x 4 angle at 45 degrees,",
         "  M12 to the arm, M16 through the post with a 5 mm packing plate.",
         "Pulleys: 100 mm steel sheaves on M12 axles with spacer tubes.",
         "Winch: brake winch rated 270 kg, two U-bolts round the post, 1 m up.",
         "Rope: 5 mm steel wire from the winch over both pulleys; hook with latch.",
         "Check: with no load the hook hangs 1.2 m out from the post."], inset=(20, -40))

    out = []
    for n in sorted(sh):
        if which and n not in which:
            continue
        out.append(sh[n]())
        print("sheet", n, flush=True)
    return out


# ----------------------------------------------------------------- joints
def joints(which=None):
    z0, zl, zt, zj, zjt = L["z0"], L["z_lid"], L["z_thr"], L["z_jkt"], L["z_jtop"]
    ro = P["OUT_D"] / 2
    J = {}

    def j(n, parts, title, sub, **kw):
        return bv.joint(parts, OUT / f"joint-{n:02d}.png", title, subtitle=sub, size=(8, 6), **kw)

    box = (-420, 420, -420, 420, -10, z0 + 40)
    bl_, bw_ = P["BLOCK"]
    q_, m_, h_ = (bl_ + bw_) / 2, (bl_ - bw_) / 2, P["BASE_H"]
    blk = [m._bx(-q_, m_, m_, q_, 0, h_), m._bx(m_, q_, -m_, q_, 0, h_), m._bx(-m_, q_, -q_, -m_, 0, h_), m._bx(-q_, -m_, -q_, m_, 0, h_)]
    J[1] = lambda box=box: j(1, [Part(f"Block {i + 1} of the pinwheel", blk[i], ("#9CA3AF", "#6B7280")[i % 2], None, (0, 0, 0), 1.0)
                                 for i in range(4)] + [
                         wpart("Block thermocouple, tip on the back block", "btc", (-420, 420, -420, 420, -10, z0 + 40)),
                         wpart("Fibre board, 25 mm (cut away)", "board", (0, 420, 0, 420, -10, z0 + 40)),
                         wpart("Ash pan (cut away)", "pan", (0, 420, 0, 420, -10, z0 + 40)),
                         wpart("Outer drum, bottom 40 mm (cut away)", "drum", (0, 420, 0, 420, z0 + 1.3, z0 + 40))],
                     "Joint 1: drum, ash pan, fibre board and block plinth",
                     "Pinwheel of blocks; 25 mm fibre board on them shields the blocks; pan and drum on the board (back right quarter shown)",
                     elev=40, azim=-65)
    a = math.radians(45)
    cx, cy = ro * math.cos(a), ro * math.sin(a)
    box = (cx - 110, cx + 120, cy - 150, cy + 80, z0 - 5, z0 + 160)
    J[2] = lambda box=box: j(2, [wpart("Outer drum (port)", "drum", box), wpart("Damper, shown open", "dampers", box),
                         wpart("Guide strips, riveted at their ends", "guides", box), wpart("Drum blanket starts here", "blanket", box)],
                     "Joint 2: sliding port damper in its guides (back right port)",
                     "The damper slides 55 mm sideways under the two guides; it closes the port with 6 mm to spare",
                     elev=10, azim=20)
    box = (-260, 260, -260, 260, z0 - 2, L["z_ret"] + 30)
    J[3] = lambda box=box: j(3, [wpart("Firebricks (drum floor not shown)", "bricks", box),
                                 wpart("Retort base with its eight gas holes", "retort", (-260, 260, -260, 260, L["z_ret"] - 1, L["z_ret"] + 40))],
                     "Joint 3: retort on its three bricks, seen from below the retort",
                     "Bricks lie round the retort's edge, 8 mm clear of the gas holes",
                     elev=-50, azim=-60)
    box = (0, 160, -160, 160, zl - 10, zt + 220)
    J[4] = lambda box=box: j(4, [qpart("Outer lid, 150 mm hole", "lid", 170, zl - 10, zt + 193),
                                 qpart("Collar, tabs riveted to the lid", "collar", 170, zl - 10, zt + 193),
                                 qpart("Throat, standing on the lid", "throat", 170, zl - 10, zt + 193),
                                 qpart("Air shroud, tabs riveted to the throat", "shroud", 170, zl - 10, zt + 193),
                                 qpart("Band damper (open)", "band", 170, zl - 10, zt + 193),
                                 qpart("Lid blanket", "lblanket", 170, zl - 10, zt + 193)],
                     "Joint 4: throat, collar, lid and air shroud (front quarter cut away)",
                     "Air enters under the shroud, 40 mm above the lid, and through the two rings of holes",
                     elev=18, azim=-135)
    box = None
    J[5] = lambda box=box: j(5, [qpart("Burner throat", "throat", 130, zj - 120, zj + 70),
                                 qpart("Jacket sleeve and bottom", "jacket", 130, zj - 120, zj + 70),
                                 qpart("Spiral baffle, bottom end", "baffle", 130, zj - 120, zj + 70),
                                 qpart("Throat probe", "probes", 130, zj - 120, zj + 70)],
                     "Joint 5: jacket sleeve over the throat (front quarter cut away)",
                     "A 50 mm slip joint, 2 mm clear all round; the flared sleeve foot guides it on; baffle 10 mm above the throat",
                     elev=15, azim=-135)
    th = math.radians(P["LEG_ANGLES"][0])
    fx, fy = 270 * math.cos(th), 270 * math.sin(th)
    box = (fx - 110, fx + 110, fy - 110, fy + 110, zj - 120, zj + 100)
    J[6] = lambda box=box: j(6, [wpart("Jacket shell and bottom", "jacket", box), wpart("Fin, welded to the shell", "fins", box),
                         wpart("Leg, flat face on the fin", "tri_leg", box), wpart("Two M10 bolts, nyloc nuts", "tri_bolts", box),
                         wpart("Jacket blanket", "jblanket", box)],
                     "Joint 6: leg bolted to its jacket fin (back right leg)",
                     "The leg's flat face lies on the fin; two bolts make the joint rigid. Seen from beside the leg", elev=10, azim=105)
    fx, fy = 707 * math.cos(th), 707 * math.sin(th)
    box = (fx - 90, fx + 90, fy - 90, fy + 90, -5, 140)
    J[7] = lambda box=box: j(7, [wpart("Leg", "tri_leg", box), wpart("Cleat", "tri_cleat", box), wpart("Foot pad", "tri_pad", box),
                         wpart("M10 pin bolt; M8 screws from below", "tri_bolts", box)],
                     "Joint 7: leg foot on its cleat and pad (back right leg)",
                     "One M10 bolt lets the leg pivot as the unit is set down", elev=20, azim=-80)
    box = None
    J[8] = lambda box=box: j(8, [qpart("Jacket sleeve (upper socket)", "jacket", 120, zjt - 30, zjt + 78),
                                 qpart("Flue foot", "flue", 120, zjt - 30, zjt + 78),
                                 wpart("Stop clip on the sleeve rim (one of three)", "clips", (-120, 0, 0, 120, zjt - 30, zjt + 78)),
                                 qpart("Hanger rod", "rod", 120, zjt - 30, zjt + 78),
                                 qpart("Baffle top, hung on the rod", "baffle", 120, zjt - 30, zjt + 78),
                                 qpart("Loose lid", "jlid", 120, zjt - 30, zjt + 78, color="#99F6E4")],
                     "Joint 8: flue foot in the sleeve socket (front quarter cut away)",
                     "The clips carry the flue on the sleeve rim; the rod through the flue foot carries the baffle",
                     elev=15, azim=-135)
    box = (-150, 150, -150, 150, L["z_out"] - 90, L["z_cap_top"] + 10)
    J[9] = lambda box=box: j(9, [wpart("Flue top", "flue", box), wpart("Cap legs, riveted to the flue", "cap_legs", box),
                         wpart("Conical rain cap", "cap", box)],
                     "Joint 9: conical rain cap on its three legs",
                     "At least 60 mm from the flue's top edge to the cap all round", elev=15, azim=-60)
    zc = L["z_core"]
    box = (0, 80, 150, 620, zc - 70, zc + 70)
    J[10] = lambda box=box: j(10, [wpart("Retort wall with probe slot", "retort", box), wpart("Outer drum wall", "drum", box),
                           wpart("Drum blanket, slit", "blanket", box), wpart("Core probe", "probes", box)],
                      "Joint 10: core probe through the drum, blanket and retort slot (cut through the probe)",
                      "Line up the retort's slot with the drum hole before the lid goes on", elev=18, azim=-150)
    box = (-260, 260, -260, 260, zjt - 20, zjt + 90)
    J[11] = lambda box=box: j(11, [wpart("Jacket shell rim and sleeve", "jacket", box), wpart("Loose lid, three tabs inside the rim", "jlid", box),
                           wpart("Vent nipple and locknuts", "vent", box), wpart("Jacket blanket", "jblanket", box)],
                      "Joint 11: jacket loose lid and vent", "The lid rests on the rim; it is never fixed or sealed",
                      elev=25, azim=-60)
    import build123d as b
    bar = Part("Lift bar, 16 mm, through the two holes", m.lift_bar(), COL["bar"], None, (0, 0, 0), 1.0)
    J[12] = lambda: j(12, [qpart("Jacket sleeve, top socket (flue lifted out)", "jacket", 130, zjt - 40, zjt + 60),
                           qpart("Loose lid", "jlid", 130, zjt - 40, zjt + 60, color="#99F6E4"), bar],
                      "Joint 12: lift bar through the sleeve socket (front quarter cut away)",
                      "Flue out first; the hook's shackle goes on the middle of the bar", elev=25, azim=-135)
    loc = m.lifting_aid_local()
    za = L["z_arm"]
    wb = (-130, 130, 450, 1420, za - 320, za + 140)
    J[13] = lambda: j(13, [Part(n_, win(m.aid_place(P, loc[k][1], arm_deg=270.0), *wb),
                                COL[k], None, (0, 0, 0), 1.0)
                           for n_, k in (("Post top", "post"), ("Arm, two angles", "arm"), ("Brace (top end)", "brace"),
                                         ("M16 bolt through the post; axles", "aid_bolts"), ("Back pulley", "pulleys"),
                                         ("Rope to the winch", "rope"))],
                      "Joint 13: lifting arm on the post top", "Both angles bolted through the post; the rope runs over the back pulley",
                      elev=15, azim=-60)
    J[14] = lambda: j(14, [part("Drum blanket", "blanket"), part("Jacket blanket", "jblanket"),
                           part("Hot-surface labels (ISO 7010 W017)", "labels")],
                      "Joint 14: hot-surface labels on the blankets", "Wired to the blanket mesh at the front right, where the operator stands",
                      elev=12, azim=-40)
    out = []
    for n in sorted(J):
        if which and n not in which:
            continue
        out.append(J[n]())
        print("joint", n, flush=True)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(which=None):
    G = {n: k for n, k in groups()}

    def g(name, explode=(0, 0, 0)):
        return part(name, G[name], explode=explode)

    bl_, bw_ = P["BLOCK"]
    q_, m_, h_ = (bl_ + bw_) / 2, (bl_ - bw_) / 2, P["BASE_H"]
    blk = [m._bx(-q_, m_, m_, q_, 0, h_), m._bx(m_, q_, -m_, q_, 0, h_), m._bx(-m_, q_, -q_, -m_, 0, h_), m._bx(-q_, -m_, -q_, m_, 0, h_)]
    plinth = [g("Concrete blocks (4)"), g("Block thermocouple"), g("Fibre board"), g("Ash pan")]
    drum = plinth + [g("Outer drum, cut"), g("Port dampers and guides"), g("Drum blanket")]
    kiln_open = drum + [g("Firebrick standoffs (3)"), g("Retort, lid and handles")]
    lid_unit = ("Outer lid, cut", "Throat collar", "Burner throat", "Air shroud and band damper", "Lid blanket")
    kiln = kiln_open + [g(n) for n in lid_unit]
    jk = [g("Water jacket with fins")]
    unit = ("Water jacket with fins", "Tap", "Jacket lid and vent nipple", "Jacket blanket", "Tripod legs (3)", "Foot cleats and pads (3)")
    full = kiln + [g(n) for n in unit]
    flue_all = ("Flue with clips and rain cap", "Spiral baffle and rod")
    sp = {
        1: (lambda: ([], [Part(f"Block {i + 1}", blk[i], ("#9CA3AF", "#6B7280")[i % 2], None, (0, 0, 0), 1.0)
                          for i in range(4)] + [part("Block thermocouple", "btc", explode=(0, 0, 0)),
                                                 part("Fibre board", "board", explode=(0, 0, 300)),
                                                 part("Ash pan", "pan", explode=(0, 0, 600))]),
            "lay the plinth", "Blocks as a pinwheel on firm level ground; thermocouple on the back block; board, then pan, centred",
            dict(elev=42, azim=-55)),
        2: (lambda: ([part("Outer drum, cut", "drum")], [part("Port dampers", "dampers", explode=(0, 0, -150)),
                                                         part("Guide strips", "guides", explode=(0, -250, 0))]),
            "fit the port dampers and guides", "Two rivets per guide through its joggled ends; check each damper slides",
            dict(elev=12, azim=-50)),
        3: (lambda: (plinth, [part("Outer drum with dampers", ("drum", "dampers", "guides"), explode=(0, 0, 500))]),
            "stand the drum on the ash pan", "Centred on the marked circle; a port at each corner of the pan",
            dict(elev=20, azim=-55)),
        4: (lambda: (plinth + [g("Outer drum, cut"), g("Port dampers and guides")], [part("Drum blanket", "blanket", explode=(-500, 0, 0))]),
            "wrap the drum blanket", "From 140 mm above the floor to 30 mm below the rim; wire mesh over it; slit at the probe hole",
            dict(elev=15, azim=-55)),
        5: (lambda: ([part("Outer drum (cut away)", "drum", alpha=1.0)], [part("Firebricks", "bricks", explode=(0, 0, 900))]),
            "set the bricks in the drum", "Long side round the retort, centred 200 mm out: one at the back, two toward the front",
            dict(elev=55, azim=-60)),
        6: (lambda: (drum + [g("Firebrick standoffs (3)")], [part("Retort, packed, lid bolted on", ("retort", "rlid", "handles"), explode=(0, 0, 900))]),
            "lower the retort onto the bricks", "Two people by the U-bolt handles; turn it so its slot faces the drum's probe hole",
            dict(elev=20, azim=-55)),
        7: (lambda: ([part("Outer lid, cut", "lid")], [part("Collar, tabs riveted to the lid", "collar", explode=(0, 0, 150)),
                                                      part("Burner throat, four rivets", "throat", explode=(0, 0, 450))]),
            "collar and throat onto the lid", "Rivet the collar's tabs; stand the throat in the collar on the lid; rivet",
            dict(elev=25, azim=-55)),
        8: (lambda: ([part("Lid, collar and throat", ("lid", "collar", "throat"))],
                     [part("Air shroud", "shroud", explode=(0, 0, 400)), part("Band damper", "band", explode=(0, 0, 250))]),
            "air shroud and band onto the throat", "Shroud 40 mm above the lid; rivet its six tabs to the throat; band on, wing screw",
            dict(elev=20, azim=-55)),
        9: (lambda: ([part("Lid unit", ("lid", "collar", "throat", "shroud", "band"))], [part("Lid blanket", "lblanket", explode=(0, 0, 350))]),
            "lid blanket onto the lid", "Ceramic fibre disc with a 280 mm hole, kept clear of the shroud; skirt over the rim; wired on",
            dict(elev=25, azim=-55)),
        10: (lambda: (kiln_open, [part("Lid unit with its blanket", ("lid", "collar", "throat", "shroud", "band", "lblanket"), explode=(0, 0, 600))]),
             "lid unit onto the drum", "Gasket clean; close the locking ring", dict(elev=18, azim=-55)),
        11: (lambda: (jk, [part("Tap", "tap", explode=(250, 0, 0)), part("Loose lid", "jlid", explode=(0, 0, 250)),
                           part("Vent nipple", "vent", explode=(0, 0, 450))]),
             "tap, loose lid and vent onto the jacket", "Tap on PTFE tape; lid loose on the rim; vent nipple and two locknuts",
             dict(elev=20, azim=-55)),
        12: (lambda: (jk + [g("Tap"), g("Jacket lid and vent nipple")], [part("Jacket blanket", "jblanket", explode=(-450, 0, 0))]),
             "wrap the jacket blanket", "Mineral wool from 60 mm above the bottom to the rim, slit round the fins; wired on",
             dict(elev=15, azim=-55)),
        13: (lambda: (jk + [g("Tap"), g("Jacket lid and vent nipple"), g("Jacket blanket")],
                      [part("Legs", "tri_leg", explode=(0, 0, -300))]),
             "legs onto the fins", "Jacket upside down on a padded stand is easiest; two M10 bolts per leg, tight",
             dict(elev=15, azim=-55)),
        14: (lambda: (jk + [g("Tap"), g("Jacket lid and vent nipple"), g("Jacket blanket"), g("Tripod legs (3)")],
                      [part("Foot cleats and pads", ("tri_cleat", "tri_pad"), explode=(0, 0, -250))]),
             "foot cleats and pads onto the legs", "Pads screwed to the cleats first; one M10 pin bolt per foot, snug",
             dict(elev=15, azim=-55)),
        15: (lambda: (kiln + [aid_part("Lifting aid post", AID_POST, 270.0), aid_part("Arm turned over the kiln", AID_ARM, 270.0)],
                      [part("Heat-recovery unit, drained", ("jacket", "fins", "tap", "jlid", "vent", "jblanket", "tri_leg", "tri_cleat", "tri_pad"),
                            explode=(0, 0, P["LIFT"])),
                       Part("Lift bar", m.lift_bar(), COL["bar"], None, (0, 0, P["LIFT"]), 1.0)]),
             "heat-recovery unit over the kiln", "Winch it up, swing the arm over the kiln, lower until the sleeve slides over the throat",
             dict(elev=12, azim=-35)),
        16: (lambda: ([part("Flue pipe", "flue")], [part("Stop clips", "clips", explode=(0, -250, 0)),
                                                    part("Rain cap legs", "cap_legs", explode=(0, -250, 0)),
                                                    part("Rain cap", "cap", explode=(0, 0, 250))]),
             "clips and rain cap onto the flue", "Rivet the clips 50 mm up from the foot, the legs at the top; cap riveted on the legs",
             dict(elev=18, azim=-55)),
        17: (lambda: ([part("Flue with clips and cap", ("flue", "clips", "cap_legs", "cap"))],
                      [part("Spiral baffle", "baffle", explode=(0, 0, -700)), part("Hanger rod", "rod", explode=(250, 0, 0))]),
             "hang the baffle in the flue foot", "Strip's hole between the two flue holes; push the rod through all three",
             dict(elev=15, azim=-55)),
        18: (lambda: (full, [part("Flue with baffle and cap", ("flue", "clips", "cap_legs", "cap", "baffle", "rod"), explode=(0, 0, 800))]),
             "flue into the jacket sleeve", "Lower it until the clips rest on the sleeve rim; the baffle goes down inside the sleeve",
             dict(elev=12, azim=-55)),
        19: (lambda: (full + [g(n) for n in flue_all],
                      [part("Logger box, strapped to the leg", "logger", explode=(0, -300, 0)),
                       part("Probes, in through the back", "probes", explode=(0, 400, 0))]),
             "logger and probes", "Seen from the back right. Core probe through the drum hole into the retort; throat probe into the throat",
             dict(elev=15, azim=40)),
    }
    out = []
    for n in sorted(sp):
        if which and n not in which:
            continue
        fn, title, sub, kw = sp[n]
        done, new = fn()
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, label_done=False, **kw))
        print("step", n, flush=True)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    what, nums = args[0], [int(a) for a in args[1:]] or None
    if len(args) > 1 or what in ("overview", "sheets", "joints", "steps"):
        fns = {"overview": lambda: overview(), "sheets": lambda: sheets(nums), "joints": lambda: joints(nums),
               "steps": lambda: steps(nums)}
        if sys.argv[1:]:
            print(what, "->", fns[what]())
        else:
            for w in ("overview", "sheets", "joints", "steps"):
                print(w, "->", fns[w]())
