import streamlit as st
from services.supabase_service import SupabaseService
import uuid
import sounddevice as sd
import wavio
import tempfile
import os

# Initialize Supabase service
supabase = SupabaseService()

# Enhanced Custom CSS with modern design elements
st.markdown("""
    <style>
        .uploadfile > div:first-child {
            color: white !important;
        }
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }

        /* Main container styling */
        .main {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Title styling with animation */
        .title-text {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            text-align: center;
            animation: fadeIn 1s ease-in;
        }

        /* Header styling */
        .header-text {
            font-size: 2.2rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }

        /* Event card styling with glass morphism */
        .event-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .event-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
            background: rgba(255, 255, 255, 0.08);
        }

        /* Event title styling */
        .event-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.8rem;
        }

        /* Event details styling */
        .event-details {
            color: #e0e0e0;
            font-size: 1rem;
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }

        /* Upload box styling with animation */
        .uploadfile {
            border: 2px dashed rgba(132, 250, 176, 0.3) !important;
            border-radius: 16px !important;
            padding: 2.5rem !important;
            background: rgba(255, 255, 255, 0.03) !important;
            transition: all 0.3s ease;
            animation: pulse 2s infinite;
        }

        .uploadfile:hover {
            border-color: rgba(132, 250, 176, 0.6) !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }

        /* Button styling */
        .stButton button {
            background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%) !important;
            color: #1a1a2e !important;
            font-weight: 600 !important;
            border-radius: 30px !important;
            padding: 0.8rem 2.5rem !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(132, 250, 176, 0.3) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }

        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(132, 250, 176, 0.4) !important;
        }

        /* Textarea styling */
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(132, 250, 176, 0.2) !important;
            border-radius: 16px !important;
            color: white !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }

        .stTextArea textarea:focus {
            border-color: rgba(132, 250, 176, 0.4) !important;
            box-shadow: 0 0 15px rgba(132, 250, 176, 0.1) !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }

        /* Animation keyframes */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(132, 250, 176, 0.1); }
            70% { box-shadow: 0 0 0 10px rgba(132, 250, 176, 0); }
            100% { box-shadow: 0 0 0 0 rgba(132, 250, 176, 0); }
        }

        /* Success message styling */
        .success-message {
            background: rgba(132, 250, 176, 0.1) !important;
            border: 1px solid rgba(132, 250, 176, 0.3) !important;
            border-radius: 16px !important;
            padding: 1rem !important;
            color: #84fab0 !important;
        }

        /* Error message styling */
        .error-message {
            background: rgba(255, 99, 132, 0.1) !important;
            border: 1px solid rgba(255, 99, 132, 0.3) !important;
            border-radius: 16px !important;
            padding: 1rem !important;
            color: #ff6384 !important;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border: 1px solid rgba(132, 250, 176, 0.2);
            border-radius: 8px;
            color: white;
            padding: 8px 16px;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(132, 250, 176, 0.1);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%) !important;
            color: #1a1a2e !important;
        }
    </style>
""", unsafe_allow_html=True)

def record_audio():
    duration = 10  # seconds
    fs = 44100  # Sample rate

    try:
        st.warning("🎙️ Recording for 10 seconds...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()

        # Save to temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            wavio.write(temp_audio.name, audio_data, fs, sampwidth=2)

        return temp_audio.name
    except Exception as e:
        st.error(f"Error recording audio: {str(e)}")
        return None

def reset_fields():
    st.session_state.description = ""
    if 'uploaded_image' in st.session_state:
        del st.session_state.uploaded_image
    if 'audio_data' in st.session_state:
        del st.session_state.audio_data

def display_events():
    events = supabase.get_all_events()

    if events:
        for event in events:
            st.markdown(f"""
                <div class="event-card">
                    <div class="event-title">📝 {event.get('name', 'N/A')}</div>
                    <div class="event-details">📅 Date: {event.get('date', 'N/A')}</div>
                    <div class="event-details">💬 {event.get('description', 'No description available')}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="event-card">
                <div class="event-title">No Reports Yet</div>
                <div class="event-details">Be the first to report an issue!</div>
            </div>
        """, unsafe_allow_html=True)

def report_issue_tab():
    if 'description' not in st.session_state:
        st.session_state.description = ""

    # File uploader with enhanced styling
    image = st.file_uploader(
        "📤 Upload an image of the issue",
        type=["png", "jpg", "jpeg"],
        key="uploaded_image"
    )

    # Description text area
    description = st.text_area(
        "✍️ Describe the issue (optional)",
        value=st.session_state.description,
        height=150,
        placeholder="Tell us more about the problem..."
    )

    # Audio recording section
    st.markdown("🎙️ **Add Voice Note (optional)**")
    if st.button("Start Recording", key="record_button"):
        audio_file = record_audio()
        if audio_file:
            st.session_state.audio_data = audio_file
            st.audio(audio_file)
            st.success("✅ Voice note recorded successfully!")

    # Submit button
    if st.button("Submit Report"):
        if image:
            try:
                with st.spinner('📤 Uploading your report...'):
                    image_name = f"{uuid.uuid4()}_{image.name}"
                    image_url = supabase.upload_image(image, image_name)

                    # Upload audio if available
                    audio_url = None
                    if 'audio_data' in st.session_state and st.session_state.audio_data:
                        audio_name = f"{uuid.uuid4()}_audio.wav"
                        with open(st.session_state.audio_data, 'rb') as audio_file:
                            audio_url = supabase.upload_audio(audio_file, audio_name)

                    if image_url:
                        response = supabase.upload_data(
                            image_url=image_url,
                            description=description,
                            audio_url=audio_url
                        )
                        if response:
                            st.markdown('<div class="success-message">✅ Report submitted successfully!</div>', unsafe_allow_html=True)
                            reset_fields()
                            # Clean up temporary audio file
                            if 'audio_data' in st.session_state and st.session_state.audio_data:
                                os.remove(st.session_state.audio_data)
                        else:
                            st.markdown('<div class="error-message">❌ Failed to submit report to database.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ Failed to upload image.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ An error occurred: {str(e)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠️ Please provide an image to report the issue.</div>', unsafe_allow_html=True)

def main():
    # Title with animation
    st.markdown('<p class="title-text">GramSeva</p>', unsafe_allow_html=True)

    # Subtitle
    st.markdown("""
        <p style='text-align: center; color: #8fd3f4; margin-bottom: 2rem; font-size: 1.2rem;'>
            Empowering communities through digital problem-solving
        </p>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2 = st.tabs(["📝 Report Issue", "🔍 Upcoming Events"])

    # Report Issue Tab
    with tab1:
        st.markdown('<p class="header-text">📸 Report an Issue</p>', unsafe_allow_html=True)
        report_issue_tab()

    # View Reports Tab
    with tab2:
        st.markdown('<p class="header-text">🔍 Upcoming Events</p>', unsafe_allow_html=True)
        display_events()

if __name__ == "__main__":
    main()