# CTI NLP Pipeline – V1 (FastAPI & spaCy)

A modular **Cyber Threat Intelligence (CTI)** API built with **FastAPI** and **Pydantic v2**.

The goal of this project is to automatically extract **Indicators of Compromise (IoCs)** and **Threat Actors** from technical PDF reports (e.g., CERT-FR reports).

The pipeline follows a clean, decoupled, and extensible architecture:

```text
PDF Document
      │
      ▼
Parser (pypdf)
      │
      ▼
Text Cleaner (Regex)
      │
      ▼
NER Engine (spaCy)
      │
      ▼
ExtractionResult
```

---

# 🏗️ Architecture

The main strength of this first version is its **complete separation of concerns**.

The business logic (PDF parsing, text cleaning, and NLP extraction) is entirely independent of FastAPI, making every component easily testable in pure Python without starting the web server.

```text
├── app/
│   ├── models/
│   │   ├── domain.py
│   │   │   # Pure domain models (Document, Entity, ExtractionResult...)
│   │   └── api.py
│   │       # FastAPI request/response models (Pydantic v2)
│   │
│   ├── services/
│   │   ├── base.py
│   │   │   # Abstract interfaces (SOLID / Dependency Inversion)
│   │   │
│   │   ├── parsers/
│   │   │   ├── pdf_parser.py
│   │   │   │   # PDF parser based on pypdf
│   │   │   └── text_cleaner.py
│   │   │       # Regex-based PDF layout cleaner
│   │   │
│   │   └── ner_extractors/
│   │       └── spacy_extractor.py
│   │           # spaCy-based IoC extraction engine
│   │
│   ├── config.py
│   │   # Centralized configuration
│   │
│   └── main.py
│       # FastAPI application entry point
│
├── data/
│   # Test reports and JSON dictionaries
│
├── connector.py
│   # CTI ingestion client simulation
│
└── requirements.txt
```

---

# 🚀 Installation & Setup

## 1. Install Dependencies

Clone the repository, create a virtual environment, and install the required packages:

```bash
pip install -r requirements.txt
```

Download the required spaCy language model (Transformer version):

```bash
python -m spacy download en_core_web_trf
```

> **Note:** If your machine has limited CPU/GPU resources, you can change the `SPACY_MODEL_NAME` variable in `app/config.py` to a lighter model such as:
>
> - `en_core_web_sm`
> - `en_core_web_md`

---

## 2. Start the FastAPI Server

Launch the development server from the project root:

```bash
uvicorn app.main:app --reload
```

At startup, the API:

- loads the spaCy NLP model,
- initializes the `EntityRuler`,
- imports the Threat Actor dictionary from `data/threat_actors.json`,
- starts listening on:

```
http://127.0.0.1:8000
```

---

## 3. Test the API with Swagger UI

Open the interactive documentation:

```
http://127.0.0.1:8000/docs
```

Upload a PDF file to the `/analyze` endpoint to test the extraction pipeline directly from your browser.

---

## 4. Simulate CTI Ingestion

Keep the FastAPI server running, open a second terminal, and execute:

```bash
python connector.py
```

The connector will:

1. Read a local PDF report.
2. Send it to the API.
3. Receive the extracted JSON response.
4. Display a structured table containing:
   - IP addresses
   - CVEs
   - Hashes
   - Threat Actors
   - Other extracted IoCs

---

# 🧪 Local Testing

Each component can be validated independently without starting the API.

## Test the Text Cleaner

```bash
python test_cleaner.py
```

This validates the Regex-based preprocessing stage.

---

## Test the Complete NLP Pipeline

```bash
python test_pipeline.py
```

This runs the complete processing chain:

```text
PDF Parser
      │
      ▼
Text Cleaner
      │
      ▼
spaCy NER Extraction
```

---

# 🔮 Roadmap — Towards Version 2

Version 1 provides a solid and modular foundation. Version 2 will introduce production-grade capabilities.

## Asynchronous Processing

- Full migration to `async/await`
- Asynchronous FastAPI endpoints
- Higher throughput
- Better scalability under concurrent ingestion workloads

---

## STIX 2.1 Integration

Support for serializing extracted entities into the official **STIX 2.1** Cyber Threat Intelligence format before forwarding them to **OpenCTI**.

---

## Cloud-Native Deployment (AWS)

Migration toward a cloud-ready architecture including:

- FastAPI deployment on **AWS ECS/Fargate** containers
- or **AWS Lambda** serverless functions
- Amazon **S3** buckets for centralized storage of raw threat reports
- Scalable ingestion pipeline for large CTI datasets

---

# ✅ Technologies

- Python 3
- FastAPI
- Pydantic v2
- spaCy
- pypdf
- Regular Expressions (Regex)
- Uvicorn
- SOLID Architecture
- Dependency Inversion Principle (DIP)
- EntityRuler
- JSON-based Threat Actor Dictionary
```