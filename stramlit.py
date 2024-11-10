import streamlit as st
import requests
from datetime import datetime

# Initialize session state to track conversation and manage context
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "current_context" not in st.session_state:
    st.session_state.current_context = "initial"
if "username" not in st.session_state:
    st.session_state.username = None

# Function to update context and generate the next question/response
def update_context_and_generate_response(user_input, assistant_response):
    # Append the user's input and the assistant's response to the conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_response})

    # Logic to update context and decide the next question or response
    if "preferences" in st.session_state.current_context and "itinerary" in assistant_response.lower():
        st.session_state.current_context = "itinerary_suggestions"
    elif "weather" in assistant_response.lower():
        st.session_state.current_context = "weather_info"
    elif "map" in assistant_response.lower():
        st.session_state.current_context = "map_info"
    else:
        st.session_state.current_context = "general"

# Streamlit UI for interacting with FastAPI
st.title("Interactive Travel Planner Assistant")

# Step 1: Ask for the user's name
if st.session_state.username is None:
    st.session_state.username = st.text_input("What's your name?", key="username_input")
    if st.button("Submit Name"):
        if st.session_state.username:
            st.write(f"👋 Hi {st.session_state.username}! Let's plan a fun and memorable day out together.")
        else:
            st.write("Please enter your name to proceed.")
else:
    # Step 2: Continue with the conversation
    st.write(f"👋 Hi {st.session_state.username}! I'm here to help you plan a fun and memorable day out. Let's chat!")

    # Display previous conversation history
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.write(f"**{st.session_state.username}:** {message['content']}")
        else:
            st.write(f"**Assistant:** {message['content']}")

    # Input for the user to continue the conversation
    message = st.text_input("Your message:", value="", key="user_input")

    # Button to send the message
    if st.button("Send"):
        if message:
            # Prepare the payload for the FastAPI call
            payload = {
                "user_id": st.session_state.username,
                "message": message,
                "context": st.session_state.current_context
            }

            # Send the message to FastAPI
            response = requests.post("http://localhost:8000/chat", json=payload)

            # Check if the response is OK
            if response.status_code == 200:
                try:
                    data = response.json()

                    # Get the assistant's message and update the context
                    assistant_message = data.get("message", "I didn't quite catch that. Could you please clarify?")
                    update_context_and_generate_response(message, assistant_message)
                    st.write(f"**Assistant:** {assistant_message}")

                    # Display additional details based on the context
                    if "itinerary" in data:
                        st.header("Itinerary Suggestions")
                        for item in data.get("itinerary", []):
                            st.write(f"📍 **{item.get('name', 'Unknown')}**")
                            st.write(f"Address: {item.get('address', 'Address not available')}")
                            
                            st.write(f"Category: {item.get('category', 'Category not available')}")
                            st.write("---")
                    elif "weather" in data:
                        st.header("Weather Forecast")
                        weather_info = data.get("weather", {})
                        if "error" in weather_info:
                            st.error(f"🚨 {weather_info['error']}")
                        else:
                            st.write(f"🌤️ **Date**: {weather_info.get('date', 'Date not available')}")
                            st.write(f"🌡️ **Min Temperature**: {weather_info.get('min_temperature', 'N/A')}°C")
                            st.write(f"🌡️ **Max Temperature**: {weather_info.get('max_temperature', 'N/A')}°C")
                            st.write(f"🌞 **Day Condition**: {weather_info.get('day_condition', 'N/A')}")
                            st.write(f"🌜 **Night Condition**: {weather_info.get('night_condition', 'N/A')}")
                            st.write(f"💡 **Recommendation**: {weather_info.get('recommendation', 'No recommendation available')}")
                    elif "map" in data:
                        st.header("Itinerary Map")
                        st.write("🌍 Here's a map to guide you:")
                        st.components.v1.html(data["map"], height=500)

                except requests.JSONDecodeError:
                    st.write("😕 Oops! Something went wrong. The response is not in JSON format.")
            else:
                st.write(f"🚨 Error {response.status_code}: {response.text}")
        else:
            st.write("Please enter a message to continue the conversation.")
