---
name: useful-or-cut
description: Hostile usefulness filter for prose — use when drafting or editing a blog post, essay, or other written piece.
---

# Useful or Cut

Based on Shreyas Doshi's flowchart: *Is it useful? → Yes: take what's useful, ignore the rest. → No: ignore the rest.*

The flowchart is a reader's filter. This skill runs it in reverse, against the draft, before the reader ever sees it. The agent plays hostile reader on its own output.

**The core rule: the "no" branch is deletion, not revision.** In the original, "no" loops back to *ignore the rest*. Here it means cut the sentence. Do not soften it, hedge it, or rewrite it into something adequate. Cut it.

## Workflow

### 1. Find the actual claim

Before writing anything, state in one sentence what the user is claiming, and what a reader can do differently after reading it. Show this to the user and get agreement.

If the idea doesn't support a claim — if it's an observation, not an argument — say so. Do not manufacture an argument to fill the shape of a blog post.

### 2. Size the piece to the idea

Estimate the length the idea can carry at full density. State the number before drafting. Common outcomes: a sharp idea is 400–800 words; a genuinely developed argument is 1200–1800.

**Never write to a target length.** If the user asks for 1500 words and the idea supports 600, write 600 and say why. Padding to hit a number is the single largest source of slop.

### 3. Draft

Write it. Don't self-censor during drafting — the cutting pass handles that.

Use the user's own words, examples, and framings from the conversation wherever they exist. Their specifics are the part no generic model output can replicate; they are the density.

### 4. The cut pass (mandatory — never skip, never merge into step 3)

Go paragraph by paragraph. For each one, write in **ten words or fewer** what the reader takes away.

Delete the paragraph if:
- You can't complete that sentence
- The takeaway duplicates an earlier paragraph's
- The takeaway is "context," "setup," "transition," or "restates the above"
- It's true but the reader already believed it

Then go sentence by sentence inside the survivors and do it again.

Expect to cut 30–50% of the draft. **If you cut less than 20%, you did the pass wrong — run it again, harder.** The common failure is grading your own writing generously.

### 5. Known slop shapes — cut on sight

- **Throat-clearing openers.** "In today's fast-paced world," "We've all been there," any scene-setting before the claim. Start at the claim.
- **The restating conclusion.** A final section that summarizes what was just said. End on the last real point.
- **"It's not X, it's Y."** Fine once per piece, maybe. Three times is a tic.
- **Rhetorical questions as transitions.** "So what does this mean for you?" Just say the thing.
- **Hedge stacks.** "It's worth noting that it may in some cases be possible that…"
- **Inflated lists.** Six items where three are real and three were generated to reach six. Ship three.
- **Symmetry padding.** Giving a weak counterpoint equal space because the structure looked balanced.
- **Adjective pairs.** "clear and concise," "robust and scalable." Pick one or neither.
- **Explaining the obvious to sound thorough.** If your reader knows what an API is, don't define it.

The following six shapes are adapted from [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT):

- **Colon reveals.** A noun phrase, a colon, then a dramatic reveal: "The best part: it learns." Rewrite as a plain sentence. Colons are for lists, labels, and quotes, not fake drama.
- **Superficial `-ing` analysis.** Trailing clauses that pretend to explain meaning: "highlighting," "underscoring," "reflecting," "showcasing." Replace with the concrete consequence or cut.
- **Importance puffery.** "Stands as a testament," "marks a pivotal moment," "plays a vital role," "underscores its significance." State the fact and let the reader judge whether it matters.
- **Weasel attribution.** "Experts agree," "studies show," "widely regarded as," "many argue." Name the source or cut the claim. No source? Ask the user — never invent one.
- **Synonym cycling.** Rotating "the agent / the assistant / the tool" for the same referent. If the clear word is right, repeat it.
- **Fake-profound kickers.** A final "deep" line that turns the point into a cute metaphor or mic-drop. Delete it — do not rewrite it into a better metaphor — and end on the clearest concrete sentence already in the draft.

### 6. Fidelity check

The draft must contain no claim the user didn't make or wouldn't endorse. Agents pad thin ideas by inventing supporting assertions, statistics, and examples. Flag anything you introduced:

> Added: the comparison to X, the figure of 40%, the anecdote about Y. Confirm or cut.

Invented numbers and fake anecdotes are worse than slop — they're wrong.

### 7. Self-check before the exit gate

Before handing the draft to your prose-quality gate (if you have one, e.g. an `npm run slop-check <file>` script), answer each with pass/fail; fix and re-check on any fail. (Self-check pattern from petergyang/no-ai-slop's eval.md, MIT.)

1. Does every paragraph have a ten-words-or-fewer takeaway that isn't "context" or "recap"?
2. Are all fifteen slop shapes in §5 absent (or flagged deliberately)?
3. Is every claim, number, and example the user's own — or explicitly flagged as added?
4. Does the piece end on its last concrete point, not a summary or kicker?
5. Would the user recognize the draft as their own voice?

### 8. Report

End with a short cut log so the user can overrule you:

```
Claim: <one line>
Drafted: 1,340 → Final: 780 words (42% cut)
Cut: opening scene-setter, section 3 (duplicated section 1),
     closing summary, 4 hedges
Added by me (confirm): the Postgres example in §2
```

## What this skill does not do

Usefulness is not the only test. A piece can pass this filter and still be dishonest, unattributed, or unkind. Accuracy, sourcing, and credit are separate gates — this one only governs whether text earns its place on the page.
