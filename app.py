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
        "with_genres": ",".join(map(str, genre_ids)) if genre_ids else None,
        "with_cast": ",".join(map(str, actor_ids)) if actor_ids else None,
        "with_crew": ",".join(map(str, director_ids)) if director_ids else None,
    }
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

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

    genres = fetch_genres()
    genre_options = list(genres.keys())
    mood_to_genre = {
        "Happy": "Comedy",
        "Sad": "Drama",
        "Excited": "Action",
        "Romantic": "Romance",
        "Scared": "Horror"
    }
    mood_options = list(mood_to_genre.keys())

    selected_genres = st.multiselect("Select Genres", genre_options)
    selected_moods = st.multiselect("Select Moods", mood_options)
    actor_query = st.text_input("Search for Actor")
    director_query = st.text_input("Search for Director")

    actor_ids = []
    if actor_query:
        actor_search_results = search_person(actor_query)
        if actor_search_results:
            selected_actor = st.selectbox("Select Actor", list(actor_search_results.keys()))
            actor_ids.append(actor_search_results[selected_actor])
        else:
            st.warning("No actors found with that name.")

    director_ids = []
    if director_query:
        director_search_results = search_person(director_query)
        if director_search_results:
            selected_director = st.selectbox("Select Director", list(director_search_results.keys()))
            director_ids.append(director_search_results[selected_director])
        else:
            st.warning("No directors found with that name.")

    if st.button("Get Recommendations"):
        genre_ids = [genres[genre] for genre in selected_genres]
        for mood in selected_moods:
            genre_name = mood_to_genre.get(mood)
            if genre_name and genre_name in genres:
                genre_ids.append(genres[genre_name])

        movies = fetch_movies(genre_ids=genre_ids, actor_ids=actor_ids, director_ids=director_ids)

        if movies:
            st.write("Here are your movie recommendations:")
            for movie in movies[:10]:
                st.write(f"**{movie['title']}** ({movie['release_date'][:4] if movie.get('release_date') else 'N/A'})")
                st.write(f"Overview: {movie.get('overview', 'No overview available.')}")
                st.write(f"Rating: {movie.get('vote_average', 'N/A')}")
                if movie.get("poster_path"):
                    st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=200)
                st.write("---")
        else:
            st.warning("No movies found matching your preferences.")

if __name__ == "__main__":
    main()
