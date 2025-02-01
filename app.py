def main():
    # Title and header
    st.markdown(
        """
        <h1 class='stHeader' style='color: red;'>
            🎬 Let's Watch<br>
            The ultimate movie recommendation system!
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.write("Select your preferences below and get personalized movie recommendations.")

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
    selected_eras = st.sidebar.multiselect("Select Movie Era 📅", era_options)

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
    if st.sidebar.button("Get Recommendations 🍿"):
        if not genre_ids and not release_date_ranges:
            st.warning("Please provide at least one genre, mood, or movie era to get recommendations.")
        else:
            # Show a progress bar while fetching recommendations
            with st.spinner("Fetching recommendations..."):
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
                st.success("Here are your movie recommendations:")
                for movie in list(unique_movies)[:10]:  # Show top 10 results
                    with st.container():
                        # Fetch additional details (top 5 actors, director, and best review)
                        top_actors, director, best_review = fetch_movie_details(movie["id"])

                        st.markdown(
                            f"""
                            <div class="movie-card">
                                {f"<img src='https://image.tmdb.org/t/p/w500{movie['poster_path']}' width='200' />" if movie.get("poster_path") else ""}
                                <h3>{movie['title']} ({movie['release_date'][:4] if movie.get('release_date') else 'N/A'})</h3>
                                <p><strong>Overview:</strong> {movie.get('overview', 'No overview available.')}</p>
                                <p><strong>Rating:</strong> ⭐ {movie.get('vote_average', 'N/A')}</p>
                                <p><strong>Top 5 Actors:</strong> {', '.join(top_actors) if top_actors else 'N/A'}</p>
                                <p><strong>Director:</strong> {director if director else 'N/A'}</p>
                                <p><strong>Best Review:</strong> {best_review['content'] if best_review else 'No reviews available.'}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.warning("No movies found matching your preferences.")

if __name__ == "__main__":
    main()
