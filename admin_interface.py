import streamlit as st
from services.supabase_service import SupabaseService
from datetime import datetime
from events import show_events_page

supabase = SupabaseService()

def show_dashboard():
    st.header("Dashboard")

    data = supabase.get_all_data()
    if data:
        sorted_data = sorted(data, key=lambda x: x.get('created_at', ''), reverse=True)

        num_cols = 3
        cols = st.columns(num_cols)

        for index, entry in enumerate(sorted_data):
            with cols[index % num_cols]:
                st.image(entry["image_url"], caption="Uploaded Image")

                description = entry.get('description')
                if description is None or description.strip() == '':
                    st.markdown("**Description:** No description was found")
                else:
                    st.markdown(f"**Description:** {description}")

                created_at = entry.get('created_at', '')
                if created_at:
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        formatted_date = dt.strftime('%B %d, %Y')
                        st.markdown(f"*Posted: {formatted_date}*")
                    except:
                        st.markdown(f"*Posted: {created_at}*")
                else:
                    st.markdown("*Posted: Time not available*")
    else:
        st.info("No data available")

def main():
    st.title("Village Problems")

    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Events"])

    # Display selected page
    if page == "Dashboard":
        show_dashboard()
    else:
        show_events_page()

if __name__ == "__main__":
    main()