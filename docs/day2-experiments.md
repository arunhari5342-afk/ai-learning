# Day 2 Agent Experiments

## Objective

The objective of Day 2 was to understand and implement an agent loop using
native LLM tool calling, followed by controlled experiments covering tool
descriptions, agent planning strategies, temperature, and tool execution.

---

## Experiment 1 — Tool Description Quality

### Objective

Compare agent behavior using poor versus clear tool descriptions.

### Setup

The agent was tested with 10 prompts.

Two tool-description configurations were compared:

1. Poor/minimal descriptions
2. Clear descriptions explaining when and why each tool should be used

### Observation

Clear tool descriptions provide the model with better information about tool
purpose and usage. This improves the model's ability to select an appropriate
tool and provide the correct arguments.

### Result

The experiment demonstrated that tool descriptions are an important part of
agent and tool design.

---

## Experiment 2 — ReAct vs Plan-and-Execute

### Objective

Compare two agent reasoning strategies.

### Strategies

- ReAct: Thought → Action → Observation loop
- Plan-and-Execute: create a plan first and then execute the required steps

### Test Set

5 multi-step tasks were evaluated.

### Observation

ReAct provides incremental decision making because each observation can affect
the next action.

Plan-and-Execute separates planning from execution and can be useful when the
overall task structure is known in advance.

### Result

Both approaches demonstrate different trade-offs between dynamic reasoning
and explicit planning.

---

## Experiment 3 — Temperature

### Objective

Observe the effect of temperature on agent responses.

### Configuration

- Temperature 0.0
- Temperature 0.7
- 5 runs for each configuration

### Observation

Lower temperature produces more deterministic responses, while a higher
temperature allows greater variation between runs.

For tool-using agents, lower temperature can be useful when predictable tool
selection and repeatability are important.

---

## Experiment 4 — Sequential vs Parallel Tool Calls

### Objective

Compare sequential and parallel execution of independent tools.

### Sequential

Tools are executed one after another.

Advantages:

- Simple control flow
- Easy debugging
- Straightforward error handling

Disadvantage:

- Independent operations may increase total execution time when run
  unnecessarily one after another.

### Parallel

Independent tools can be executed concurrently.

Advantages:

- Potentially lower latency
- Better utilization when multiple independent operations are required

Disadvantages:

- More complex execution logic
- More complicated error handling

### Result

Parallel execution is useful when tool calls are independent, while sequential
execution is simpler when later actions depend on earlier observations.

---

## Agent Reliability Features

The refactored agent includes:

- Maximum step limit
- Tool argument validation
- Tool execution error handling
- Retry handling
- Timeout protection
- Thought/Action/Observation logging

---

## Refactoring Result

The original notebook agent loop was separated into reusable modules:

```text
src/
└── agent_core/
    ├── __init__.py
    ├── agent.py
    ├── tools.py
    └── schemas.py