# PolicyRAG

A Retrieval-Augmented Generation (RAG) based AI assistant for querying insurance policy documents using semantic search, vector embeddings, ChromaDB, and an LLM.

PolicyRAG allows users to ask natural-language questions about insurance policies and retrieve relevant information from the underlying policy documents.

---

## Features

- Load insurance policy documents in Markdown format
- Split large documents into smaller chunks
- Generate semantic embeddings using OpenAI
- Store embeddings and documents in ChromaDB
- Perform semantic similarity search
- Retrieve relevant sections of insurance policies
- Generate natural-language responses using GPT-4o-mini
- Interactive question-answering interface using Gradio
- Environment variables for securely managing API keys

---

## Architecture

```text
                 Insurance Policy Documents
                           │
                           ▼
                    Document Loading
                           │
                           ▼
                     Text Chunking
                           │
                           ▼
              RecursiveCharacterTextSplitter
                           │
                           ▼
                  OpenAI Embeddings
              text-embedding-3-large
                           │
                           ▼
                       ChromaDB
                    Vector Database
                           │
                           ▼
                    Similarity Search
                           │
                           ▼
                 Relevant Policy Chunks
                           │
                           ▼
                     GPT-4o-mini
                           │
                           ▼
                    Final Answer
Tech Stack
Technology	Purpose
Python	Core programming language
LangChain	RAG pipeline and document processing
OpenAI	Embeddings and LLM
text-embedding-3-large	Text embeddings
GPT-4o-mini	Response generation
ChromaDB	Vector database
Gradio	User interface
Docling	PDF/document conversion
Python-dotenv	Environment variable management
Project Structure
Insurance-Policy-QA/
│
├── data/
│   └── knowledge-base/
│       ├── policy1.md
│       ├── policy2.md
│       └── ...
│
├── ingest/
│   └── ...
│
├── retrieval/
│   └── retriever.py
│
├── vector_db/
│   └── ...
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
How the Project Works

PolicyRAG is divided into two major stages:

Ingestion
Retrieval

The ingestion pipeline prepares the knowledge base and creates the vector database.

The retrieval pipeline searches the vector database when the user asks a question.

1. Document Ingestion

The insurance policy documents are first converted into Markdown files.

The Markdown files are stored inside:

data/knowledge-base/

The documents are then loaded using LangChain's DirectoryLoader.

loader = DirectoryLoader(
    "data/knowledge-base",
    glob="*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()

The loader reads the Markdown files and converts them into LangChain Document objects.

2. Text Chunking

Large policy documents are split into smaller chunks using:

RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

The pipeline becomes:

Large Policy Document
        │
        ▼
RecursiveCharacterTextSplitter
        │
        ├── Chunk 1
        ├── Chunk 2
        ├── Chunk 3
        ├── Chunk 4
        └── ...
Chunk Size
chunk_size=1000

This specifies the target size of each chunk in characters.

Chunk Overlap
chunk_overlap=200

This allows consecutive chunks to share some text and helps preserve context across chunk boundaries.

3. Generate Embeddings

Each chunk is converted into a numerical vector using OpenAI's embedding model:

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

Conceptually:

Policy Chunk
     │
     ▼
OpenAI Embedding Model
     │
     ▼
Numerical Vector

The vector represents the semantic meaning of the text.

This allows the system to search based on meaning rather than only exact keyword matches.

4. Store Embeddings in ChromaDB

The generated embeddings are stored in ChromaDB:

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=db_name
)

ChromaDB stores information associated with the chunks, including:

Document content
Embeddings
Metadata

The resulting vector database is stored locally.

vector_db/

The overall process is:

Policy Chunks
     │
     ▼
OpenAI Embeddings
     │
     ▼
Vectors
     │
     ▼
ChromaDB
5. Retrieval

When a user asks a question, the question is converted into an embedding using the same embedding model.

For example:

"What is the waiting period for pre-existing diseases?"

becomes:

Question
   │
   ▼
text-embedding-3-large
   │
   ▼
Question Vector

The question vector is then compared against the vectors stored in ChromaDB.

The most semantically similar chunks are retrieved.

User Question
      │
      ▼
Question Embedding
      │
      ▼
ChromaDB
      │
      ▼
Similarity Search
      │
      ▼
Relevant Policy Chunks
6. LLM Response Generation

The retrieved policy chunks are provided to GPT-4o-mini as context.

The system prompt instructs the model to use the retrieved information when answering the user's question.

Conceptually:

User Question
      │
      ├─────────────────────┐
      │                     │
      ▼                     ▼
Question              Retrieved
                       Policy Chunks
      │                     │
      └──────────┬──────────┘
                 ▼
             GPT-4o-mini
                 │
                 ▼
            Final Answer

This is the core RAG process.

Complete RAG Pipeline
                 INGESTION
                     │
                     ▼
              Policy Documents
                     │
                     ▼
               Markdown Files
                     │
                     ▼
              DirectoryLoader
                     │
                     ▼
                 Documents
                     │
                     ▼
        RecursiveCharacterTextSplitter
                     │
                     ▼
                   Chunks
                     │
                     ▼
        text-embedding-3-large
                     │
                     ▼
                 Embeddings
                     │
                     ▼
                 ChromaDB
                     │
             ────────┴────────
                     │
                     ▼
                 RETRIEVAL
                     │
                     ▼
                User Question
                     │
                     ▼
            Question Embedding
                     │
                     ▼
             Similarity Search
                     │
                     ▼
           Relevant Policy Chunks
                     │
                     ▼
                 GPT-4o-mini
                     │
                     ▼
                Final Answer
Example Questions

Users can ask natural-language questions such as:

What is the waiting period for pre-existing diseases?
What are the exclusions under the policy?
Does the policy cover ambulance charges?
What is the procedure for filing a claim?
Are daycare procedures covered under the policy?
What are the eligibility conditions for this policy?
What happens if I receive treatment at a non-network hospital?
Running the Project
1. Clone the Repository
git clone https://github.com/anishpulsay/Insurance-Policy-QA.git

Navigate into the project:

cd Insurance-Policy-QA
2. Create a Virtual Environment
python3 -m venv .venv

Activate it:

source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt

If you are using uv:

uv sync
Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key

The .env file should never be committed to GitHub.

Make sure .gitignore contains:

.env
.venv/
__pycache__/
vector_db/
Running the Ingestion Pipeline

Run the ingestion pipeline to create or update the Chroma vector database.

The process is:

Markdown Documents
        ↓
Document Loading
        ↓
Chunking
        ↓
Embeddings
        ↓
ChromaDB
Running the Retrieval Application

The retrieval application is located in:

retrieval/retriever.py

Run it using:

uv run retrieval/retriever.py

The Gradio interface will start locally.

Open the local URL displayed in the terminal, typically:

http://127.0.0.1:7860
Example RAG Interaction
User
What is the waiting period for pre-existing diseases?
System
Question
   ↓
Generate Question Embedding
   ↓
Search ChromaDB
   ↓
Retrieve Relevant Policy Chunks
   ↓
Provide Context to GPT-4o-mini
   ↓
Generate Answer

The answer should be based on the information retrieved from the policy documents.

Why RAG?

Insurance policies can contain large amounts of information spread across many pages.

Users may have difficulty finding specific information such as:

Waiting periods
Exclusions
Coverage conditions
Claim procedures
Eligibility requirements
Hospitalisation rules
Policy limitations

Instead of manually searching through long policy documents, PolicyRAG allows users to ask questions in natural language.

The system retrieves the relevant sections and uses them as context for generating the answer.

Key Concepts Demonstrated
Retrieval-Augmented Generation

Combining document retrieval with an LLM to provide context-specific answers.

Embeddings

Representing text as numerical vectors that capture semantic meaning.

Vector Databases

Storing and searching embeddings efficiently.

Semantic Search

Finding relevant information based on meaning rather than exact keyword matches.

Document Chunking

Breaking large documents into smaller units suitable for embedding and retrieval.

Prompt Grounding

Providing retrieved documents to an LLM as context for generating responses.

Future Improvements
 Add source citations to answers
 Display retrieved policy sections in the UI
 Add metadata-based filtering
 Add hybrid keyword + semantic search
 Add a reranking model
 Improve chunking strategy for policy documents
 Add retrieval evaluation metrics
 Add support for multiple insurance providers
 Add conversational memory
 Improve the Gradio interface
 Add automated evaluation of retrieved chunks
 Add direct PDF ingestion
Limitations

The quality of the final answer depends on:

The quality of the source documents
The document conversion process
The chunking strategy
The embedding model
The quality of retrieved chunks
The LLM's ability to use the retrieved context

If relevant information is not retrieved, the final answer may not contain the required information.

Disclaimer

This project is developed for educational and experimental purposes.

The responses generated by the system should not be considered professional insurance, legal, or financial advice.

Users should refer to the original insurance policy documents and consult the insurance provider for authoritative information.

License

This project is licensed under the MIT License.
