import os
from supabase import create_client, Client
from dotenv import load_dotenv
from io import BytesIO

class SupabaseService:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get Supabase credentials
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.bucket_name = "village-problems"  # Your Supabase storage bucket name

        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Missing Supabase credentials. Please ensure SUPABASE_URL and SUPABASE_KEY "
                "are set in your .env file."
            )

        self.client = create_client(self.supabase_url, self.supabase_key)

    def upload_image(self, image_file, image_name: str) -> str:
        """
        Upload image to Supabase Storage and return the public URL
        """
        try:
            # Read image data
            file_data = image_file.getvalue()

            # Upload to Supabase Storage
            response = self.client.storage.from_(self.bucket_name).upload(
                path=image_name,
                file=file_data,
                file_options={"content-type": image_file.type}
            )

            # Get public URL
            image_url = self.client.storage.from_(self.bucket_name).get_public_url(image_name)
            return image_url

        except Exception as e:
            print(f"Error uploading image to storage: {str(e)}")
            return None
    def upload_audio(self, audio_file, audio_name: str) -> str:
        """
        Upload audio to Supabase Storage and return the public URL
        """
        try:
            # Read audio file data directly from the file
            file_data = audio_file.read()  # Read bytes directly from the file object

            # Upload to Supabase Storage
            response = self.client.storage.from_(self.bucket_name).upload(
                path=audio_name,
                file=file_data,
                file_options={"content-type": "audio/wav"}
            )

            # Get public URL
            audio_url = self.client.storage.from_(self.bucket_name).get_public_url(audio_name)
            return audio_url

        except Exception as e:
            print(f"Error uploading audio to storage: {str(e)}")
            return None

    def upload_data(self, image_url: str, description: str, audio_url: str = None):
        try:
            data = {
                "image_url": image_url,
                "description": description,
            }

            # Add audio_url if available
            if audio_url:
                data["audio_url"] = audio_url

            response = self.client.table("village_problems").insert(data).execute()
            return response
        except Exception as e:
            print(f"Error uploading data: {str(e)}")
            return None

    def get_all_data(self):
        try:
            response = self.client.table("village_problems").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return []
    def add_event(self, event_data):
        try:
            response = self.client.table("events").insert(event_data).execute()
            return response
        except Exception as e:
            print(f"Error adding event: {str(e)}")
        return None
    def get_all_events(self):
        try:
            response = self.client.table("events").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching events: {str(e)}")
            return []
