# Architecture

## Processing of one player message

```
player message
 -> input_guard         detect cheating / prompt injection (log + in-character refusal)
 -> intent_classifier   label + confidence
 -> evidence check      did the player present evidence? -> engine may break a planned lie
 -> router
      key-clue intent AND canonical answer AND unlock conditions met
        -> canonical answer (optional short in-character rephrase)
      otherwise
        -> suspect agent: persona + own knowledge + statement ledger + rolling memory
           ONE LLM call, JSON output {"reply": str, "claims": [str]}
 -> output_guard        block leaks (culprit identity, forbidden facts)
 -> consistency         NLI: new claims vs sheet + this suspect's ledger
      accidental contradiction -> regenerate once -> safe fallback line
      planned contradiction    -> keep, flag as clue in notebook
 -> statement ledger    store accepted claims (re-injected next turns)
 -> game_engine         notebook, discovered clues, phase, confession gate
 -> storage             log turn + guard / consistency decisions (SQLite)
```

## Layout

| Path | Responsibility |
|---|---|
| `app/streamlit_app.py` | UI only, calls the engine API |
| `alibi/config.py` | Settings from environment |
| `alibi/llm/` | Provider-agnostic client, retries, disk cache |
| `alibi/scenarios/` | Scenario schema, loader, library |
| `alibi/agents/` | Suspect prompt building, persona, rolling memory |
| `alibi/engine/` | Game state, turn pipeline, confessions, statement ledger, consistency |
| `alibi/guards/` | Input and output guards |
| `alibi/nlu/` | Intent classifier and NLI contradiction detector |
| `alibi/recsys/` | Scenario recommendation |
| `alibi/storage/` | SQLite repository |
| `scenarios/` | Game content (YAML) |
| `data/` | Labelled intents and NLI evaluation pairs |
| `eval/` | Detective agent, attack battery, evaluation scripts |
| `gen/` | Optional scenario generation pipeline |
| `models/` | Trained artefacts (not versioned, rebuilt by script) |
