# BookMatch — AI-Powered Book Recommendation System

BookMatch is an AI-powered book recommendation application that helps readers discover books based on their interests, reading preferences, and natural-language requests. Instead of relying solely on traditional categories or fixed filters, users can describe the type of book they want, request recommendations similar to a particular title, and explore books that match their preferred mood, genre, or reading style.

The application combines large language models, multilingual text embeddings, semantic similarity search, and book metadata from Open Library to provide relevant recommendations with concise, AI-generated explanations.

## Features

* **Natural-Language Search:** Describe your reading preferences in everyday language.
* **Reference-Based Recommendations:** Discover books similar to a title you are currently reading or already know.
* **Semantic Book Search:** Retrieve and rank books based on the meaning of the user's request rather than exact keyword matching alone.
* **Preference-Based Filtering:** Support preferences such as genre, mood, language, and page limits where the required metadata is available.
* **AI-Generated Explanations:** Receive a short explanation of why each recommended book matches your request.
* **Book Covers and Catalogue Links:** Display available book covers and links to their Open Library pages.
* **Interactive Library-Style Interface:** Explore recommendations through a Streamlit application.

## Technologies Used

| Technology                            | Purpose                                               |
| ------------------------------------- | ----------------------------------------------------- |
| Python                                | Main programming language                             |
| Streamlit                             | Interactive frontend                                  |
| FastAPI                               | Backend API                                           |
| Hugging Face Transformers             | Loading and running the language model                |
| Qwen2.5-1.5B-Instruct                 | Query understanding and recommendation explanations   |
| Sentence Transformers                 | Generating semantic text embeddings                   |
| paraphrase-multilingual-MiniLM-L12-v2 | Multilingual embedding model                          |
| FAISS                                 | Vector indexing and similarity search                 |
| Open Library API                      | Retrieving book metadata and cover information        |
| Requests                              | HTTP communication between the frontend and backend   |
| python-dotenv                         | Loading local configuration from `.env`               |
| Pyngrok                               | Exposing the development backend through a public URL |


## System Architecture

BookMatch follows a frontend–backend architecture.

1. **User Input:** The user submits a natural-language request through the Streamlit interface.
2. **Query Understanding:** The language model identifies relevant preferences, such as a reference title, genre, mood, and page limits, and converts them into structured JSON.
3. **Candidate Retrieval:** The backend searches the Open Library catalogue to retrieve potential book recommendations.
4. **Text Embedding:** The embedding model converts book descriptions constructed from available metadata into numerical vectors.
5. **Vector Search:** FAISS performs similarity search to rank candidate books against the user's request.
6. **Filtering and Ranking:** The system applies supported user constraints and selects the most relevant candidates.
7. **Explanation Generation:** The language model generates concise explanations based on the available book metadata.
8. **Results Display:** The backend returns structured JSON to the Streamlit frontend, which displays the recommendations.

### Workflow

User Query → Query Understanding → Open Library Retrieval → Text Embeddings → FAISS Similarity Search → Filtering and Ranking → AI Explanations → Streamlit Results

## Models and Data Source

### Language Model

**Qwen2.5-1.5B-Instruct**

Used for understanding natural-language requests and generating recommendation explanations. The model is loaded through Hugging Face Transformers in the backend environment.

### Embedding Model

**paraphrase-multilingual-MiniLM-L12-v2**

Used to represent user requests and book metadata as semantic vectors. Its multilingual capabilities provide a foundation for supporting English and other languages, although multilingual recommendation quality depends on candidate retrieval and available catalogue metadata as well.

### Vector Search

**FAISS**

Used to build a vector index and retrieve books according to embedding similarity.

### Book Catalogue

**Open Library API**

Provides dynamically retrieved book metadata, including titles, authors, subjects, publication years, page information, and cover identifiers when available.

Catalogue completeness varies. Some books may not have covers, page counts, or direct catalogue links.

## Project Structure

```text
BookMatch/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── .env                  # Local only; excluded from Git
```

* `app.py` — Streamlit frontend.
* `requirements.txt` — Frontend dependencies.
* `README.md` — Project documentation.
* `.gitignore` — Excludes local configuration, secrets, and unnecessary files.
* `.env.example` — Example configuration template for other developers.
* `.env` — Local environment configuration; should never be committed.

