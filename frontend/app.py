import streamlit as st
import requests

st.set_page_config(page_title="AI Travel Planner", layout="centered")

st.title("✈️ AI Travel Planner")
st.markdown("Plan your perfect trip in seconds using AI.")

# -------------------------
# Travel Planner Section
# -------------------------
st.header("📍 Plan a Trip")
city = st.selectbox("Select a City", ["Goa", "Paris", "Tokyo"])
budget = st.slider("Select Your Budget (in USD)", 100, 10000, 1500, step=100)

if st.button("🧳 Plan My Trip"):
    with st.spinner("Generating your travel plan..."):
        response = requests.post(
            "http://127.0.0.1:8000/plan",
            json={"city": city, "budget": budget}
        )
        if response.status_code == 200:
            plan = response.json()
            st.success("Here's your AI-generated travel plan:")
            st.markdown(f"""
            ### 🌍 Destination: {city}
            **Budget**: ${budget}

            **Plan**:  
            {plan["plan"]}
            """)
        else:
            st.error("Something went wrong. Please try again.")

# -------------------------
# Chatbot Section
# -------------------------
st.divider()
st.header("💬 Travel Chat Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask a travel-related question", key="user_input")
if st.button("💡 Ask AI"):
    if user_query.strip() != "":
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"query": user_query, "city": city}
            )
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    st.warning(data["message"])
                else:
                    st.session_state.chat_history.append(("You", user_query))
                    st.session_state.chat_history.append(("AI", data["results"]))
            else:
                st.error("Failed to get response from chatbot.")

# Show chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")
