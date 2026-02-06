Project Pixo: Master Design Document
Version: 1.0 (Locked) Status: Pre-Phase 1 Execution Date: 2026-02-06

1. Project Identity & Core Doctrine
Identity: Pixo is a WhatsApp-native, privacy-first personal agent. It is designed to be "invisible"—removing friction rather than adding it.

Core Philosophy:

Reality Is The Spec: We prioritize user experience and behavior over clean code architecture. If it works for the user, it is correct.

Trust > Growth: We reject any feature that feels "creepy" (e.g., silent monitoring, unprompted messaging).

Replace, Don't Refactor: We do not patch individual lines of code. We replace entire modules atomically to ensure consistency.

Thin Backend: The Python layer is a "dumb" pipe. Intelligence resides in the Model (LLM), and State resides in the Database.

2. Operating Constraints (The "Red Lines")
NO Third-Party Wrappers: We strictly use the Official Meta Cloud API. No Twilio, Wati, or unauthorized tools.

NO "App" Dependencies: Pixo is a WhatsApp Contact. There is no Android/iOS app to download.

NO Silent Data Collection: Pixo only remembers what is explicitly stated or contextually necessary.

NO Training on User Data: User messages are control signals, not datasets for training.

NO Auto-Pilot: Pixo never sends a message to a third party or spends money without an explicit user_confirm=True signal.

3. Capabilities & Success Metrics
Action Space
Cognitive: Always-on drafting, planning, simplifying, and reasoning.

Memory (Opt-In): Storing structured facts (e.g., "My gate code is 1234").

Delegated Action: Sending messages strictly after user confirmation.

Success Targets
The "No-Prompting" Standard: The user speaks naturally; Pixo figures out the intent.

The "Trust-Action" Barrier: The user trusts Pixo enough to let it draft high-stakes messages.

The "Silent Fix": Pixo never makes the same mistake twice for the same user.

4. Technical Architecture (The Stack)
Infrastructure (Zero-Cost Start)
Hosting: Render (Free Tier) + UptimeRobot (Keep-Alive Ping).

Database: Supabase (Free Tier) – PostgreSQL + pgvector.

Intelligence: Google Gemini 1.5 Flash (Free Tier) via AI Studio.

Transport: Meta Cloud API (Free Tier for first 1,000 conversations).

The Security Shield (4 Layers)
Doorway (Layer 1): HMAC Signature Verification. The server rejects any request lacking a valid cryptographic signature from Meta.

Brain (Layer 2): Prompt Hardening. System prompts include "Immutable Identity" blocks to resist injection attacks.

Vault (Layer 3): PII Hashing. Phone numbers are stored as SHA256 hashes. Raw logs are auto-expired.

Circuit Breaker (Layer 4): Human-in-the-Loop (HITL). Hard-coded requirement for user confirmation before external API calls.

5. Repository Structure (Canonical)
This structure is forward-compatible. We build this skeleton in Phase 1 and populate it over time.

Plaintext
pixo-core/
├── .env                    # [Security] Secrets (Gitignored)
├── .gitignore              # [Security] Blocked files
├── DOCTRINE.md             # [Reference] This document
├── requirements.txt        # Python Dependencies
├── run.py                  # Entry point (Starts the server)
│
├── app/                    # Application Logic
│   ├── __init__.py
│   ├── main.py             # FastAPI App & Webhook Entry
│   │
│   ├── core/               # Configuration & Security
│   │   ├── __init__.py
│   │   ├── config.py       # Load .env variables
│   │   └── security.py     # HMAC Verification Logic
│   │
│   ├── services/           # External Integrations
│   │   ├── __init__.py
│   │   ├── whatsapp.py     # Meta API (Send/Receive)
│   │   ├── llm.py          # Gemini Interface
│   │   ├── memory.py       # (Phase 4) Vector DB Interface
│   │   └── tools.py        # (Phase 4) Action Tools
│   │
│   ├── routing/            # The Brain Strategy
│   │   ├── __init__.py
│   │   └── router.py       # Logic: Intent Classifier -> Model Selection
│   │
│   └── db/                 # Database Layer
│       ├── __init__.py
│       ├── session.py      # Connection Logic
│       ├── models.py       # SQL Tables (Users, Memories)
│
└── tests/                  # Quality Assurance
    ├── __init__.py
    └── boundary_check.py   # The "Torture Suite" (Edge Case Testing)
6. Implementation Phases (The Roadmap)
PHASE 1: Exposure ("Hello World")
Goal: Connect WhatsApp → Server → Reply. No AI yet.

Key Files: main.py, core/security.py, services/whatsapp.py.

Validation: Pixo replies "Signal Received" to a real WhatsApp message.

PHASE 2: The Brain (Intelligence)
Goal: Connect Gemini API. Enable conversation.

Key Files: services/llm.py, routing/router.py.

Validation: Pixo can answer general knowledge questions.

PHASE 3: Reliability ("The Vault")
Goal: Database integration & Persistence.

Key Files: db/session.py, db/models.py.

Tech: Initialize PostgreSQL with PII hashing.

Validation: User data survives a server restart.

PHASE 4: Tooling (Agentic Capabilities)
Goal: Long-term Memory and Actions.

Key Files: services/memory.py, services/tools.py.

Tech: Enable pgvector for memory retrieval.

Validation: Pixo remembers a fact ("Gate code") and drafts a message.

PHASE 5: Monetization
Goal: Revenue generation.

Key Files: services/payment.py.

Strategy: "Privacy Tier" (Paid users routed to Private APIs).

Validation: First successful Stripe transaction.

PHASE 6: Sovereignty ("The End Game")
Goal: Full independence from Google.

Strategy: Replace Gemini API with self-hosted Llama 3 on rented GPU servers.

Validation: Pixo runs without a single external AI API call.

7. Development Methodology
AI-First, Human-Veto: The AI plans and writes code; the Human reviews and deploys.

Atomic Replacement: Files are rewritten entirely, not patched.

Boundary Testing: Every update must pass the tests/boundary_check.py suite.

End of Document