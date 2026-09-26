"""CharCube sizing and first-principles checks (CCB-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv (one row per requirement).

Geometry comes from PARAMS in cad/src/model.py and prices from bom/bom.csv,
so the model, the drawing CCB-DWG-001 and the note agree. Everything here is
a paper estimate for TRL 3; nothing is measured.

v0.2 (DDR-002, 2026-09-25): spiral baffle insert and jacket blanket (item 12),
lid and top band blanket (item 13), R5 relaxed to 5 h (item 14), R9 restated
to 700 °C (item 15).
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, levels  # noqa: E402

L = levels()
SIGMA = 5.670e-8
G = 9.81
T_AMB = 20.0
RHO_STEEL = 7850.0
LATENT = 2.442          # MJ/kg, latent heat of water at 25 °C (HHV to LHV)
EVAP = 2.257            # MJ/kg at 100 °C
CP_W = 4.19             # kJ/kg K, water
CP_GAS = 1.15           # kJ/kg K, flue gas, mean 20 to 600 °C
R_GAS = 347.0           # rho = R_GAS / T(K) for flue gas and air at 1 atm (M about 28.5 g/mol)
out = []


def pr(label, value, unit="", fmt="{:.2f}"):
    s = fmt.format(value) if isinstance(value, (int, float)) else str(value)
    print(f"  {label:58s} {s} {unit}")
    return value


def head(t):
    print(f"\n{t}")


def rho_gas(t_c):
    return R_GAS / (t_c + 273.15)


def channiwala(c, h, o, n, a, s=0.0):
    """HHV in MJ/kg (dry) from ultimate analysis in wt % (Channiwala and Parikh 2002)."""
    return 0.3491 * c + 1.1783 * h + 0.1005 * s - 0.1034 * o - 0.0151 * n - 0.0211 * a


def stoich_air(c_kg, h_kg, o_kg):
    """kg of air for complete combustion of the given element masses."""
    return 11.53 * c_kg + 34.34 * (h_kg - o_kg / 8.0)


def h_outside(ts, emiss=0.9):
    """Combined radiation and natural-convection coefficient, W/m2 K, surface at ts in still air."""
    t1, t2 = ts + 273.15, T_AMB + 273.15
    dt = max(ts - T_AMB, 0.1)
    return emiss * SIGMA * (t1 ** 4 - t2 ** 4) / dt + 1.52 * dt ** (1 / 3)


def surface(t_in, h_in, r_layer, area):
    """Heat loss (W) and outer surface temperature for gas at t_in, inside coefficient h_in,
    a layer of resistance r_layer (m2 K/W) and still-air outside. Solves by bisection."""
    lo, hi = T_AMB + 0.01, t_in
    for _ in range(80):
        ts = (lo + hi) / 2
        q_out = h_outside(ts) * (ts - T_AMB)
        q_in = (t_in - ts) / (1.0 / h_in + r_layer)
        lo, hi = (ts, hi) if q_in > q_out else (lo, ts)
    return q_out * area, ts


# ---------------------------------------------------------------- 1. inputs
head("1. Inputs (assumptions, see note section 1)")
MOIST = 0.12            # wet basis, air-dry feed
RHO_PACK = 120.0        # kg/m3, air-dry bundled straw, stalks, cobs
RHO_LOOSE = 40.0        # kg/m3, loose chopped straw (outside the decided feedstock)
YIELD = {"low": 0.20, "central": 0.28, "high": 0.35}       # char per dry feed
FEED = dict(c=45.0, h=5.8, o=40.4, n=0.8, a=8.0)           # dry wt %, mixed stalks and bundled straw
CHAR_C, CHAR_H, CHAR_N = 55.0, 2.5, 1.0                    # wt %, O by difference after ash
WOOD = dict(c=50.0, h=6.0, o=43.2, n=0.3, a=0.5)
WOOD_MOIST = 0.12
F_PERM = 0.80           # IPCC 2019 medium-temperature (450 to 600 °C) permanence factor
H_MULT_BAFFLE = 3.0     # gas-side convection multiplier of the spiral baffle insert (assumption, DDR-002 item 12)
K_BAFFLE = 4.0          # extra velocity heads lost across the insert (friction and swirl; assumption)
K_WOOL = 0.05           # W/m K, mineral wool on the jacket shell (water side below 100 °C)
CH4_PER_CHAR = 0.024    # kg CH4 per kg char, retort field average (Sparrevik et al. 2015)
GWP_CH4 = 28.0
BATCHES = 250
T_EX = 600.0            # °C, mean gas in the burner throat, for its wall loss only
T_WALL = 600.0          # °C, retort wall during the burn
T_CORE = 450.0          # °C, R3 core target
T_WARM_H = 0.5          # h, light-up until the retort wall is at temperature
DH_PYR = 0.4            # MJ/kg dry, net endothermic heat of pyrolysis (literature range about 0 to 1)
CP_BIO = 1.5            # kJ/kg K, dry biomass and char mean to 500 °C (char taken as 1.0 below)
# scenario settings: effective bed conductivity (W/m K), overall excess air, combustion efficiency
SCEN = {
    "favourable":   dict(k=0.50, lam=1.6, ce=0.95, yld="high"),
    "central":      dict(k=0.35, lam=2.0, ce=0.90, yld="central"),
    "unfavourable": dict(k=0.20, lam=2.4, ce=0.85, yld="low"),
}
for k, v in [("moisture (wet basis)", MOIST), ("packed density kg/m3", RHO_PACK), ("F_perm", F_PERM),
             ("annulus gas °C", 650.0), ("pyrolysis heat MJ/kg dry", DH_PYR)]:
    pr(k, v)

# ---------------------------------------------------------------- 2. batch (R1)
head("2. Retort volume and batch (R1)")
d_ret_i = (P["RET_D"] - 2 * P["RET_T"]) / 1000
v_drum = math.pi / 4 * d_ret_i ** 2 * P["RET_H"] / 1000
v_fill = math.pi / 4 * d_ret_i ** 2 * P["FILL_H"] / 1000
m_ad = v_fill * RHO_PACK
m_dry = m_ad * (1 - MOIST)
m_h2o = m_ad * MOIST
pr("retort geometric volume", v_drum * 1000, "L", "{:.0f}")
pr("fill volume at FILL_H", v_fill * 1000, "L", "{:.0f}")
pr("air-dry feed per batch (packed)", m_ad, "kg", "{:.1f}")
pr("  of which dry matter", m_dry, "kg", "{:.2f}")
pr("  of which water", m_h2o, "kg", "{:.2f}")
pr("loose chopped straw per batch (not the decided feedstock)", v_fill * RHO_LOOSE, "kg", "{:.1f}")
gap = (P["OUT_D"] - 2 * P["OUT_T"] - P["RET_D"]) / 2
pr("annulus gap, outer drum to retort", gap, "mm", "{:.0f}")
pr("clearance, retort lid to outer lid", L["z_lid"] - L["z_ret_top"] - 1.5, "mm", "{:.0f}")

# ---------------------------------------------------------------- 3. fuels and char
head("3. Fuel properties and char (R2)")
hhv_feed = pr("feed HHV, dry (Channiwala-Parikh)", channiwala(**FEED), "MJ/kg")
hhv_feed_ad = pr("feed HHV, air-dry basis", hhv_feed * (1 - MOIST), "MJ/kg")
hhv_wood = channiwala(**WOOD)
lhv_wood_ad = hhv_wood * (1 - WOOD_MOIST) - LATENT * (9 * WOOD["h"] / 100 * (1 - WOOD_MOIST) + WOOD_MOIST)
pr("wood HHV dry / LHV air-dry", f"{hhv_wood:.1f} / {lhv_wood_ad:.1f}", "MJ/kg")
air_wood = stoich_air(*(x / 100 * (1 - WOOD_MOIST) for x in (WOOD["c"], WOOD["h"], WOOD["o"])))
pr("wood stoichiometric air", air_wood, "kg/kg air-dry")


def char_props(y):
    m_char = m_dry * y
    ash = FEED["a"] / 100 * m_dry / m_char * 100
    o = 100 - CHAR_C - CHAR_H - CHAR_N - ash
    return m_char, ash, o, channiwala(CHAR_C, CHAR_H, o, CHAR_N, ash)


for s, y in YIELD.items():
    m_char, ash, o, hhv_c = char_props(y)
    pr(f"char at {y:.0%} yield ({s}): mass, ash %, O %, HHV", f"{m_char:.2f} kg, {ash:.0f} %, {o:.0f} %, {hhv_c:.1f} MJ/kg")
m_char, ash_char, o_char, hhv_char = char_props(YIELD["central"])
c_ret = m_char * CHAR_C / 100 / (m_dry * FEED["c"] / 100)
pr("carbon retained in char (central)", c_ret * 100, "%", "{:.0f}")
if ash_char > 45:
    print("  WARNING: char ash above 45 %, the 55 % carbon assumption is not consistent")

# ---------------------------------------------------------------- 4. charge heating time (R3, R5)
head("4. Heating the charge: conduction time (R3, R5)")
R_c = d_ret_i / 2
H_half = P["FILL_H"] / 2000
rho_bed_dry = m_dry / v_fill
c_eff = CP_BIO + (m_h2o / m_dry * EVAP * 1000 + DH_PYR * 1000) / (T_WALL - T_AMB)   # kJ/kg K per kg dry
pr("bed dry density", rho_bed_dry, "kg/m3", "{:.0f}")
pr("effective heat capacity incl. drying and pyrolysis", c_eff, "kJ/kg K")
theta = (T_WALL - T_CORE) / (T_WALL - T_AMB)
# one-term product solution: infinite cylinder (Bi large) x plane wall of half-height H_half
A_c, z_c = 1.602, 2.405
A_p, z_p = 1.273, math.pi / 2
s_needed = math.log(A_c * A_p / theta) / (z_c ** 2 / R_c ** 2 + z_p ** 2 / H_half ** 2)
pr("core temperature ratio at 450 °C", theta, "")
TIMES = {}
for name, sc in SCEN.items():
    alpha = sc["k"] / (rho_bed_dry * c_eff * 1000)
    t_core = s_needed / alpha / 3600
    t_b = T_WARM_H + t_core + 0.5
    TIMES[name] = t_b
    pr(f"{name}: k_eff {sc['k']} W/m K, core to 450 °C / light to end of burn", f"{t_core:.1f} h / {t_b:.1f} h")

# ---------------------------------------------------------------- 5. shell losses
head("5. Shell heat loss during the burn")
T_ANN = 650.0           # °C, annulus gas
ro = P["OUT_D"] / 2000
h_ann = 25.0            # W/m2 K, annulus flame to drum wall (convection plus radiation)
K_BLANKET = 0.09        # W/m K, ceramic fibre 128 kg/m3 at a mean of about 350 °C
ins_h = (P["OUT_H"] - P["INS_BOTTOM"] - P["INS_TOP_GAP"]) / 1000
a_ins = math.pi * (P["OUT_D"] / 1000 + 2 * P["INS_T"] / 1000) * ins_h
a_bot = math.pi * P["OUT_D"] / 1000 * P["INS_BOTTOM"] / 1000
a_top = math.pi * P["OUT_D"] / 1000 * P["INS_TOP_GAP"] / 1000 + math.pi * (ro + 0.006) ** 2
a_thr = math.pi * P["FLUE_D"] / 1000 * P["THROAT_H"] / 1000
q_ins, ts_ins = surface(T_ANN, h_ann, P["INS_T"] / 1000 / K_BLANKET, a_ins)
q_bot, ts_bot = surface(350.0, 15.0, 0.0, a_bot)            # port band, cooled by incoming air
R_LID = P["LID_INS_T"] / 1000 / K_BLANKET
a_lid_bare = math.pi * (((P["SHROUD_D"] / 2 + 25) / 1000) ** 2 - (P["FLUE_D"] / 2000) ** 2)   # left clear under the shroud
q_top_bare, ts_top_bare = surface(T_ANN, 15.0, 0.0, a_top)  # lid and top band bare (v0.1 design)
q_t1, ts_top = surface(T_ANN, 15.0, R_LID, a_top - a_lid_bare)   # lid blanket (DDR-002 item 13)
q_t2, ts_under = surface(T_ANN, 15.0, 0.0, a_lid_bare)
q_top = q_t1 + q_t2
q_thr, ts_thr = surface(T_EX, 12.0, 0.0, a_thr)             # bare throat
q_ins_bare, ts_bare = surface(T_ANN, h_ann, 0.0, a_ins)     # the same band without the blanket
P_SHELL = q_ins + q_bot + q_top + q_thr
for lab, q, ts, a in [("insulated side", q_ins, ts_ins, a_ins), ("port band (bare)", q_bot, ts_bot, a_bot),
                      ("lid and top band (blanketed)", q_t1, ts_top, a_top - a_lid_bare),
                      ("lid under the shroud (bare)", q_t2, ts_under, a_lid_bare), ("burner throat (bare)", q_thr, ts_thr, a_thr)]:
    pr(f"{lab}: area, surface °C, loss", f"{a:.2f} m2, {ts:.0f} °C, {q / 1000:.2f} kW")
pr("total shell loss while burning", P_SHELL / 1000, "kW")
pr("side band without blanket: surface °C, loss", f"{ts_bare:.0f} °C, {q_ins_bare / 1000:.1f} kW")
pr("lid and top band if left bare (v0.1): surface °C, loss", f"{ts_top_bare:.0f} °C, {q_top_bare / 1000:.2f} kW")
pr("saving from the lid blanket", (q_top_bare - q_top) / 1000, "kW")
P_SHELL_V01 = P_SHELL - q_top + q_top_bare

# ---------------------------------------------------------------- 6. masses (R11) and stored heat
head("6. Masses (R11) and heat stored in the structure")
def cyl_area(d, h):
    return math.pi * d * h


def disc(d, d_hole=0.0):
    return math.pi / 4 * (d ** 2 - d_hole ** 2)


mm = 1e-3
m_outer = RHO_STEEL * P["OUT_T"] * mm * (cyl_area(P["OUT_D"] * mm, P["OUT_H"] * mm) + disc(P["OUT_D"] * mm)) + 2.0  # hoops and locking ring
m_lid = RHO_STEEL * P["LID_T"] * mm * (disc((P["OUT_D"] + 12) * mm) + cyl_area(P["FLUE_D"] * mm, P["COLLAR_H"] * mm))
m_ret = RHO_STEEL * P["RET_T"] * mm * (cyl_area(P["RET_D"] * mm, P["RET_H"] * mm) + disc(P["RET_D"] * mm)) \
    + RHO_STEEL * 1.2 * mm * disc((P["RET_D"] + 20) * mm) + 0.8                                                  # lid and bolt ring
m_thr = RHO_STEEL * P["FLUE_T"] * mm * cyl_area(P["FLUE_D"] * mm, P["THROAT_H"] * mm)
m_shr = RHO_STEEL * 1.5 * mm * (cyl_area(P["SHROUD_D"] * mm, P["SHROUD_H"] * mm) + disc(P["SHROUD_D"] * mm, P["FLUE_D"] * mm)
                                 + cyl_area(P["SHROUD_D"] * mm, 0.04))
m_bricks = 3 * 0.114 * 0.064 * P["STANDOFF"] * mm * 2000
m_blanket = 128 * a_ins * P["INS_T"] * mm
m_lidins = 128 * (a_top - a_lid_bare) * P["LID_INS_T"] * mm + 0.1                     # plus wire
d_bore0 = (P["SLEEVE_D"] - 2 * P["SLEEVE_T"]) * mm
m_baffle = RHO_STEEL * P["BAFFLE_T"] * mm * P["BAFFLE_W"] * mm * (P["JKT_H"] - 10) * mm + RHO_STEEL * 1e-4 * P["FLUE_D"] * mm
m_jins = 100 * cyl_area((P["JKT_D"] + P["JKT_INS_T"]) * mm, (P["JKT_H"] - 60) * mm) * P["JKT_INS_T"] * mm + 0.3   # rock wool, wire
m_jkt = RHO_STEEL * (P["JKT_T"] * mm * (cyl_area(P["JKT_D"] * mm, P["JKT_H"] * mm) + disc(P["JKT_D"] * mm, P["SLEEVE_D"] * mm))
                     + P["SLEEVE_T"] * mm * cyl_area(P["SLEEVE_D"] * mm, (P["JKT_H"] + 2 * P["SOCKET"]) * mm)
                     + 1.0 * mm * disc((P["JKT_D"] + 10) * mm, P["SLEEVE_D"] * mm)) + 0.3                         # loose lid, vent
m_tap = 0.6
m_flue = RHO_STEEL * P["FLUE_T"] * mm * cyl_area(P["FLUE_D"] * mm, (P["FLUE_ABOVE"] + P["SOCKET"]) * mm) + 1.0      # cap
rseat = (P["JKT_D"] / 2 + 12) * mm
leg = math.hypot(P["FOOT_R"] * mm - rseat, (L["z_jkt"] - 12) * mm)
m_tripod = 3 * leg * 2.42 + 2 * math.pi * rseat * 1.88 + 3 * 0.4                                                   # 40x40x4 angle, 40x6 flat ring, feet
m_unit = m_jkt + m_tap + m_flue + m_tripod + m_baffle + m_jins
v_water = math.pi / 4 * ((P["JKT_D"] - 2 * P["JKT_T"]) ** 2 - P["SLEEVE_D"] ** 2) * mm ** 2 * P["WATER_H"] * mm
m_water = v_water * 1000
for lab, m in [("outer drum with hoops and ring", m_outer), ("outer lid with collar", m_lid), ("retort with lid", m_ret),
               ("burner throat", m_thr), ("air shroud and damper", m_shr), ("firebricks (3)", m_bricks),
               ("blanket", m_blanket), ("lid and top band blanket", m_lidins), ("water jacket, empty", m_jkt),
               ("spiral baffle insert", m_baffle), ("jacket shell blanket", m_jins), ("flue with cap", m_flue),
               ("tripod", m_tripod), ("tap", m_tap)]:
    pr(lab, m, "kg", "{:.1f}")
m_total = m_outer + m_lid + m_ret + m_thr + m_shr + m_bricks + m_blanket + m_lidins + m_unit + 1.5   # logger, hardware
pr("kiln total without plinth and water", m_total, "kg", "{:.0f}")
pr("water in jacket at WATER_H", v_water * 1000, "L", "{:.1f}")
pr("jacket full", m_jkt + m_water, "kg", "{:.0f}")
pr("heat-recovery unit (tripod, drained jacket, flue, tap)", m_unit, "kg", "{:.1f}")
pr("  per person with two people", m_unit / 2, "kg", "{:.1f}")
m_ret_full = m_ret + m_char
pr("retort with char, one person", m_ret_full, "kg", "{:.1f}")
# stored heat at the end of the burn, MJ
q_struct = (m_outer * 0.5 * (450 - T_AMB) + (m_lid + m_thr + m_shr) * 0.5 * (450 - T_AMB)
            + m_bricks * 0.9 * (500 - T_AMB) + (m_blanket + m_lidins) * 1.0 * (330 - T_AMB)) / 1000
pr("heat stored in drum, lid, throat, bricks and blanket", q_struct, "MJ", "{:.1f}")
# tripod leg buckling, pinned-pinned, 40x40x4 angle
A_ang, r_min = 308e-6, 7.8e-3
slender = leg / r_min
p_cr = math.pi ** 2 * 210e9 * A_ang * r_min ** 2 / leg ** 2
cos_leg = (L["z_jkt"] - 12) * mm / leg
p_leg = (m_jkt + m_water + m_flue + m_tap + m_baffle + m_jins + 2 * math.pi * rseat * 1.88) * G / 3 / cos_leg
pr("tripod leg: length, slenderness", f"{leg:.2f} m, {slender:.0f}")
pr("tripod leg: load full / Euler load / factor", f"{p_leg:.0f} N / {p_cr / 1000:.1f} kN / {p_cr / p_leg:.0f}")

# ---------------------------------------------------------------- 7. energy balance and start-up wood (R8)
head("7. Energy balance per batch and start-up wood (R8)")
SEC = 0.40              # share of the overall air that enters as secondary air at the throat
F_THROAT = 0.15         # share of the volatiles that burns in the throat rather than the annulus
RES = {}
for name, sc in SCEN.items():
    y = YIELD[sc["yld"]]
    mc, ashc, oc, hhvc = char_props(y)
    c_v = m_dry * FEED["c"] / 100 - mc * CHAR_C / 100
    h_v = m_dry * FEED["h"] / 100 - mc * CHAR_H / 100
    o_v = m_dry * FEED["o"] / 100 - mc * oc / 100
    hhv_v = m_dry * hhv_feed - mc * hhvc
    lhv_v = hhv_v - LATENT * (9 * h_v + m_h2o)
    air_v = stoich_air(c_v, h_v, o_v)
    lam_p = (1 - SEC) * sc["lam"]
    gas_v = lam_p * air_v + (m_dry - mc) + m_h2o          # annulus gas from the volatiles, primary air only
    gas_w = lam_p * air_wood + 1.0                        # per kg of wood
    t_b = TIMES[name]
    q_ret = (m_dry * CP_BIO * (500 - T_AMB) + m_h2o * (CP_W * 80 + EVAP * 1000) + DH_PYR * 1000 * m_dry
             + m_ret * 0.5 * (550 - T_AMB)) / 1000
    q_shell_body = (P_SHELL - q_thr) * t_b * 3600 / 1e6
    h_ann_gas = CP_GAS * (T_ANN - T_AMB) / 1000           # MJ/kg of annulus gas leaving at T_ANN
    need = q_ret + q_struct + q_shell_body + gas_v * h_ann_gas - sc["ce"] * (1 - F_THROAT) * lhv_v
    per_kg_w = sc["ce"] * lhv_wood_ad - gas_w * h_ann_gas
    m_wood_bal = max(need / per_kg_w, 0.0)
    # minimum wood for light-up only: warm the steel, bricks and outer half of the charge, 35 % of wood heat retained
    q_warm = ((m_ret + m_outer + m_lid + m_thr) * 0.5 * 280 + m_bricks * 0.9 * 280 + (m_blanket + m_lidins) * 150
              + m_dry / 2 * CP_BIO * 130 + m_h2o / 2 * (CP_W * 80 + EVAP * 1000)) / 1000
    m_wood_min = q_warm / (0.35 * lhv_wood_ad)
    m_wood = max(m_wood_bal, m_wood_min)
    m_prim = gas_v + gas_w * m_wood
    m_sec = SEC * sc["lam"] * (air_v + air_wood * m_wood)
    m_gas = m_prim + m_sec
    # throat: mix secondary air (preheated to 200 °C by the throat wall), burn the rest, lose heat through the wall
    e_thr = (m_prim * h_ann_gas + sc["ce"] * F_THROAT * lhv_v
             - q_thr * t_b * 3600 / 1e6)
    t_ex = T_AMB + e_thr / (m_gas * CP_GAS / 1000)
    released = sc["ce"] * (lhv_v + lhv_wood_ad * m_wood)
    RES[name] = dict(y=y, m_char=mc, t_b=t_b, lhv_v=lhv_v, q_ret=q_ret, q_shell=q_shell_body + q_thr * t_b * 3600 / 1e6,
                     m_wood=m_wood, m_wood_min=m_wood_min, m_gas=m_gas, released=released, air_v=air_v, lam=sc["lam"],
                     vol_mass=m_dry - mc + m_h2o, q_char=mc * hhvc, t_ex=t_ex, q_flue=e_thr)
    print(f"  [{name}] yield {y:.0%}, char {mc:.2f} kg, burn {t_b:.1f} h, lambda {sc['lam']} (primary {lam_p:.2f})")
    pr("    volatiles LHV (if all burned)", lhv_v, "MJ", "{:.0f}")
    pr("    energy left in the char", mc * hhvc, "MJ", "{:.0f}")
    pr("    sinks: retort charge and steel / structure / shell", f"{q_ret:.0f} / {q_struct:.0f} / {RES[name]['q_shell']:.0f} MJ")
    pr("    wood needed to hold the annulus at 650 °C (light-up minimum)", f"{m_wood:.1f} kg ({m_wood_min:.1f} kg)")
    pr("    heat released in the kiln", released, "MJ", "{:.0f}")
    pr("    flue gas mass per batch", m_gas, "kg", "{:.0f}")
    pr("    gas leaving the throat (jacket inlet), mean", t_ex, "°C", "{:.0f}")
    pr("    flue gas heat above 20 °C at the jacket inlet", e_thr, "MJ", "{:.0f}")
C = RES["central"]

# ---------------------------------------------------------------- 8. gas flow, draft and holes (R4)
head("8. Gas flow, draft, gas holes, primary and secondary air (R4)")
t_pyro = C["t_b"] - T_WARM_H - 0.5
PEAK = 2.0
m_vol_peak = C["vol_mass"] / (t_pyro * 3600) * PEAK
pr("volatiles release: mean over pyrolysis, peak (x2)", f"{m_vol_peak / PEAK * 1000:.2f} / {m_vol_peak * 1000:.2f} g/s")
rho_v = 101325 * 0.025 / (8.314 * (400 + 273.15))
a_gh = P["N_GAS_HOLES"] * math.pi / 4 * (P["GAS_HOLE_D"] / 1000) ** 2
v_gh = m_vol_peak / rho_v / a_gh
dp_gh = 0.5 * rho_v * (v_gh / 0.6) ** 2
pr("gas holes: area / velocity / pressure drop at peak", f"{a_gh * 1e4:.1f} cm2 / {v_gh:.1f} m/s / {dp_gh:.1f} Pa")
m_gas_mean = C["m_gas"] / (C["t_b"] * 3600)
m_gas_peak = m_gas_mean * PEAK
pr("flue gas: mean, peak", f"{m_gas_mean * 1000:.1f} / {m_gas_peak * 1000:.1f} g/s")
# jacket (computed in section 9) sets the flue temperatures; use the central outlet temperature here
d_bore = (P["SLEEVE_D"] - 2 * P["SLEEVE_T"]) / 1000
a_bore = math.pi / 4 * d_bore ** 2
d_flue_i = (P["FLUE_D"] - 2 * P["FLUE_T"]) / 1000
a_flue = math.pi / 4 * d_flue_i ** 2
MU_G = 3.6e-5
K_G = 0.058


def jacket_rate(m_dot, t_in, t_w, h_mult=H_MULT_BAFFLE):
    """Heat to water (W) and gas outlet temperature for mean flow m_dot through the jacket sleeve."""
    re = 4 * m_dot / (math.pi * d_bore * MU_G)
    f = (0.79 * math.log(re) - 1.64) ** -2
    nu = max(3.66, (f / 8) * (re - 1000) * 0.7 / (1 + 12.7 * math.sqrt(f / 8) * (0.7 ** (2 / 3) - 1)))
    h_c = nu * K_G / d_bore * h_mult
    tg = t_in - 60
    h_r = 0.08 * SIGMA * ((tg + 273.15) ** 4 - (t_w + 273.15) ** 4) / (tg - t_w)
    ua = (h_c + h_r) * math.pi * d_bore * P["JKT_H"] / 1000
    ntu = ua / (m_dot * CP_GAS * 1000)
    eff = 1 - math.exp(-ntu)
    q = eff * m_dot * CP_GAS * 1000 * (t_in - t_w)
    return q, t_in - q / (m_dot * CP_GAS * 1000), re, h_c, h_r, ua, eff


q_j, t_j_out, *_ = jacket_rate(m_gas_mean, C["t_ex"], 60.0)
segs = [(L["z_ports"], L["z_lid"], T_ANN), (L["z_thr"], L["z_jkt"], C["t_ex"]),
        (L["z_jkt"], L["z_jtop"], (C["t_ex"] + t_j_out) / 2), (L["z_jtop"], L["z_out"], t_j_out - 20)]
rho_a = rho_gas(T_AMB)
draft = sum(G * (b - a) / 1000 * (rho_a - rho_gas(t)) for a, b, t in segs)
pr("stack height, air ports to flue outlet", (L["z_out"] - L["z_ports"]) / 1000, "m")
pr("available draft (central temperatures)", draft, "Pa", "{:.1f}")
# losses at peak flow
rho_thr = rho_gas(C["t_ex"])
v_thr = m_gas_peak / rho_thr / a_flue
k_sum = 0.5 + 0.045 * (P["THROAT_H"] + P["JKT_H"] + P["FLUE_ABOVE"]) / 1000 / d_flue_i + 1.0 + 1.0 + 1.0 + K_BAFFLE   # entry, friction, air mixing, exit, cap, baffle
dp_flow = k_sum * 0.5 * rho_thr * v_thr ** 2
a_ports = P["N_PORTS"] * P["PORT_W"] * P["PORT_H"] * 1e-6
m_air_peak = m_gas_peak * 0.6 * C["lam"] / (C["lam"] + 0.1)
v_port = m_air_peak / rho_a / a_ports
dp_port = 1.5 * 0.5 * rho_a * v_port ** 2
pr("throat gas velocity at peak", v_thr, "m/s")
pr("flow losses at peak: flue path / primary ports", f"{dp_flow:.1f} / {dp_port:.2f} Pa")
pr("draft margin at peak (draft / losses)", draft / (dp_flow + dp_port + dp_gh), "", "{:.1f}")
pr("flue gas velocity above the jacket, mean", m_gas_mean / rho_gas(t_j_out) / a_flue, "m/s")
# secondary air: SEC of the overall air enters through the throat holes, preheated to 200 °C
m_sec_peak = SEC * C["lam"] * C["air_v"] / (t_pyro * 3600) * PEAK
z_holes = L["z_thr"] + P["SHROUD_Z"] + 75
above = [(max(a, z_holes), b, t) for a, b, t in segs if b > z_holes]
draft_above = sum(G * (b - a) / 1000 * (rho_a - rho_gas(t)) for a, b, t in above)
dp_down = (1.0 + 1.0 + K_BAFFLE + 0.045 * (L["z_out"] - z_holes) / 1000 / d_flue_i) * 0.5 * rho_thr * v_thr ** 2
dp_sec = draft_above - dp_down
rho_sec = rho_gas(200.0)
v_hole = 0.62 * math.sqrt(2 * dp_sec / rho_sec)
a_sec_need = m_sec_peak / rho_sec / v_hole
a_sec = P["N_AIR_HOLES"] * math.pi / 4 * (P["AIR_HOLE_D"] / 1000) ** 2
pr("secondary air at peak (40 % of air)", m_sec_peak * 1000, "g/s")
pr("suction at the air holes at peak", dp_sec, "Pa", "{:.1f}")
pr("secondary hole area needed / provided", f"{a_sec_need * 1e4:.1f} / {a_sec * 1e4:.1f} cm2 ({P['N_AIR_HOLES']} x {P['AIR_HOLE_D']:.0f} mm)")
pitch = math.pi * P["FLUE_D"] / (P["N_AIR_HOLES"] / P["AIR_RINGS"])
pr("hole pitch around the throat, per ring", pitch, "mm", "{:.0f}")
v_ring25 = m_sec_peak / rho_a / (math.pi / 4 * 0.027 ** 2)
pr("TRL 2 25 mm inlet pipe: velocity / loss (rejected)", f"{v_ring25:.1f} m/s / {1.5 * 0.5 * rho_a * v_ring25 ** 2:.0f} Pa")
a_shroud = math.pi / 4 * ((P["SHROUD_D"] - 3) ** 2 - P["FLUE_D"] ** 2) * 1e-6
pr("shroud intake gap area / velocity at peak", f"{a_shroud * 1e4:.0f} cm2 / {m_sec_peak / rho_a / a_shroud:.2f} m/s")

# ---------------------------------------------------------------- 9. hot water (R6, R7)
head("9. Water jacket (R6, R7)")
a_jkt_out = cyl_area(P["JKT_D"] / 1000, P["JKT_H"] / 1000) + disc(P["JKT_D"] / 1000)
cap = m_water * CP_W * (100 - T_AMB) / 1000


R_JINS = P["JKT_INS_T"] / 1000 / K_WOOL


def water_heat(r, h_mult=H_MULT_BAFFLE, r_jkt=R_JINS):
    """Net heat to water per batch (MJ). h_mult scales gas-side convection (flue insert);
    r_jkt is an insulation resistance on the jacket shell (m2 K/W). Iterates on the mean water temperature."""
    md = r["m_gas"] / (r["t_b"] * 3600)
    tw, net = 40.0, 0.0
    for _ in range(30):
        q, tout, re, hc, hr, ua, eff = jacket_rate(md, r["t_ex"], tw, h_mult)
        loss = (tw - T_AMB) / (1 / h_outside(tw) + r_jkt) * a_jkt_out
        net = (q - loss) * r["t_b"] * 3600 / 1e6
        tw = T_AMB + min(net, cap) * 1000 / (m_water * CP_W) / 2
    return net, q, loss, tout, re, hc, hr, ua, eff, tw


for name, r in RES.items():
    net, q, loss, tout, re, hc, hr, ua, eff, tw = water_heat(r)
    r["q_water"] = min(net, cap)
    r["boils"] = net > cap
    print(f"  [{name}] Re {re:.0f}, h_conv {hc:.1f}, h_rad {hr:.1f} W/m2 K, UA {ua:.2f} W/K, effectiveness {eff:.2f}")
    pr("    heat to water rate / jacket shell loss (mean water °C)", f"{q / 1000:.2f} / {loss / 1000:.2f} kW ({tw:.0f} °C)")
    pr("    net heat to water per batch", net, "MJ", "{:.1f}")
    pr("    gas leaving the jacket", tout, "°C", "{:.0f}")
pr("heat to bring the water from 20 °C to boiling", cap, "MJ", "{:.1f}")
pr("central temperature rise of the water", RES["central"]["q_water"] * 1000 / (m_water * CP_W), "K", "{:.0f}")
pr("TRL 2 estimate for comparison (U 15 W/m2 K assumed)", "about 15 MJ")
pr("scenarios where the water reaches boiling", ", ".join(k for k, r in RES.items() if r["boils"]) or "none")
print("  comparison, central case (flue temperatures as the design):")
for lab, hm, rj in [("plain sleeve, bare jacket (v0.1 design)", 1.0, 0.0), ("jacket blanket only", 1.0, R_JINS),
                    ("baffle insert only (h_conv x 3)", H_MULT_BAFFLE, 0.0), ("both (design, DDR-002 item 12)", H_MULT_BAFFLE, R_JINS)]:
    net = water_heat(RES["central"], hm, rj)[0]
    pr(f"    {lab}", net, "MJ", "{:.1f}")
pr("sleeve wall temperature (water side 20 to 100 °C)", "below tar dew point: tar and soot will deposit")
pr("flue gas water dew point (about 8 % H2O by volume)", "about 41 °C: condensate while the water is cold")
pr("vent pipe bore / open area", "24 mm / always open (R7)")

# cooling after the burn (R5, second part)
head("9a. Sealed cooling (R5)")
c_kiln = (m_char * 1.0 + m_ret * 0.5 + m_outer * 0.5 + m_bricks * 0.9 + (m_lid + m_thr + m_shr) * 0.5 + (m_blanket + m_lidins) * 1.0) * 1000
ua_cool = ((a_ins + a_top - a_lid_bare) / (P["INS_T"] / 1000 / K_BLANKET + 1 / 10.0) + (a_lid_bare + a_bot + a_thr) * 12.0)
tau = c_kiln / ua_cool / 3600
t_lump = tau * math.log((500 - T_AMB) / (60 - T_AMB))
rho_char_bed = m_char / (v_fill * 0.6)
alpha_c = 0.15 / (rho_char_bed * 1000)
s_c = math.log(A_c * A_p / ((60 - T_AMB) / (500 - T_AMB))) / (z_c ** 2 / R_c ** 2 + z_p ** 2 / (H_half * 0.6) ** 2)
t_cond = s_c / alpha_c / 3600
pr("heat capacity of kiln and char / shell UA", f"{c_kiln / 1000:.0f} kJ/K / {ua_cool:.1f} W/K")
pr("time constant / shell to 60 °C (lumped)", f"{tau:.1f} h / {t_lump:.1f} h")
pr("char core to 60 °C by conduction (bed k 0.15 W/m K)", t_cond, "h", "{:.1f}")
t_cool = t_lump + t_cond
pr("cooling estimate (sum, conservative)", t_cool, "h", "{:.1f}")
pr("light to unload, central", C["t_b"] + t_cool, "h", "{:.1f}")

# ---------------------------------------------------------------- 10. carbon
head("10. Carbon per batch and per year")
for name, r in RES.items():
    c_store = r["m_char"] * CHAR_C / 100 * F_PERM
    co2 = c_store * 44 / 12
    ch4 = r["m_char"] * CH4_PER_CHAR * GWP_CH4
    r.update(co2=co2, ch4=ch4, net=co2 - ch4)
    pr(f"[{name}] C stored 100 yr / CO2 / CH4 penalty / net", f"{c_store:.2f} kg C / {co2:.1f} / {ch4:.1f} / {co2 - ch4:.1f} kg CO2e")
pr("central per year: char / net removal / residue diverted",
   f"{C['m_char'] * BATCHES:.0f} kg / {C['net'] * BATCHES / 1000:.2f} t CO2e / {m_ad * BATCHES / 1000:.1f} t")

head("10a. Energy flow per batch, central (for media/flow.png)")
e_in = m_ad * hhv_feed_ad + C["m_wood"] * lhv_wood_ad
pr("residue (HHV) and wood (LHV) in", e_in, "MJ", "{:.0f}")
pr("kept in the char", C["q_char"], "MJ", "{:.0f}")
pr("latent heat and unburned gas", e_in - C["q_char"] - C["released"], "MJ", "{:.0f}")
pr("heat released in the kiln", C["released"], "MJ", "{:.0f}")
pr("retort charge, structure and shell", C["released"] - C["q_flue"], "MJ", "{:.0f}")
pr("flue gas at the jacket inlet", C["q_flue"], "MJ", "{:.0f}")
pr("hot water", C["q_water"], "MJ", "{:.1f}")
pr("up the stack and jacket shell", C["q_flue"] - C["q_water"], "MJ", "{:.0f}")

# ---------------------------------------------------------------- 11. logger (R9)
head("11. Logger (R9)")
tc_cls1 = max(1.5, 0.004 * 1000)
tc_cls2_700 = max(2.5, 0.0075 * 700)
pr("type K class 2 at 700 °C / class 1 at 700 °C", f"±{tc_cls2_700:.1f} / ±{0.004 * 700:.1f} °C")
pr("RSS with MAX31855 ±2 °C (to 700 °C): class 2 / class 1", f"±{math.hypot(tc_cls2_700, 2):.1f} / ±{math.hypot(0.004 * 700, 2):.1f} °C")
pr("R9 as restated (DDR-002 item 15): ±5 °C to 700 °C, indicative above", "met with class 1 probes")
pr("class 1 at 1,000 °C (amplifier not specified above 700 °C)", f"±{tc_cls1:.1f} °C plus amplifier")
e_log = 0.25 * 24
pr("logger energy for 24 h at 0.25 W / usable bank (10 Ah, 3.7 V, 85 %)", f"{e_log:.0f} / {10 * 3.7 * 0.85:.0f} Wh")
pr("data per 24 h at 10 s, 2 channels, 32 B/row", 8640 * 32 / 1000, "kB", "{:.0f}")

# ---------------------------------------------------------------- 12. cost (R10)
head("12. Cost (R10)")
rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
pr("BOM lines / total", f"{len(rows)} / ${total:.0f}")
BUDGET = next(float(l.split(":")[1].split("#")[0]) for l in (ROOT / "project.yaml").read_text().splitlines()
              if l.startswith("budget_usd:"))   # project.yaml budget_usd, kiln parts only ($320, DDR-002 item 17)
pr("budget_usd / margin", f"${BUDGET:.0f} / ${BUDGET - total:.0f}")
added = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].split()[0] in ("15", "16", "17"))
pr("of which DDR-002 lines 15 to 17", f"${added:.0f}")
galv = [r["item"] for r in rows if "galvanized" in (r["spec"] + r["notes"]).lower() and "not galvanized" not in (r["spec"] + r["notes"]).lower()]
pr("BOM lines calling for galvanized parts", len(galv), "", "{:d}")

# ---------------------------------------------------------------- 13. requirements
head("13. Requirements")
F, U = RES["favourable"], RES["unfavourable"]
rq = [
    ("R1", "Batch of 10 kg or more air-dry residue (packed or bundled feed, decided)", f"{m_ad:.1f} kg packed (loose straw {v_fill * RHO_LOOSE:.1f} kg, excluded)", ">= 10 kg", "met"),
    ("R2", "Biochar 25 % or more of dry feed", f"{C['y']:.0%} ({U['y']:.0%} to {F['y']:.0%}); {C['m_char']:.2f} kg", ">= 25 %", "at risk"),
    ("R3", "Core 450 °C or more for 30 min, logged", f"core at 450 °C {C['t_b'] - 0.5:.1f} h after lighting ({F['t_b'] - 0.5:.1f} to {U['t_b'] - 0.5:.1f} h) if the annulus is held at 650 °C", "450 °C, 30 min", "at risk"),
    ("R4", "Burn the gas; smoke limits; CH4 below 24 g/kg char", f"routing closed by design; draft margin {draft / (dp_flow + dp_port + dp_gh):.1f}; emissions not calculable", "< 24 g/kg", "not verifiable at TRL 3"),
    ("R5", "Light to end of flaming 5 h or less (relaxed, DDR-002); unload within 16 h", f"burn {C['t_b']:.1f} h ({F['t_b']:.1f} to {U['t_b']:.1f} h); unload after about {C['t_b'] + t_cool:.0f} h", "<= 5 h; <= 16 h", "met" if U["t_b"] <= 5 else ("at risk" if C["t_b"] <= 5 else "not met")),
    ("R6", "10 MJ or more into water per batch", f"{C['q_water']:.1f} MJ with baffle insert and jacket blanket ({min(F['q_water'], U['q_water']):.1f} to {max(F['q_water'], U['q_water']):.1f} MJ)", ">= 10 MJ", "met" if min(F['q_water'], U['q_water']) >= 10 else ("at risk" if C['q_water'] >= 10 else "not met")),
    ("R7", "Water circuit open to air, no sealing valve, tap at base, jacket on tripod", "open vent and loose lid; tripod-carried", "by design", "met"),
    ("R8", "5 kg or less of dry wood per batch", f"{C['m_wood']:.1f} kg ({F['m_wood']:.1f} to {U['m_wood']:.1f}); light-up alone {C['m_wood_min']:.1f} kg", "<= 5 kg", "not met" if C["m_wood"] > 5 else ("at risk" if U["m_wood"] > 5 else "met")),
    ("R9", "2 x type K, ±5 °C to 700 °C and indicative to 1,000 °C (restated, DDR-002), 10 s, 24 h on a power bank", f"±{math.hypot(0.004 * 700, 2):.1f} °C to 700 °C with class 1 probes; {e_log:.0f} of {10 * 3.7 * 0.85:.0f} Wh", "±5 °C to 700 °C", "met"),
    ("R10", f"Parts ${BUDGET:.0f} or less (top-up, DDR-002 item 17); safety kit listed separately (decided)", f"${total:.0f} (lines 15 to 17 add ${added:.0f})", f"<= ${BUDGET:.0f}", "met" if total <= BUDGET else "not met"),
    ("R11", "Hand tools, one welded part, no lift above 25 kg per person", f"unit {m_unit:.1f} kg for two ({m_unit / 2:.1f} kg each); retort with char {m_ret_full:.1f} kg", "<= 25 kg", "met" if m_unit / 2 <= 25 and m_ret_full <= 25 else "not met"),
    ("R12", "Outlet 2.5 m or more; 5 m clearance; no galvanized hot parts", f"outlet {L['z_out'] / 1000:.2f} m; {len(galv)} galvanized lines", ">= 2.5 m", "met" if L["z_out"] >= 2500 and not galv else "not met"),
]
for r in rq:
    print(f"  {r[0]:4s} {r[4]:24s} {r[2]}")
counts = {}
for r in rq:
    counts[r[4]] = counts.get(r[4], 0) + 1
print("  counts:", ", ".join(f"{k} {v}" for k, v in counts.items()))
with open(ROOT / "docs/04-calcs/results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "requirement", "value", "target", "status"])
    w.writerows(rq)
print("\nwrote docs/04-calcs/results.csv")
