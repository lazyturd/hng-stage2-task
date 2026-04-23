# hng14-stage2-devops

# HNG14 Stage 2: Containerized Job Processing Stack

This repository contains a containerized job processing system consisting of a Node.js frontend, a FastAPI backend, a Python background worker, and a Redis message broker. It includes a full CI/CD pipeline implemented via GitHub Actions.

## Prerequisites
To run this application from scratch on a clean machine, ensure you have the following installed:
* **Git** (to clone the repository)
* **Docker** (v20.10+ recommended)
* **Docker Compose** (v2.0+ recommended)

No local Python or Node.js environments are required, as everything runs within isolated containers.

## Bringing the Stack Up

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/hng14-stage2-devops.git](https://github.com/YOUR_USERNAME/hng14-stage2-devops.git)
   cd hng14-stage2-devops

Configure Environment Variables:
A template file .env.example is provided. Create your local .env file from this template:

Bash
cp .env.example .env
(Note: The default values in the example file will work out-of-the-box for local testing).

Build and Start the Containers:
Execute the following command to build the multi-stage images and start the services in the background:

Bash
docker-compose up -d --build
What a Successful Startup Looks Like
The docker-compose.yml file is configured with strict dependency checks. Services will wait for their dependencies to become healthy before starting.

Check Container Status:
Run docker ps. You should see 4 containers running, and after about 10-15 seconds, all of them should display a (healthy) status:

hng14-stage2-devops-frontend-1 (Port 3000)

hng14-stage2-devops-worker-1

hng14-stage2-devops-api-1 (Port 8000)

hng14-stage2-devops-redis-1 (Internal only)

Access the Application:

Open your web browser and navigate to http://localhost:3000. You will see the Job Processor Dashboard.

Click Submit New Job. The UI will display "Submitted: [UUID]" and begin polling.

After a few seconds, the status will automatically update from pending (or queued) to completed.

Verify Logs:
To watch the background worker process the jobs in real-time, run:

Bash
docker-compose logs -f worker
You should see output similar to:

Plaintext
Processing job 123e4567-e89b-12d3-a456-426614174000
Done: 123e4567-e89b-12d3-a456-426614174000
Teardown
To cleanly stop the application and remove the containers, networks, and default volumes, run:

Bash
docker-compose down
