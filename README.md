# kre8 Framework (Demo Repository)

This repository contains the **prototype implementation environment** for the **kre8 Thinking Platform Layer (TPL)**.

The demo repo exists primarily to make development and experimentation easier by allowing all components to run together locally.  
In the intended architecture, each kre8 component will live in **its own repository** and evolve independently.

---

# What is kre8?

**kre8** is a **Thinking Platform Layer (TPL)** designed to sit above infrastructure control planes such as Terraform and cloud APIs.

Instead of directly provisioning infrastructure, kre8 focuses on **understanding intent, reasoning about architecture, and producing structured infrastructure design plans**.

The core philosophy is to **separate thinking from execution**.

Conceptual flow:

User Intent  
↓  
Intent Extraction  
↓  
Design Reasoning (I2D2)  
↓  
Design Plan  
↓  
Render (future)  
↓  
Execution (future)

kre8 therefore acts as a **design intelligence layer for infrastructure platforms**.

---

# Core Concept: Thinking Platform Layer (TPL)

The Thinking Platform Layer performs four major roles:

1. **Intent Understanding**
   - Accept natural language infrastructure intent.
   - Convert intent into structured design inputs.

2. **Design Reasoning**
   - Analyze infrastructure needs.
   - Generate architecture design decisions.

3. **Constraint Enforcement**
   - Apply platform rules and guardrails (kre8_laws).

4. **Structured Output**
   - Produce deterministic design plans.

The TPL does **not directly provision infrastructure**.

It produces **design artifacts** which can later be rendered and executed by infrastructure tooling.

---

# Current Status

Version:

0.01.0

This repository currently contains a **working skeleton implementation** of the kre8 architecture.

Capabilities implemented so far:

- FastAPI ingress for intent requests
- Intent extraction pipeline
- I2D2 orchestration layer
- LLM adapter layer (stub)
- Plan validation pipeline
- Working `/plan` API endpoint

The system currently runs using **stubbed AI responses** to validate architecture and data flow.

Actual LLM integration (AWS Bedrock) will be introduced later.

---

# Repository Structure

This demo repository hosts multiple kre8 components together for development convenience.

Intended production structure:

Each component will eventually live in its **own repository**.

Current demo layout:

```
kre8-framework-demo
│
├── kre8_gate
│   FastAPI ingress layer
│
├── kre8_think
│   Core reasoning engine (Thinking Platform Layer)
│
├── kre8_agent
│   LLM adapter / orchestration layer
│
├── kre8_cli
│   CLI client placeholder
│
├── docs
│   Architecture logs and development notes
│
└── requirements.txt
```

---

# Core Components

## kre8_gate

Entry point for external requests.

Responsibilities:

- Accept HTTP requests
- Forward intent to the thinking layer

---

## kre8_think

The core **reasoning engine** of kre8.

Responsibilities:

- Intent extraction orchestration
- Running the I2D2 design engine
- Applying constraints
- Producing structured design output

---

## I2D2

**Intelligent Infrastructure Design Decision**

Internal design engine responsible for generating infrastructure architecture decisions.

Responsibilities:

- Interpret structured intent
- Generate architecture recommendations
- Produce structured design outputs

---

## kre8_agent

Interface between kre8 and external AI/LLM services.

Responsibilities:

- LLM interaction
- Structured JSON enforcement
- Prompt orchestration

Currently implemented as a **stub agent** for development.

---

# Current Request Flow

The current working pipeline:

curl / API request  
↓  
FastAPI (`kre8_gate`)  
↓  
`i2d2.process_intent()`  
↓  
`intent.extract_intent()`  
↓  
`Kre8Agent.extract_intent()` (stub)  
↓  
StructuredIntent  
↓  
`Kre8Agent.call_llm()` (stub)  
↓  
Plan validation  
↓  
JSON response

This validates the **end‑to‑end architecture** before real LLM integration.

---

# Local Development

Create a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the API:

```
uvicorn kre8_gate.app:app --reload
```

Test using curl:

```
curl -X POST http://127.0.0.1:8000/plan   -H "Content-Type: application/json"   -d '{"intent":"I have two clusters in us-east-1 and us-west-2 and need secure communication between them"}'
```

---

# Future Work

Upcoming development areas:

- Bedrock LLM integration
- Real intent extraction
- DesignPlan generation
- Terraform rendering
- Execution engine
- Infrastructure inventory integration
- Cost modeling

---

# Project Philosophy

kre8 follows a few core principles:

- Separate **thinking from execution**
- Generate **structured design artifacts**
- Enforce **deterministic constraints**
- Expand through **small architecture slices**
- Treat the Thinking Platform Layer as the differentiating system

