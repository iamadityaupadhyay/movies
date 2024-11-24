import streamlit as st
import pickle
import pandas as pd
import gdown # type: ignore

# Replace with your Google Drive file ID
similarity_url = "https://drive.google.com/file/d/1SGX2Sdtk1bgXOGfvDptSI_v8WLJ2THIZ/view?usp=sharing"
movies_url = "https://drive.google.com/file/d/1UMTxYoAz4BKHeZX0_JQBNT8bvJDJ1lSq/view?usp=sharing"

# Download pickle files
gdown.download(similarity_url, "similarity.pkl", quiet=False)
gdown.download(movies_url, "movies_dict.pkl", quiet=False)

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
    for i in movies_list:
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie_name)
    
    # Display recommendations in columns
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])