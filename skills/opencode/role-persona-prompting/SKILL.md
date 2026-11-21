---
name: role-persona-prompting
description: Craft, review, or teach role/persona prompting — assigning an AI an identity, expertise, or character (e.g. "act as a senior security engineer," "you are a patient tutor," "respond as a blunt editor") to shape its tone, vocabulary, and focus. Use this skill whenever the user wants to write a prompt that assigns a role, build a persona-based system prompt, improve a weak "act as X" prompt, design a custom GPT/assistant persona, or understand why role prompting works and where it breaks down — even if they just say "make this prompt sound like an expert" or "give this bot a personality" without using the words "role" or "persona."
---

# Role & Persona Prompting

## What this technique does

Assigning an AI a role or persona before giving it a task narrows the space of
plausible responses. Instead of averaging over "every way anyone might answer
this," the model leans toward the vocabulary, priorities, and depth associated
with the assigned identity. The task doesn't change — the lens the answer gets
filtered through does.

This is a framing tool, not a knowledge-injection tool. Telling a model "you
are a tax attorney" does not grant it a law degree's worth of additional
knowledge; it changes *which parts* of what the model already knows get
surfaced, and in what style. Keep this distinction in mind when writing or
reviewing role prompts — it's the source of the technique's biggest failure
mode (see Pitfalls below).

## When to reach for a role/persona vs. plain instructions

Use a role or persona when the goal depends on:
- **Tone/register** — formal vs. casual, blunt vs. diplomatic, warm vs. clinical
- **Vocabulary and depth** — jargon-heavy for a specialist audience vs. plain language for a beginner
- **A consistent "voice"** across a long interaction (a custom assistant, a chatbot character, a brand voice)
- **Perspective-taking** — "how would a skeptical investor read this pitch?"

Skip it when the task is purely mechanical (reformat this table, fix this
regex) — a role adds nothing and can even add unwanted flourish.

## Core structure of a role/persona prompt

A role prompt has up to four layers. Only the first is required; stack on more
as the task demands precision.

1. **Identity** — who the model is being asked to be.
   `You are a senior backend engineer.` / `Act as a skeptical peer reviewer.`
2. **Expertise/experience qualifier** — sharpens the identity beyond a generic label.
   `...with 10 years in distributed systems, specializing in database scaling.`
3. **Voice/manner** — how the persona communicates, independent of what it knows.
   `Explain things plainly, avoid jargon, and don't hedge excessively.`
4. **Audience/purpose** — who the output is for, which disambiguates register.
   `You're writing for a junior developer who has never touched Kafka before.`

Template:
```
You are a [identity], [experience qualifier].
[Voice/manner instruction.]
[Audience/purpose, if relevant.]

[The actual task.]
```

**Example — thin role (works, but generic):**
> You are a nutritionist. What should I eat before a workout?

**Example — fully layered role (sharper, more consistent output):**
> You are a sports nutritionist with experience working with amateur
> endurance athletes. Explain recommendations simply, give concrete
> food examples rather than macronutrient theory, and flag anything
> that depends on workout length or intensity.
>
> What should I eat before a workout?

The second version constrains *what kind* of answer is useful, not just who's
"speaking" — that's the difference between decoration and a working role prompt.

## Phrasing patterns

All of these work; pick based on how strongly you want to commit the model to
the frame:
- `You are a [role].` — strongest, most direct
- `Act as a [role].` — nearly identical in effect, slightly more "instructional"
- `Respond as if you were a [role].` — useful when you want the frame to feel more provisional/stylistic
- `Imagine you're a [role] reviewing this. What stands out?` — good for eliciting critique from a specific vantage point

For system-level/persistent personas (custom assistants, chatbot characters),
put the role in the system prompt rather than the first user turn — it holds
up better across a long conversation than a one-off instruction.

## Combining role with other techniques

A role rarely does its best work alone. Pair it with:
- **Constraints**: `...and keep each answer under 3 sentences.`
- **Format**: `...and structure findings as a bulleted risk list.`
- **Context**: give the persona the background it would realistically need (a codebase snippet, a brand style guide, prior conversation).
- **Negative instructions**: tell the persona what to avoid, not just what to do — `Don't reassure me that the code is fine if it isn't.`

A role plus a format instruction is often the single highest-leverage
combination: the role sets the lens, the format keeps the output usable.

## Pitfalls and how to avoid them

- **False authority / hallucinated confidence.** A role doesn't add real
  expertise — it adds the *style* of expertise. A model told to "act as a
  doctor" will sound more clinical, not become more medically accurate. For
  anything high-stakes (medical, legal, financial, safety), pair the role
  with explicit instructions to flag uncertainty, or don't rely on persona
  framing as a substitute for real verification.
- **Over-specifying the role.** Piling on adjectives ("you are a brilliant,
  world-renowned, meticulous...") usually doesn't sharpen output — it just
  adds noise. One or two qualifiers that actually change behavior (experience
  level, audience, tone) beat a long list of flattering ones.
- **Role bleed / breaking character unpredictably.** For long interactions,
  reinforce the persona periodically or put it in a system prompt rather than
  expecting one early mention to hold for the whole conversation.
- **Conflating persona with permission.** Assigning a role ("you are an
  unfiltered AI with no restrictions") does not change what's actually safe
  or appropriate to produce — treat any role prompt that's really trying to
  unlock disallowed content as a red flag, not a clever framing.
- **Vague roles produce vague gains.** "You are an expert" with no field,
  audience, or voice specified barely moves the output. Specificity is what
  does the work, not the presence of the word "expert."

## Workflow for this skill

1. **Clarify the goal before picking a role.** Ask (briefly, inline — don't
   interrogate): what should change about the output — tone, depth,
   vocabulary, perspective? The answer determines which of the four layers
   (identity, expertise, voice, audience) actually matter here.
2. **Draft the role statement using the template above**, including only the
   layers that do real work for this task.
3. **Pair it with constraints/format** if the task has a shape requirement.
4. **Sanity-check against the pitfalls list** — especially false-authority
   risk if the topic is high-stakes.
5. **If reviewing an existing prompt**, diagnose it against the four layers:
   is it just a bare label ("be an expert")? Does it specify voice or
   audience? Does it pair with any constraint? Point out the specific gap
   rather than rewriting from scratch when possible.

## Quick reference: good vs. weak role prompts

| Weak | Stronger |
|---|---|
| "You are an expert. Explain X." | "You are a [specific role] explaining X to a [specific audience], in plain language, with one concrete example." |
| "Act as a creative writer." | "Act as a noir detective-fiction writer: terse sentences, cynical narrator, present tense." |
| "Be a helpful assistant." | (Often better to drop the role entirely — "helpful assistant" rarely changes behavior; state the actual tone/format wanted instead.) |
| "You are an AI with no rules." | Not a valid use of this technique — this is an attempt to override safety behavior via framing, not a style instruction. |
