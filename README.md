**Interactive Travel Planner Assistant**


This project is an interactive travel planning assistant that leverages Streamlit for the frontend, FastAPI for API handling, Neo4j for user preference storage, Folium for map generation, and Ollama with Llama 3.2 for natural language understanding. The assistant can interpret user inputs to generate an itinerary, provide weather updates, retrieve relevant news, and display an interactive map for planned locations.

# Project Structure
Key Components

Frontend: Built using Streamlit, providing an interactive chat-based interface for users to communicate with the assistant.
Backend: FastAPI is used to handle requests and connects the frontend to various agents (itinerary, memory, weather, etc.).
Database: Neo4j serves as a graph database to store user preferences and interactions, allowing for easy retrieval and personalized recommendations.
Natural Language Understanding: Ollama and Llama 3.2 are leveraged for language processing, parsing user inputs, and generating contextually aware responses.
Mapping: Folium is used to generate interactive maps that visually display itineraries based on user preferences.
Agents: Each feature (weather, itinerary generation, memory storage) is handled by individual agents, making the code modular and easy to maintain.

# Approach and Solution
Problem Analysis

The project’s goal is to create an AI-powered travel assistant that:

Understands user preferences through natural language input.
Retrieves relevant weather and news information for specific locations.
Generates a recommended itinerary based on user-defined preferences.
Displays an interactive map for easy navigation of the planned itinerary.

# Solution Design
Natural Language Processing with Ollama and Llama 3.2:

Llama 3.2 deployed via Ollama interprets user queries, extracts actionable information, and guides actions by other agents based on user intent.

Memory Storage with Neo4j:
Neo4j is used to store user preferences and past interactions as triplets, representing relationships that allow for easy recall and retrieval.
The MemoryAgent extracts and stores relationships based on user input, enabling the assistant to maintain a memory of user preferences and retrieve them for future sessions.

Conversation Management:
Streamlit session state is used to maintain conversation context, tracking the current stage (itinerary, weather, etc.) of interaction.
Context switching allows the assistant to shift focus seamlessly between itinerary suggestions, weather updates, and map views.

Itinerary Generation:
Foursquare API is integrated to fetch places of interest based on user preferences.
The ItineraryGenerationAgent processes preferences such as city, interests, and budget to create a list of recommended locations, sorted based on relevance.

Weather and News Information:
WeatherAgent and NewsAgent handle real-time data fetching, providing information about current conditions and recent events relevant to the destination.

Map Generation:
MapGenerationAgent uses Folium to generate interactive maps that display the itinerary locations with markers.
The generated map includes a route path between points, offering a visual guide for the user’s day out.


# Workflow

User Input:
The user provides input in the Streamlit app, specifying travel preferences or questions.

Backend Processing:
FastAPI processes requests from the frontend and initiates calls to relevant agents based on extracted user intent.
Ollama interprets user input using Llama 3.2, parsing it to identify preferences, interests, and any actions to take.

Action Execution:
Based on Llama 3.2's response, the system executes relevant actions through agents, such as generating itineraries, fetching weather data, or recalling user preferences from Neo4j.

Frontend Display:
The assistant’s response is displayed in the Streamlit app, including preferences, itinerary suggestions, weather information, and an interactive map.
Maps are generated using Folium and displayed through streamlit_folium for interactivity.



link to demo video:
https://drive.google.com/file/d/19XmeXGIZS5MtwGAOtGrWpCJdNMtt8dwu/view?usp=drive_link

