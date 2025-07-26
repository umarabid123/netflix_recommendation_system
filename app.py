import streamlit as st
import pickle
import pandas as pd
import requests

# Page configuration for better appearance
st.set_page_config(
    page_title="Movies Recommender System",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
    /* Import Netflix-like font */
    @import url('https://fonts.googleapis.com/css2?family=Netflix+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Global Netflix styling */
    .stApp {
        background: #141414;
        color: #ffffff;
        font-family: 'Netflix Sans', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Netflix header styling */
    .netflix-header {
        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(229, 9, 20, 0.3);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #f0f0f0;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Selection container Netflix style */
    .selection-container {
        background: #222222;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid #333333;
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .selection-label {
        font-size: 1.1rem;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    /* Selectbox Netflix styling */
    .stSelectbox > div > div {
        background: #333333 !important;
        border: 2px solid #555555 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #e50914 !important;
        box-shadow: 0 0 10px rgba(229, 9, 20, 0.3) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    /* Netflix button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e50914 0%, #b20710 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #f40612 0%, #d40813 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6) !important;
    }
    
    /* Recommendations container */
    .recommendations-container {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid #333333;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .recommendations-header {
        text-align: center;
        font-size: 2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e50914;
        position: relative;
    }
    
    .recommendations-header::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e50914, transparent);
    }
    
    /* FLEXBOX GRID FOR MOVIE CARDS */
    .movies-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 2rem;
        justify-content: center;
        align-items: stretch;
    }
    
    /* Netflix movie card styling - ENHANCED WITH FLEXBOX */
    .movie-container {
        background: #2a2a2a;
        border-radius: 8px;
        padding: 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        border: 1px solid #404040;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        aspect-ratio: 2/3;
        
        /* Flexbox properties for responsive layout */
        flex: 0 1 calc(33.333% - 1.5rem); /* 3 cards per row with gap */
        min-width: 250px;
        max-width: 350px;
    }
    
    /* Movie image container */
    .movie-image-container {
        position: relative;
        width: 100%;
        height: 75%;
        overflow: hidden;
        border-radius: 8px 8px 0 0;
    }
    
    .movie-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: all 0.4s ease;
        border-radius: 8px 8px 0 0;
    }
    
    /* Netflix-style overlay */
    .movie-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            to bottom,
            rgba(0,0,0,0) 0%,
            rgba(0,0,0,0.1) 20%,
            rgba(0,0,0,0.8) 100%
        );
        opacity: 0;
        transition: all 0.4s ease;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 1rem;
    }
    
    /* Action buttons */
    .movie-actions {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.4s ease;
    }
    
    .action-btn {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .action-btn:hover {
        background: #ffffff;
        transform: scale(1.1);
    }
    
    .play-btn {
        background: #ffffff !important;
        color: #000000;
        font-weight: bold;
    }
    
    .like-btn {
        color: #46d369;
    }
    
    .dislike-btn {
        color: #e50914;
    }
    
    .info-btn {
        color: #0071eb;
    }
    
    /* Movie info in overlay */
    .movie-info {
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.4s ease 0.1s;
    }
    
    .movie-rating {
        color: #46d369;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .movie-genre {
        color: #cccccc;
        font-size: 0.7rem;
        margin-bottom: 0.25rem;
    }
    
    /* Movie title at bottom */
    .movie-title {
        background: #2a2a2a;
        padding: 0.75rem;
        font-weight: 500;
        font-size: 0.9rem;
        color: #ffffff;
        text-align: center;
        line-height: 1.3;
        height: 25%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-shadow: none;
        border-radius: 0 0 8px 8px;
        transition: all 0.4s ease;
    }
    
    /* Hover effects */
    .movie-container:hover {
        transform: scale(1.05) translateY(-10px);
        border-color: #e50914;
        box-shadow: 0 15px 35px rgba(229, 9, 20, 0.4);
        z-index: 10;
    }
    
    .movie-container:hover .movie-image {
        transform: scale(1.1);
    }
    
    .movie-container:hover .movie-overlay {
        opacity: 1;
    }
    
    .movie-container:hover .movie-actions {
        opacity: 1;
        transform: translateY(0);
    }
    
    .movie-container:hover .movie-info {
        opacity: 1;
        transform: translateY(0);
    }
    
    .movie-container:hover .movie-title {
        background: #1a1a1a;
        color: #e50914;
    }
    
    /* Quality badge */
    .quality-badge {
        position: absolute;
        top: 8px;
        left: 8px;
        background: rgba(229, 9, 20, 0.9);
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.7rem;
        font-weight: 600;
        z-index: 2;
    }
    
    /* Duration badge */
    .duration-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.7rem;
        z-index: 2;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #e50914;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #f40612;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* RESPONSIVE BREAKPOINTS */
    
    /* Large screens (3 cards per row) */
    @media (min-width: 1200px) {
        .movie-container {
            flex: 0 1 calc(33.333% - 1.5rem);
        }
    }
    
    /* Medium screens (2 cards per row) */
    @media (max-width: 1199px) and (min-width: 768px) {
        .movie-container {
            flex: 0 1 calc(50% - 1rem);
        }
        
        .movies-grid {
            gap: 1.5rem;
        }
    }
    
    /* Small screens (1 card per row) */
    @media (max-width: 767px) {
        .movie-container {
            flex: 0 1 100%;
            max-width: 300px;
            margin: 0 auto;
        }
        
        .movies-grid {
            gap: 1rem;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .recommendations-header {
            font-size: 1.5rem;
        }
        
        .recommendations-container {
            padding: 1rem;
        }
    }
    
    /* Extra small screens */
    @media (max-width: 480px) {
        .movie-container {
            min-width: 200px;
        }
        
        .netflix-header {
            padding: 1rem;
        }
        
        .main-title {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Your original functions - keeping them exactly the same
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    print("data", data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:7]:
        row = movies.iloc[i[0]]
        st.write(row)  # 
        movies_id = row.get('movie_id', None)
        if movies_id:
            recommended_movie_posters.append(fetch_poster(movies_id))
            recommended_movie_names.append(row['title'])
    return recommended_movie_names, recommended_movie_posters

# Netflix-style header
st.markdown('''
<div class="netflix-header">
    <h1 class="main-title">🎬 NETFLIX RECOMMENDATION</h1>
    <p class="subtitle">Movie Recommender System</p>
</div>
''', unsafe_allow_html=True)

# Your original data loading - keeping it exactly the same
movies = pd.DataFrame(pickle.load(open('movies_dict.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = list(movies['title'].values)

# Selection container with Netflix styling
st.markdown('<div class="selection-container">', unsafe_allow_html=True)
st.markdown('<p class="selection-label">🎭 Choose a movie you like:</p>', unsafe_allow_html=True)
selected_movie = st.selectbox("", movie_list, key="movie_select")

if st.button('🔍 Get Recommendations'):
    with st.spinner('Finding perfect matches for you...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        if len(recommended_movie_names) < 6:
            print("Not enough recommendations found!")
        else:
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recommendations container with Netflix styling
            st.markdown('<div class="recommendations-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="recommendations-header">🍿 Recommended for You</h2>', unsafe_allow_html=True)
            
            # Create flexbox grid for movie cards
            movies_grid_html = '<div class="movies-grid">'
            
            for i in range(len(recommended_movie_names)):
                movie_card_html = f'''
                <div class="movie-container">
                    <div class="movie-image-container">
                        <div class="quality-badge">HD</div>
                        <div class="duration-badge">2h 15m</div>
                        <img src="{recommended_movie_posters[i]}" class="movie-image" alt="{recommended_movie_names[i]}">
                        
                        <div class="movie-overlay">
                            <div class="movie-actions">
                                <button class="action-btn play-btn" title="Play">▶</button>
                                <button class="action-btn like-btn" title="Like">👍</button>
                                <button class="action-btn dislike-btn" title="Dislike">👎</button>
                                <button class="action-btn info-btn" title="More Info">ℹ</button>
                            </div>
                            
                            <div class="movie-info">
                                <div class="movie-rating">⭐ 8.5/10</div>
                                <div class="movie-genre">Action • Drama • Thriller</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="movie-title">{recommended_movie_names[i]}</div>
                </div>
                '''
                movies_grid_html += movie_card_html
            
            movies_grid_html += '</div>'
            st.markdown(movies_grid_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

if 'movie_select' not in st.session_state:
    st.markdown('</div>', unsafe_allow_html=True)
