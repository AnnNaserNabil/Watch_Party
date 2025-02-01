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

    # Map movie eras to release date ranges
    era_to_dates = {
        "1950s": ("1950-01-01", "1959-12-31"),
        "1960s": ("1960-01-01", "1969-12-31"),
        "1970s": ("1970-01-01", "1979-12-31"),
        "1980s": ("1980-01-01", "1989-12-31"),
        "1990s": ("1990-01-01", "1999-12-31"),
        "2000s": ("2000-01-01", "2009-12-31"),
        "2010s": ("2010-01-01", "2019-12-31"),
        "2020s": ("2020-01-01", "2029-12-31"),
    }
    era_options = list(era_to_dates.keys())

    # User inputs
    st.sidebar.header("Filters")
    selected_genres = st.sidebar.multiselect("Select Genres", genre_options)
    selected_moods = st.sidebar.multiselect("Select Moods", mood_options)
    selected_eras = st.sidebar.multiselect("Select Movie Era", era_options)

    # Map selected moods to genre IDs
    genre_ids = [genres[genre] for genre in selected_genres if genre in genres]
    for mood in selected_moods:
        genre_name = mood_to_genre.get(mood)
        if genre_name and genre_name in genres:
            genre_ids.append(genres[genre_name])

    # Ensure genre IDs are unique
    genre_ids = list(set(genre_ids))

    # Map selected eras to release date ranges
    release_date_ranges = []
    for era in selected_eras:
        if era in era_to_dates:
            release_date_ranges.append(era_to_dates[era])

    # Fetch recommendations when the button is clicked
    if st.sidebar.button("Get Recommendations"):
        if not genre_ids and not release_date_ranges:
            st.warning("Please provide at least one genre, mood, or movie era to get recommendations.")
        else:
            # Fetch movies for each release date range and combine results
            all_movies = []
            for release_date_gte, release_date_lte in release_date_ranges:
                movies = fetch_movies(genre_ids=genre_ids, release_date_gte=release_date_gte, release_date_lte=release_date_lte)
                all_movies.extend(movies)

            # If no eras are selected, fetch movies without date filters
            if not release_date_ranges:
                all_movies = fetch_movies(genre_ids=genre_ids)

            # Remove duplicates (if any)
            unique_movies = {movie["id"]: movie for movie in all_movies}.values()

            if unique_movies:
                st.write("Here are your movie recommendations:")
                for movie in list(unique_movies)[:10]:  # Show top 10 results
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
