import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

# Configure page settings
st.set_page_config(
    page_title="AI Assistant Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    /* Headers */
    .css-10trblm {
        color: #1e3d59;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        border-bottom: 2px solid #ff6e40;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1e3d59;
        padding: 2rem 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #ff6e40;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #ff5722;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        border-radius: 5px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        border-radius: 5px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
        font-size: 1rem;
        background-color: #ffffff;
    }
    
    /* Radio buttons */
    .stRadio > div {
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Cards */
    .css-card {
        border-radius: 10px;
        padding: 1.5rem;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Success messages */
    .success-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
    
    /* Error messages */
    .stException {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        color: #721c24;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-color: #ff6e40;
    }
</style>
""", unsafe_allow_html=True)

# Configure API Key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Custom card container
def card_container(title, content):
    st.markdown(f"""
        <div class="css-card">
            <h3 style="color: #1e3d59; margin-bottom: 1rem;">{title}</h3>
            {content}
        </div>
    """, unsafe_allow_html=True)

# App Header
st.markdown("""
    <h1 style='text-align: center; color: #1e3d59; margin-bottom: 2rem;'>
        🤖 AI Assistant Hub
    </h1>
    <p style='text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 3rem;'>
        Explore the power of Google's Generative AI (Gemini)
    </p>
""", unsafe_allow_html=True)

# Sidebar with gradient background
st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #1e3d59, #17314a); 
                padding: 1rem; 
                border-radius: 10px; 
                margin-bottom: 1rem;'>
        <h2 style='color: white; text-align: center; margin-bottom: 1rem;'>🎮 Control Panel</h2>
    </div>
""", unsafe_allow_html=True)

option = st.sidebar.radio(
    "Choose your AI Experience:",
    ("Image Analysis", "Chat with AI"),
    key="nav"
)

model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')


# Chat with AI Section
if option == "Chat with AI":
    st.markdown("""
        <h2 style='text-align: center; color: #1e3d59; margin-bottom: 2rem;'>
            💬 AI Chat Assistant
        </h2>
    """, unsafe_allow_html=True)
    
    # Initialize chat
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat()
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div style='background-color: #e3f2fd; 
                          padding: 1rem; 
                          border-radius: 10px; 
                          margin: 0.5rem 0; 
                          text-align: left;'>
                    <strong>You:</strong> {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color: white; 
                          padding: 1rem; 
                          border-radius: 10px; 
                          margin: 0.5rem 0;
                          border-left: 4px solid #ff6e40;'>
                    <strong>AI:</strong> {message["content"]}
               
            """, unsafe_allow_html=True)

    # User input
    user_message = st.text_input("Type your message:", key="user_input")
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Send Message"):
            if user_message:
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": user_message})
                
                # Get AI response
                with st.spinner('AI is thinking...'):
                    try:
                        response = st.session_state.chat_session.send_message(user_message)
                        st.session_state.messages.append({"role": "ai", "content": response.text})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
if option == "Image Analysis":
    # Image Analysis Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ff6e40, #ff5722); 
                    padding: 1rem; 
                    border-radius: 10px; 
                    margin-top: 2rem;'>
            <h3 style='color: white; text-align: center;'>🖼️ Image Analysis</h3>
        </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Upload an image for analysis",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:
        st.markdown("""
            <div style='background-color: white; 
                        padding: 1rem; 
                        border-radius: 10px; 
                        margin-top: 1rem;'>
        """, unsafe_allow_html=True)
        
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            try:
                img = Image.open(uploaded_image)
                response = model.generate_content(['Describe this image in detail:', img])
                st.markdown(f"""
                    <div style='background-color: #f8f9fa; 
                            padding: 1rem; 
                            border-radius: 5px; 
                            margin-top: 1rem;'
                            >
                        <strong>AI Analysis:</strong><br>{response.text}
                 
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
        
    

# Footer
st.markdown("""
    <div style='position: fixed; 
                bottom: 0; 
                left: 0; 
                width: 100%; 
                background-color: #1e3d59; 
                color: white; 
                text-align: center; 
                padding: 1rem;'>
        Created with ❤️ using Streamlit and Google's Generative AI
    </div>
""", unsafe_allow_html=True)