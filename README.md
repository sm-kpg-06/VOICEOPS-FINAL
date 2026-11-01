# VoiceOps 2026: ZentroMart Support Agent
## Architecture: Hybrid Retrieval and Reranking Agent

**Capstone Project:** VoiceOps 2026 (LLM & Generative AI Course, Consulting & Analytics Club, IIT Guwahati × Gnani.ai)  
**Public GitHub Repository:** `https://github.com/sm-kpg-06/VOICEOPS-FINAL`  

---

## 1. Project Overview & Architecture

This repository implements a high-precision **Hybrid Retrieval and Reranking Support Agent** for ZentroMart, an Indian online store. It fuses lexical BM25 matching and dense semantic vector search via Reciprocal Rank Fusion (RRF), coupled with a policy-authority cross-scoring reranker and native Gnani.ai voice STT/TTS models.

### Key Architectural Characteristics:
- **Dual Retrieval Pipelines:**
  1. *Lexical Pipeline:* BM25Okapi scoring over tokenized section chunks with exact code and keyword matching.
  2. *Dense Semantic Pipeline:* Sublinear TF-IDF character/word n-gram vector space with cosine distance calculation.
- **Reciprocal Rank Fusion (RRF):** Fuses rankings using the formula:
  $$\text{RRF Score}(d) = \frac{1}{k + r_{\text{lexical}}(d)} + \frac{1}{k + r_{\text{dense}}(d)}$$
  (with standard smoothing constant $k=60$).
- **Authority Cross-Scoring Reranker:** Boosts official policy documents over FAQs and marketing content per `KB-00.1`, applies penalty to superseded versions, and filters redundant chunks.
- **Evidence Provenance & Inspection Tool:** Tracks exact ranking components (BM25 rank, dense rank, RRF score, final reranked score) and exposes an interactive CLI inspector (`python run.py --inspect "query"`).
- **Gnani.ai Speech Suite:** Official STT and TTS integration (voice: `Kaveri`, model: `timbre-v2.5`), supporting audio batch processing.

---

## 2. Directory Structure

```text
voiceops-2026/
├── README.md                      # Architecture and setup guide
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Dependencies
├── run.py                         # Unified entry point
├── Capstone_Project_Dataset_FTTT_2026/ # Knowledge base docs, CSV tables & mock tools
├── src/
│   ├── knowledge_base.py          # Knowledge base & catalog parser
│   ├── retriever.py               # Hybrid BM25 + Dense Vector + RRF fusion engine
│   ├── evidence_inspector.py      # Evidence provenance breakdown inspector
│   ├── llm_adapter.py             # LLM provider adapter
│   ├── baseline.py                # Step 1: Prompt-only baseline
│   ├── rag_agent.py               # Step 2: Grounded hybrid RAG agent
│   ├── tools_adapter.py           # Step 3: Identity-gated order lookup & ticket creation
│   ├── conversation_agent.py      # Step 3: Multi-turn dialog manager
│   └── voice_adapter.py           # Step 4: Gnani voice STT/TTS adapter
├── tests/
│   ├── test_agent.py              # Unit & integration tests
│   └── test_gnani_live.py         # Live Gnani STT/TTS integration test
├── evaluation/
│   ├── eval_questions.py          # Step 1 vs Step 2 benchmark runner
│   └── eval_conversations.py      # Step 3 multi-turn benchmark runner
├── sample_outputs/                # Evaluation outputs & audio responses
│   ├── baseline_results.csv
│   ├── rag_results.csv
│   ├── conversation_results.json
│   ├── evaluation_summary.json
│   └── batch_audio_results/
└── demo_instructions.md           # 2-minute demo instructions
```

---

## 3. Installation & Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Configuration & Gnani.ai Credentials

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### Gnani.ai Speech Services Configuration (Step 4 Voice)
To enable genuine speech-to-text and text-to-speech voice operations:
1. Visit [app.gnani.ai/voice](https://app.gnani.ai/voice) and sign in to your Gnani account.
2. Under API Keys, generate a key. A single key covers both Gnani STT and TTS services.
3. Add the key to your `.env` file:
   ```bash
   GNANI_API_KEY=your_actual_gnani_api_key
   GNANI_TTS_VOICE=Kaveri
   GNANI_TTS_MODEL=timbre-v2.5
   GNANI_LANGUAGE_CODE=en-IN
   ```
   Or export it in your terminal:
   ```bash
   export GNANI_API_KEY="your_actual_gnani_api_key"
   ```
4. Run the live integration test to verify genuine API communication:
   ```bash
   python tests/test_gnani_live.py
   ```
   If `GNANI_API_KEY` is absent, the test strictly reports `BLOCKED — credentials not configured` and does not pass.
5. **Strict No-Mock Runtime Policy:** Offline mock transcriptions and synthetic audio generators have been removed from the runtime path. All audio input is transcribed by Gnani STT and answered via Gnani TTS. If credentials are not configured, runtime voice execution halts and reports `BLOCKED — credentials not configured`.

---

## 5. Execution Commands

### A. Run Full Practice Evaluation
```bash
python run.py --mode evaluate
```

### B. Inspect Evidence Provenance & RRF Fusion
```bash
python run.py --inspect "How fast are refunds to the ZentroMart Wallet?"
```

### C. Required Batch Audio Processing
```bash
python run.py --input-dir sample_outputs/test_audio --output-dir sample_outputs/batch_audio_results
```

### D. Run Automated Test Suite
```bash
python -m unittest discover tests
```

---

## 5. Evaluation Results Summary

| Metric | Step 1 Baseline | Step 2 Hybrid RAG | Step 3 Conversational |
| :--- | :---: | :---: | :---: |
| **Decision Accuracy** | 88.5% | **88.5%** | **88.5%** |
| **Fact Coverage Rate** | 13.5% | **53.8%** | **56.2%** |
| **Gold Evidence Recall** | 0.0% | **67.3%** | **91.2%** |
| **Tool-Call Accuracy** | N/A | N/A | **94.8%** |
