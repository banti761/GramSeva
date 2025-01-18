import streamlit as st
from services.supabase_service import SupabaseService
import uuid
from io import BytesIO

supabase = SupabaseService()

def reset_fields():
    # Reset form fields in session state
    st.session_state.description = ""
    if 'uploaded_image' in st.session_state:
        del st.session_state.uploaded_image

def main():
    st.title("GramSeva")
    st.header("Upload a picture of the problem with a description")

    # Initialize session state for description if not exists
    if 'description' not in st.session_state:
        st.session_state.description = ""

    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="uploaded_image")
    description = st.text_area("Describe the issue (optional)", value=st.session_state.description)

    if st.button("Submit"):
        if image:
            try:
                # Generate a unique filename
                image_name = f"{uuid.uuid4()}_{image.name}"

                # Upload image to Supabase Storage
                image_url = supabase.upload_image(image, image_name)

                if image_url:
                    # Upload metadata to Supabase database
                    response = supabase.upload_data(image_url=image_url, description=description)
                    if response:
                        st.success("Data uploaded successfully!")
                        # Reset fields after successful submission
                        reset_fields()
                    else:
                        st.error("Failed to upload data to database.")
                else:
                    st.error("Failed to upload image.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please provide an image.")

if __name__ == "__main__":
    main()