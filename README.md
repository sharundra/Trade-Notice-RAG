# 🚢 Trade Policy RAG Agent

An AI-powered Retrieval-Augmented Generation (RAG) system designed to answer questions about **India's Export Policy (Trade Notice No. 11/2024-25)**. This system accurately interprets complex tabular data containing ITC(HS) Codes, descriptions, and export conditions.

## 🧠 The Challenge: Tabular Data in PDFs

Standard PDF parsing often fails on documents like Trade Notices because they consist primarily of **multi-page, structured tables**.
*   **Problem:** Traditional chunking (e.g., recursive character splitting) breaks table rows, separating the "Item Code" from its "Policy," leading to hallucinations.
*   **Solution:** This project uses **`pdfplumber`** to extract tables row-by-row. It implements a **Semantic Row Serialization** strategy, converting every table row into a self-contained, meaningful sentence before embedding it. This ensures high retrieval accuracy.

---

## 📂 Project Structure

```text
export_policy_rag/
│
├── data/
│   ├── raw/
│   │   └── Trade_Notice_11_2024_25.pdf  # The source document
│   └── chroma_db/                       # Persisted Vector Database (Generated)
│
├── src/
│   ├── __init__.py
│   ├── config.py       # Central configuration & API keys
│   ├── ingest.py       # Logic to parse PDF tables & clean data
│   ├── vector_store.py # Logic to initialize/load ChromaDB
│   └── rag_chain.py    # RAG Retrieval & LLM Chain definition
│
├── app.py              # Streamlit User Interface
├── requirements.txt    # Project dependencies
└── .env                # Environment variables (API Keys)
---
```

## 🚀 Flow of Execution & Setup

Follow these steps to set up and run the project.

### 1. Prerequisites
*   Python 3.9+
*   An OpenAI API Key

### 2. Installation
Create a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add your key:
```text
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Configuration (`src/config.py`)
The `config.py` file manages settings like chunk size, model selection (GPT-4o/GPT-3.5), and file paths. No changes are usually needed here unless you want to switch models.

### 4. Data Ingestion (`src/ingest.py`)
This script handles the complex logic of parsing the PDF tables. You can run it independently to verify that the data is being extracted correctly:
```bash
python -m src.ingest
```
*Output: You will see a sample parsed document printed in the console.*

### 5. Vector Store Creation (`src/vector_store.py`)
This module handles embedding the parsed data into **ChromaDB**. It is automatically called by the application, but it ensures that embeddings are created only once and persisted to disk for efficiency.

### 6. Run the Application
Launch the Streamlit Interface. The first run will take a few seconds to process the PDF and build the vector database.
```bash
streamlit run app.py
```

---

## 🧪 Sample Queries to Try

Once the UI is running, try asking:
*   *"What is the export policy for Natural Rubber?"*
*   *"Is the export of Red Sanders allowed?"*
*   *"What are the conditions for exporting Skeletons?"*
*   *"Tell me about the policy for Peacock Tail Feathers."*

---

## 🛠️ Tech Stack
*   **LangChain:** Framework for RAG and LLM orchestration.
*   **OpenAI:** LLM (GPT-4o) and Embeddings (text-embedding-3-small).
*   **ChromaDB:** Local Vector Store.
*   **pdfplumber:** Advanced PDF Table Extraction.
*   **Streamlit:** Interactive Web UI.
