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
    response = requests.get(url, params={"api_key": TMDB_API_KEY, "language": "en-US"}).json()
    return {g["name"]: g["id"] for g in response.get("genres", [])}

def search_person(query):
    """Search for an actor or director based on user input."""
    url = f"{TMDB_BASE_URL}/search/person"
    response = requests.get(url, params={"api_key": TMDB_API_KEY, "query": query}).json()
    return [person["name"] for person in response.get("results", [])]

def fetch_movies(genre_id=None, actor_id=None, director_id=None):
    """Fetch movies based on genre, actor, or director ID."""
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": False,
    }
    if genre_id:
        params["with_genres"] = genre_id
    if actor_id:
        params["with_cast"] = actor_id
    if director_id:
        params["with_crew"] = director_id

    url = f"{TMDB_BASE_URL}/discover/movie"
    response = requests.get(url, params=params).json()
    return response.get("results", [])

def main():
    st.title("Movie Recommendation System")
    st.write("Start typing to get suggestions for genre, actor, or director.")
    
    genres = fetch_genres()
    genre = st.selectbox("Select Genre", [""] + list(genres.keys()))
    actor_query = st.text_input("Search for an Actor")
    director_query = st.text_input("Search for a Director")
    
    actor_options = search_person(actor_query) if actor_query else []
    director_options = search_person(director_query) if director_query else []
    
    actor = st.selectbox("Select Actor", [""] + actor_options)
    director = st.selectbox("Select Director", [""] + director_options)
    
    if st.button("Get Recommendations"):
        genre_id = genres.get(genre)
        actor_id = search_person(actor)[0] if actor else None
        director_id = search_person(director)[0] if director else None
        
        movies = fetch_movies(genre_id=genre_id, actor_id=actor_id, director_id=director_id)
        
        if movies:
            st.write("Here are your movie recommendations:")
            for movie in movies[:10]:
                st.write(f"**{movie['title']}** ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})")
                st.write(f"Overview: {movie['overview']}")
                st.write(f"Rating: {movie['vote_average']}")
                if movie["poster_path"]:
                    st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=200)
                st.write("---")
        else:
            st.warning("No movies found matching your preferences.")

if __name__ == "__main__":
    main()
