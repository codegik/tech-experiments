---
name: tech-list
description: Add a tech from a photo or name to the team tech list.
version: 0.1.0
author: codegik, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [tech-list, telegram, whatsapp, readme, git]
---

# Tech list

Keeps the team's tech list in `README.md` of the tech-experiments repo. The
user sends a photo of a technology (slide, tweet, screen, booth) or a text such
as `add this into the list "cua"`. You identify the tech, find its official
link, add it, commit and push to main. All edits and git go through
`./techs.sh`. Never edit the table by hand and never run git yourself.

Repo root = this skill's dir `../../..` (skill_dir is printed by `skill_view`).
Run every command with `terminal(command=..., workdir=<repo root>)`.

## When to Use

- A photo with "add", "save", "list", "salva", "adiciona", or with no caption
  when it clearly shows a dev tool, library, service or framework.
- Text like `add "X" to the list`, `adiciona X na lista`, `salva essa tech`.
- "What's on the list?" → `./techs.sh list`.

Don't use for: receipts or purchases (those go to the `recibos` skill).

## Procedure

1. **Identify.** For a photo, `vision_analyze` it and read the product name,
   logo, URL or repo path shown. Combine it with the caption. Done when you have
   one candidate name, or two or three if it's ambiguous.
2. **Find the link.** `web_search` for the name plus the words on the photo.
   Pick in this order: the official site, then the GitHub/GitLab repo. Never use
   an article, a blog, a listing (Product Hunt, awesome lists) or a social post.
   When several projects share the name (e.g. "cua"), pick the one that best
   matches the photo/caption and a developer audience. Don't ask, the user
   chose "pick the most likely and say which". Done when `web_extract` of the
   URL confirms it is that product's own page.
3. **Already listed?** `./techs.sh list`. If it's there (same name or same
   link), reply that it's already in the category and stop.
4. **Describe and categorize.** Description: one line in English, ≤ 100 chars,
   what it is and not marketing, no `|`. Category: reuse an existing one from
   `list` when it fits (case doesn't matter). Create a new one only when none
   fits, using a short plural noun phrase like "AI Agents", "Databases",
   "Observability".
5. **Add.**
   `./techs.sh add --name "<Name>" --url "<url>" --category "<Category>" --desc "<desc>"`
   Exit 3 = already listed (go to step 3's reply). Exit 1 = fix the argument
   and retry.
6. **Publish.** `./techs.sh publish "Add <Name>"`. Done when it prints
   `pushed: <commit url>`.
7. **Reply** in the user's language, short:
   `Added <Name> to <Category>: <url> — <desc>. Commit: <commit url>`.
   If you picked between candidates, add one line: `I picked <url>; the other
   match was <name/url>. Want me to swap it?`

Several techs in one photo: repeat steps 2–5 for each, then one publish
(`"Add A, B and C"`) and one reply listing them all.

## Fixing an entry

When the user says the pick was wrong ("not that one, I meant …"), there is no
edit command. Remove the wrong row with `patch` on `README.md` (remove the
category heading and table too if it becomes empty), run `./techs.sh add` for
the right one, then publish with `"Replace <Old> with <New>"`.

## Pitfalls

- `publish` refuses when files other than `README.md` are modified. Report
  that to the user instead of cleaning the tree.
- Push uses HTTPS + `gh auth git-credential`. If it fails on auth, report the
  error. Don't switch to SSH or try another credential.
- If `publish` fails after the commit (network, push conflict), the commit
  stays local. Rerun the same `publish` once. It pushes pending commits even
  with no new edit. If it fails again, tell the user and show the error.

## Verification

`./techs.sh check` prints `ok`, and the commit URL from `publish` opens on GitHub.
