import streamlit as st
import requests
import os

# Load TMDB API key from environment variable
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    st.error("TMDB API key not found. Please set the TMDB_API_KEY environment variable.")
    st.stop()

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Custom CSS for beautification
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .movie-card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        background-color: #ffffff;  /* White background */
        color: #333333;  /* Dark gray text */
    }
    .movie-card h3 {
        margin-top: 0;
        color: #4CAF50;  /* Green header */
    }
    .movie-card p {
        color: #333333;  /* Dark gray text */
    }
    .movie-card img {
        border-radius: 10px;
    }
    .stHeader {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;  /* Green header */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def fetch_genres():
    """Fetch list of genres from TMDB API."""
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    response = requests.get(url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {g["name"]: g["id"] for g in genres}
    else:
        st.error("Failed to fetch genres.")
        return {}

def fetch_movies(genre_ids=None, release_date_gte=None, release_date_lte=None):
    """Fetch movies based on genre IDs and release date range."""
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": False,
    }

    # Add genre IDs if provided
    if genre_ids:
        params["with_genres"] = ",".join(map(str, genre_ids))

    # Add release date range if provided
    if release_date_gte:
        params["primary_release_date.gte"] = release_date_gte
    if release_date_lte:
        params["primary_release_date.lte"] = release_date_lte

    url = f"{TMDB_BASE_URL}/discover/movie"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error("Failed to fetch movie recommendations.")
        return []

def main():
    # Title and header
    st.markdown("<h1 class='stHeader'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
    st.write("Welcome to the ultimate movie recommendation system! Select your preferences below and get personalized movie recommendations.")

    # Fetch genres from TMDB
    genres = fetch_genres()
    genre_options = list(genres.keys())

    # Map moods to genres
    mood_to_genre = {
        "😊 Happy": "Comedy",
        "😢 Sad": "Drama",
        "🎉 Excited": "Action",
        "💖 Romantic": "Romance",
        "👻 Scared": "Horror"
    }
    mood_options =
