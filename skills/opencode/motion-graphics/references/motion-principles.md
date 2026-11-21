# Motion principles: the numbers that decide whether it looks professional

Every number here is sourced. Where a number is practitioner convention rather
than an official spec it says so. Use the official numbers first.

---

## 1. Easing

### The one rule that fixes most amateur motion

**Ease-out for entrances. Ease-in for exits. Ease-in-out only for moves that stay
on screen.**

Material Design states the reasoning, and it is the reasoning to follow:

- For entrances, "slow acceleration is unnecessary as focus should be on the final
  resting point." The viewer's attention belongs where the thing *lands*, so be
  fastest on arrival.
- For exits, "slow deceleration is unnecessary as the ending point isn't visible."
  Don't spend frames settling something that's gone.
- For an element returning from a temporary exit, ease-out again.
- Ease-in-out only when the motion is *coupled* to another element's, so neither
  starts nor stops abruptly.

This is the opposite of physical intuition. Val Head notes that animations
following real-world acceleration/deceleration "often feel odd." Screen-native
rules win.

### Named curves with real numbers

CSS `cubic-bezier(x1, y1, x2, y2)` values, with GSAP equivalents:

| Curve | cubic-bezier | GSAP | Use it for |
|---|---|---|---|
| easeOutQuad | `(0.5, 1, 0.89, 1)` | `power1.out` | GSAP's default. Hover, focus, small shifts |
| easeOutCubic | `(0.33, 1, 0.68, 1)` | `power2.out` | Safe general-purpose entrance |
| easeOutQuart | `(0.25, 1, 0.5, 1)` | `power3.out` | Snappy arrivals, short travel |
| easeOutExpo | `(0.16, 1, 0.3, 1)` | `expo.out` | Dramatic "premium" entrance, hero reveals |
| easeOutSine | `(0.61, 1, 0.88, 1)` | `sine.out` | Softest decel, long ambient moves |
| easeOutCirc | `(0, 0.55, 0.45, 1)` | `circ.out` | Strong late deceleration |
| **easeOutBack** | **`(0.34, 1.56, 0.64, 1)`** | `back.out(1.7)` | One overshoot. Tune: 1.4 soft, 2.0 firm, 2.8 cartoony |
| easeInQuad | `(0.11, 0, 0.5, 0)` | `power1.in` | Exits |
| easeInCubic | `(0.32, 0, 0.67, 0)` | `power2.in` | Standard exit |
| easeInExpo | `(0.7, 0, 0.84, 0)` | `expo.in` | Aggressive exit |
| easeInOutCubic | `(0.65, 0.35, 0.35, 1)` | `power2.inOut` | On-screen repositioning, camera moves |
| easeInOutExpo | `(0.87, 0, 0.13, 1)` | `expo.inOut` | Cinematic |

**Elastic and bounce have no `cubic-bezier()` form.** They need multi-keyframe
approximations in CSS, or GSAP: `elastic.out(amplitude, period)` — default
`elastic.out(1, 0.3)`; amplitude is overshoot distance, period is oscillation
spacing (smaller = tighter, more wobbles). `bounce.out` takes no parameters and
its decay is fixed.

CSS keyword defaults, from the spec: `ease` = `(0.25, 0.1, 0.25, 1)`, `ease-in` =
`(0.42, 0, 1, 1)`, `ease-out` = `(0, 0, 0.58, 1)`, `ease-in-out` =
`(0.42, 0, 0.58, 1)`, `linear` = `(0, 0, 1, 1)`.

Material Design's four curves, which are worth memorising because they map
cleanly onto jobs:

| Job | Curve | Value |
|---|---|---|
| Element **entering** | Decelerate | `cubic-bezier(0, 0, 0.2, 1)` |
| Element **permanently leaving** | Accelerate | `cubic-bezier(0.4, 0, 1, 1)` |
| Element **temporarily** leaving | Sharp | `cubic-bezier(0.4, 0, 0.6, 1)` |
| **On-screen move** | Standard | `cubic-bezier(0.4, 0, 0.2, 1)` |

---

## 2. Duration

### Material Design, official numbers

Use these as the backbone; they are the most defensible numbers available.

| Situation | Duration |
|---|---|
| Element entering the screen | **225 ms** |
| Element leaving the screen | **195 ms** |
| Typical mobile transition | **300 ms** |
| Large, complex, full-screen transition | **375 ms** |
| Desktop animations | **150–200 ms** (faster than mobile) |
| Tablet | ~30% longer than mobile |
| Wearable | ~30% shorter than mobile |
| Anything over 400 ms | Feels too slow |

**Duration must scale with distance and size.** "Use longer durations when objects
need to travel large distances or have dramatic changes in surface area. Use
shorter durations when objects travel short distances or have minor changes in
surface area." Larger screens need longer durations because the same pixel
distance is a smaller fraction of the frame.

