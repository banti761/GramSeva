import streamlit as st
from services.supabase_service import SupabaseService
import uuid

# Initialize Supabase service
supabase = SupabaseService()

# Custom CSS to enhance the UI
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }

        /* Custom title styling */
        .title-text {
            font-size: 3.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        /* Header styling */
        .header-text {
            font-size: 2rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 1.5rem;
        }

        /* Event card styling */
        .event-card {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }

        .event-card:hover {
            background-color: rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
        }

        /* Event title styling */
        .event-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }

        /* Event details styling */
        .event-details {
            color: #e0e0e0;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }

        /* Upload box styling */
        .uploadfile {
            border: 2px dashed rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            padding: 2rem !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
        }

        .uploadfile:hover {
            border-color: rgba(255, 255, 255, 0.4) !important;
            background-color: rgba(255, 255, 255, 0.08) !important;
        }

        /* Button styling */
        .stButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 25px !important;
            padding: 0.5rem 2rem !important;
            border: none !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }

        .stButton button:hover {
            background-color: #45a049 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        }

        /* Textarea styling */
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: white !important;
            padding: 1rem !important;
        }

        .stTextArea textarea:focus {
            border-color: rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
        }

        /* Dark theme overrides */
        .stApp {
            background-color: #1a1a1a;
        }
    </style>
""", unsafe_allow_html=True)

def reset_fields():
    st.session_state.description = ""
    if 'uploaded_image' in st.session_state:
        del st.session_state.uploaded_image

def display_events():
    st.markdown('<p class="header-text">Recent Events</p>', unsafe_allow_html=True)
    events = supabase.get_all_events()

    if events:
        for event in events:
            st.markdown(f"""
                <div class="event-card">
                    <div class="event-title">{event.get('name', 'N/A')}</div>
                    <div class="event-details">📅 Date: {event.get('date', 'N/A')}</div>
                    <div class="event-details">📝 Description: {event.get('description', 'No description available')}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No events available")

def main():
    # Title
    st.markdown('<p class="title-text">GramSeva</p>', unsafe_allow_html=True)

    # Create two columns with custom width ratio
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<p class="header-text">Upload a picture of the problem with a description</p>', unsafe_allow_html=True)

        if 'description' not in st.session_state:
            st.session_state.description = ""

        # File uploader
        image = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg"],
            key="uploaded_image"
        )

        # Description text area
        description = st.text_area(
            "Describe the issue (optional)",
            value=st.session_state.description,
            height=150
        )

        # Submit button
        if st.button("Submit"):
            if image:
                try:
                    image_name = f"{uuid.uuid4()}_{image.name}"
                    image_url = supabase.upload_image(image, image_name)

                    if image_url:
                        response = supabase.upload_data(image_url=image_url, description=description)
                        if response:
                            st.success("✅ Data uploaded successfully!")
                            reset_fields()
                        else:
                            st.error("❌ Failed to upload data to database.")
                    else:
                        st.error("❌ Failed to upload image.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
            else:
                st.error("⚠️ Please provide an image.")

    with col2:
        display_events()

if __name__ == "__main__":
    main()