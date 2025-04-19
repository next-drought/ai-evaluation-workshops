<div align="center">
  <h1>LLM & RAG Evaluation Playbook</h1>
  <h3>A comprehensive guide for evaluating LLMs and RAG systems in production applications</h3>
  <p class="tagline"> <a href="https://odsc.com/speakers/llm-rag-evaluation-playbook-for-production-apps/">ODSC 2025 Webinar by Paul Iusztin</a> - Click to learn more about the webinar and speaker</p>
</div>

This guide will help you set up and run the webinar.

# 📑 Table of Contents

- [📋 Prerequisites](#-prerequisites)
- [🎯 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [🏗️ Set Up Your Local Infrastructure](#-set-up-your-local-infrastructure)
- [⚡️ Running the Code](#️-running-the-code)
- [👀 Qdrant Visualizations](#-qdrant-visualizations)
- [📚 Resources](#-resources)

# 📋 Prerequisites

## Local Tools

For all the modules, you'll need the following tools installed locally:

| Tool | Version | Purpose | Installation Link |
|------|---------|---------|------------------|
| Python | ≥ 3.12 | Programming language runtime | [Download](https://www.python.org/downloads/) |
| uv | ≥ 0.4.30 | Python package installer and virtual environment manager | [Download](https://github.com/astral-sh/uv) |
| GNU Make | ≥ 3.81 | Build automation tool | [Download](https://www.gnu.org/software/make/) |
| Git | ≥2.44.0 | Version control | [Download](https://git-scm.com/downloads) |
| Docker | ≥27.4.0 | Containerization platform | [Download](https://www.docker.com/get-started/) |

<details>
<summary><b>📌 Windows users also need to install WSL (Click to expand)</b></summary>

We will be using Unix commands across the course, so if you are using Windows, you will need to **install WSL**, which will install a Linux kernel on your Windows machine and allow you to use the Unix commands from our course (this is the recommended way to write software on Windows). 

🔗 [Follow this guide to install WSL](https://www.youtube.com/watch?v=YByZ_sOOWsQ).
</details>

## Cloud Services

Also, the course requires access to these cloud services. The authentication to these services is done by adding the corresponding environment variables to the `.env` file:

| Service | Purpose | Cost | Environment Variable | Setup Guide |
|---------|---------|------|---------------------|-------------|
| [Opik](https://rebrand.ly/philoagents-opik) | LLMOps | Free tier (Hosted on Comet - same API Key) | `COMET_API_KEY` | [Quick Start Guide](https://rebrand.ly/philoagents-opik-quickstart) |
| [OpenAI API](https://openai.com/index/openai-api/) | LLM API used for evaluation | Pay-per-use | `OPENAI_API_KEY` | [Quick Start Guide](https://platform.openai.com/docs/quickstart) |

# 🎯 Getting Started

## 1. Clone the Repository

Start by cloning the repository and navigating to the `philoagents-api` project directory:
```
git clone https://github.com/decodingml/workshops.git
cd workshops/odsc-2025-evaluation-playbook/template
```

Next, we have to prepare your Python environment and its dependencies.

## 2. Installation

We will use `uv` to install the dependencies and activate the virtual environment:

```bash
uv sync
```

Test that you have Python 3.12.7 installed in your new `uv` environment:
```bash
uv run python --version
# Output: Python 3.12.7
```

This command will:
- Create a virtual environment with the Python version specified in `.python-version` using `uv`
- Activate the virtual environment
- Install all dependencies from `pyproject.toml`

## 3. Environment Configuration

Before running any command, inside the `philoagents-api` directory, you have to set up your environment:
1. Create your environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure the required credentials following the inline comments and the recommendations from the [Cloud Services](#-prerequisites) section.

# 📁 Project Structure

The project follows a clean architecture structure commonly used in production Python projects:

```bash
philoagents-api/
    ├── data/                       # Data files
    ├── src/evaluation_playbook/    # Python package
    ├── tools/                      # Entrypoint scripts that use the Python package
    ├── .env.example                # Environment variables template
    ├── .python-version             # Python version specification
    ├── docker-compose.yml          # Docker compose hosting Qdrant through Docker
    ├── Makefile                    # Project commands
    └── pyproject.toml              # Project dependencies
```

# 🏗️ Set Up Your Local Infrastructure

We use Docker to set up the local infrastructure (Game UI, Agent API, MongoDB).

> [!WARNING]
> Before running the command below, ensure you do not have any processes running on ports `6333` (Qdrant).

From the root `odsc-2025-evaluation-playbook/template` directory, to start the Docker infrastructure, run:
```bash
make local-infrastructure-up
```

From the root `odsc-2025-evaluation-playbook/template` directory, to stop the Docker infrastructure, run:
```bash
make local-infrastructure-down
```

# ⚡️ Running the Code

The project provides several make commands to interact with the philosophical agent and run evaluations:

## 1. Initialize Long-Term Memory

Before using the agent, you need to initialize its long-term memory:

```bash
make create-long-term-memory
```

## 2. Query the Agent

You can interact with the philosophical agent using the `call-agent` command. By default, it uses Plato as the philosopher and asks about his birth:

```bash
make call-agent
```

You can customize the philosopher and query using variables:

```bash
make call-agent PHILOSOPHER_ID="aristotle" QUERY="What is your view on ethics?"
```

## 3. Run Evaluations

To evaluate the agent's performance, first upload an evaluation dataset:

```bash
make upload-evaluation-dataset
```

You can specify a custom dataset name:
```bash
make upload-evaluation-dataset EVALUATION_DATASET_NAME="my-custom-dataset"
```

Then run the evaluation:

```bash
make evaluate-agent
```

The evaluation runs with 2 workers and 2 samples by default. You can customize the dataset:

```bash
make evaluate-agent EVALUATION_DATASET_NAME="my-custom-dataset"
```

## 4. Help

For help on all the supported commands, run:

```bash
make help
```

# 👀 Qdrant Visualizations

Type in your browser `localhost:6333/dashboard` to access [Qdrant's Dashboard](localhost:6333/dashboard).

Visualize:
```
{
  "limit": 500,
   "filter": {
        "must": [
            { "key": "metadata.philosopher_id", "match": { "value": "plato" } }
        ]
    }
}
```

Graph
```
{
  "sample": 400,
  "filter": {
        "must": [
            { "key": "metadata.philosopher_id", "match": { "value": "plato" } }
        ]
    }
}
```

# 📚 Resources

Continue your learning journey with our [**PhiloAgents Course**](https://github.com/neural-maze/philoagents-course).

Other useful resources:
- [Opik Documentation](https://www.comet.com/docs/opik/)
- [🚀 LangGraph Quickstart](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- [Qdrant Installation](https://qdrant.tech/documentation/guides/installation/)
- [Qdrant Quickstart](https://qdrant.tech/documentation/quickstart/)
- [Qdrant LangChain](https://python.langchain.com/docs/integrations/vectorstores/qdrant/)


