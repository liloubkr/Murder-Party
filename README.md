# Alibi

A murder-mystery chatbot game. You are the detective: interrogate suspects in free conversation,
cross-check their statements, collect clues in your notebook, then accuse the culprit with
evidence. Each suspect is an LLM agent that only knows its own truth; confessions, key clues and
forbidden reveals are controlled by the game engine, not by the model. After each case, a
recommender suggests the next scenario matched to your skill and tastes.

> Status: under construction.

## Requirements

- Python 3.11
- A free [Groq](https://console.groq.com) API key, or a local [Ollama](https://ollama.com) install

## Installation

```bash
git clone https://github.com/liloubkr/Murder-Party.git
cd Murder-Party
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt --extra-index-url https://download.pytorch.org/whl/cpu
cp .env.example .env   # then fill in the values
```

## Configuration

| Variable | Role |
|---|---|
| `LLM_PROVIDER` | `groq` or `ollama` |
| `GROQ_API_KEY` | Groq API key (secret) |
| `GROQ_MODEL` / `OLLAMA_MODEL` | Exact model identifiers |
| `OLLAMA_BASE_URL` | Default `http://localhost:11434/v1` |
| `LLM_TEMPERATURE` | 0.3-0.5 recommended (default 0.4) |
| `LLM_TIMEOUT_SECONDS` | Request timeout (default 30) |
| `MAX_REGENERATIONS` | Regenerations after an accidental contradiction (default 1) |
| `LLM_CACHE` / `LLM_CACHE_DIR` | Disk cache of LLM answers (`on` in dev/tests, `off` in demo) |
| `DB_PATH` | SQLite database file |
| `INTENT_MODEL_PATH` | Trained intent classifier artefact |

## Usage

Coming soon.

## Development

```bash
ruff check . && ruff format --check . && pytest
```

Branches: `main` (stable), `dev` (integration), `feature/<issue>-<short-name>` (one per issue).
Open pull requests against `dev`.

## Credits

Some scenarios are adapted from MuSR (Sprague et al., 2024), licensed CC BY 4.0.
