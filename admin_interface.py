import streamlit as st
from services.supabase_service import SupabaseService
from datetime import datetime

supabase = SupabaseService()

def main():
    st.title("Village Problems")
    st.header("Dashboard")

    data = supabase.get_all_data()
    if data:
        sorted_data = sorted(data, key=lambda x: x.get('created_at', ''), reverse=True)

        num_cols = 3
        cols = st.columns(num_cols)

        for index, entry in enumerate(sorted_data):
            with cols[index % num_cols]:
                st.image(entry["image_url"], caption="Uploaded Image")

                # Check if description is None or empty string
                description = entry.get('description')
                if description is None or description.strip() == '':
                    st.markdown("**Description:** No description was found")
                else:
                    st.markdown(f"**Description:** {description}")

                # Format the timestamp
                created_at = entry.get('created_at', '')
                if created_at:
                    try:
                        # Parse the timestamp and format it
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        formatted_date = dt.strftime('%B %d, %Y')
                        st.markdown(f"*Posted: {formatted_date}*")
                    except:
                        st.markdown(f"*Posted: {created_at}*")
                else:
                    st.markdown("*Posted: Time not available*")
    else:
        st.info("No data available")

if __name__ == "__main__":
    main()