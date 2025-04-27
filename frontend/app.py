import streamlit as st
import requests

# Set the page title and layout
st.title("AI Travel Planner")
st.write("Enter your city and budget to plan your next trip!")

# Inputs
city = st.text_input("Enter your city")
budget = st.number_input("Enter your budget ($)", min_value=100, step=50)

# Plan your trip
if st.button("Plan My Trip"):
    if city and budget:
        # Make request to FastAPI backend
        response = requests.post("http://127.0.0.1:8000/plan_trip/", json={"city": city, "budget": budget})
        
        if response.status_code == 200:
            plan = response.json().get("plan")
            st.write(plan)
        else:
            st.error(f"Error: {response.json().get('detail')}")
    else:
        st.error("Please fill in both city and budget!")
