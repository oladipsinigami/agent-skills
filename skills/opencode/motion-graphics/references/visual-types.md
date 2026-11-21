# Visual types: structure, pacing, and a default preset for each

Nine types. Each gets: typical structure, pacing, the mistakes that make it look
cheap, and a spec you can start from immediately.

---

## 1. Kinetic typography

Text is the subject. Everything else supports it.

**Structure:** a cold open line, 2–4 beats that build, a landing line that holds.

**Pacing:** Each line 1.5–3 s depending on length. ~0.3 s per word plus a 0.5 s
beat to land. Cap 42 characters per line, 2 lines. Stagger words within a line by
20–30 ms so the eye is led left to right rather than reading a block.

**Common mistakes:**
- Animate the whole line as one object. Split it (GSAP `SplitText` is free since
  3.13) and animate words or characters.
- Centre everything. Left-aligned text with a consistent baseline reads as
  designed; centred text stacked in the middle reads as a slideshow.
- More than two type sizes. Pick a display size and a supporting size.
- Text that animates in and immediately out with no hold. Every line needs a
  readable rest state.

**Default preset:**
```
type:        display 96-160px @ weight 800, tracking -0.02 to -0.03em
             supporting 40-56px @ weight 500
entrance:    word-by-word, y: 0.6em -> 0, power3.out, 500ms
             stagger 25ms between words
exit:        opacity 1 -> 0, 240ms, power2.in, or scroll off x: 0 -> -40px
hold:        2.5s minimum per line
safe:        90% of frame
```

---

## 2. Logo reveal / sting

2–4 seconds. One idea. The logo should be readable in the final 1.5 s.

**Structure:** (a) mark only → (b) mark settles + wordmark in → (c) hold with
tagline or lockup → out.

**Pacing:** Build 0.8–1.5 s, settle 0.5–1 s, hold 1–1.5 s. Total under 4 s or
you have a film, not a sting.

**Common mistakes:**
- Animating the logo itself (scaling the mark, rotating it). Animate what
  surrounds it — a mask wipe, a shape that draws on, a colour field that washes
  through. Logos are fixed assets; distorting them is a brand violation.
- Forgetting clear space. See `image-handling.md`.
- A sting that doesn't loop. If it will be reused as an outro, build the out as
  the reverse of the in so it can play in both directions.
- More than two moves. One entrance plus one supporting element.

**Default preset:**
```
entrance:    clip-path or mask wipe reveal, power2.out, 900ms
mark:        scale 0.94 -> 1, power2.out, 700ms, on the mark's own container only
wordmark:    opacity 0 -> 1 + y 24 -> 0, power3.out, 500ms, starts at +300ms
hold:        1.2s on the full lockup
out:         opacity -> 0, 280ms
palette:     one brand colour + near-black/near-white only
```

---

## 3. Explainer / infographic

The 30-second explainer is the workhorse: hook, problem, mechanism, proof,
call to action.

**Structure:** hook (0–3 s) → problem (3–8) → how it works (8–20) → payoff
(20–27) → CTA (27–30). Roughly one idea per 5 seconds; if a section needs more
than 8 s, split it into two.

**Pacing:** Scene holds 2.5–4 s. Transitions 500–700 ms. Text cards hold at
2.5 s minimum. Build diagrams element by element at 20–30 ms stagger so the
assembly itself explains the relationship.

**Common mistakes:**
- A wall of text. If a scene has more than ~2 lines of body copy, it needs a
  diagram or a split.
- Constant motion. The build should settle before the next idea arrives;
  everything moving at once reads as noise and nothing is memorable.
- Diagrams that appear fully formed. Animate the construction order so the
  structure is legible.
- No visual anchor between scenes. A consistent element position (a title bar, a
  numbered step) makes the whole piece feel authored.

**Default preset:**
```
scene:       hold 3s, transition 600ms power2.inOut
diagram:     elements build in logic order, stagger 30ms, power2.out, 400ms
labels:      fade + y 12 -> 0, 350ms
title bar:   fixed position, 1 line, 48-64px, persists across scenes
total:       one idea per 5s, one scene per 6-8s
fps:         30
```

---

## 4. Data visualisation / charts

The chart is the argument. The animation is the argument's narration.

**Structure:** axes establish → data draws → the significant point highlights →
the number lands as text.

**Pacing:** Axis build 400–600 ms. Data draw 1.5–3 s depending on point count.
Highlight 300 ms. Number lands at the end and holds 1.5 s. Total 5–15 s per chart;
a piece with more than 3 charts needs a through-line.

**Common mistakes:**
- Animating the chart to grow from the axis on every data change. Use a line
  draw for the first appearance, then cross-fade values on update.
- No easing on a bar or line growth — linear growth reads as a loading bar, not a
  story.
- Labels that appear with the data and then fight it. Labels in after, at
  lower amplitude.
- 3D charts. They distort the comparison and there is no reason.
- Y-axis that doesn't start at zero on a bar chart. It is the single most common
  way to make a chart lie.

**Default preset:**
```
axes:        draw on, power2.out, 500ms
bars:        scaleY 0 -> 1 from baseline, power3.out, 700ms, stagger 30ms
lines:       stroke-dashoffset draw, power2.inOut, 1.8s
value labels: fade + y 8 -> 0, 280ms, land AFTER the growth finishes
number land: count-up over 600ms, power2.out, then hold 1.5s
highlight:   colour shift + 4px scale, 300ms
```

---

## 5. UI / product demo

Show the product, not a camera moving around a mockup.

**Structure:** context shot → the interaction → the result. Screen recordings and
screenshots both work.

