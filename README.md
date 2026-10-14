# 🎬 End-to-End Content-Based Movie Recommender System

A production-grade, content-based movie recommender system that vectorizes movie metadata, computes real-time similarity metrics, fetches poster artwork on the fly via external APIs, and serves recommendations through an intuitive Streamlit interface.

The project includes unit test validation with PyTest, automated container builds via GitHub Actions CI/CD, publishing to Docker Hub, and live deployments on both Render and Streamlit Cloud.

---

## 🚀 Quick Start: 2 Ways to Run on Your Computer

Choose whichever option works best for your setup:

### Option 1: Run with Docker Desktop (Containerized)

No need to install Python or project libraries manually—Docker packages everything into an isolated container.

1. **Make sure Docker Desktop is running** on your computer.
2. Open your terminal / command prompt.
3. **Run the container directly from Docker Hub:**
   ```bash
   docker run -d -p 8501:8501 --name movie-recommender <your-dockerhub-username>/movie-recommender:latest
   ```
   *(Or if you cloned the repository and want to build it locally:)*
   ```bash
   docker build -t movie-recommender .
   docker run -p 8501:8501 movie-recommender
   ```
4. Open your browser and go to:
   ```text
   http://localhost:8501
   ```
5. **To stop the app:**
   ```bash
   docker stop movie-recommender
   ```

---

### Option 2: Run Live with Streamlit

🌐 Live Deployments

* **Streamlit Cloud:** `https://movie-recommender-docker-cicd-k52qpqunmsjfdck9hesnnr.streamlit.app/`

---

## 🌟 Key Features

* **Content-Based Filtering:** Computes similarity metrics using TF-IDF vectorization and Scikit-Learn's `linear_kernel`.
* **Dynamic On-the-Fly Scoring:** Instead of precomputing and storing a heavy multi-gigabyte cosine distance matrix, similarity scores are computed dynamically in milliseconds per query vector ($O(N)$), keeping model artifacts light (< 30 MB) and eliminating cloud storage requirements.
* **Real-Time Poster Retrieval:** Integrated with OMDb REST endpoints to fetch live high-resolution posters without ISP DNS-level blocking.
* **Robust Exception Handling:** Gracefully handles ambiguous title duplicates, missing IDs, and fallback placeholder covers.
* **Automated CI/CD Pipeline:** Fully configured GitHub Actions workflow that executes PyTest test suites, validates artifacts, builds a multi-layer Docker image, and pushes versioned tags to Docker Hub.
* **Cloud-Ready Deployment:** Production configuration ready for containerized hosting on Render and serverless hosting on Streamlit Community Cloud.

---

## 🏗️ Architecture & Workflow

```text
[Raw Metadata (CSV)]
       │
       ▼
[Data Preprocessing & Feature Extraction]
  - Combined features (Overview, Genres, Keywords, Cast)
  - Text normalization & stop-word pruning
       │
       ▼
[TF-IDF Vectorization]
  - Generated tfidf_matrix.pkl (~17.9 MB)
  - Serialized df.pkl (~28.2 MB) & indices.pkl (~1.4 MB)
       │
       ▼
[Streamlit Application (app.py)]
  - In-memory cached artifact loading (@st.cache_resource)
  - On-the-fly cosine similarity calculation via linear_kernel
  - Poster extraction via OMDb API query
       │
       ▼
[CI/CD & Containerization Pipeline]
  - PyTest suite validation (test_app.py)
  - Automated GitHub Actions trigger on push
  - Docker container build & Docker Hub push
  - Cloud deployment webhook / Streamlit Cloud sync
```

---

## 🛠️ Tech Stack & Tooling

| Domain | Technologies & Libraries |
| :--- | :--- |
| **User Interface** | [Streamlit](https://streamlit.io/) |
| **Machine Learning & NLP** | [Scikit-Learn](https://scikit-learn.org/) (`TfidfVectorizer`, `linear_kernel`), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) |
| **API & Networking** | [Requests](https://requests.readthedocs.io/), [OMDb API](https://www.omdbapi.com/) |
| **Testing** | [PyTest](https://docs.pytest.org/) |
| **Containerization** | [Docker](https://www.docker.com/), Docker Desktop |
| **CI/CD & Automation** | [GitHub Actions](https://github.com/features/actions) |
| **Cloud Deployments** | [Render](https://render.com/), [Streamlit Community Cloud](https://streamlit.io/cloud) |

---

## 🧠 Model Training & Artifact Generation

The recommendation model was trained with the following pipeline:

1. **Feature Engineering:** Extracted relevant metadata columns including movie overviews, genres, cast members, and keywords. Text fields were sanitized, lowercased, and combined into a single unified representation.
2. **TF-IDF Transformation:** Transformed textual metadata into sparse feature vectors using Scikit-Learn’s `TfidfVectorizer` (with English stop-words removed).
3. **Artifact Serialization:**
   * `df.pkl`: Cleaned Pandas DataFrame holding titles, metadata, and movie identifiers.
   * `indices.pkl`: Mapping dictionary / Series connecting movie titles to matrix row indices.
   * `tfidf_matrix.pkl`: Compressed sparse matrix of TF-IDF feature representations.
   *(Note: By saving the sparse feature matrix rather than the dense full pairwise similarity matrix, file size was kept under 30 MB, completely avoiding Git LFS bottlenecks).*

---

## 📁 Repository Structure

```text
movie-recommender-docker-cicd/
│
├── .github/
│   └── workflows/
│       └── main.yml           # Automated CI/CD test and Docker Hub deploy pipeline
│
├── df.pkl                     # Cleaned movie metadata DataFrame (~28 MB)
├── indices.pkl                # Title-to-index lookup table (~1.4 MB)
├── tfidf_matrix.pkl           # Serialized TF-IDF feature matrix (~18 MB)
│
├── app.py                     # Streamlit frontend & inference script
├── test_app.py                # Automated PyTest unit tests
├── requirements.txt           # Project dependencies
├── Dockerfile                 # Docker container build specifications
├── .dockerignore              # Files excluded from the Docker build context
└── README.md                  # System documentation
```

---

## 🧪 Running Unit Tests

Run automated tests locally with PyTest before committing changes:

```bash
pytest test_app.py
```

This validates that all required pickle artifacts are present and that the recommendation math produces valid outputs.

---

## 🔄 CI/CD Automation (GitHub Actions)

The `.github/workflows/main.yml` pipeline runs automatically on every push to `main`:

1. **Environment Provisioning:** Spins up an Ubuntu runner with Python 3.10.
2. **Dependency Resolution:** Installs libraries specified in `requirements.txt`.
3. **Unit Testing:** Executes `pytest test_app.py` to assert that artifacts exist, load cleanly, and recommendation dimensions remain accurate.
4. **Docker Packaging:** Logs in to Docker Hub using encrypted repository secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) and pushes the latest container image.
5. **Deployment Trigger:** Calls Render's deploy hook URL to automatically trigger a live redeployment.

