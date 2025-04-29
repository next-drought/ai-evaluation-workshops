ifeq (,$(wildcard .env))
$(error .env file is missing. Please create one based on .env.example. Run: "cp .env.example .env" and fill in the missing values.)
endif

include .env

# --- Default Values ---

CHECK_DIRS := .

PHILOSOPHER_ID = "plato"
QUERY = "When and where were you born? Also tell me more about your life, work and beliefs."

EVALUATION_DATASET_NAME = "odsc-2025-evaluation-playbook-slim-dataset"

# --- Utilities ---

help: # Display this help message with available commands
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# --- Infrastructure --- 

local-infrastructure-up: # Start local infrastructure services using Docker Compose
	docker compose -f docker-compose.yml up -d

local-infrastructure-down: # Stop and remove local infrastructure services
	docker compose -f docker-compose.yml down

# --- Run ---

create-long-term-memory: # Initialize the long-term memory for the agent
	uv run python -m tools.create_long_term_memory

call-agent: # Query the philosophical agent with a specific question
	TOKENIZERS_PARALLELISM=true uv run python -m tools.call_agent --philosopher-id "$(PHILOSOPHER_ID)" --query "$(QUERY)"

upload-evaluation-dataset: # Upload a dataset for agent evaluation
	uv run python -m tools.upload_evaluation_dataset --dataset-name $(EVALUATION_DATASET_NAME)

evaluate-agent: # Run evaluation tests on the agent using the specified dataset
	uv run python -m tools.evaluate_agent --dataset-name $(EVALUATION_DATASET_NAME) --workers 1 --nb-samples 6

# --- QA ---

format-fix: # Fix code formatting issues using ruff
	uv run ruff format $(CHECK_DIRS)
	uv run ruff check --select I --fix  $(CHECK_DIRS)

lint-fix: # Fix linting issues using ruff
	uv run ruff check --fix $(CHECK_DIRS)

format-check: # Check code formatting without making changes
	uv run ruff format --check $(CHECK_DIRS) 
	uv run ruff check -e $(CHECK_DIRS)
	uv run ruff check --select I -e $(CHECK_DIRS)

lint-check: # Check code for linting issues without making changes
	uv run ruff check $(CHECK_DIRS)
