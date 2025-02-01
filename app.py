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
    return {person["name"]: person["id"] for person in response.get("results", [])}

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
    st.write("Start typing a word to get suggestions for actors, directors, moods, or genres.")
    
    genres = fetch_genres()
    query = st.text_input("Search for a Movie, Actor, Director, or Mood")
    
    actor_options = list(search_person(query).keys()) if query else []
    director_options = list(search_person(query).keys()) if query else []
    genre_options = [g for g in genres.keys() if query.lower() in g.lower()]
    mood_to_genre = {"happy": "Comedy", "sad": "Drama", "excited": "Action", "romantic": "Romance", "scared": "Horror"}
    mood_options = [mood for mood in mood_to_genre.keys() if query.lower() in mood]
    
    selected_option = st.selectbox("Suggestions", [""] + actor_options + director_options + genre_options + mood_options)
    
    if st.button("Get Recommendations") and selected_option:
        genre_id = genres.get(selected_option) or genres.get(mood_to_genre.get(selected_option, ""))
        actor_id = search_person(selected_option).get(selected_option)
        director_id = search_person(selected_option).get(selected_option)
        
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