### Motion-graphics scene timing

This is convention, not spec, but it is what working pieces do:

| Beat | Duration |
|---|---|
| Scene hold, minimum for a text card to be readable | 2.5–3 s |
| Text line entrance | 500–700 ms |
| Exit (accelerate off) | 250–350 ms |
| Transition between scenes | 400–800 ms |
| Logo sting, total | 2–4 s |
| Hero reveal | 500–800 ms |

### Perception thresholds — these are why very short animations read as broken

- Motion is perceived at about **10 fps (one frame per ~100 ms)**. Below that,
  changes read as a jump rather than movement.
- Smooth apparent movement wants 20–30 fps minimum.
- Viewers discriminate transition-length changes of **2–3 frames** for
  start-end transitions and **7–10 frames** for centre-aligned ones. So a 2-frame
  timing change is visible; do not fiddle below that.
- Nielsen's limits: **0.1 s** feels instantaneous, **1.0 s** keeps the flow of
  thought uninterrupted, **10 s** is the limit of attention.

### Which fps

Frame durations: 24fps = 41.7 ms, 25fps = 40 ms, 30fps = 33.3 ms, 60fps = 16.7 ms.

**Default to 30 fps for motion graphics.** Designed motion uses easing, and 30 fps
presents easing cleanly while 60 fps often looks unnaturally smooth for 2D
graphic work. Choose 60 fps when the piece overlays fast continuous motion —
particle streams, rapid tickers, screen recordings, cursor work. It costs
roughly 50% more bitrate at equal resolution and twice the render time.

Use 24 fps only when matching film footage, and be consistent — mixing frame rates
in one timeline is the most common source of visible stutter.

---

## 3. Stagger

Material Design's choreography page gives the one hard number: **begin each
item's staggered entrance no more than 20 ms apart.** It also specifies ordering —
grid items populate left to right, top to bottom.

Practitioner ranges, consistent across sources: **20–50 ms per item**. Above
~100 ms the stagger itself becomes visible and reads as lag. Below 20 ms it is
imperceptible.

**Cap it, or long lists crawl.** The standard fix clamps the multiplier:

```css
animation-delay: calc(min(var(--index), 8) * var(--stagger));
```

so a 3-item and a 300-item list finish at roughly the same time. Keep total added
stagger under ~300 ms and total animation time under ~500 ms.

Order geometrically (top-to-bottom for lists, row-major for grids,
outward-from-origin for menus). Reverse it on exit and tighten the offset to
10–15 ms. Don't stagger elements the viewer is waiting to interact with.

---

## 4. Reading time for on-screen text

These are the best-sourced numbers in the whole discipline, because broadcasters
had to solve the same problem.

**Netflix (English, USA) Timed Text Style Guide:**
- **42 characters per line**
- Reading speed up to **20 cps** adult, **17 cps** children's
- Maximum **two lines**
- Minimum event duration **5/6 s** at 24fps; reserve that for one- or two-word
  cards
- Maximum **7 s** per event
- Minimum **2 frames** between events
- Out-time should be at least **half a second** past the end of the audio

**BBC Subtitle Guidelines:**
- Recommended **160–180 wpm**, i.e. **0.33–0.375 s per word**
- Minimum on-screen time ~**0.3 s per word** (their example: 1.2 s for 4 words)
- Online line length: **68% of the width of a 16:9 video**, 90% for 4:3, 1:1 or
  9:16
- Max 2 lines landscape/square, 3 lines for 9:16
- Minimum **1.5 s gap** between subtitles — shorter is "very jerky"
- Worked scale: short familiar phrase 1.5–2 s; half a line 2–2.5 s; one line
  2.5–3 s; two lines 5–6 s

**Silent reading speed** for context (Brysbaert 2019, meta-analysis): 238 wpm for
English non-fiction, 260 wpm fiction, 183 wpm reading aloud. On-screen captioned
text runs slower than raw reading speed, which is why broadcast limits exist.

**What to do:** for on-screen text, hold **at least 2.5 s for a one-line card**,
cap at **42 characters per line and 2 lines**, and time longer cards at
**~0.3 s per word plus a 0.5 s beat** for the eye to land. Use the tighter of the
two official limits (~17 cps / 160–180 wpm) rather than the looser one.

Line length for body copy: 45–75 characters is the widely accepted range, with 66
often cited as ideal (Bringhurst); WCAG 1.4.8 requires ≤80 characters and 1.5em
line height. On-screen text should be shorter still, because it is read at
distance, in motion, under time pressure.

---

## 5. Safe margins

The "title safe 10% / action safe 5%" figure is the **legacy SD** rule. Current
HD/UHD figures are tighter.

