# disk-check

![CI](https://github.com/theprajwalm/disk-check/actions/workflows/ci.yml/badge.svg)

A small Python disk checker with a full CI pipeline: every push is tested automatically, and only tested code is built into a Docker image.

## What it does

`app.py` reads how full the root filesystem (`/`) is and reports a status:

| Disk usage | Status |
| --- | --- |
| below 75 % | `OK` |
| 75 % to 89.9 % | `WARNING` |
| 90 % and above | `CRITICAL` |

Example output:

```
Disk usage on /: 13.9% -> OK
```

The status logic (`classify()`) is a pure function, separate from the disk reading, so it can be tested without filling up a real disk.

## Run it locally

```bash
python3 app.py
```

## Run the tests

```bash
sudo apt install python3-pytest
python3 -m pytest -v
```

The tests cover normal values, the boundary values 75 and 90, and invalid input (values outside 0–100 raise a `ValueError`).

## Run it with Docker

```bash
docker build -t disk-check .
docker run --rm disk-check
```

The image is based on `python:3.12-slim`, contains only `app.py`, and runs as a non-root user.

## CI pipeline

Defined in `.github/workflows/ci.yml`, triggered on every push to `main` and on every pull request.

```
git push  ->  Job 1: test (pytest)  ->  passed?  ->  Job 2: build (docker build + run)
                                          |
                                          no  ->  red X, build skipped
```

- **test**: checks out the code, sets up Python 3.12, installs pytest and runs the tests.
- **build**: builds the Docker image and runs it once. It has `needs: test`, so it only runs if all tests pass.

Each step's exit code decides the result: `0` means success, anything else fails the job.

## Project structure

```
disk-check/
├── app.py                    # the disk checker
├── test_app.py               # pytest tests
├── Dockerfile                # image recipe
├── .gitignore
└── .github/workflows/ci.yml  # CI pipeline
```

## Next steps

- Push the image to a container registry (GitHub Container Registry or a self-hosted Forgejo registry)
- Add a linter step (e.g. `ruff`) before the tests
- Move the pipeline to Forgejo Actions on a self-hosted Forgejo instance
