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

## 🚀 Development & Execution Flow

Follow these steps to build and run the project from scratch.

### 1. Prerequisites & Setup
Create a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```
Create a `.env` file in the root directory and add your OpenAI key:
```text
OPENAI_API_KEY=sk-your-api-key-here
```

### 2. Configuration (`src/config.py`)
Set up the `config.py` file to manage settings like chunk size, model selection (GPT-4o), and file paths.

### 3. Data Ingestion Logic (`src/ingest.py`)
Implement the PDF parsing logic using `pdfplumber`. This script handles the extraction of tabular data and row serialization.
*   **Test this step:** Run the script independently to verify data is being parsed correctly.
    ```bash
    python -m src.ingest
    ```
    *(You should see a sample parsed document printed in the console).*

### 4. Vector Store Logic (`src/vector_store.py`)
Implement the logic to initialize **ChromaDB**. This script creates embeddings from the parsed data and persists them to disk so we don't have to re-process the PDF every time.

### 5. RAG Chain Logic (`src/rag_chain.py`)
Create the retrieval chain. This script connects the Vector Store to the LLM and defines the system prompt that ensures the AI interprets Export Policies strictly.

### 6. User Interface (`app.py`)
Build the **Streamlit** frontend. This script imports the RAG chain and provides a chat interface for the user.

### 7. Run the Application
Launch the final application. The first run will take a few seconds to process the PDF and build the vector database.
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
