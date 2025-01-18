import streamlit as st
from datetime import datetime
from services.supabase_service import SupabaseService

def add_event_form():
    st.subheader("Add New Event")
    with st.form("event_form"):
        event_name = st.text_input("Event Name")
        event_date = st.date_input("Event Date")
        event_description = st.text_area("Event Description")

        submitted = st.form_submit_button("Submit Event")

        if submitted:
            if event_name and event_date and event_description:
                supabase = SupabaseService()
                response = supabase.add_event({
                    "name": event_name,
                    "date": event_date.isoformat(),
                    "description": event_description
                })

                if response:
                    st.success("Event added successfully!")
                else:
                    st.error("Failed to add event")
            else:
                st.warning("Please fill in all fields")

def show_events_list():
    st.subheader("Events List")

    supabase = SupabaseService()
    events = supabase.get_all_events()

    if events:
        sorted_events = sorted(events, key=lambda x: x.get('date', ''))

        for event in sorted_events:
            with st.container():
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"### {event['name']}")
                    st.write(event['description'])

                with col2:
                    event_date = datetime.fromisoformat(event['date']).strftime('%B %d, %Y')
                    st.markdown(f"**Date:** {event_date}")

                st.divider()
    else:
        st.info("No events available")

def show_events_page():
    st.header("Events")

    tab1, tab2 = st.tabs(["Events List", "Add Event"])

    with tab1:
        show_events_list()

    with tab2:
        add_event_form()