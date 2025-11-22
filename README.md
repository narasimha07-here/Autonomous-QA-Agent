# 🤖 Autonomous QA Agent for Test Case & Script Generation

An intelligent QA automation system that generates documentation-grounded test cases and executable Selenium scripts

## Overview

The **Autonomous QA Agent** is an intelligent automation tool designed to accelerate the Quality Assurance lifecycle. This system analyzes functional requirements and directly matches them with UI elements from your HTML source code. This approach eliminates the disconnect between requirements and testing by ensuring every generated test case is grounded in documentation, and every script uses real DOM selectors.

---

## Key Capabilities

- **📄 Doc-to-Test:** Converts PDFs, Markdown, and JSON documents into comprehensive positive and negative test scenarios.
- **💻 HTML-to-Script:** Mines ID, Class, and Name attributes from HTML to build robust Selenium Python scripts that reflect your actual UI.
- **🧠 Smart Context:** Uses ChromaDB vector search to prevent AI hallucinations by explicitly citing the specific source documents for each test case.
- **⚡ Instant Execution:** Generates standard `unittest`-compatible Python files, ready for immediate download and execution.


## System Architecture

- **Frontend:** streamlit  
  [Autonomous qa agent](https://autonomous-agent.streamlit.app/)

- **Backend:** hugging face  
  [API](https://your-backend-url.com/api)

```
                ┌──────────────────────────────────────────────────┐
                │                     Streamlit UI                 │
                │  - Document Upload                               │
                │  - HTML Upload                                   │
                │  - Build Knowledge Base                          │
                │  - Generate Test Cases                           │
                │  - Generate Selenium Scripts                     │
                └────────────────────┬─────────────────────────────┘
                                     │
                       Frontend-Backend API Calls (FastAPI)
                                     │
                ┌────────────────────▼─────────────────────────────┐
                │                     FastAPI Backend              │
                │  (main.py)                                       │
                │   • /upload-documents                            │
                │   • /upload-html                                 │
                │   • /build-knowledge-base                        │
                │   • /generate-test-cases                         │
                │   • /generate-script                             │
                └────────────────────┬─────────────────────────────┘
                                     │
                      Internal Calls (Document Parsing, RAG, LLM)
                                     │
        ┌────────────────────────────┼─────────────────────────────┐
        │                            │                             │
┌───────▼──────────┐     ┌───────────▼────────────┐     ┌─────────▼──────────┐
│    RAGSystem     │     │  TestCaseGenerator     │     │  ScriptGenerator   │
│  - Load Docs     │     │  - LLM test case agent │     │  - HTML selector   │
│  - Chunking      │     │  - Markdown parsing    │     │    mining          │
│  - Embedding     │     │                        │     │  - Selenium script │
│  - ChromaDB      │     │                        │     │    LLM             │
└──────────────────┘     └────────────────────────┘     └────────────────────┘
```

---

## Project Structure

```
qa-agent/
│
├── backend/                       
│   ├── main.py                    # FastAPI Backend APIs & Endpoints
│   ├── config.py                  # Model/API Configuration
│   ├── rag_system.py              # RAG Engine
│   ├── test_case_generator.py     # Test Case Generation Agent
│   ├── script_generator.py        # Selenium Script Generation Agent
│   ├── __init__.py                
│   │
│   ├── uploads/                   # Uploaded Support Documents
│   │
│   ├── html_files/                # Uploaded HTML File
│   │
│   └── chroma_db/                 # ChromaDB Vector Store (auto-generated)
│
├── frontend/                     
│   └── app.py                     # Streamlit 
│
├── Supported_docs/                # Sample Support Documents
│
├── .env                           
├── .gitignore                     
├── requirements.txt              
└── README.md                      
```

---

## Core Components

### 1. RAG Engine (`rag_system.py`)

The **RAGSystem** class is the heart of the QA agent.

#### Responsibilities

| Feature           | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| Document Loading  | Supports PDF, Markdown, JSON, TXT, HTML                       |
| Semantic Chunking | Uses **SemanticChunker** for accurate contextual segmentation |
| Embeddings        | Powered by **BAAI/bge-small-en-v1.5**                         |
| Vector Store      | Stored in **ChromaDB** with document metadata                 |
| Retrieval         | `k=5` chunk retrieval tuned for precision                     |
| LLM Interface     | Gemini 2.5 Flash for answer synthesis                         |

---

### 2. Test Case Generator (`test_case_generator.py`)

#### How It Works

1. Retrieves contextual chunks for the user's query
2. Feeds **query + documents** into Gemini LLM
3. Instructs the model to output a **strict Markdown table**
4. Parses table → JSON structure
5. Used by Streamlit UI to display expandable test cases

#### Output Structure

Each test case returns:

```json
{
  "test_id": "TC-001",
  "feature": "Discount Code",
  "test_scenario": "Apply valid discount code SAVE15",
  "test_steps": [
    "Open checkout page",
    "Add items to cart",
    "Enter discount code SAVE15",
    "Click Apply"
  ],
  "expected_result": "Total price reduced by 15%",
  "test_type": "Positive",
  "grounded_in": "product_specs.md"
}
```
### 3. Selenium Script Generator (`script_generator.py`)

This module produces **fully executable, real-world Selenium scripts**.

#### Key Capabilities

| Capability            | Explanation                                            |
| --------------------- | ------------------------------------------------------ |
| HTML Selector Mining  | Extracts ID, Name, Class from raw HTML                 |
| Context Retrieval     | Test case + documentation context retrieved            |
| LLM Prompt            | Extremely detailed prompt template ensures reliability |
| Selenium 4 Compliance | Uses Service() + webdriver-manager                     |
| Page Load Waits       | Uses `document.readyState` check                       |
| Scroll into view      | Ensures non-visible elements are clickable             |
| Assertion Strategy    | Avoids hardcoded values; parses values dynamically     |
| Error Handling        | Try/Except + logging recommendations                   |

#### Output Script Format

* `unittest.TestCase` structure
* `setup()` and `tearDown()` lifecycle
* Explicit waits with minimum 15 seconds
* Full selector mapping from HTML

#### Script Generation Pipeline

1. **Analyze HTML** → Extract all selectors
2. **Retrieve Context** → Get feature documentation
3. **Generate Prompt** → Comprehensive instructions to LLM
4. **Extract Code** → Parse from markdown code blocks
5. **Validate & Clean** → Add missing imports, structure

---

### 4. Backend API (`main.py`)

Implements FastAPI endpoints with full error handling.

#### API Endpoints

| Endpoint                | Method | Purpose                                 |
| ----------------------- | ------ | --------------------------------------- |
| `/upload-documents`     | POST   | Ingest support docs (PDF, MD, TXT, JSON) |
| `/upload-html`          | POST   | Ingest HTML file for selector extraction |
| `/build-knowledge-base` | POST   | Build RAG vector database               |
| `/generate-test-cases`  | POST   | Returns structured test cases           |
| `/generate-script`      | POST   | Produces Selenium script from test case |
| `/health`               | GET    | Health check endpoint                   |
| `/status`               | GET    | System status (KB built, HTML uploaded) |

---

### 5. Streamlit UI (`app.py`)

#### UI Workflow

1. **Upload Support Docs** → Sidebar file uploader
2. **Build Knowledge Base** → Button triggers vector DB creation
3. **Upload HTML** → Separate uploader for HTML files
4. **Generate Test Cases** → Text area query input
5. **Generate Per-Test Selenium Scripts** → Button per test case
6. **Download Script (.py)** → Download button for each script

## Installation

### Prerequisites

- **Python 3.10 - 3.11**
- **Chrome Browser** (for running Selenium tests)
- **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/narasimha07-here/Autonomous-QA-Agent.git
cd Autonomous-QA-Agent
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
4. **Configure Environment Variables**

Create `.env` file in the root directory:
```env
GOOGLE_API_KEY=api_key
```
**NOTE**: Keep this key in `.env` and add `.env` to `.gitignore`.
---

## Running the System

### Start Backend (FastAPI)

Open **Terminal 1**:

```bash
cd backend
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Backend is now running at:** `http://localhost:8000`

---

### Start Frontend (Streamlit)

Open **Terminal 2** (keep backend running):

```bash
cd frontend
streamlit run app.py
```

Or from root:
```bash
streamlit run frontend/app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Frontend will open automatically in your browser.**

---

## Usage Guide

### Step 1 – Upload Support Documents

1. Navigate to **sidebar** in Streamlit UI
2. Click **"Upload support documents"**
3. Select files (PDF, Markdown, TXT, JSON)
4. Click **"Upload Documents"** button
5. Wait for success message: ✅ Documents uploaded successfully!

**Files are stored in:** `backend/uploads/`

---

### Step 2 – Build Knowledge Base

1. In sidebar, click **"Build Knowledge Base"**
2. System performs:
   - Document loading and parsing
   - Semantic chunking
   - Embedding generation (BGE-small-en-v1.5)
   - ChromaDB vector store creation
3. Wait for success: ✅ Knowledge base built successfully!
4. Status indicator shows: 📚 Knowledge Base: ✅ Built

**Vector database stored in:** `backend/chroma_db/`

---

### Step 3 – Upload HTML File

1. In sidebar, under **"3. Upload HTML File"**
2. Click **"Upload HTML file"**
3. Select your target HTML file
4. Click **"Upload HTML"** button
5. Success message: ✅ HTML file uploaded successfully!
6. Status shows: 📄 HTML File: ✅ Uploaded

**HTML stored in:** `backend/html_files/`

---

### Step 4 – Generate Test Cases

1. Navigate to **"Test Case Generation"** tab
2. Enter query in text area, for example:

```
Generate all positive and negative test cases for the discount code feature
```

3. Click **"Generate Test Cases"** button
4. Wait for generation (usually 5-15 seconds)
5. Success message

#### Test Case Display

Each test case shows in expandable section with:
- Test ID
- Feature
- Scenario
- Test Steps
- Expected Result
- Test Type (Positive/Negative)
- Source Document

---

### Step 5 – Generate Selenium Scripts

1. Locate desired test case in the list
2. Click **"Generate Script"** button (must have HTML uploaded)
3. Wait for script generation (10-30 seconds)
4. Success: ✅ Script generated!
5. Navigate to **"Script Generation"** tab
6. View generated Python script in code block
7. Click **"📥 Download TC-XXX.py"** to save
---

### Step 6 – Run Generated Script

```bash
python TC-XXX.py
```
Chrome browser will launch automatically and execute test steps.
---

## THANK YOU ❤️
