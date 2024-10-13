import streamlit as st
import pickle
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
# Load the movie dataset and similarity matrix
movies_data = pd.read_csv('movies.csv')

# Fill any missing values in the relevant columns
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director', 'overview', 'id']
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Function to recommend movies by name
# Function to recommend movies by name and display posters
# Function to recommend movies by name and display posters horizontally
def name_wise(selected_movie, numbers):
    combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + \
                        movies_data['cast'] + ' ' + movies_data['director'] + ' ' + movies_data['overview'] + ' ' + \
                        movies_data['id'].astype(str)

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)

    similarity = cosine_similarity(feature_vectors)

    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(selected_movie, list_of_all_titles)
    
    if not find_close_match:
        st.write("No matching movies found.")
        return
    
    close_match = find_close_match[0]
    index_of_the_movie = movies_data[movies_data.title == close_match].index[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    st.write("Movies suggested for you: \n")
    
    # Create columns to display movies horizontally
    cols = st.columns(numbers)
    
    for i, movie in enumerate(sorted_similar_movies[:numbers]):
        index = movie[0]
        title_from_index = movies_data['title'].iloc[index]
        movie_id = movies_data['id'].iloc[index]
        
        # Fetch and display the movie poster and title in columns
        poster_url = fetch_poster(movie_id)
        with cols[i]:  # Display in each column
            st.image(poster_url, use_column_width=True)
            st.write(f"{title_from_index}")

# Function to recommend movies by actor and display posters horizontally
def actor_wise(actor, numbers):
    matching_movies = movies_data[movies_data['cast'].str.contains(actor, case=False)]
    
    if matching_movies.empty:
        st.write("No movies found for the given actor.")
        return
    
    matching_movies = matching_movies.reset_index(drop=True)
    list_of_all_titles = matching_movies['title'].tolist()

    combined_features = matching_movies['genres'] + ' ' + matching_movies['keywords'] + ' ' + matching_movies['tagline'] + ' ' + \
                        matching_movies['cast'] + ' ' + matching_movies['director'] + ' ' + matching_movies['overview'] + ' ' + \
                        matching_movies['id'].astype(str)

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)
    
    find_close_match = difflib.get_close_matches(list_of_all_titles[0], list_of_all_titles)
    index_of_the_movie = matching_movies[matching_movies.title == find_close_match[0]].index[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    st.write("Movies suggested for you: \n")
    
    # Create columns to display movies horizontally
    cols = st.columns(numbers)
    
    for i, movie in enumerate(sorted_similar_movies[:numbers]):
        index = movie[0]
        title = matching_movies['title'].iloc[index]
        movie_id = matching_movies['id'].iloc[index]
        
        # Fetch and display the movie poster and title in columns
        poster_url = fetch_poster(movie_id)
        with cols[i]:
            st.image(poster_url, use_column_width=True)
            st.write(f"{title}")

# Function to recommend movies by genre and display posters horizontally
def genre_wise(genre, numbers):
    matching_movies = movies_data[movies_data['genres'].str.contains(genre, case=False)]
    
    if matching_movies.empty:
        st.write("No movies found for the specified genre.")
        return
    
    matching_movies = matching_movies.reset_index(drop=True)
    list_of_all_titles = matching_movies['title'].tolist()

    combined_features = matching_movies['genres'] + ' ' + matching_movies['keywords'] + ' ' + matching_movies['tagline'] + ' ' + \
                        matching_movies['cast'] + ' ' + matching_movies['director'] + ' ' + matching_movies['overview'] + ' ' + \
                        matching_movies['id'].astype(str)

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)

    find_close_match = difflib.get_close_matches(list_of_all_titles[0], list_of_all_titles)
    index_of_the_movie = matching_movies[matching_movies.title == find_close_match[0]].index[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    st.write("Movies suggested for you: \n")
    
    # Create columns to display movies horizontally
    cols = st.columns(numbers)
    
    for i, movie in enumerate(sorted_similar_movies[:numbers]):
        index = movie[0]
        title = matching_movies['title'].iloc[index]
        movie_id = matching_movies['id'].iloc[index]
        
        # Fetch and display the movie poster and title in columns
        poster_url = fetch_poster(movie_id)
        with cols[i]:
            st.image(poster_url, use_column_width=True)
            st.write(f"{title}")

# Function to recommend movies by director and display posters horizontally
def director_wise(director, numbers):
    matching_movies = movies_data[movies_data['director'].str.contains(director, case=False)]
    
    if matching_movies.empty:
        st.write("No movies found for the given director.")
        return
    
    matching_movies = matching_movies.reset_index(drop=True)
    list_of_all_titles = matching_movies['title'].tolist()

    combined_features = matching_movies['genres'] + ' ' + matching_movies['keywords'] + ' ' + \
                        matching_movies['tagline'] + ' ' + matching_movies['cast'] + ' ' + \
                        matching_movies['director'] + ' ' + matching_movies['overview'] + ' ' + \
                        matching_movies['id'].astype(str)

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)

    find_close_match = difflib.get_close_matches(list_of_all_titles[0], list_of_all_titles)
    index_of_the_movie = matching_movies[matching_movies.title == find_close_match[0]].index[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    st.write("Movies suggested for you: \n")
    
    # Create columns to display movies horizontally
    cols = st.columns(numbers)
    
    for i, movie in enumerate(sorted_similar_movies[:numbers]):
        index = movie[0]
        title = matching_movies['title'].iloc[index]
        movie_id = matching_movies['id'].iloc[index]
        
        # Fetch and display the movie poster and title in columns
        poster_url = fetch_poster(movie_id)
        with cols[i]:
            st.image(poster_url, use_column_width=True)
            st.write(f"{title}")


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZDA2ZmY5OWQ5Mzc4ZjAwYTVjZGIxOTlkYTcxN2U4NiIsIm5iZiI6MTcyODUwMzEwMy4xMDk0NDUsInN1YiI6IjY3MDZkOGIwOGZiNzIzYTBiNmUwYjdjZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0OPL_fWUGh2jY4S8xexDQipIt8gG4m6HOQ8Pufiljgg"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


# Streamlit UI
st.title("Movie Recommender System")


# Select how to receive movie suggestions
option = st.selectbox(
    "How would you like to receive movie suggestions?",
    ("By Movie Name", "By Actor's Name", "By Genre", "By Director"),
    index=None, placeholder="Select suggestion method"
)
st.write("You selected:", option)

# Handle suggestions by movie name
if option == "By Movie Name":
    selected_movie = st.selectbox(
        "Enter your movie name:",
        movies_data['title'].values, index=None, placeholder="Select movie name"
    )
    st.write("You selected:", selected_movie)

    numbers = st.selectbox(
        "Enter the number of movies:",
        range(1, 11), index=0, placeholder="Number of movies"
    )

    if st.button("Recommend"):
        name_wise(selected_movie, int(numbers))

# Handle suggestions by actor's name
elif option == "By Actor's Name":
    actor = st.text_input("Enter the actor's name:", placeholder="Actor...")
    st.write("You selected:", actor)

    numbers = st.selectbox(
        "Enter the number of movies:",
        range(1, 11), index=0, placeholder="Number of movies"
    )

    if st.button("Recommend"):
        actor_wise(actor, int(numbers))

# Handle suggestions by genre
elif option == "By Genre":
    genre = st.selectbox(
        "Enter genre:",
        ("Adventure", "Action", "Comedy", "Sci-fi", "Thriller", "Horror", "Drama", "Fantasy", "Animation", "Musical"),
        index=None, placeholder="Genre"
    )
    st.write("You selected:", genre)

    numbers = st.selectbox(
        "Enter the number of movies:",
        range(1, 11), index=0, placeholder="Number of movies"
    )

    if st.button("Recommend"):
        genre_wise(genre, int(numbers))


elif option == "By Director":
    director = st.selectbox(
        "Enter the directors name:",
        movies_data['director'].values, index=None, placeholder="Director:"
    )
    st.write("You selected:", director)

    numbers = st.selectbox(
        "Enter the number of movies:",
        range(1, 11), index=0, placeholder="Number of movies"
    )

    if st.button("Recommend"):
        director_wise(director, int(numbers))
