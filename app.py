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
    try:
        response = requests.get(url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
        response.raise_for_status()  # Raise an error for bad status codes
        genres = response.json().get("genres", [])
        return {g["name"]: g["id"] for g in genres}
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch genres: {e}")
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
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch movie recommendations: {e}")
        return []

def fetch_movie_details(movie_id):
    """Fetch additional details (credits and reviews) for a movie."""
    credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    reviews_url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"

    try:
        # Fetch credits
        credits_response = requests.get(credits_url, params={"api_key": TMDB_API_KEY})
        credits_response.raise_for_status()
        credits = credits_response.json()

        # Fetch reviews
        reviews_response = requests.get(reviews_url, params={"api_key": TMDB_API_KEY})
        reviews_response.raise_for_status()
        reviews = reviews_response.json().get("results", [])

        # Extract top 5 actors and director
        cast = credits.get("cast", [])
        crew = credits.get("crew", [])
        top_actors = [actor["name"] for actor in cast[:5]]  # Top 5 actors
        director = next((member["name"] for member in crew if member["job"] == "Director"), None)

        # Find the best-written review (highest-rated review)
        best_review = None
        if reviews:
            best_review = max(reviews, key=lambda x: x.get("author_details", {}).get("rating", 0))

        return top_actors, director, best_review
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch movie details: {e}")
        return None, None, None

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
    mood_options = list(mood_to_genre.keys())

    # Map movie eras to release date ranges
    era_to_dates = {
        "1950s 🕺": ("1950-01-01", "1959-12-31"),
        "1960s 🌸": ("1960-01-01", "1969-12-31"),
        "1970s 🕶️": ("1970-01-01", "1979-12-31"),
        "1980s 🎸": ("1980-01-01", "1989-12-31"),
        "1990s 📼": ("1990-01-01", "1999-12-31"),
        "2000s 📱": ("2000-01-01", "2009-12-31"),
        "2010s 🚀": ("2010-01-01", "2019-12-31"),
        "2020s 🎥": ("2020-01-01", "2029-12-31"),
    }
    era_options = list(era_to_dates.keys())

    # Sidebar for filters
    st.sidebar.header("🎛️ Filters")
    selected_genres = st.sidebar.multiselect("Select Genres 🎭", genre_options)
    selected_moods = st.sidebar.multiselect("Select Moods 😃", mood_options)
    selected_eras
