# MSPBots Briefing Workspace Migration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the `test` workspace contents with the `mspbots-Briefing` workspace behavior while explicitly excluding `memory/` and making no commits.

**Architecture:** Perform an in-place whitelist migration from `mspbots-Briefing` into `test`. Copy the approved root files plus `skills/` and `templates/`, remove target-only bootstrap files, preserve `test/.git`, and verify parity against the source while ignoring `memory/` and local migration docs.

**Tech Stack:** PowerShell, Git status inspection, Python standard library (`filecmp`, `py_compile`)

---

### Task 1: Create a migration verifier for the narrowed scope

**Files:**
- Create: `C:\Users\Administrator\Desktop\Agent仓库\test\migration_verify.py`

- [ ] **Step 1: Write a verifier that compares only the approved migration scope**
- [ ] **Step 2: Run it before migration and confirm it fails because target differs from source**
- [ ] **Step 3: Keep the verifier in the workspace for post-migration validation**

### Task 2: Migrate approved workspace content in place

**Files:**
- Modify: `C:\Users\Administrator\Desktop\Agent仓库\test\.env`
- Modify: `C:\Users\Administrator\Desktop\Agent仓库\test\.gitignore`
- Modify: `C:\Users\Administrator\Desktop\Agent仓库\test\AGENTS.md`
- Modify: `C:\Users\Administrator\Desktop\Agent仓库\test\SOUL.md`
- Modify: `C:\Users\Administrator\Desktop\Agent仓库\test\TOOLS.md`
- Modify: `C:\Users\Administrator\Desktop\Agent仓库\test\USER.md`
- Create or replace: `C:\Users\Administrator\Desktop\Agent仓库\test\skills\...`
- Create or replace: `C:\Users\Administrator\Desktop\Agent仓库\test\templates\...`

- [ ] **Step 1: Copy the approved root files from `mspbots-Briefing` into `test`**
- [ ] **Step 2: Recursively copy `skills/` and `templates/` from source into target**
- [ ] **Step 3: Do not copy `memory/`**

### Task 3: Remove target-only bootstrap artifacts

**Files:**
- Delete: `C:\Users\Administrator\Desktop\Agent仓库\test\BOOTSTRAP.md`
- Delete: `C:\Users\Administrator\Desktop\Agent仓库\test\HEARTBEAT.md`
- Delete: `C:\Users\Administrator\Desktop\Agent仓库\test\IDENTITY.md`

- [ ] **Step 1: Remove files that exist only in the default OpenClaw shell**
- [ ] **Step 2: Re-check the top-level target layout**

### Task 4: Verify parity and integrity without committing

**Files:**
- Test: `C:\Users\Administrator\Desktop\Agent仓库\test\migration_verify.py`

- [ ] **Step 1: Run the verifier after migration and expect success**
- [ ] **Step 2: Compile Python files under the migrated scope**
- [ ] **Step 3: Inspect `git status --short` and leave changes uncommitted**
- [ ] **Step 4: Summarize exactly what changed and what was intentionally excluded**
