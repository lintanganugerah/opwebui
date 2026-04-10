<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# docs

## Purpose

Project documentation for ARSA. Contains guides for contributors, security policy, deployment configuration, and workflow diagrams. These files live alongside the source code and are referenced by GitHub issue templates, pull request templates, and community onboarding flows.

## Key Files

| File | Description |
|------|-------------|
| `CONTRIBUTING.md` | Contribution guide covering issue reporting, pull request workflow, i18n translation process, and scope of support. Referenced by GitHub community files. |
| `SECURITY.md` | Security policy defining supported versions, vulnerability reporting rules, PoC requirements, and disclosure policy. Last updated 2026-03-20. |
| `README.md` | Project workflow diagram rendered via Mermaid, showing the development and release process visually. |
| `apache.md` | Guide for hosting ARSA and Ollama on separate servers behind an Apache reverse proxy, including SSL setup with certbot. |

## Subdirectories

None. All documentation files are at the top level of this directory.

## For AI Agents

### Working In This Directory

- These are human-facing markdown documents. When updating them, match the existing tone and formatting conventions.
- `SECURITY.md` has strict content rules (vulnerability reporting requirements). Do not soften or rephrase its policy language.
- `CONTRIBUTING.md` references paths like `src/lib/i18n/locales` and external repos like `arsa/docs`. Verify those paths still exist before editing references.
- The Mermaid diagram in `README.md` is encoded as a pako-compressed URL. To update it, edit the source at mermaid.live and replace both the image URL and the edit link.

### Testing Requirements

- No automated tests for documentation files.
- Verify markdown renders correctly after edits (links, tables, callout blocks).
- Cross-check that referenced file paths and URLs are valid.

### Common Patterns

- GitHub-flavored markdown with admonition blocks (`> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]`).
- External documentation lives in a separate repository at `github.com/lintanganugerah/docs`. This directory only contains in-repo docs.
- Security policy uses numbered rules with bold headings.

## Dependencies

### Internal

- `src/lib/i18n/locales/` referenced by `CONTRIBUTING.md` for translation file paths.
- Root `README.md` and `.github/` issue/PR templates link to `CONTRIBUTING.md` and `SECURITY.md`.

### External

- External documentation site: `docs.arsa.com` (separate repository at `github.com/lintanganugerah/docs`).
- GitHub Security Advisories for vulnerability reporting.
- Ollama documentation and FAQ referenced in `apache.md`.
