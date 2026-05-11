# 📊 AutoBI-Agent: Multi-Agent Business Intelligence & Anomaly Attribution

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)
![AutoGen](https://img.shields.io/badge/Powered%20by-AutoGen-orange.svg)

## 📖 Overview
**AutoBI-Agent** is an intelligent, multi-agent collaborative workflow designed to automate complex business data analysis and anomaly attribution. Traditional BI tools require manual SQL writing and tedious troubleshooting when core metrics fluctuate. AutoBI-Agent solves this by leveraging an LLM-driven multi-agent architecture to automatically parse intents, query databases, run statistical anomaly detection in a sandbox, and generate executive insights.

## 🏗️ Architecture (Agent Workflow)
The system operates using three core agents via `pyautogen`:
1. **🔍 Intent & SQL Agent:** Parses natural language business questions, translates them into optimized multi-dimensional SQL queries, and extracts data.
2. **🧠 Code Analyzer Agent (Sandbox):** Operates in a secure Docker/local sandbox. It writes and executes Python scripts (using Pandas/Scikit-learn) to perform long-chain reasoning, isolate variables (e.g., holidays, normal fluctuations), and pinpoint the root cause of anomalies.
3. **📝 Report Generator Agent:** Synthesizes the raw data and script outputs into a structured, highly readable executive business insight report.

## 🚀 Quick Start

### 1. Installation
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/YourUsername/AutoBI-Agent.git](https://github.com/YourUsername/AutoBI-Agent.git)
cd AutoBI-Agent
pip install -r requirements.txt
