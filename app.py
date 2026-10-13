import streamlit as st
import pickle
import requests
from sklearn.metrics.pairwise import linear_kernel

# Your OMDb API Key
OMDB_API_KEY = "f6647b87"

def fetch_poster_by_title(title):
    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={"t": title.strip(), "apikey": OMDB_API_KEY},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            poster = data.get("Poster")
            if poster and poster != "N/A":
                return poster
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

@st.cache_resource
def load_artifacts():
    with open("df.pkl", "rb") as f:
        df = pickle.load(f)
    with open("indices.pkl", "rb") as f:
        indices = pickle.load(f)
    with open("tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)
    return df, indices, tfidf_matrix

df, indices, tfidf_matrix = load_artifacts()

def get_recommendations(title, top_n=5):
    idx = indices[title]
    if hasattr(idx, "__len__"):
        idx = idx.iloc[0]

    # Calculate similarity on the fly
    cosine_sim = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Grab top recommendations (skip self at index 0)
    sim_scores = sim_scores[1:top_n + 1]
    
    recommended_titles = []
    recommended_posters = []
    
    for i, _ in sim_scores:
        movie_title = df.iloc[i]["title"]
        recommended_titles.append(movie_title)
        recommended_posters.append(fetch_poster_by_title(movie_title))
        
    return recommended_titles, recommended_posters

# --- UI Layout ---
st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.title("🎬 Movie Recommender System")

movie_list = df["title"].dropna().unique()
selected_movie = st.selectbox("Select a movie from the catalog:", movie_list)

if st.button("Show Recommendations"):
    with st.spinner("Fetching recommendations and posters..."):
        names, posters = get_recommendations(selected_movie)
        
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.text(name)
                st.image(poster, use_container_width=True)