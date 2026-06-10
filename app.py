import pickle
import streamlit as st

st.title("🎬 Movie Recommendation System")

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.write("Movies loaded ✔")

# show dropdown safely
movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended = []

    for i in distances[1:6]:
        recommended.append(movies.iloc[i[0]].title)

    return recommended


if st.button("Show Recommendation"):
    results = recommend(selected_movie)

    st.subheader("Recommended Movies:")

    for i in results:
        st.write(i)