**SMPTE ST 2046-1 and EBU R95:**
- Safe **action** area: **93%** of width and height (3.5% margin per edge)
- Safe **title/graphics** area: **90%** (5% margin per edge)

At 1920×1080 that is a graphics-safe box of **1728×972 px** (96 px left/right,
54 px top/bottom).

**Platform overlays, which is where most social videos actually lose content.**

Meta's official guidance for Reels and Stories: leave roughly **14% of the top,
35% of the bottom, and 6% of each side** free from text, logos and key elements.
On a 1080×1920 frame that is top 269 px, bottom 672 px, sides 65 px — leaving a
950×979 px box. Meta recommends a **1440×2560** master for vertical ads.

YouTube's vertical template is labelled 288 px top, 672 px bottom, 48 px left,
192 px right on 1080×1920, leaving 840×960. *These pixel values sit inside
Google's diagram asset rather than in page text; multiple third parties read the
same numbers off it, but treat them as measured rather than published.*

TikTok publishes **no fixed pixel safe zone** — their own help text says the zone
depends on dimension, caption length, and additional formats, and "the longer a
caption is, the smaller the safe zone will be." Every set of TikTok pixel numbers
in circulation is a third-party measurement, and they disagree widely (top
130–240 px, bottom 484–660 px). Design for a short caption and verify in-app.

**Do this by default:** keep everything important inside **90% of the frame**, and
for 9:16 keep it above the bottom 35% and below the top 14%.

---

## 6. Aspect ratios and export sizes

Primary-source where available:

| Placement | Aspect | Resolution |
|---|---|---|
| YouTube | 16:9 | 1920×1080 (3840×2160, 7680×4320 also listed) |
| Instagram Reels / Stories (ads) | 9:16 | **1440×2560** |
| Facebook Reels (ads) | 9:16 | **1440×2560** |
| Instagram feed | 4:5 | 1080×1350 |
| Square | 1:1 | 1080×1080 |
| TikTok | 9:16 | 1080×1920 (min 540×960) |
| X / Twitter | 16:9 | 1280×720 or 1920×1080 |
| LinkedIn | 1:2.4–2.4:1 | 256×144 min, 4096×2304 max |
| Broadcast | 16:9 | 3840×2160 or 1920×1080 |

YouTube never publishes "9:16 1080×1920" for Shorts in its help pages — it says
"square or vertical" with a 1080p ceiling. The 9:16 figure appears in Google Ads
documentation.

---

## 7. The 12 principles, as controls you actually set

Only some of these apply to motion graphics. Ranked by how much work they do for
you:

**High value — set these every time:**

1. **Slow in / slow out** — this is the easing rule in §1. Replaces constant
   velocity with a curve. Nothing else fixes "amateur" as reliably.
2. **Timing** — duration encodes weight. Small element = short duration, large =
   long. See §2.
3. **Staging** — one focal element gets the biggest move and the longest duration;
   everything else changes opacity only. Give the eye one thing to follow.
4. **Follow through / overlapping action** — parts arrive at different rates.
   Offset followers with a stagger (§3) and give them slightly longer durations
   than the leader.
5. **Anticipation** — a small wind-up before the main move, 4–8 px or scale 0.98,
   so the main action reads as caused.
6. **Exaggeration** — overshoot eases for entrances. Too much and it's annoying.

**Use where the brief calls for character:**

7. **Squash and stretch** — conserve volume: `scale.x` up means `scale.y` down.
   Press feedback defaults: 0.96 subtle, 0.92 default, 0.88 dramatic. Never below
   0.85 (reads as broken) or above 0.98 (imperceptible).
8. **Arc** — natural motion follows curves. Use `motionPath`/`offset-path` rather
   than a straight `translate` for anything organic.
9. **Secondary action** — a supporting beat on the same trigger frame as the
   primary, at lower amplitude.

**Low value here:** straight-ahead action is a production technique, not a
property — you'll use pose-to-pose (keyframe start and end states). Solid drawing
collapses into ordinary visual-consistency work. Appeal is a brand judgement, not
a setting.

---

## 8. A default motion spec you can hand to any piece

When you have no reference and no brand system, use this and state that you did:

```
easing:       power3.out entrances, power2.in exits, power2.inOut on-screen moves
              (cubic-bezier 0.33,1,0.68,1 / 0.32,0,0.67,1 / 0.65,0.35,0.35,1)
entrance:     600 ms
exit:         280 ms
scene hold:   2.5 s minimum per text card
stagger:      30 ms per item, capped at 8 items
overshoot:    back.out(1.4) on primary elements only
fps:          30
safe area:    90% of frame; for 9:16 also clear bottom 35% and top 14%
type:         >=2.5s per line, <=42 chars per line, <=2 lines
```

It is defensible, sourced, and boring in the right way. Deviate when the brief or
a reference video says so — and say that you did.
