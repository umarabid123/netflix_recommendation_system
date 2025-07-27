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
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #0f0f0f 100%);
        color: #ffffff;
        font-family: 'Netflix Sans', 'Helvetica Neue', Arial, sans-serif;
        background-attachment: fixed;
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
    
    /* Enhanced Netflix header styling */
    .netflix-header {
        background: linear-gradient(135deg, #e50914 0%, #b20710 50%, #8b0000 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(229, 9, 20, 0.4),
            0 0 60px rgba(229, 9, 20, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .netflix-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.8),
            0 0 20px rgba(229, 9, 20, 0.3);
        letter-spacing: -0.02em;
        background: linear-gradient(45deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #f0f0f0;
        margin-top: 0.5rem;
        font-weight: 300;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Enhanced selection container */
    .selection-container {
        background: linear-gradient(135deg, #222222 0%, #2a2a2a 100%);
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid #404040;
        box-shadow: 
            0 4px 20px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(255,255,255,0.05);
        position: relative;
    }
    
    .selection-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e50914, transparent);
        border-radius: 16px 16px 0 0;
    }
    
    .selection-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Enhanced selectbox styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #333333 0%, #3a3a3a 100%) !important;
        border: 2px solid #555555 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #e50914 !important;
        box-shadow: 
            0 0 20px rgba(229, 9, 20, 0.4) !important,
            0 4px 15px rgba(0,0,0,0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    /* Enhanced Netflix button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e50914 0%, #b20710 50%, #8b0000 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        margin: 2rem 0 !important;
        box-shadow: 
            0 6px 20px rgba(229, 9, 20, 0.5) !important,
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #f40612 0%, #d40813 50%, #a00000 100%) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 8px 25px rgba(229, 9, 20, 0.7) !important,
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.01) !important;
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-color: #e50914 !important;
        border-top-color: transparent !important;
        width: 60px !important;
        height: 60px !important;
        animation: enhanced-spin 1s linear infinite !important;
    }
    
    @keyframes enhanced-spin {
        0% { 
            transform: rotate(0deg) scale(1);
            box-shadow: 0 0 10px rgba(229, 9, 20, 0.3);
        }
        50% { 
            transform: rotate(180deg) scale(1.1);
            box-shadow: 0 0 20px rgba(229, 9, 20, 0.6);
        }
        100% { 
            transform: rotate(360deg) scale(1);
            box-shadow: 0 0 10px rgba(229, 9, 20, 0.3);
        }
    }
    
    /* Custom loading overlay */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        backdrop-filter: blur(5px);
    }
    
    .loading-content {
        text-align: center;
        color: white;
    }
    
    .loading-spinner {
        width: 80px;
        height: 80px;
        border: 4px solid #333;
        border-top: 4px solid #e50914;
        border-radius: 50%;
        animation: loading-spin 1s linear infinite;
        margin: 0 auto 20px;
        box-shadow: 0 0 30px rgba(229, 9, 20, 0.4);
    }
    
    @keyframes loading-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.2rem;
        font-weight: 500;
        animation: loading-pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes loading-pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* Enhanced recommendations container */
    .recommendations-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        border: 1px solid #404040;
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .recommendations-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #e50914, #f40612, #e50914);
        border-radius: 20px 20px 0 0;
    }
    
    .recommendations-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 3rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid transparent;
        background: linear-gradient(90deg, transparent, #e50914, transparent) bottom/100% 2px no-repeat;
        position: relative;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .recommendations-header::after {
        content: '';
        position: absolute;
        bottom: -6px;
        left: 50%;
        transform: translateX(-50%);
        width: 120px;
        height: 6px;
        background: linear-gradient(90deg, transparent, #e50914, transparent);
        border-radius: 3px;
        box-shadow: 0 0 15px rgba(229, 9, 20, 0.5);
    }
    
    /* Enhanced flexbox grid for movie cards */
    .movies-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 2.5rem;
        justify-content: center;
        align-items: stretch;
        margin-top: 2rem;
    }
    
    /* Stunning Netflix movie card styling */
    .movie-container {
        background: linear-gradient(135deg, #2a2a2a 0%, #333333 100%);
        border-radius: 16px;
        padding: 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        aspect-ratio: 2/3;
        flex: 0 1 calc(33.333% - 2rem);
        min-width: 280px;
        max-width: 380px;
        box-shadow: 
            0 8px 25px rgba(0,0,0,0.4),
            0 2px 10px rgba(0,0,0,0.2);
    }
    
    .movie-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(229, 9, 20, 0) 0%, rgba(229, 9, 20, 0.1) 100%);
        opacity: 0;
        transition: all 0.4s ease;
        z-index: 1;
        border-radius: 16px;
    }
    
    /* Movie image container */
    .movie-image-container {
        position: relative;
        width: 100%;
        height: 75%;
        overflow: hidden;
        border-radius: 16px 16px 0 0;
    }
    
    .movie-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        border-radius: 16px 16px 0 0;
        filter: brightness(0.9) contrast(1.1);
    }
    
    /* Enhanced Netflix-style overlay */
    .movie-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            to bottom,
            rgba(0,0,0,0) 0%,
            rgba(0,0,0,0.1) 30%,
            rgba(0,0,0,0.8) 100%
        );
        opacity: 0;
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 1.5rem;
        z-index: 2;
    }
    
    /* Enhanced action buttons */
    .movie-actions {
        display: flex;
        gap: 0.8rem;
        margin-bottom: 1rem;
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .action-btn {
        background: rgba(255, 255, 255, 0.95);
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        font-size: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .action-btn:hover {
        background: #ffffff;
        transform: scale(1.15) translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    .play-btn {
        background: #ffffff !important;
        color: #000000;
        font-weight: bold;
        font-size: 18px;
    }
    
    .play-btn:hover {
        background: #f0f0f0 !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.5);
    }
    
    .like-btn {
        color: #46d369;
    }
    
    .like-btn:hover {
        background: rgba(70, 211, 105, 0.1) !important;
        color: #46d369;
    }
    
    .dislike-btn {
        color: #e50914;
    }
    
    .dislike-btn:hover {
        background: rgba(229, 9, 20, 0.1) !important;
        color: #e50914;
    }
    
    .info-btn {
        color: #0071eb;
    }
    
    .info-btn:hover {
        background: rgba(0, 113, 235, 0.1) !important;
        color: #0071eb;
    }
    
    /* Enhanced movie info in overlay */
    .movie-info {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.1s;
    }
    
    .movie-rating {
        color: #46d369;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .movie-genre {
        color: #cccccc;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
        font-weight: 300;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Enhanced movie title */
    .movie-title {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        padding: 1rem;
        font-weight: 600;
        font-size: 1rem;
        color: #ffffff;
        text-align: center;
        line-height: 1.4;
        height: 25%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        border-radius: 0 0 16px 16px;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        z-index: 3;
    }
    
    /* Enhanced hover effects */
    .movie-container:hover {
        transform: scale(1.08) translateY(-15px);
        border-color: #e50914;
        box-shadow: 
            0 20px 50px rgba(229, 9, 20, 0.4),
            0 10px 30px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(255,255,255,0.1);
        z-index: 10;
    }
    
    .movie-container:hover::before {
        opacity: 1;
    }
    
    .movie-container:hover .movie-image {
        transform: scale(1.15);
        filter: brightness(1.1) contrast(1.2);
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
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        color: #e50914;
        text-shadow: 0 0 10px rgba(229, 9, 20, 0.3);
    }
    
    /* Enhanced quality badge */
    .quality-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        z-index: 3;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(229, 9, 20, 0.4);
    }
    
    /* Enhanced duration badge */
    .duration-badge {
        position: absolute;
        top: 12px;
        right: 12px;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 500;
        z-index: 3;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }
    
    /* Enhanced custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(229, 9, 20, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f40612 0%, #d40813 100%);
        box-shadow: 0 2px 8px rgba(229, 9, 20, 0.5);
    }
    
    /* Enhanced loading animation */
    @keyframes custom-loading-spin {
        0% { 
            transform: rotate(0deg);
            box-shadow: 0 0 10px rgba(229, 9, 20, 0.3);
        }
        50% { 
            transform: rotate(180deg);
            box-shadow: 0 0 25px rgba(229, 9, 20, 0.8);
        }
        100% { 
            transform: rotate(360deg);
            box-shadow: 0 0 10px rgba(229, 9, 20, 0.3);
        }
    }
    
    /* Custom Loading Overlay */
    .custom-loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(20, 20, 20, 0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        backdrop-filter: blur(10px);
    }
    
    .custom-loading-spinner {
        width: 80px;
        height: 80px;
        border: 4px solid #333333;
        border-top: 4px solid #e50914;
        border-radius: 50%;
        animation: custom-loading-spin 1.2s linear infinite;
        margin-bottom: 30px;
        position: relative;
    }
    
    .custom-loading-spinner::before {
        content: '';
        position: absolute;
        top: -4px;
        left: -4px;
        right: -4px;
        bottom: -4px;
        border: 2px solid transparent;
        border-top: 2px solid rgba(229, 9, 20, 0.3);
        border-radius: 50%;
        animation: custom-loading-spin 2s linear infinite reverse;
    }
    
    .custom-loading-text {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .custom-loading-subtitle {
        color: #cccccc;
        font-size: 1rem;
        font-weight: 300;
        text-align: center;
        animation: loading-pulse 2s ease-in-out infinite;
    }
    
    @keyframes loading-pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Loading dots animation */
    .loading-dots {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 20px;
        margin-top: 20px;
    }
    
    .loading-dots div {
        position: absolute;
        top: 0;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #e50914;
        animation: loading-dots-bounce 1.2s infinite ease-in-out both;
    }
    
    .loading-dots div:nth-child(1) {
        left: 8px;
        animation-delay: -0.24s;
    }
    
    .loading-dots div:nth-child(2) {
        left: 32px;
        animation-delay: -0.12s;
    }
    
    .loading-dots div:nth-child(3) {
        left: 56px;
        animation-delay: 0;
    }
    
    @keyframes loading-dots-bounce {
        0%, 80%, 100% {
            transform: scale(0);
        }
        40% {
            transform: scale(1);
        }
    }
    
    /* ENHANCED RESPONSIVE BREAKPOINTS */
    
    /* Force exactly 3 cards per row on larger screens */
    @media (min-width: 900px) {
        .movie-container {
            flex: 0 1 calc(33.333% - 1.67rem);
            max-width: calc(33.333% - 1.67rem);
        }
        .movies-grid {
            gap: 2.5rem;
            justify-content: flex-start;
        }
    }
    
    /* Medium screens (2 cards per row) */
    @media (max-width: 899px) and (min-width: 600px) {
        .movie-container {
            flex: 0 1 calc(50% - 1.25rem);
            max-width: calc(50% - 1.25rem);
        }
        .movies-grid {
            gap: 2rem;
            justify-content: center;
        }
        .main-title {
            font-size: 2.8rem;
        }
        .recommendations-header {
            font-size: 2.2rem;
        }
    }
    
    /* Small screens (1 card per row) */
    @media (max-width: 599px) {
        .movie-container {
            flex: 0 1 100%;
            max-width: 320px;
            margin: 0 auto;
        }
        .movies-grid {
            gap: 1.5rem;
            justify-content: center;
        }
        .main-title {
            font-size: 2.2rem;
        }
        .recommendations-header {
            font-size: 1.8rem;
        }
        .recommendations-container {
            padding: 2rem;
        }
        .netflix-header {
            padding: 2rem;
        }
        .selection-container {
            padding: 2rem;
        }
    }
    
    /* Extra small screens */
    @media (max-width: 480px) {
        .movie-container {
            min-width: 220px;
        }
        .netflix-header {
            padding: 1.5rem;
        }
        .main-title {
            font-size: 1.8rem;
        }
        .recommendations-header {
            font-size: 1.5rem;
        }
        .recommendations-container {
            padding: 1.5rem;
        }
        .selection-container {
            padding: 1.5rem;
        }
        .action-btn {
            width: 35px;
            height: 35px;
            font-size: 14px;
        }
    }
    
    /* Add entrance animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .movie-container {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .movie-container:nth-child(1) { animation-delay: 0.1s; }
    .movie-container:nth-child(2) { animation-delay: 0.2s; }
    .movie-container:nth-child(3) { animation-delay: 0.3s; }
    .movie-container:nth-child(4) { animation-delay: 0.4s; }
    .movie-container:nth-child(5) { animation-delay: 0.5s; }
    .movie-container:nth-child(6) { animation-delay: 0.6s; }
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
        html_row = f"""
        <div style='max-width:100%; margin:10px auto; background:#222; padding:10px; border-radius:8px; color:white;'>
            {row.to_frame().to_html()}
        </div>
        """
        st.markdown(html_row, unsafe_allow_html=True)
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Updated file loading (alternative)
movies = pd.DataFrame(pickle.load(open(os.path.join(BASE_DIR, 'movies_dict.pkl'), 'rb')))
similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))
movie_list = list(movies['title'].values)

# Selection container with Netflix styling
st.markdown('<div class="selection-container">', unsafe_allow_html=True)
st.markdown('<p class="selection-label">🎭 Choose a movie you like:</p>', unsafe_allow_html=True)
selected_movie = st.selectbox("", movie_list, key="movie_select")

if st.button('🔍 Get Recommendations'):
    # Custom loading overlay
    loading_placeholder = st.empty()
    loading_placeholder.markdown('''
    <div class="custom-loading-overlay">
        <div class="custom-loading-spinner"></div>
        <div class="custom-loading-text">🎬 Finding Perfect Matches</div>
        <div class="custom-loading-subtitle">Analyzing your movie preferences...</div>
        <div class="loading-dots">
            <div></div>
            <div></div>
            <div></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Add a small delay to show the loading animation
    import time
    time.sleep(2)
    
    try:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        loading_placeholder.empty()  # Remove loading overlay
    except Exception as e:
        loading_placeholder.empty()
        st.error("Sorry, something went wrong. Please try again.")
        st.stop()
        
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
                        <div class="quality-badge">4K</div>
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