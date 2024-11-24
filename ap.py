# prompt: now using streamlit,pickle and pandas make a website

import streamlit as st
import pickle
import pandas as pd
import requests

import gdown

# Replace with your Google Drive file ID
similarity_url = "https://drive.google.com/file/d/1SGX2Sdtk1bgXOGfvDptSI_v8WLJ2THIZ/view?usp=sharing"
movies_url = "https://drive.google.com/file/d/1UMTxYoAz4BKHeZX0_JQBNT8bvJDJ1lSq/view?usp=sharing"

gdown.download(similarity_url, "similarity.pkl", quiet=False)
gdown.download(movies_url, "movies.pkl", quiet=False)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
# Load the pickled data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

# Streamlit app
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)
def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in movies_list:
            # print(movies.iloc[i[0]].movie_id)
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names

if st.button('Show Recommendation'):
    recommended_movie_names= recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        # st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        # st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        # st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        # st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        # st.image(recommended_movie_posters[4])