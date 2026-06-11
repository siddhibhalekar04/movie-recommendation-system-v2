import os
import pickle
import requests
import streamlit as st
import gdown

# Download similarity.pkl from Google Drive
FILE_ID = "10G7Wix8qVcm8PRnallzWIMBpHWHa5Qtm"

if not os.path.exists("similarity.pkl"):
    url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
    gdown.download(url, "similarity.pkl", quiet=False,)

# Load files
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Poster function
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()

        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommendation function
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

# UI
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])