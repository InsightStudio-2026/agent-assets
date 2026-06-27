# Agent Assets · A VS Code Copilot Customization Kit

> **中文版**：请阅读 [`README.md`](./README.md)。The canonical, Chinese-first version lives there. This English file is a faithful translation for international readers; when in doubt, the Chinese version prevails.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Made for VS Code](https://img.shields.io/badge/Made%20for-VS%20Code-007ACC.svg)](https://code.visualstudio.com/)
[![Copilot Agent Mode](https://img.shields.io/badge/Copilot-Agent%20Mode-00A4EF.svg)](https://code.visualstudio.com/docs/copilot/copilot-chat)
[![Markdownlint](https://img.shields.io/badge/markdownlint-clean-success.svg)](https://github.com/DavidAnson/vscode-markdownlint)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

**One-liner**: A pure Markdown + JSON asset repository (no runtime code) that turns GitHub Copilot in VS Code into a project-level **DRI (Directly Responsible Individual)** — with enforceable spec-driven workflows, 14-surface audits, and three-Gate decision governance.

---

## 📑 Table of Contents

- [What It Is](#what-it-is)
- [What It Is Not](#what-it-is-not)
- [Quick Start](#quick-start)
- [Why VS Code Native](#why-vs-code-native)
- [Core Methodology](#core-methodology)
- [Workflow Routing Table](#workflow-routing-table)
- [Project Structure](#project-structure)
- [Acknowledgements & Design Lineage](#acknowledgements--design-lineage)
- [Honest Statement · Known Limitations](#honest-statement--known-limitations)
- [Contributing](#contributing)
- [License](#license)

---

## What It Is

`agent-assets` is a **Markdown + JSON configuration kit that you clone into any project** — custom-built for VS Code + GitHub Copilot. It injects the judgement, discipline, and rollback boundaries of a human "project DRI" into Copilot via **all official VS Code Agent Customization entry points**:

- **`instructions/`**: domain conventions auto-loaded by file pattern (`applyTo`) — frontend, backend, database, documentation, PowerShell, TDD, code review, compliance, master rules.
- **`skills/`**: 60+ semantically-triggered workflow skills (write spec, execute spec, project diagnosis, bug audit, root-cause diagnosis, ...).
- **`agents/`**: 3 persistent roles (planner / implementer / code-reviewer), switchable via `@name`.
- **`prompts/`**: 5 slash command templates (`/specs-write`, `/specs-execute`, ...).
- **`hooks/`**: PreToolUse safety interception (`rm -rf` / `DROP TABLE` / `git push --force`) + PostToolUse audit logging.
- **`.vscode/settings.json`**: binds Copilot commit / PR / review generation behaviour to this repo's conventions.

**Result**: Copilot in this repo is no longer an "answer-the-question" assistant — it actively maintains project overview, routes by workflow, validates by DoD gates, decides by three-Gate policy, and never drifts from SSOT.

## What It Is Not

To save your evaluation effort:

- **Not** a Copilot prompt collection or "magic spell" — every protocol has runnable verification commands (ESLint / Ruff / pytest / 14-layer drift defense / TDD-Lock SHA-256).
- **Not** an MCP server, VS Code extension, or script tool — **zero install**, clone and use.
- **Not** adapted for other IDEs (Cursor / Cline / Claude Code have their own asset conventions; this repo ships `CLAUDE.md` as a cross-agent bridge only).
- **Not** forcing you to copy verbatim — the entire protocol is grounded in **DRI autonomy**; what you must decide is strictly narrowed to Strategy / Critical Design / Irreversible Side Effects.
- **Not** only for large teams — solo developers also benefit from "auto-maintain SSOT, auto-audit, auto-validate DoD gates".

## Quick Start

**Prerequisite**: [VS Code](https://code.visualstudio.com/) + [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) installed and signed in.

```text
1. Clone this repo to your project root (or as a sub-directory)
   git clone https://github.com/<owner>/agent-assets.git
   cd agent-assets

2. Open in VS Code
   code .

3. Replace the LICENSE placeholder
   Edit line 3 of LICENSE and replace [Your Name / Your Studio] with your real attribution

4. Start chatting
   In Copilot Chat, say: "Project status unclear" → Copilot auto-hits /project-steward
                or say: "I want to build feature X" → Copilot auto-hits /specs-write
```

VS Code auto-detects `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/`, `.github/skills/` and injects them into Copilot context. No manual configuration.

> 💡 **To migrate assets into an existing project**: copy `.github/`, `AGENTS.md`, `CLAUDE.md`, `.vscode/settings.json`, `LICENSE`, `.markdownlint.json`. The `docs/` directory is created at runtime by the spec workflow; the repo does not pre-ship it.

## Why VS Code Native

Other agent solutions put rules into a single file (`.cursorrules` / `.clinerules` / `CLAUDE.md`). This repo **exclusively uses official VS Code Agent Customization entry points**, aligned with [VS Code official docs](https://code.visualstudio.com/docs/copilot/copilot-chat):

| VS Code Entry Point | Usage | Advantage |
| ---- | ---- | ---- |
| `AGENTS.md` | Cross-agent central registry | Auto-detected by VS Code, zero config |
| `.github/copilot-instructions.md` | Core protocol cheat-sheet | Project-level always-on |
| `.github/instructions/*.md` + `applyTo` | 9 domain conventions loaded by file type | **On-demand injection** avoids context pollution |
| `.github/skills/*/SKILL.md` | 60+ semantically-triggered workflows | Copilot auto-recognizes task semantics |
| `.github/agents/*.agent.md` | 3 persistent roles + tool restrictions + model preferences | Clear role boundaries, isolated permissions |
| `.github/prompts/*.prompt.md` | 5 slash commands | Invoke via `/specs-write` |
| `.github/hooks/*.json` | PreToolUse / PostToolUse | **Hard interception of catastrophic commands** + audit log |
| `.vscode/settings.json` | Copilot commit/PR/review generation binding | Copilot output conforms to repo conventions |

## Core Methodology

This repo is not "prompts" but a **self-consistent engineering philosophy**. Core terms (all from `rules.instructions.md`):

| Concept | One-liner |
| ---- | ---- |
| **DRI (Directly Responsible Individual)** | Copilot is the default project DRI — proactively maintains overview, identifies next step, fills context, executes verification, archives evidence |
| **Three Gates** | Strategy (product direction) / Critical Design (architecture contract) / Real-World Side Effect (irreversible) — only these three require user sign-off |
| **Decision Ownership Matrix (DOM)** | L-STRAT strategic / L-DESIGN design / L-IMPL implementation / L-ROUTINE routine — Copilot's autonomy grows downward |
| **Pause-and-Ask Allowlist** | Only 5 situations allow blocking questions (strategy / critical design <70% confidence / irreversible / spec breach / low confidence) |
| **14-Surface Audit** | Documentation SSOT / History / Live Database / Static Data / Architecture / Contracts / Dependencies / Runtime Deploy / Code Entrypoints / UI / Tests / Security&Privacy / Observability / Compliance |
| **SSOT Three-Layer Docs** | L1 strategic SSOT / L2 execution contract / L3 delivery archive — one fact defined once, others reference it |
| **Four Questions Before Coding** | Think clearly → Minimal sufficient → Surgical → Verifiable |
| **Three TDD Loops** | ATDD (AC→acceptance test) / BDD (US→scenario) / TDD (unit test pass) — `/specs-execute` Phase 7 requires all three |
| **14-Layer Drift Defense** | Any schema change must pass 14 layers: migration integrity / ORM alignment / live DB readback / column types / CHECK / indexes / triggers / views / mypy / OpenAPI contract freeze, ... |

## Workflow Routing Table

| Scenario | Command / Skill | One-liner |
| ---- | ---- | ---- |
| Project status unclear / next step unknown | `/project-steward` | Global diagnosis and routing |
| No master / L1 SSOT | `/project-inception` | 0 → 1 inception |
| New feature / cross-module refactor | `/specs-write` | Requirement → Spec contract (seven-piece set) |
| Execute approved Task | `/specs-execute TASK-###` | Forced recap + TDD Red-Green-Refactor |
| Review implemented diff | `review` | Standards / Spec / Verification three axes |
| Root-cause / performance regression | `diagnose` | Feedback-loop-driven disciplined diagnosis |
| Bug impact scope unknown | `/bug-audit` | Breadth + depth defect audit |
| Architecture friction / shallow modules | `/architecture-audit` | Seam / interface reshape |
| Business loop / MVP survival | `/business-model-audit` | Buyer / alternatives / ROI |
| Local small feature / simple bug | `tdd` or direct | Local Red-Green-Refactor |

> Full workflow list and trigger conditions: [`AGENTS.md`](./AGENTS.md).

## Project Structure

```text
agent-assets/
├── AGENTS.md                         # Cross-agent central registry (auto-detected by VS Code)
├── CLAUDE.md                         # Claude Code / Cursor / Windsurf bridge entry
├── LICENSE                           # MIT
├── .markdownlint.json                # Markdown rule config
├── .vscode/
│   ├── settings.json                 # Copilot behaviour binding (commit / PR / review / skillTool)
│   └── tasks.json                    # markdownlint full-scan task
└── .github/
    ├── copilot-instructions.md       # Core protocol auto-loaded by VS Code (cheat-sheet + routing)
    ├── instructions/                 # 9 domain conventions auto-loaded by applyTo
    ├── skills/                       # 60+ semantically-triggered workflows
    ├── prompts/                      # 5 slash command templates
    ├── agents/                       # 3 persistent roles
    ├── hooks/                        # Lifecycle interception (safety-guard + audit-log)
    └── verify-completeness.ps1       # Asset completeness self-check
```

## Acknowledgements & Design Lineage

This repo insists on **honest attribution of external sources**. Asset absorption falls into four categories, each with clear source, mode, and provenance records — we never vaguely claim "clean-room design".

### 1. Direct Vendor (MIT License)

The following skills are **copied wholesale + locally adapted** from external repos (retaining MIT), each explicitly approved by the user and recorded in the repo's built-in provenance audit files:

- **[greensock/gsap-skills](https://github.com/greensock/gsap-skills)** (GreenSock / Webflow) — 8 GSAP animation skills directly migrated:
  - `gsap-core` · `gsap-timeline` · `gsap-scrolltrigger` · `gsap-plugins` · `gsap-utils` · `gsap-react` · `gsap-performance` · `gsap-frameworks`
  - **Approval record**: User explicitly approved on 2026-05-29 (original quote: "直接搬迁，做好windsurf及本地适配化即可")
  - **Provenance file**: [`.github/skills/asset-quality-gates/references/external-provenance-gsap-skills.md`](./.github/skills/asset-quality-gates/references/external-provenance-gsap-skills.md)

### 2. Mechanism Absorption & Functional Coverage

The **design mechanisms** of the following workflows are absorbed from external AI engineering asset repos, **rewritten into Chinese protocols via mechanism reference** (not source copy):

- **[garrytan/gstack](https://github.com/garrytan/gstack)** — many core workflow mechanisms originate from gstack, including:
  - **Lifecycle loop** (think-plan-build-review-test-ship-retro) → `/project-inception` + `/specs-write` + `/specs-execute` + `review` + `webapp-testing` + `/release-deploy` + `engineering-retro`
  - **Release readiness dashboard** → `/release-deploy` readiness-dashboard
  - **Session save/restore** → `session-context` skill
  - **Operational learnings ledger** → `operational-learnings` skill
  - **Browser QA & visual evidence** → `webapp-testing` skill
  - **Security audit & threat modeling** → `/security-privacy-audit` (STRIDE + OWASP)
  - **Scope guard & edit lock** → `scope-guard` skill
  - **Code health dashboard** → `/code-health-dashboard`
  - **Engineering retro** → `engineering-retro`
  - **Browser flow codifier** → `browser-flow-codifier` skill
  - **Ownership-aware questioning** → DOM decision matrix + Pause-and-Ask allowlist
  - **Provenance file**: [`.github/skills/asset-quality-gates/references/external-provenance-gstack-main.md`](./.github/skills/asset-quality-gates/references/external-provenance-gstack-main.md) (full functional coverage matrix)

> gstack's `/gstack-upgrade` (silent self-update), `/setup-gbrain` (vector DB daemon), `/setup-browser-cookies` (cookie decryption) — features with security/compliance risks are **explicitly excluded**; see provenance file for rationale.

### 3. Clean-room Philosophy Absorption

The **design philosophy and directory conventions** of the following are clean-room absorbed; no source copy:

- **[VS Code Agent Customization docs](https://code.visualstudio.com/docs/copilot/copilot-chat)** — authoritative basis for every entry point. Goal: **perfectly align with official setup guide**.
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** / **Claude Design** — clean-room absorption of Anthropic's "project-level AI protocol file" paradigm (`CLAUDE.md`). This repo's `CLAUDE.md` honours this paradigm; the "Project DRI protocol" design philosophy is influenced by Claude Code's "agentic coding with guardrails" concept.
- **[GitHub Spec Kit](https://github.com/github/spec-kit)** / [gistdotdev spec-kit](https://github.com/gistdotdev/spec-kit) — inspired the "requirement → executable contract" decomposition in `/specs-write`.

### 4. Methodology References (Books & Ideas)

- **[EARS Notation](https://alistairmavin.com/ears/)** (Alistair Mavin), **[BDD](https://en.wikipedia.org/wiki/Behavior-driven_development)** (Dan North), **[TDD: By Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/)** (Kent Beck), **[GOOS](https://www.informit.com/store/growing-object-oriented-software-guided-by-tests-9780321503626)** (Freeman & Pryce), **[Debugging: 9 Rules](https://debuggingrules.com/)** (Agans), **[The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)** (Thomas & Hunt), **DRI culture** (Apple / Tesla), **[Contributor Covenant](https://www.contributor-covenant.org/)**.

### External Asset Intake Protocol

This repo maintains a strict **external asset intake protocol** (6-step + R-CHK-10~15) via `/asset-quality-gates` skill: any external asset must pass quarantine, license compatibility, frontmatter adaptation, eval seeding, AGENTS.md indexing, and user approval before entering the enabled path. See [`.github/skills/asset-quality-gates/protocols/intake-protocol.md`](./.github/skills/asset-quality-gates/protocols/intake-protocol.md). This is the institutional guarantee of "honest external attribution".

### Boundary Statement

This repo is **not** a fork or wrapper of [Cursor](https://cursor.com/) / [Cline](https://github.com/cline/cline) / [Roo Code](https://github.com/RooCodeInc/Roo-Code) / [Aider](https://aider.chat/) / [Continue](https://www.continue.dev/) / [Cody](https://sourcegraph.com/cody). It targets GitHub Copilot exclusively.

## Honest Statement · Known Limitations

This repo pursues "high autonomy requires high audit" and "quality first", but **candidly acknowledges the following limitations**. This is honest engineering stance, not marketing.

### Design Philosophy

- **Still evolving**: Core methodology (DRI / three Gates / DOM / 14-surface audit / 14-layer drift defense) is distilled from solo independent development practice; **not yet validated long-term in large teams / complex distributed systems / heavily-regulated industries (finance / healthcare)**.
- **Potentially over-engineered**: "Symmetric aesthetics" numbers like 14/14 may bring process overhead exceeding benefit in some scenarios. Small teams / solo projects should self-prune.
- **Steep terminology curve**: DRI / DOM / SSOT / Pause-and-Ask / Gate A-B-C are dense; newcomer onboarding cost is non-trivial.

### Process Loop

- **Limited validation samples**: The full seven-piece spec contract (`/specs-write` → `/specs-execute`) is mainly proven in Chinese solo projects; **English projects, cross-border collaboration, multi-person concurrent spec scenarios are under-validated**.
- **Cross-agent compat is one-way bridge**: `CLAUDE.md` is only an entry pointer for Claude Code / Cursor / Windsurf; **no guarantee** these agents fully reproduce VS Code Copilot's skill triggering, instruction applyTo, hook interception.
- **Hook interception depends on host**: `.github/hooks/safety-guard.json` PreToolUse interception depends on VS Code Copilot's hook mechanism; if user disables Autopilot advanced evaluator, **catastrophic command fallback relies entirely on this repo's PowerShell script**, with theoretical bypass risk.

### Usability

- **Chinese-first**: Protocol body and most skills are Chinese; **non-Chinese international users face higher barrier**. `README.en.md` is a translation reference; most skills still need translation.
- **GSAP skills are direct translations**: 8 gsap-* skills are directly migrated from GSAP official docs; **no content-level localization innovation or Chinese scenario adaptation** — essentially official docs in Chinese + AGENTS.md indexing.
- **Windows / PowerShell bias**: Many DoD commands assume Windows + PowerShell (e.g. `.\venv\Scripts\python.exe`); macOS / Linux users need to adapt.

### Maintenance

- **Solo maintainer primarily**: Project is currently advanced by maintainer via AI collaboration; **60+ skills have uneven coverage depth**; dead links, stale references, contradictory corner cases may exist.
- **Pressure to follow official evolution**: VS Code Copilot Agent Customization is still rapidly evolving; entry-point APIs may change; this repo's sync speed depends on maintainer bandwidth.
- **No automated tests**: This is a pure asset repo; **no automated test suite for skill trigger accuracy or instruction load correctness** (`/skill-eval` provides a manual eval framework, but not CI-ified).

### How We View These Limitations

We don't dodge or sugarcoat. If you encounter specific problems from these limitations, **feel free to give candid feedback in [Issues](../../issues)** — especially "this is over-engineered" or "this fails in large teams" type **negative feedback** is most valuable to us.

## Contributing

This is a **long-term maintained, community-driven** open-source project. We welcome:

- 🐛 **Bug reports & suggestions**: via [GitHub Issues](../../issues); please search first.
- 🔀 **Pull Requests**: protocol additions, new Skills, English translation, cross-agent compatibility. Read [`CONTRIBUTING.md`](./CONTRIBUTING.md) first.
- 🌐 **Internationalization**: translations to English / Japanese / Korean are welcome. This project is **Chinese-first** but welcomes bilingual coexistence.
- 💡 **Use-case sharing**: using this repo in your project? Share scenarios and suggestions in [Discussions](../../discussions).
- ⭐ **Star & Fork**: if this repo helps you, starring helps others find it.

**Contribution principles** (details in [`CONTRIBUTING.md`](./CONTRIBUTING.md)):

1. **Chinese-first, internationally open** — protocol body in Chinese; issue / PR / commit message accept bilingual.
2. **Clean-room absorption** — external concepts must be rewritten into Chinese protocol with explicit acknowledgement; **direct source code copy is prohibited**.
3. **DRI culture** — every PR must have a clear author and verifiable DoD.
4. **Spec-first** — large changes go through `/specs-write`; "prompt-piling" PRs are rejected.

**Maintenance cadence**: iterates alongside VS Code Copilot Agent Customization official evolution; semantic versioning in [`CHANGELOG.md`](./CHANGELOG.md).

## License

[MIT License](./LICENSE) © 2026 海口秀英区洞悉人工智能应用软件工作室 (Haikou Xiuying District Dongxi AI Application Software Studio)

> **Copyright holder / registration entity**: 海口秀英区洞悉人工智能应用软件工作室
> **Unified Social Credit Code**: 92460000MAK66KH20N
>
> Detailed attribution rules in [`.github/instructions/compliance.instructions.md`](./.github/instructions/compliance.instructions.md) and [`NOTICE`](./NOTICE).

---

**Let Copilot be your project's chief responsible individual, not just an assistant.** 🚀
