import streamlit as st
from services.supabase_service import SupabaseService

supabase = SupabaseService()

def main():
    st.title("Village Problems")
    st.header("Dashboard")

    data = supabase.get_all_data()
    if data:
        num_cols = 3
        cols = st.columns(num_cols)

        for index, entry in enumerate(data):
            with cols[index % num_cols]:
                st.image(entry["image_url"], caption="Uploaded Image")
                st.markdown(f"**Description:** {entry['description']}")
    else:
        st.info("No data available")

if __name__ == "__main__":
    main()
