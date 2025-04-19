ifeq (,$(wildcard .env))
$(error .env file is missing. Please create one based on .env.example. Run: "cp .env.example .env" and fill in the missing values.)
endif

include .env

# --- Default Values ---

CHECK_DIRS := .

PHILOSOPHER_ID = "plato"
QUERY = "When and where were you born?"

EVALUATION_DATASET_NAME = "odsc-2025-evaluation-playbook-slim-dataset"

# --- Utilities ---

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# --- Infrastructure --- 

local-infrastructure-up:
	docker compose -f docker-compose.yml up -d

local-infrastructure-down:
	docker compose -f docker-compose.yml down

# --- Run ---

create-long-term-memory:
	uv run python -m tools.create_long_term_memory

call-agent:
	TOKENIZERS_PARALLELISM=true uv run python -m tools.call_agent --philosopher-id $(PHILOSOPHER_ID) --query $(QUERY)

upload-evaluation-dataset:
	uv run python -m tools.upload_evaluation_dataset --dataset-name $(EVALUATION_DATASET_NAME)

evaluate-agent:
	uv run python -m tools.evaluate_agent --dataset-name $(EVALUATION_DATASET_NAME) --workers 2 --nb-samples 2

# --- QA ---

format-fix:
	uv run ruff format $(CHECK_DIRS)
	uv run ruff check --select I --fix  $(CHECK_DIRS)

lint-fix:
	uv run ruff check --fix $(CHECK_DIRS)

format-check:
	uv run ruff format --check $(CHECK_DIRS) 
	uv run ruff check -e $(CHECK_DIRS)
	uv run ruff check --select I -e $(CHECK_DIRS)

lint-check:
	uv run ruff check $(CHECK_DIRS)
