# 🛡️ Insurance Policy QA

A **Retrieval-Augmented Generation (RAG)** based AI assistant that allows users to ask natural-language questions about insurance policy documents.

The system converts insurance policy PDFs into searchable text, splits them into meaningful chunks, generates vector embeddings, stores them in a **Chroma vector database**, retrieves the most relevant sections for a user's question, and uses an LLM to generate an answer based **only on the retrieved policy information**.

This helps users understand complex insurance policies without manually searching through lengthy policy documents.

---

## 🚀 Features

* 📄 **PDF Policy Processing**

  * Converts insurance policy PDFs into Markdown using [Docling](https://github.com/docling-project/docling).

* ✂️ **Document Chunking**

  * Splits policy documents into smaller overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`.

* 🧠 **Semantic Search**

  * Converts document chunks into vector embeddings using OpenAI's `text-embedding-3-large` model.

* 🗄️ **Vector Database**

  * Stores embeddings in ChromaDB for efficient similarity-based retrieval.

* 🔎 **Top-K Retrieval**

  * Retrieves the 5 most relevant document chunks for each user question.

* 🤖 **LLM-Powered Answers**

  * Uses `gpt-4o-mini` to generate answers from the retrieved policy context.

* 🛡️ **Context-Grounded Responses**

  * The assistant is explicitly instructed not to invent policy information or use external knowledge when the answer cannot be found in the retrieved documents.

* 💬 **Interactive Chat Interface**

  * Provides a simple Gradio interface for asking questions about the policies.

---

## 🧠 How It Works

The project follows a standard **RAG pipeline**:

```text
                  Insurance Policy PDF
                          │
                          ▼
                 ┌─────────────────┐
                 │     Docling     │
                 │ PDF → Markdown  │
                 └────────┬────────┘
                          │
                          ▼
                    Policy Text
                          │
                          ▼
              ┌──────────────────────┐
              │  Text Chunking       │
              │  LangChain           │
              │  1000 tokens/chars   │
              │  200 overlap         │
              └──────────┬───────────┘
                         │
                         ▼
                 Document Chunks
                         │
                         ▼
              ┌──────────────────────┐
              │ OpenAI Embeddings    │
              │ text-embedding-3-    │
              │ large                │
              └──────────┬───────────┘
                         │
                         ▼
                 ┌─────────────────┐
                 │    ChromaDB     │
                 │  Vector Store   │
                 └────────┬────────┘
                          │
              User Question
                          │
                          ▼
                 Query Embedding
                          │
                          ▼
                 Similarity Search
                          │
                          ▼
                Top 5 Relevant Chunks
                          │
                          ▼
                 ┌─────────────────┐
                 │    GPT-4o-mini  │
                 │ Answer Generator│
                 └────────┬────────┘
                          │
                          ▼
                    Final Answer
```

---

## 🏗️ Project Architecture

The project is separated into two major stages:

### 1. Ingestion

The ingestion pipeline prepares the insurance documents for retrieval.

```text
PDF
 │
 ▼
Docling
 │
 ▼
Markdown
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
ChromaDB
```

### 2. Retrieval & Generation

The retrieval pipeline handles user questions.

```text
User Question
      │
      ▼
Semantic Retrieval
      │
      ▼
Top 5 Relevant Chunks
      │
      ▼
Context Construction
      │
      ▼
GPT-4o-mini
      │
      ▼
Answer
```

---

## 📂 Project Structure

```text
Insurance-Policy-QA/
│
├── data/
│   ├── knowledge-base/
│   │   └── *.md
│   │
│   └── original-pdfs/
│       └── *.pdf
│
├── ingest/
│   ├── convert.py
│   ├── clean.py
│   └── chunk.py
│
├── retrieval/
│   ├── embeddings.py
│   ├── retriever.py
│   └── vector_store.py
│
├── vector_db/
│   └── ChromaDB files
│
├── ok.ipynb
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

The repository currently separates document ingestion under `ingest/` and retrieval under `retrieval/`.

---

# ⚙️ Technologies Used

| Technology             | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| **Python**             | Core programming language                 |
| **Docling**            | PDF document conversion                   |
| **LangChain**          | Document loading, splitting and retrieval |
| **OpenAI Embeddings**  | Semantic vector representations           |
| **ChromaDB**           | Vector database                           |
| **OpenAI GPT-4o-mini** | Answer generation                         |
| **Gradio**             | Chat interface                            |
| **python-dotenv**      | Environment variable management           |

The current `requirements.txt` includes Docling, while the application code uses additional LangChain, OpenAI, Chroma and Gradio components.

---

# 🔧 Installation

## 1. Clone the repository

```bash
git clone https://github.com/anishpulsay/Insurance-Policy-QA.git
cd Insurance-Policy-QA
```

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

If additional dependencies used by the ingestion and retrieval modules are not included in `requirements.txt`, install them with:

```bash
pip install langchain
pip install langchain-openai
pip install langchain-community
pip install langchain-text-splitters
pip install langchain-chroma
pip install langchain-huggingface
pip install chromadb
pip install openai
pip install gradio
pip install python-dotenv
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

The application loads the API key using `python-dotenv`.

> **Important:** Never commit your `.env` file or expose your OpenAI API key publicly.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
```

---

# 📄 Adding Insurance Policies

Place your original PDF policy documents inside:

```text
data/original-pdfs/
```

For example:

```text
data/
└── original-pdfs/
    ├── health-insurance-policy.pdf
    ├── life-insurance-policy.pdf
    └── motor-insurance-policy.pdf
```

---

# 🔄 Document Ingestion Pipeline

The `convert.py` script converts PDF files into Markdown documents using Docling.

```python
from docling.document_converter import DocumentConverter
```

The converter processes every PDF in the source directory and exports the document as Markdown.

Run:

```bash
python ingest/convert.py
```

The resulting Markdown files are stored in:

```text
data/knowledge-base/
```

Example:

```text
data/
└── knowledge-base/
    ├── health-insurance-policy.md
    ├── life-insurance-policy.md
    └── motor-insurance-policy.md
```

---

# ✂️ Chunking & Embedding

After conversion, the documents are loaded and divided into smaller chunks.

The current implementation uses:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

This creates chunks of approximately 1000 characters with 200 characters of overlap between neighboring chunks.

The overlap helps preserve contextual information between adjacent sections of a policy.

---

# 🧠 Embeddings

Each document chunk is converted into a numerical vector using:

```python
OpenAIEmbeddings(
    model="text-embedding-3-large"
)
```

These vectors capture the semantic meaning of the text.

For example:

```text
"What is the waiting period for pre-existing diseases?"
```

can retrieve a policy section containing wording such as:

```text
"Pre-existing diseases are subject to a waiting period..."
```

even when the exact words used in the question and document are different.

---

# 🗄️ ChromaDB

The generated embeddings are stored in a Chroma vector database.

The vector database is created using the processed document chunks:

```python
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=db_name
)
```

The resulting database is stored locally in:

```text
vector_db/
```

The retrieval system then loads this vector store and performs semantic similarity search.

---

# 🔎 Retrieval

When the user asks a question, the retriever searches the vector database for the most semantically relevant chunks.

The current configuration retrieves:

```python
search_kwargs={"k": 5}
```

Therefore, the **top 5 relevant chunks** are passed to the language model.

Example question:

```text
What is the waiting period for pre-existing diseases?
```

The system:

1. Converts the question into an embedding.
2. Searches ChromaDB.
3. Finds the most relevant policy chunks.
4. Combines those chunks into a context.
5. Sends the context and question to the LLM.
6. Generates the final answer.

---

# 🤖 Answer Generation

The project uses:

```text
GPT-4o-mini
```

for answer generation.

The model receives:

```text
System Prompt
      +
Retrieved Policy Context
      +
User Question
```

The system prompt instructs the model to:

* Use only the retrieved policy information.
* Avoid using general knowledge.
* Never invent policy details.
* Explicitly state when the provided documents do not contain enough information.

This makes the application more grounded than a normal LLM chatbot.

---

# 💬 Running the Application

After creating the vector database, run:

```bash
python retrieval/retriever.py
```

The application launches a Gradio chat interface:

```python
gr.ChatInterface(answer_question).launch()
```

You can then ask questions such as:

```text
What is the waiting period for pre-existing diseases?
```

```text
Are maternity expenses covered?
```

```text
What are the exclusions in this policy?
```

```text
Is room rent capped?
```

```text
What happens if I make a claim during the waiting period?
```

```text
Does the policy cover hospitalization expenses?
```

---

# 🧪 Example RAG Flow

### User Question

```text
What is the waiting period for pre-existing diseases?
```

### Retrieval

The retriever searches the vector database and returns the five most relevant policy chunks.

```text
Retrieved Chunk 1
Retrieved Chunk 2
Retrieved Chunk 3
Retrieved Chunk 4
Retrieved Chunk 5
```

### Context

These chunks are combined into a single context.

```text
Policy Context
      +
User Question
```

### LLM

GPT-4o-mini generates the final response using the retrieved information.

### Result

```text
According to the policy, pre-existing diseases are subject
to a specified waiting period before they become eligible
for coverage.
```

The exact answer depends on the contents of the uploaded policy documents.

---

# 🛡️ Hallucination Control

One of the important design decisions in this project is restricting the LLM to the retrieved context.

The system prompt contains the following principle:

```text
Answer the user's question using ONLY the information
provided in the context.
```

If the required information is not present, the assistant is instructed to respond:

```text
I don't have enough information in the provided policy
documents to answer that.
```

This prevents the model from filling gaps using potentially incorrect general knowledge.

---

# 📊 RAG Components

The project can be understood as five major components:

### 1. Document Loader

Loads the converted Markdown policy documents.

### 2. Text Splitter

Breaks large documents into manageable chunks.

```text
1000 character chunks
200 character overlap
```

### 3. Embedding Model

Converts text into numerical vectors.

```text
text-embedding-3-large
```

### 4. Vector Database

Stores and searches embeddings.

```text
ChromaDB
```

### 5. LLM

Generates the final response from retrieved context.

```text
GPT-4o-mini
```

---

# 🧩 Why RAG?

A normal LLM does not automatically know the contents of a user's private insurance policy.

RAG solves this problem by providing the relevant policy sections to the LLM at query time.

Instead of:

```text
Question → LLM → Answer
```

this project uses:

```text
Question
   ↓
Semantic Search
   ↓
Relevant Policy Sections
   ↓
LLM
   ↓
Grounded Answer
```

This makes RAG particularly useful for document-heavy domains such as insurance, legal documents, finance and compliance.

---

# 📈 Future Improvements

The current implementation provides the foundation for a more advanced insurance policy assistant.

Potential improvements include:

### 🔹 Hybrid Search

Combine:

* semantic/vector search
* keyword/BM25 search

to improve retrieval for exact policy terminology.

### 🔹 Metadata Filtering

Store metadata such as:

```text
Policy Name
Section
Page Number
Policy Type
Insurer
```

and use it during retrieval.

### 🔹 Source Citations

Return the exact:

```text
Policy → Page → Section
```

used to generate an answer.

### 🔹 Reranking

Retrieve more candidates initially and use a reranker to select the most relevant chunks.

```text
Query
 ↓
Retrieve 20 chunks
 ↓
Reranker
 ↓
Top 5 chunks
 ↓
LLM
```

### 🔹 Better Document Parsing

Improve handling of:

* tables
* headers
* footers
* page numbers
* policy clauses
* structured sections

### 🔹 Evaluation

Introduce a RAG evaluation pipeline measuring:

* retrieval precision
* retrieval recall
* answer faithfulness
* context relevance
* answer correctness

### 🔹 Conversational Memory

Allow users to ask follow-up questions while maintaining relevant conversation context.

### 🔹 Multi-Policy Comparison

Allow users to compare multiple insurance policies:

```text
Policy A vs Policy B

Waiting Period
Room Rent
Maternity
Co-pay
Exclusions
Coverage
```

---

# 🎯 Learning Objectives

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation (RAG)
* Semantic search
* Vector embeddings
* Vector databases
* Document preprocessing
* Document chunking
* LangChain
* OpenAI APIs
* ChromaDB
* Prompt engineering
* LLM grounding
* Gradio application development

---

# ⚠️ Disclaimer

This project is intended for **educational and demonstration purposes**.

The answers generated by the system should not be considered legal, financial, medical, or insurance advice.

Always refer to the original insurance policy and consult the relevant insurer or qualified professional when making important decisions.

---

# 📜 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

# 👨‍💻 Author

**Anish Pulsay**

GitHub: [@anishpulsay](https://github.com/anishpulsay)

---

## ⭐ If You Found This Useful

Consider giving the repository a ⭐ on GitHub!

[Repository](https://github.com/anishpulsay/Insurance-Policy-QA)
