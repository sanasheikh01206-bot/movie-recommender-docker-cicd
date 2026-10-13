import os
import pickle
import pytest
from sklearn.metrics.pairwise import linear_kernel

def test_artifacts_exist():
    assert os.path.exists("df.pkl"), "df.pkl is missing"
    assert os.path.exists("indices.pkl"), "indices.pkl is missing"
    assert os.path.exists("tfidf_matrix.pkl"), "tfidf_matrix.pkl is missing"

def test_recommendation_logic():
    with open("df.pkl", "rb") as f:
        df = pickle.load(f)
    with open("indices.pkl", "rb") as f:
        indices = pickle.load(f)
    with open("tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)

    # Pick the first movie title
    sample_title = df["title"].iloc[0]
    idx = indices[sample_title]
    if hasattr(idx, "__len__"):
        idx = idx.iloc[0]

    sim_scores = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    top_indices = sim_scores.argsort()[::-1][1:6]

    assert len(top_indices) == 5, "Recommendation count should be 5"