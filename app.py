import streamlit as st
import requests

# TMDB API configuration
TMDB_API_KEY = "your_tmdb_api_key_here"  # Replace with your TMDB API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Fetch genres from TMDB
def fetch_genres():
    url = f"{TMDB_BASE_URL}/genre/movie/list?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"]: genre["id"] for genre in genres}
    else:
        st.error("Failed to fetch genres from TMDB.")
        return {}

# Fetch movies based on filters
def fetch_movies(genre_ids=None, release_date_gte=None, release_date_lte=None):
    url = f"{TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}"
    if genre_ids:
        url += f"&with_genres={','.join(map(str, genre_ids))}"
    if release_date_gte:
        url += f"&release_date.gte={release_date_gte}"
    if release_date_lte:
        url += f"&release_date.lte={release_date_lte}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error("Failed to fetch movies from TMDB.")
        return []

# Fetch movie details (top 5 actors, director, and best review)
def fetch_movie_details(movie_id):
    # Fetch credits
    credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits?api_key={TMDB_API_KEY}"
    credits_response = requests.get(credits_url)
    top_actors = []
    director = None
    if credits_response.status_code == 200:
        credits = credits_response.json()
        top_actors = [actor["name"] for actor in credits.get("cast", [])[:5]]
        director = next((member["name"] for member in credits.get("crew",
