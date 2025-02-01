import streamlit as st
import requests
import os

# Load TMDB API key from environment variable
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    st.error("TMDB API key not found. Please set the TMDB_API_KEY environment variable.")
    st.stop()

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Function to fetch movies based on genre, actor, director, or mood
def fetch_movies(genre=None, actor=None, director=None, mood=None):
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": False,
    }

    if genre:
        # Fetch genre ID from genre name
        genre_url = f"{TMDB_BASE_URL}/genre/movie/list"
        genre_response = requests.get(genre_url, params={"api_key": TMDB_API_KEY}).json()
        genre_id = next((g["id"] for g in genre_response["genres"] if g["name"].lower() == genre.lower()), None)
        if genre_id:
            params["with_genres"] = genre_id

    if actor:
        # Fetch movies featuring the actor
        search_url = f"{TMDB_BASE_URL}/search/person"
        search_params = {"api_key": TMDB_API_KEY, "query": actor}
        search_response = requests.get(search_url, params=search_params).json()
        if search_response["results"]:
            actor_id = search_response["results"][0]["id"]
            params["with_cast"] = actor_id

    if director:
        # Fetch movies directed by the director
        search_url = f"{TMDB_BASE_URL}/search/person"
        search_params = {"api_key": TMDB_API_KEY, "query": director}
        search_response = requests.get(search_url, params=search_params).json()
        if search_response["results"]:
            director_id = search_response["results"][0]["id"]
            params["with_crew"] = director_id

    if mood:
        # Map mood to genre (example mapping)
        mood_to_genre = {
            "happy": "Comedy",
            "sad": "Drama",
            "excited": "Action",
            "romantic": "Romance",
            "scared": "Horror",
        }
        genre = mood_to_genre.get(mood.lower())
        if genre:
            genre_url = f"{TMDB_BASE_URL}/genre/movie/list"
            genre_response = requests.get(genre_url, params={"api_key": TMDB_API_KEY}).json()
            genre_id = next((g["id"] for g in genre_response["genres"] if g["name"].lower() == genre.lower()), None)
            if genre_id:
                params["with_genres"] = genre_id

    # Fetch movies based on the parameters
    discover_url = f"{TMDB_BASE_URL}/discover/movie"
    response = requests.get(discover_url, params=params).json()
    return response.get("results", [])

# Streamlit app
def main():
    st.title("Movie Recommendation System")
    st.write("Enter your preferences to get movie recommendations!")

    # User inputs
    genre = st.text_input("Enter your preferred genre (e.g., Action, Comedy, Drama):")
    actor = st.text_input("Enter your favorite actor:")
    director = st.text_input("Enter your favorite director:")
    mood = st.text_input("Enter your current mood (e.g., happy, sad, excited):")

    if st.button("Get Recommendations"):
        if not any([genre, actor, director, mood]):
            st.error("Please provide at least one preference.")
        else:
            movies = fetch_movies(genre=genre, actor=actor, director=director, mood=mood)
            if movies:
                st.write("Here are your movie recommendations:")
                for movie in movies[:10]:  # Display top 10 recommendations
                    st.write(f"**{movie['title']}** ({movie['release_date'][:4]})")
                    st.write(f"Overview: {movie['overview']}")
                    st.write(f"Rating: {movie['vote_average']}")
                    if movie["poster_path"]:
                        st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=200)
                    st.write("---")
            else:
                st.warning("No movies found matching your preferences.")

if __name__ == "__main__":
    main()
