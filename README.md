
This project is a lightweight, modular chatbot built using FastAPI. It provides a responsive UI with HTML templates and serves chatbot-style responses using structured data from stock exchanges.

The application is containerized with Docker and includes a Makefile for quick development and deployment workflows. It is currently deployed on AWS and accessible at:

**Live URL**: http://63.177.98.101:8000/

---

## Architecture and Design 

### Why FastAPI?

FastAPI was chosen primarily because it allows building APIs quickly and with minimal boilerplate—  
which made it a great fit for a small project with limited scope.

That said, it also offers some solid technical benefits as:
- Asynchronous support out-of-the-box, which is ideal for chat-based interactions
- Lightweight and modular, which makes it easy to scale and maintain
- High performance comparable to Node.js and Go for I/O-bound workloads

---

## How the UI Was Built

The chatbot interface was built using Jinja2 templates, rendered directly by FastAPI. This allowed to serve a clean, single-page HTML interface without needing a full frontend framework like React or Vue.

Main advantages:
- HTML templates are served using FastAPI’s built-in support for Jinja2
- Static assets like CSS and images are handled automatically
- JavaScript powers the message bubbles, user input, and typing animation
- Everything runs as a single-page app backed by FastAPI routes

---

## Running the Application (Using Makefile)

To simplify usage, this project includes a `Makefile` that abstracts away all run logic using Poetry or Docker.

### Prerequisites

Install **either**:

- [Poetry](https://python-poetry.org/docs/#installation) if you'd like to run locally using Python
- [Docker](https://docs.docker.com/get-docker/) if you prefer isolated container execution

---

### Commands via Makefile

```bash
make build            # Build Docker image
make run              # Run container on port 8000
make stop             # Stop and remove container
make logs             # Tail logs from container
make poetry-install   # Install Python dependencies using Poetry
make poetry-run       # Run app locally using Poetry
make poetry-shell     # Open Poetry shell environment
```

Use the `poetry-*` commands if running via Python/Poetry locally, or the default `build`, `run`, etc. for Docker.

---

## Deployment – AWS Setup

The app is deployed on an Amazon EC2 instance running Amazon Linux 2023 using Docker.

## Tooling Choices

### Why Docker?

Used Docker to make the app easy to run and deploy anywhere — whether on a developer's laptop or in the cloud. It wraps everything the app needs (code, dependencies, runtime) into one container, leading to no environment mismatches, no "it works on my machine" issues, and a smoother experience overall.

It also let us deploy the app to AWS in just a couple of steps.

### Why Poetry?

Poetry helped keeping development clean and consistent. It manages all dependencies, handle virtual environments for isolation, and gives simple commands to install and run the app. Compared to old-school `requirements.txt`, Poetry just made everything easier to manage — especially in a team setting.

---
