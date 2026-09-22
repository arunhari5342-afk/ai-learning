# Agent Architecture

## Overview

The Day 2 agent uses a native LLM tool-calling architecture.

The LLM receives a user request and a list of available tools. It decides
whether a tool is required. When a tool is selected, the application validates
the arguments, executes the tool, returns the observation to the LLM, and
continues the loop until a final answer is produced.

---

## Architecture

```text
User
  |
  v
Agent Runner
  |
  v
LLM
  |
  +--------------------+
  |                    |
  | No tool required   | Tool required
  |                    |
  v                    v
Final Answer       Tool Call
                       |
                       v
                Argument Validation
                       |
                       v
                  Tool Executor
                       |
                       v
                   Observation
                       |
                       v
                      LLM
                       |
                       v
                 Final Answer