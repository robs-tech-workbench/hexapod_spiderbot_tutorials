# AGENTS.md

Instructions for AI coding agents working in this repository.

This is a tutorial repository for a 3D-printed hexapod spider robot. Each `tutorial_*` folder contains a `README.md` (the tutorial), supporting Jupyter notebooks, and Python sources. Prefer minimal, quality-focused edits (links, typos, doc/code mismatches, obvious bugs) over rewriting tutorial content.

## Changelog policy (required)

**Every change must include a corresponding entry in [CHANGELOG.md](CHANGELOG.md).** Do not commit or push any change without it.

- Add entries under a heading for the current date; create a new `## YYYY-MM-DD` section at the top when the most recent section is for a different day.
- Use the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) categories: `Added`, `Changed`, `Fixed`, `Removed`.
- One bullet per user-visible change, past tense ("Fixed ...", "Added ...").
- The changelog update belongs in the same commit as the change it describes.

## Other conventions

- Keep the companion-article link at the top of each tutorial README intact when editing.
- Do not reformat notebook JSON wholesale; make targeted edits so diffs stay reviewable.
- After editing Python sources or notebooks, verify they still compile before committing.
