# The router

Setup ends by writing one more skill into the home repo: the router. The person describes a situation. The router names the skill or the sequence of skills that fits, the repo to work in, and the source to read. Then it stops.

It answers from a map written into its own file. It does not scan the disk each time. That keeps it fast, lets it list skills the harness hides from the model, and puts the map under review like any other file.

## Name and place

- The name is the one the person chose in setup. Recommend `ask-home`, or `ask-<team>`.
- It lives in the skills folder, see [harnesses.md](harnesses.md).
- Only the person starts it. Set the flag for each harness in use.

## Build the map

One line per item that was kept in the home repo, plus every `installed` and `repo-specific` skill the person may still want to reach.

1. **Draft each line from the item itself.** A skill: its description, and its first paragraph when the description is thin. A repo or source: its pointer. A tool: its usage line. Write what it is for and when to pick it, in the person's words where they exist.
2. **Find the flows.** Look for skills that hand over to each other: one writes a file the next one reads, or one names the next. Put them in order. Skills that stand alone go under Standalone.
3. **Mark the human decisions.** Where a skill waits for an approval or an answer, say so on its line.
4. **Write a test for each close pair.** When two lines look alike, add the one question that tells them apart.
5. **Show the draft in the plan step.** The person corrects it. Their wording wins.

Do not guess a flow. If the skills form none, the map is a flat list by kind, and that is fine.

## The router file

Fill this in and write it as the router's `SKILL.md`. Keep the headings.

````markdown
---
name: <router name>
description: When the user types /<router name> to ask which skill, repo, or source fits a situation.
disable-model-invocation: true
---

You are the router for this home repo. The person describes a situation. Name what fits, then stop.

## How to answer

1. Read the situation. If it could mean two different things, ask one question. Otherwise do not ask.
2. Find where it sits on the map: a step in a flow, an on-ramp, or a standalone.
3. Answer in this shape:

   ```text
   Use:    <skill, or skill → skill → skill>
   In:     <repo, with its path>
   Read:   <source, and how to reach it>      (leave out if none)
   You decide: <where the person must choose or approve>
   Next:   <the exact thing to type>
   ```

4. Add one line of why, only when two entries were close.
5. Stop. Do not start the skill. Do not open files. Do not change anything.

## Rules

- Answer from the map below. Open a skill's own file only when the person asks, or when two lines are too close to choose between.
- When the map and a skill's own file disagree, the skill's file is right. Say the map is behind and name the line.
- When nothing fits, say so and name the nearest entry. Do not stretch one to fit.
- When the person already named a skill, tell them to type it. They do not need a router.
- A skill missing from the list the harness shows you may still exist. The map is written from disk and is the authority.

## The map

Written by setup-home-repo on <date>. Keep it current with its add and cleanup modes.

### Flows

<flow name>: <skill> → <skill> → <skill>

- <skill>: <what it is for>. Pick it when <situation>. <Human decides: what.>

### On-ramps

- <situation that arrives from outside>: start at <skill>, then join <flow> at <step>.

### Standalone

- <skill>: <what it is for>. Pick it when <situation>.

### Close pairs

- <skill a> or <skill b>: <the one question that tells them apart>.

### Repos

- <name>: <what it is>. Work here when <kind of task>.

### Sources

- <name> (<kind>): look here for <what>. Reach via <how>.

### Tools

- <name>: <what it does>.
````

Leave out a heading that has no lines. Past about 20 repos, the Repos part lists the areas and points at the `repos/` files.

For Codex, add `agents/openai.yaml` beside it with `policy.allow_implicit_invocation: false`.

## A good line and a bad one

Good: `review-pr: reviews one pull request against the team checklist. Pick it when a pull request exists and you want findings before a human reads it. Human decides: which findings to fix.`

Bad: `review-pr: a skill for reviewing`. It repeats the name and gives no reason to pick it.

## Keep the map true

The map is only useful while it matches the disk.

- **Add** writes or changes the item's map line in the same diff as the item.
- **Cleanup** removes the map line of anything it removes, and renames what it renames.
- **Advise** reports a map line with no item, an item with no map line, a line that names an old skill name, and a flow whose step is gone.

Never rebuild the whole map on a re-run. The person has edited its wording. Change only the lines that are wrong.
