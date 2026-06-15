# nature-skills Installation Guide

`nature-skills` is a collection of Codex-style skills for academic writing,
paper reading, citation search, figure generation, paper-to-PPT workflows,
reviewer responses, patent drafting, and related research tasks.

The repository is not a Python package or npm package. Each installable skill is
a full folder under `skills/`, centered on `SKILL.md`.

The most important rule:

- install or reference the whole `skills/nature-*` folder
- keep `skills/_shared/` available next to the skill folders
- do not copy only `SKILL.md`

Many skills depend on `references/`, `static/`, `manifest.yaml`, scripts,
assets, or shared files. Copying only one file can make a skill appear installed
while breaking the workflow at runtime.

---

## Recommended: install with Codex

For Codex users, the simplest installation method is to give Codex this GitHub
link and ask it to install the skills locally:

```text
https://github.com/Yuan1z0825/nature-skills.git
```

Use a prompt like this:

```text
Install the Codex skills from this repository:
https://github.com/Yuan1z0825/nature-skills.git

Please install the full skill folders under skills/, including skills/_shared,
into my Codex skills directory. Do not copy only SKILL.md.
```

Codex should clone or read the repository, then copy the required folders into
your Codex skills directory, usually `~/.codex/skills`. Grant filesystem and
network permissions if Codex asks for them.

To install only one skill, name it explicitly:

```text
Install only nature-polishing from:
https://github.com/Yuan1z0825/nature-skills.git

Also install skills/_shared if the skill needs shared support files.
```

To update later, give Codex the same link and ask it to update the installed
skills from the latest `main` branch.

---

## What Codex should install

The repository layout is:

```text
skills/
├── _shared/
└── nature-<topic>/
    ├── SKILL.md
    ├── README.md
    ├── manifest.yaml
    ├── static/
    ├── references/
    ├── scripts/
    └── ...
```

Not every skill has every subfolder, but the folder should be preserved as a
unit. The current skill folders include:

- `nature-academic-search`
- `nature-citation`
- `nature-data`
- `nature-figure`
- `nature-paper-to-patent`
- `nature-paper2ppt`
- `nature-polishing`
- `nature-reader`
- `nature-response`
- `nature-reviewer`
- `nature-writing`

For a full installation, Codex should install `skills/_shared` plus every
`skills/nature-*` folder.

---

## Manual fallback

Use this only if you are not asking Codex to do the installation for you.

```bash
git clone https://github.com/Yuan1z0825/nature-skills.git
cd nature-skills
mkdir -p ~/.codex/skills
cp -R skills/_shared ~/.codex/skills/
cp -R skills/nature-polishing ~/.codex/skills/
```

For all skills:

```bash
git clone https://github.com/Yuan1z0825/nature-skills.git
cd nature-skills
mkdir -p ~/.codex/skills
cp -R skills/_shared ~/.codex/skills/
for d in skills/nature-*; do
  cp -R "$d" ~/.codex/skills/
done
```

After manual installation, start a fresh Codex session so the new skills are
discovered.

---

## Claude Code and other agents

Claude Code does not consume these folders exactly like Codex local skills. The
portable approach is to keep a stable clone of this repository and create a thin
wrapper that tells the agent to read the real `SKILL.md` file from that clone.

Example setup:

```bash
mkdir -p ~/ai-skills
cd ~/ai-skills
git clone https://github.com/Yuan1z0825/nature-skills.git
```

Example Claude Code subagent wrapper:

```bash
mkdir -p ~/.claude/agents
cat > ~/.claude/agents/nature-polishing.md <<'EOF'
---
name: nature-polishing
description: Use proactively for Nature-style academic polishing, restructuring, or Chinese-to-English manuscript refinement.
---

When invoked, first read `~/ai-skills/nature-skills/skills/nature-polishing/SKILL.md`.
Treat that file as the governing workflow.
If the skill references supporting files, read only the directly needed files from
`~/ai-skills/nature-skills/skills/nature-polishing/` and
`~/ai-skills/nature-skills/skills/_shared/`.
Do not replace the skill with a generic polishing response.
EOF
```

The same pattern works for slash commands or other agents that support custom
prompt bundles: point the wrapper at the real skill folder and preserve relative
support files.

---

## Verification

After installation, start a new Codex session and ask for a task that clearly
matches one of the installed skills, for example:

```text
Polish this abstract in Nature style.
```

```text
Turn this paper into a Chinese journal-club PPT.
```

```text
Translate this paper into a full Chinese-English markdown reader.
```

If the skill is installed correctly, Codex should follow the corresponding
skill-specific workflow instead of giving a generic one-shot answer.

---

## Troubleshooting

If the agent gives a generic answer:

- start a fresh agent session
- make sure the whole `skills/nature-*` folder was installed
- make sure `skills/_shared/` was also installed
- ask for a task that clearly matches the skill description

If a skill cannot find references, scripts, or static files:

- reinstall the whole skill folder
- check that the folder structure under `~/.codex/skills` still matches the
  repository layout
- do not flatten the files into a single directory

If updates are not reflected locally:

- ask Codex to update from `https://github.com/Yuan1z0825/nature-skills.git`
- or run `git pull` in your local clone and reinstall the updated folders
