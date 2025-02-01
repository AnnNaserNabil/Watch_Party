import streamlit as st
import requests
import os

# Load TMDB API key from environment variable
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    st.error("TMDB API key not found. Please set the TMDB_API_KEY environment variable.")
    st.stop()

TMDB_BASE_URL = "https://api.themoviedb.org/3"

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

def search_person(query):
    """Search for a person (actor or director) based on user input."""
    url = f"{TMDB_BASE_URL}/search/person"
    response = requests.get(url, params={"api_key": TMDB_API_KEY, "query": query})
    if response.status_code == 200:
        results = response.json().get("results", [])
        return {person["name"]: person["id"] for person in results}
    else:
        st.error("Failed to search for person.")
        return {}

def fetch_movies(genre_ids=None, actor_ids=None, director_ids=None):
    """Fetch movies based on genre, actor, or director IDs."""
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": False,
    }

    # Add genre IDs if provided
    if genre_ids:
        params["with_genres"] = ",".join(map(str, genre_ids))

    # Add actor IDs if provided
    if actor_ids:
        params["with_cast"] = ",".join(map(str, actor_ids))

    # Add director IDs if provided
    if director_ids:
        params["with_crew"] = ",".join(map(str, director_ids))

    url = f"{TMDB_BASE_URL}/discover/movie"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error("Failed to fetch movie recommendations.")
        return []

def main():
    st.title("Movie Recommendation System")
    st.write("Enter your preferences to get movie recommendations.")

    # Fetch genres from TMDB
    genres = fetch_genres()
    genre_options = list(genres.keys())

    # Map moods to genres
    mood_to_genre = {
        "Happy": "Comedy",
        "Sad": "Drama",
        "Excited": "Action",
        "Romantic": "Romance",
        "Scared": "Horror"
    }
    mood_options = list(mood_to_genre.keys())

    # User inputs
    selected_genres = st.multiselect("Select Genres", genre_options)
    selected_moods = st.multiselect("Select Moods", mood_options)
    actor_query =
