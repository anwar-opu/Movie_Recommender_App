import requests
import streamlit as st
import pickle
import pandas as pd

# Function to fetch movie posters
def fetch_poster(movie_id):
    api_key = "06c0a930553b6496d17b10a9c882b9d0"  # Replace with your actual API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    if 'poster_path' in data and data['poster_path']:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]

        recommended_movies = []
        recommended_posters = []

        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id  # Ensure 'movie_id' exists in your dataset
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))  # Fetch poster for each movie

        return recommended_movies, recommended_posters
    except IndexError:
        return ["Movie not found in the dataset. Please select another."], []

# Load movies data
with open('movies_dict.pkl', 'rb') as file:
    movies_dict = pickle.load(file)

movies = pd.DataFrame(movies_dict)

# Load similarity matrix
with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

st.title('🎬 Movie Recommender System')

# Dropdown for movie selection
selected_movie_name = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)  # Display 5 movies side by side
    for i in range(len(recommendations)):
        with cols[i]:
            st.image(posters[i], width=150)
            st.write(recommendations[i])
