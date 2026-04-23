---

### 2. `FIXES.md`

```markdown
# Application Bug Fixes

The following issues were identified in the source code preventing the application from running in a distributed, containerized environment. Every bug was remediated prior to containerization.

### 1. Hardcoded Redis Connection in API
* **File:** `api/main.py`
* **Line:** 8
* **Issue:** The Redis host was hardcoded to `"localhost"` and port `6379`, and it did not utilize the `REDIS_PASSWORD` from the environment. This prevented the API container from resolving the Redis container on the Docker bridge network.
* **Fix:** Replaced hardcoded values with the `os.getenv()` module to dynamically pull `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASSWORD`. Added fallback defaults to prevent `NoneType` integer casting errors during testing.

### 2. Hardcoded Redis Connection in Worker
* **File:** `worker/worker.py`
* **Line:** 6
* **Issue:** Similar to the API, the worker's Redis client was hardcoded to `localhost`, causing the worker container to look for Redis inside its own isolated environment rather than the shared message broker.
* **Fix:** Applied the identical `os.getenv()` configuration used in the API to allow dynamic connection routing via environment variables.

### 3. Hardcoded API Routing in Frontend
* **File:** `frontend/app.js`
* **Line:** 6
* **Issue:** `const API_URL = "http://localhost:8000";` was hardcoded. Inside a Docker network, the Node.js Express server needs to route requests to the `api` service container name, not localhost.
* **Fix:** Updated the definition to accept an environment variable: `const API_URL = process.env.API_URL || "http://localhost:8000";`, allowing Docker Compose to inject `http://api:8000`.

### 4. Unpinned and Missing Dependencies
* **File:** `api/requirements.txt` & `worker/requirements.txt`
* **Line:** 1-3
* **Issue:** Dependencies like `fastapi`, `uvicorn`, and `redis` lacked version pinning, risking non-deterministic builds and future pipeline failures. Additionally, testing libraries were missing.
* **Fix:** Pinned strict versions for production libraries (e.g., `fastapi==0.103.1`) and created a separate requirement step in the CI/CD pipeline for testing tools (`pytest`, `pytest-cov`, `httpx`, `fakeredis`).

### 5. Frontend Build Failure (NPM CI without Lockfile)
* **File:** `frontend/Dockerfile` (Stage 1) / `frontend/package.json`
* **Issue:** The standard DevOps practice of using `npm ci --omit=dev` inside the Dockerfile failed because the starter code did not include a `package-lock.json` file.
* **Fix:** Switched the build instruction from `npm ci` to `npm install --omit=dev` within the Dockerfile to allow dynamic dependency resolution without requiring a committed lockfile.