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

    def upload_data(self, image_url: str, description: str):
        try:
            response = self.client.table("village_problems").insert({
                "image_url": image_url,
                "description": description
            }).execute()
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