**Pacing:** 2–4 s per interaction. Hold the result state long enough to read —
2 s minimum, more if there is text in the UI. Cursor moves use
`power2.inOut`; anything the user "clicks" gets a small press affordance (scale
0.96, 120 ms down, `back.out(1.4)` up).

**Common mistakes:**
- Moving the frame constantly. A slow push-in at the start that then holds is
  stronger than continuous camera drift.
- Interactions faster than a human could perform them. Each step should take
  0.5–1 s.
- Showing the UI at a size where text is unreadable after compression. Frame the
  region that matters and crop the rest.
- No safe-area allowance if this will run as a vertical ad — keep the CTA out of
  the bottom 35%.

**Default preset:**
```
camera:      one push-in, scale 1 -> 1.06, 3s, power2.inOut, then hold
cursor:      moves power2.inOut, 600-900ms; click = scale 0.96, 120ms
state change: 700ms, power2.out
result hold: 2s minimum, 3s if the state contains text
zoom:        scale from a fixed origin, no camera drift
crop:        frame only the region of interest
```

---

## 6. Social / short-form promo

Vertical, front-loaded, and the first frame has to work as a thumbnail.

**Structure:** hook in the first 1.5 s → the point → payoff → loop back to the
hook if it will autoplay.

**Pacing:** Faster than you think. Cut every 1.5–3 s. Nothing holds longer than
3 s. Assume no audio — on-screen text has to carry the meaning.

**Common mistakes:**
- A slow build. Vertical viewers decide in under a second.
- Content in the bottom 35% or top 14% (see `motion-principles.md` §5) where the
  platform UI covers it.
- Text sized for landscape. Design at 1080×1920 with a type scale that is
  readable on a phone at arm's length — display 72–110 px, supporting 40–56 px.
- No loop point. If it autoplays, the last frame should connect to the first.

**Default preset:**
```
size:        1080x1920 (1440x2560 for paid placement)
safe:        clear top 14% and bottom 35%; sides 6%
hook:        on screen by frame 1, movement in first 300ms
cut:         every 1.5-3s
type:        display 72-110px, supporting 40-56px
hold:        max 3s per beat, 2s minimum
audio:       assume muted; burned-in text carries the message
loop:        last frame connects to first
```

---

## 7. Lower thirds, titles, overlays

Graphics that sit *on* someone else's footage. Restraint is the whole skill.

**Structure:** bar or plate slides in → text sets → holds → slides out. Two lines
maximum.

**Pacing:** In 400–600 ms, hold 2–3 s, out 300–400 ms. If it is on screen longer
than 5 s the viewer stops listening and starts reading.

**Common mistakes:**
- Animation that competes with the subject. The graphic supports; it does not
  perform.
- Text over busy footage with no plate, shadow, or gradient scrim. Legibility is
  not optional.
- More than two lines.
- Ignoring the platform's safe area, so a caption UI covers the text.

**Default preset:**
```
in:          plate x -100 -> 0, power3.out, 500ms; text at +180ms
text:        2 lines max, 40-52px, weight 600
hold:        2-3s
out:         x 0 -> -100, power2.in, 350ms
legibility:  plate at 60-80% opacity, or a 120px gradient scrim behind text
safe:        90% of frame
```

---

## 8. Slideshow / photo-driven motion

Photographs carry the emotion; motion just keeps them alive.

**Structure:** establish → 3–6 images → close.

**Pacing:** 2.5–4 s per image. Ken Burns move 3–4 s so it completes exactly as
the next image arrives. Cross-dissolve 400–600 ms.

**Common mistakes:**
- Ken Burns on every image at the same speed and direction. Vary the direction
  and alternate with a static hold so it doesn't feel mechanical.
- A move so slow it reads as a frozen frame. Zoom 5–10% over the shot's length.
- Dissolving during a pan.
- Upscaling too aggressively — a soft source upscaled 4× looks worse than a
  tight crop.

**Default preset:**
```
per image:   3s hold, 500ms cross-dissolve
ken burns:   scale 1.0 -> 1.08, transform-origin varied per image,
             power2.inOut, ease through, never linear
zoompan:     avoid it (steppy); use a paused timeline + frame capture instead
static:      every third image holds with no move
caption:     2.5s minimum, 42 chars/line
```

---

## 9. Looping / abstract backgrounds

Ambient motion behind content. It should never be the thing you look at.

**Structure:** one continuous loop, no start or end.

**Pacing:** Cycles of 8–20 s. Slow enough to sit behind text without competing.

**Common mistakes:**
- A visible seam. Build the loop so frame 0 equals frame N, then verify by playing
  the last frame against the first.
- Motion that draws the eye. If a viewer notices it, it is too fast or too
  contrasted.
- Anything that pulses at a rate that fights reading speed (roughly 1–3 Hz).

**Default preset:**
```
cycle:       12s, seamless — first frame identical to last
easing:      sine.inOut only; no overshoot, no bounce
amplitude:  low contrast, low saturation, or blurred behind a scrim
verify:      extract first and last frame and compare pixel difference
gif:         loop with --gif-loop 0 (infinite)
```

---

## Choosing between them

| If the user says… | Default to |
|---|---|
| "make this text move", "kinetic text" | Kinetic typography |
| "logo animation", "sting", "intro/outro" | Logo reveal |
| "explainer", "how it works", "product video" | Explainer |
| "chart", "data viz", "these numbers" | Data visualisation |
| "app demo", "UI walkthrough", "screen recording" | UI / product demo |
| "Reel", "TikTok", "short", "promo", "vertical" | Social short-form |
| "lower third", "title card", "subtitle style" | Lower third / overlay |
| "photo slideshow", "wedding", "memories" | Slideshow |
| "background", "looping", "ambient", "wallpaper" | Looping abstract |

If the request is genuinely ambiguous, **recommend one and say why**, do not ask
another question.