The FastAPI recommendation backend currently runs separately in a Kaggle notebook and is exposed through an ngrok tunnel.

## Installation and Setup

### Prerequisites

* Python installation compatible with the project's dependencies.
* Visual Studio Code or another Python development environment.
* A Kaggle account for running the backend notebook.
* An active internet connection.

### 1. Clone or Download the Project

If the repository is hosted on GitHub:

```bash
git clone <YOUR_REPOSITORY_URL>
cd BookMatch
```

Alternatively, download the project and open its folder in VS Code.

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can instead use the VS Code terminal with Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install Frontend Dependencies

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains the dependencies needed by the Streamlit frontend. The language model, embedding model, FAISS, and FastAPI dependencies are installed separately in the backend environment.

### 4. Configure Environment Variables

Create a `.env` file in the project root, in the same directory as `app.py`.

Add the following variable:

```dotenv
BOOKMATCH_API_URL=https://YOUR-NGROK-URL.ngrok-free.dev
```

Replace the placeholder with the actual public URL printed by your running backend notebook. Do not include additional quotation marks around the URL value.

The `.env` file is used to configure the backend endpoint without hardcoding it into the application source code.

A `.env.example` file is included as a template:

```dotenv
BOOKMATCH_API_URL=https://YOUR-NGROK-URL.ngrok-free.dev
```

Copy `.env.example` to `.env` and replace the placeholder with your actual URL.

**Security note:** Never commit your real `.env` file or any authentication tokens to GitHub. The `.env` file should be excluded through `.gitignore`.

### 5. Start the Backend

1. Open the BookMatch backend notebook in Kaggle.
2. Install the backend dependencies and load the required models.
3. Start the FastAPI server.
4. Configure the ngrok authentication token using Kaggle Secrets.
5. Start the ngrok tunnel and copy its public HTTPS URL.

Keep the Kaggle notebook session running while using the application. The backend URL is temporary and may change when the tunnel is restarted.


### 6. Run the Streamlit Application

From the project directory, execute:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, normally:

`http://localhost:8501`

Ensure the Kaggle backend and ngrok tunnel are active before submitting recommendation requests.

## Example Requests

* "I want a dark mystery with suspense."
* "I'm currently reading The Alchemist and want something similar."
* "Recommend a fantasy adventure similar to Harry Potter."
* "I'm in the mood for something emotional but not too long."

## Current Limitations

* Recommendation quality depends on the books and metadata retrieved from Open Library.
* Some books may be unavailable in the catalogue search results or may have incomplete metadata.
* Covers and book links are displayed only when corresponding information is available.
* Multilingual recommendations require further validation to ensure reliable retrieval of books in Arabic, Japanese, Chinese, Korean, and other languages.
* The backend currently depends on an active Kaggle session and ngrok tunnel, so it is not yet a permanent production deployment.

## Future Improvements

* Expand candidate retrieval through multiple catalogue searches and better deduplication.
* Improve multilingual retrieval and language-aware ranking.
* Support recommendations for relevant books even when covers or direct catalogue links are unavailable.
* Improve recommendation diversity and reference-title matching.
* Add more robust error handling, caching, and API deployment options.
* Improve the interface and recommendation presentation.

## Learning Objectives

This project demonstrates the practical integration of several AI concepts:

* Large language models and prompt engineering.
* Structured JSON output and query understanding.
* Text embeddings and semantic representations.
* Vector indexing and similarity search with FAISS.
* Retrieval-based recommendation workflows.
* API-based backend/frontend integration.
* Interactive AI application development.

## Acknowledgements

* [Open Library](https://openlibrary.org/) — Book catalogue and metadata.
* [Hugging Face](https://huggingface.co/) — Language and embedding models.
* [FAISS](https://github.com/facebookresearch/faiss) — Vector similarity search.
* [Streamlit](https://streamlit.io/) — Interactive web application framework.
* [FastAPI](https://fastapi.tiangolo.com/) — Backend API framework.

---

**BookMatch** — Discover your next favourite book through AI.
