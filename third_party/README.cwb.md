# CWB source inputs for Docker build

The backend Dockerfiles (`Dockerfile` and `Dockerfile.prod`) compile CWB from
the `MMG/corpus_workbench` folder using the same flags and steps as the previous
MMG setup.

Current source paths (relative to workspace root):

- `MMG/corpus_workbench/cwb-3.5.0-src/`
- `MMG/corpus_workbench/cwb-code-r1901-perl-trunk-CWB/`

Backend image builds must use the workspace root as their Docker build context
so these paths are available during `COPY`. The deployment Compose files are
already configured this way.

## Recommended version policy

- Use release source as the default production baseline.
- Only switch to trunk when you need a specific fix.
- If using trunk, pin to a specific revision for reproducibility.

Example (pinned trunk checkout):

```bash
svn checkout -r <REVISION> https://svn.code.sf.net/p/cwb/code/ cwb-code
```
