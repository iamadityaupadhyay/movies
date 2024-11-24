import streamlit as st
import pickle
import pandas as pd
import gdown
import os

st.set_page_config(page_title="Movie Recommender", layout="wide")

@st.cache_resource
def load_files_from_gdrive():
    try:
        # File IDs from your Google Drive links
        similarity_file_id = "1SGX2Sdtk1bgXOGfvDptSI_v8WLJ2THIZ"
        movies_file_id = "1UMTxYoAz4BKHeZX0_JQBNT8bvJDJ1lSq"
        
        # Create download URLs
        similarity_url = f'https://drive.google.com/uc?id={similarity_file_id}'
        movies_url = f'https://drive.google.com/uc?id={movies_file_id}'
        
        # Download files if they don't exist
        if not os.path.exists('similarity.pkl'):
            with st.spinner('Downloading similarity matrix... This might take a while.'):
                gdown.download(similarity_url, 'similarity.pkl', quiet=False)
        
        if not os.path.exists('movies_dict.pkl'):
            with st.spinner('Downloading movies data...'):
                gdown.download(movies_url, 'movies_dict.pkl', quiet=False)
        
        # Load the pickled data
        movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        
        return movies_dict, similarity
    
    except Exception as e:
        st.error(f"Error loading files: {str(e)}")
        return None, None

# Add some custom CSS to make it look better
st.markdown("""
    <style>
    .movie-title {
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
movies_dict, similarity = load_files_from_gdrive()

if movies_dict is None or similarity is None:
    st.stop()

# Convert to DataFrame
movies = pd.DataFrame(movies_dict)

# Streamlit app
st.title('🎬 Movie Recommender System')
st.markdown("---")

# Add some description
st.markdown("""
    Select a movie you like, and we'll recommend similar movies you might enjoy!
""")

# Create the selectbox with a larger width
selected_movie_name = st.selectbox(
    'Select a movie you like',
    movies['title'].values,
    index=0
)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    for i in movies_list:
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names

# Center the button
col1, col2, col3 = st.columns([1,1,1])
with col2:
    show_rec = st.button('Show Recommendations', use_container_width=True)

if show_rec:
    with st.spinner('Finding movies you might like...'):
        recommended_movie_names = recommend(selected_movie_name)
    
    st.markdown("### 🌟 Recommended Movies")
    st.markdown("---")
    
    # Display recommendations in columns
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-title">
                    {recommended_movie_names[idx]}
                </div>
                """, unsafe_allow_html=True)

st.markdown("""
    Made By Aditya Upadhyay
""")