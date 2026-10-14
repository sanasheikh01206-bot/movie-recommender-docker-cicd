# 🎬 End-to-End Content-Based Movie Recommender System

A production-grade, content-based movie recommender system that vectorizes movie metadata, computes real-time similarity metrics, fetches poster artwork on the fly via external APIs, and serves recommendations through an intuitive Streamlit interface. 

The project includes unit test validation with PyTest, automated container builds via GitHub Actions CI/CD, publishing to Docker Hub, and live deployments on both Render and Streamlit Cloud.

---

## 🌟 Key Features

- **Content-Based Filtering:** Computes similarity metrics using TF-IDF vectorization and Scikit-Learn's `linear_kernel`.
- **Dynamic On-the-Fly Scoring:** Instead of precomputing and storing a heavy multi-gigabyte cosine distance matrix, similarity scores are computed dynamically in milliseconds per query vector ($O(N)$), keeping model artifacts light (< 30 MB) and eliminating heavy cloud storage requirements.
- **Real-Time Poster Retrieval:** Integrated with OMDb/TMDB REST endpoints to fetch live high-resolution posters without ISP DNS-level blocking.
- **Robust Exception Handling:** Gracefully handles ambiguous title duplicates, missing IDs, and fallback placeholder covers.
- **Automated CI/CD Pipeline:** Fully configured GitHub Actions workflow that executes PyTest test suites, validates artifacts, builds a multi-layer Docker image, and pushes versioned tags to Docker Hub.
- **Cloud-Ready Deployment:** Production configuration ready for containerized hosting on Render and serverless hosting on Streamlit Community Cloud.

---

## 🏗️ Architecture & Workflow

```
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
| **API & Networking** | [Requests](https://requests.readthedocs.io/), [OMDb API](https://www.omdbapi.com/) / [TMDB API](https://www.themoviedb.org/) |
| **Testing** | [PyTest](https://docs.pytest.org/) |
| **Containerization** | [Docker](https://www.docker.com/) |
| **CI/CD & Automation** | [GitHub Actions](https://github.com/features/actions) |
| **Deployment Platforms** | [Render](https://render.com/), [Streamlit Community Cloud](https://streamlit.io/cloud) |

---

## 🧠 Model Training & Artifact Generation

The content-based recommendation model was developed through the following stages:

1. **Feature Engineering:** Extracted relevant metadata columns including movie overviews, genres, cast members, and director information. Text fields were sanitized, lowercased, and combined into a single unified `tags`/`soup` representation.
2. **TF-IDF Transformation:** Transformed textual metadata into sparse feature vectors using Scikit-Learn’s `TfidfVectorizer` (with English stop-words removed).
3. **Artifact Serialization:**
   - `df.pkl`: Filtered Pandas DataFrame holding titles, metadata, and movie identifiers.
   - `indices.pkl`: Mapping dictionary / Series connecting movie titles to matrix row indices.
   - `tfidf_matrix.pkl`: Compressed sparse matrix of TF-IDF feature representations.
   *(Note: By saving the vector matrix rather than the dense full pairwise similarity matrix, file size was constrained under 30 MB, avoiding Git LFS bottlenecks).*

---

## 📁 Repository Structure

```text
movie-recommender-docker-cicd/
│
├── .github/
│   └── workflows/
│       └── main.yml           # Automated CI/CD test and Docker Hub deploy pipeline
│
├── artifacts/ (or root)
│   ├── df.pkl                 # Cleaned movie metadata DataFrame (~28 MB)
│   ├── indices.pkl            # Title-to-index lookup table (~1.4 MB)
│   └── tfidf_matrix.pkl       # Serialized TF-IDF feature matrix (~18 MB)
│
├── app.py                     # Streamlit frontend & inference script
├── test_app.py                # Automated PyTest unit tests
├── requirements.txt           # Project dependencies
├── Dockerfile                 # Docker container build specifications
├── .dockerignore              # Files excluded from the Docker build context
└── README.md                  # System documentation
```

---

## ⚡ Local Setup & Execution

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/<your-username>/movie-recommender-docker-cicd.git
cd movie-recommender-docker-cicd

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure API Credentials
Open `app.py` and assign your activated OMDb API key:
```python
OMDB_API_KEY = "your_omdb_key"
```

### 4. Run Automated Unit Tests
```bash
pytest test_app.py
```

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🐳 Docker Setup

### Build the Image
```bash
docker build -t movie-recommender:latest .
```

### Run the Container
```bash
docker run -p 8501:8501 movie-recommender:latest
```
Access the application locally at `http://localhost:8501`.

---

## 🔄 CI/CD Automation (GitHub Actions)

The included `.github/workflows/main.yml` pipeline triggers automatically on any `push` to `main`:

1. **Environment Provisioning:** Sets up a clean Ubuntu runner with Python 3.10.
2. **Dependency Resolution:** Installs libraries specified in `requirements.txt`.
3. **Unit Testing:** Executes `pytest test_app.py` to assert that artifacts exist, load properly, and recommendation dimensions remain strictly consistent.
4. **Docker Packaging:** Logs in to Docker Hub using GitHub Encrypted Secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) and pushes the newly compiled container image.
5. **Deployment Webhook (Optional):** Pings Render's deploy hook to redeploy the newly updated image automatically.

---

## 🌐 Deployments

* **Render Deployment:** Hosted as a containerized web service with dynamic port assignment (`--server.port $PORT --server.address 0.0.0.0`).
* **Streamlit Community Cloud:** Connected directly to the repository branch, launching `app.py` with zero container overhead.

---

## 📜 License
Distributed under the MIT License. Feel free to use, modify, and distribute for educational and commercial projects.