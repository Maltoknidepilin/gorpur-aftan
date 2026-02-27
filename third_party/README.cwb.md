# CWB source inputs for Docker build

The backend Dockerfiles (`Dockerfile` and `Dockerfile.prod`) compile CWB from MMG source folders using the same flags/steps as the previous MMG setup.

Current source paths (relative to workspace root):

- `MMG/docker/korp-docker/cwb-3.5.0-src/`
- `MMG/docker/korp-docker/cwb-code-r1901-perl-trunk-CWB/`

Note: backend image builds use workspace-root Docker build context so these paths are available during `COPY`.

## Recommended version policy

- Use release source as the default production baseline.
- Only switch to trunk when you need a specific fix.
- If using trunk, pin to a specific revision for reproducibility.

Example (pinned trunk checkout):

```bash
svn checkout -r <REVISION> https://svn.code.sf.net/p/cwb/code/ cwb-code
```
