myno-core
A structured Python application framework for modularity and architectural excellence.
Python 3.8+ Architecture Modular

myno-core is a highly modular Python application framework designed to separate execution
logic from core business services. This ensures that your system remains scalable, maintainable,
and easy to test as it grows in complexity.

Project Structure

Path Purpose
app/ The Heart: Business logic, service layers, and API definitions.
tests/ Validation: Comprehensive test suites mirroring the app/ structure.
run.py Bootstrap: Main entry point, env setup, and app orchestration.
DOCTRINE.md The Bible: Coding standards, patterns, and source of truth.
requirements.txt Dependencies: Third-party libraries and packages.

🛠 Architectural Principles
The repository follows a strict development philosophy detailed in DOCTRINE.md . Key
expectations include:
Logic Isolation: Business rules reside strictly in the app/ directory.
Test-Driven Reliability: Every feature in app/ requires a corresponding test in tests/ .
Consistency: Adherence to formatting and structural rules to maintain a "single source of
truth."
•
•
•

Getting Started
1. Environment Setup
Ensure Python 3.8+ is installed. Use a virtual environment to isolate dependencies:

2. Installation

3. Running the App

Testing
Execute the test suite using pytest to ensure system stability:

Verification Status: This document describes the framework's intended architecture. - [Inference] Logic isolation and
test mirroring are expected behaviors based on project layout. - [Unverified] Specific internal configurations of
DOCTRINE.md were not provided.
# Create virtual environment
python -m venv venv
# Activate (macOS/Linux)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

pip install -r requirements.txt

python run.py

pytest
