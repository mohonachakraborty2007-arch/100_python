"""
Cute Weather Cycle Animation
----------------------------
Loops: Sun -> Clouds -> Rain -> Night (moon+stars) -> back to Sun
with smooth cross-fade transitions and a pastel color palette.
Perfect as an aesthetic Instagram reel background loop.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation, PillowWriter

# ---------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------
HOLD = 28          # frames each stage stays fully visible
FADE = 18          # frames spent cross-fading to the next stage
STAGE_LEN = HOLD + FADE
N_STAGES = 4
TOTAL_FRAMES = STAGE_LEN * N_STAGES
FPS = 20

BG_COLORS = [
    "#FFE9B0",  # sunny - warm pastel peach
    "#DCEAF5",  # cloudy - soft powder blue
    "#AAB8C9",  # rainy - muted blue-grey
    "#2D2B55",  # night - deep pastel indigo
]

STAGE_LABELS = ["sunny", "cloudy", "rainy", "starry night"]

CX, CY = 0, 0.3  # icon center


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*(int(round(c * 255)) for c in rgb))


def blend(c1, c2, t):
    r1, r2 = hex_to_rgb(c1), hex_to_rgb(c2)
    return rgb_to_hex(tuple(a + (b - a) * t for a, b in zip(r1, r2)))


# ---------------------------------------------------------------
# FIGURE SETUP
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

# ground shadow (always present, subtle)
ground = mpatches.Ellipse((CX, -2.1), 2.6, 0.35, color="#000000", alpha=0.08, zorder=1)
ax.add_patch(ground)

# ---------------------------------------------------------------
# SUN
# ---------------------------------------------------------------
sun_artists = []
for r, c, a in [(1.35, "#FFE9B0", 0.20), (1.05, "#FFDD8A", 0.30)]:
    glow = mpatches.Circle((CX, CY), r, color=c, alpha=a, zorder=2)
    ax.add_patch(glow)
    sun_artists.append(glow)

for ang in np.linspace(0, 2 * np.pi, 10, endpoint=False):
    x0, y0 = CX + 0.72 * np.cos(ang), CY + 0.72 * np.sin(ang)
    x1, y1 = CX + 1.0 * np.cos(ang), CY + 1.0 * np.sin(ang)
    ray, = ax.plot([x0, x1], [y0, y1], color="#FFC857", lw=4, solid_capstyle="round", zorder=2)
    sun_artists.append(ray)

sun_body = mpatches.Circle((CX, CY), 0.62, color="#FFCF5C", zorder=3)
ax.add_patch(sun_body)
sun_artists.append(sun_body)

sun_face_l = mpatches.Circle((CX - 0.18, CY + 0.05), 0.05, color="#8A5A2B", zorder=4)
sun_face_r = mpatches.Circle((CX + 0.18, CY + 0.05), 0.05, color="#8A5A2B", zorder=4)
sun_smile = mpatches.Arc((CX, CY - 0.05), 0.3, 0.22, angle=0, theta1=200, theta2=340,
                          color="#8A5A2B", lw=2.5, zorder=4)
ax.add_patch(sun_face_l); ax.add_patch(sun_face_r); ax.add_patch(sun_smile)
sun_artists += [sun_face_l, sun_face_r, sun_smile]

# ---------------------------------------------------------------
# CLOUD (shared shape, reused lighter for "cloudy", darker for "rain")
# ---------------------------------------------------------------
def make_cloud(color, zbase):
    parts = []
    puffs = [(-0.55, -0.05, 0.42), (-0.15, 0.15, 0.55), (0.3, 0.05, 0.48), (0.65, -0.1, 0.35)]
    for dx, dy, r in puffs:
        p = mpatches.Circle((CX + dx, CY + dy), r, color=color, zorder=zbase)
        ax.add_patch(p)
        parts.append(p)
    base = mpatches.FancyBboxPatch((CX - 0.85, CY - 0.28), 1.7, 0.4,
                                    boxstyle="round,pad=0,rounding_size=0.2",
                                    linewidth=0, facecolor=color, zorder=zbase)
    ax.add_patch(base)
    parts.append(base)
    return parts


cloud_artists = make_cloud("#FFFFFF", 3)

rain_cloud_artists = make_cloud("#B0BEC5", 3)
N_DROPS = 7
rain_drop_x0 = np.linspace(-0.9, 0.9, N_DROPS)
rain_drops = []
for x0 in rain_drop_x0:
    d, = ax.plot([], [], color="#6FA8DC", lw=2.5, solid_capstyle="round", zorder=2)
    rain_drops.append(d)
rain_artists = rain_cloud_artists + rain_drops

# ---------------------------------------------------------------
# NIGHT: moon + stars
# ---------------------------------------------------------------
moon_base = mpatches.Circle((CX, CY), 0.55, color="#FFF6D6", zorder=3)
moon_shadow = mpatches.Circle((CX + 0.22, CY + 0.06), 0.5, color="#2D2B55", alpha=0.88, zorder=4)
ax.add_patch(moon_base); ax.add_patch(moon_shadow)

star_positions = [(-1.6, 1.4), (1.5, 1.6), (-1.2, -0.4), (1.7, 0.2), (-0.3, 1.9), (0.9, -1.1)]
star_scatter = ax.scatter(*zip(*star_positions), marker="*",
                           s=[90, 70, 60, 80, 50, 65], color="#FFF6D6", zorder=2)
star_phases = np.random.uniform(0, 2 * np.pi, len(star_positions))

night_artists = [moon_base, moon_shadow]  # star_scatter handled separately

# ---------------------------------------------------------------
# LABEL TEXT
# ---------------------------------------------------------------
label = ax.text(0, -2.55, "", ha="center", va="center", fontsize=17,
                 fontstyle="italic", color="#5A4A3A", zorder=5)

ALL_GROUPS = [sun_artists, cloud_artists, rain_artists, night_artists]


def set_group_alpha(group, alpha):
    for a in group:
        a.set_alpha(alpha)


# ---------------------------------------------------------------
# ANIMATION UPDATE
# ---------------------------------------------------------------
def update(frame):
    stage = (frame // STAGE_LEN) % N_STAGES
    local = frame % STAGE_LEN
    nxt = (stage + 1) % N_STAGES

    if local < HOLD:
        a_cur, a_nxt, t = 1.0, 0.0, 0.0
    else:
        t = (local - HOLD) / FADE
        a_cur, a_nxt = 1.0 - t, t

    for i, grp in enumerate(ALL_GROUPS):
        if i == stage:
            set_group_alpha(grp, a_cur)
        elif i == nxt:
            set_group_alpha(grp, a_nxt)
        else:
            set_group_alpha(grp, 0.0)

    # stars only belong to "night" group visually
    star_alpha_stage = a_cur if stage == 3 else (a_nxt if nxt == 3 else 0.0)
    twinkle = 0.5 + 0.5 * np.sin(frame * 0.15 + star_phases)
    star_scatter.set_alpha(np.clip(star_alpha_stage * twinkle, 0, 1).mean())

    # falling raindrops (continuous motion, only visible via alpha)
    speed = 0.09
    for i, (drop, x0) in enumerate(zip(rain_drops, rain_drop_x0)):
        cycle = 1.4
        y_top = ((CY - 0.35 - speed * frame + i * 0.15) % cycle) - cycle + (CY + 0.1)
        drop.set_data([x0, x0], [y_top, y_top - 0.18])

    # background cross-fade
    bg = blend(BG_COLORS[stage], BG_COLORS[nxt], t)
    fig.set_facecolor(bg)
    ax.set_facecolor(bg)

    # label cross-fade
    label.set_text(STAGE_LABELS[stage] if a_cur >= a_nxt else STAGE_LABELS[nxt])
    label.set_alpha(max(a_cur, a_nxt))

    return []


anim = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=1000 / FPS, blit=False)

anim.save("weather_cycle.gif", writer=PillowWriter(fps=FPS))
print("Saved weather_cycle.gif")