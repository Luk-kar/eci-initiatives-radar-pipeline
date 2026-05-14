# 🔄 Workflows

This directory contains the CI/CD automation for the ECI pipeline project.
The workflow is written for **GitHub Actions** but the logic is provider-agnostic —
every step **should** map directly to an equivalent in GitLab CI, Bitbucket Pipelines, or
any other runner-based system. The YAML comments inside `run_pipeline.yml` document
each mapping explicitly.

## What the workflow does

`run_pipeline.yml` runs the full end-to-end pipeline on a schedule (every Saturday)
or manually on demand:

| Step | What happens |
|------|-------------|
| 0 | Checkout the pipeline repo |
| 1 | Restore cached Python virtual environments |
| 2 | Set up `data_pipeline` and `page_creator` environments via `commands/set_up_enviro.sh` |
| 3 | Random short delay to stagger load on shared runners |
| 4 | Run all 9 pipeline stages via `commands/run_pipeline.sh` |
| 5 | Resolve the latest data run directory via `commands/give_path_latest_data.sh` |
| 6 | Compress the run directory into a `.tar.gz` artifact |
| 7 | Upload the archive (kept 30 days, downloadable from the Actions run page) |
| 8 | Checkout the dashboard repo (`eci-initiatives-radar-dashboard`) |
| 9 | Sync `page_to_export/` into the dashboard repo via `rsync` |
| 10 | Open a Pull Request in the dashboard repo with a link back to this run |

Any step failure is critical — the job stops immediately.

## One-time setup

*(As of 14.02.2026)*

### 1. Create a Personal Access Token (PAT)

Go to **GitHub → Settings → Developer settings → Personal access tokens →
Fine-grained tokens → Generate new token** and configure:

- **Token name:** `eci-dashboard-deploy`
- **Description:** `Allows the eci-initiatives-radar-pipeline workflow to push updates and open PRs in the dashboard repo.`
- **Expiration:** 1 year (set a calendar reminder to rotate it)
- **Repository access:** only `eci-initiatives-radar-dashboard`
- **Minimum Permissions:** `Contents` → Read and write, `Pull requests` → Read and write

### 2. Add the PAT as a repository secret

Go to **`pipeline repo` → Settings → Secrets and variables → Actions →
New repository secret**:

- **Name:** `DASHBOARD_REPO_PAT`
- **Value:** the token from step 1

### 3. Add the PR label in the dashboard repo

Go to **`eci-initiatives-radar-dashboard` → Issues → Labels → New label**
and create a label named `automated-pr`.

### 4. Configure GitHub Pages

Go to **`eci-initiatives-radar-dashboard` → Settings → Pages →
Build and deployment → Deploy from a branch** and select **`update-dashboard-html`** and the **`/docs`** folder.

## Porting to another provider

The three shell scripts in `commands/` contain no GitHub-specific logic —
they are plain Bash and run identically on any Linux runner.
Only the workflow YAML is provider-specific. Each GitHub Actions concept
has a direct equivalent; see the dictionary at the top of `run_pipeline.yml`
for the full mapping to GitLab CI terms.

```
GitHub Actions            GitLab CI equivalent
─────────────────────     ────────────────────────────────
on: / schedule:           rules: / schedule:
runs-on:                  image: / tags:
actions/cache             cache: paths:
actions/upload-artifact   artifacts: paths: + expire_in:
create-pull-request       glab mr create (CLI v18.11)
secrets.*                 CI/CD variable (masked + protected)
```
