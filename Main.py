from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import re
from datetime import datetime, timedelta
import folium
from geopy.geocoders import Nominatim
from neo4j import GraphDatabase
import re
import geopy.distance
import gradio as gr
import folium
from geopy.distance import geodesic
import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
import time
import streamlit as st
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import re
from datetime import datetime
from neo4j import GraphDatabase, basic_auth
class ItineraryGenerationAgent:
    """Generates an initial itinerary based on user preferences."""
    
    def __init__(self, api_key, geocode_api_key):
        self.api_key = api_key
        self.base_url = "https://api.foursquare.com/v3/places/search"
        self.geocode_api_key = geocode_api_key
        self.geocode_url = "https://api.opencagedata.com/geocode/v1/json"
    




   
# taking Input inputs

import re

class UserInteractionAgent:
    """Handles user input collection and preference gathering."""

    def __init__(self):
        self.preferences = {
            "city": None,
            "timing": None,
            "budget": None,
            "interests": [],
            "starting_point": None
        }

    def collect_preferences(self, user_input):
        """
        Parses user input to extract city, timings, budget, and interests.
        Updates preferences dictionary with extracted information.
        """
        # Improved regular expression for extracting multi-word city names
        city_match = re.search(r'\b(?:in|to|visit|trip to|trip in|city) ([A-Za-z ]+)', user_input, re.IGNORECASE)
        if city_match:
            self.preferences['city'] = city_match.group(1).strip().title()

        # Extract budget
        budget_match = re.search(r'\$(\d+)', user_input)
        if budget_match:
            self.preferences['budget'] = int(budget_match.group(1))

        # Extract timing or day/time duration for the trip
        timing_match = re.search(r'(morning|afternoon|evening|night|whole day|all day)', user_input, re.IGNORECASE)
        if timing_match:
            self.preferences['timing'] = timing_match.group(1).lower()

        # Extract interests (e.g., culture, adventure, food, shopping)
        interests_match = re.findall(r'\b(art|food|culture|adventure|shopping|history|nature|music|outdoors)\b', user_input, re.IGNORECASE)
        if interests_match:
            self.preferences['interests'].extend([interest.lower() for interest in interests_match])

        return self.preferences

class ItineraryGenerationAgent:
    """Generates an initial itinerary based on user preferences."""
    
    def __init__(self, api_key, geocode_api_key):
        self.api_key = api_key
        self.base_url = "https://api.foursquare.com/v3/places/search"
        self.geocode_api_key = geocode_api_key
        self.geocode_url = "https://api.opencagedata.com/geocode/v1/json"
    
    def generate_itinerary(self, preferences):
        """
        Generates an initial itinerary based on user preferences.
        Calls Foursquare API to get points of interest.
        """
        city = preferences.get('city')
        interests = preferences.get('interests', [])
        budget = preferences.get('budget', 0)
        
        if not city:
            raise ValueError("City is required to generate an itinerary.")
        
        # Get the latitude and longitude of the city
        lat, lon = self.get_city_coordinates(city)
        if lat is None or lon is None:
            raise ValueError("Could not find coordinates for the specified city.")
        
        # Compile itinerary based on interests
        itinerary = []
        for interest in interests:
            places = self.get_places_by_interest(lat, lon, interest, budget)
            itinerary.extend(places)
        
        # Sort the itinerary by proximity or other factors as needed
        sorted_itinerary = self.sort_itinerary(itinerary)
        return sorted_itinerary
    
    def get_city_coordinates(self, city):
        """
        Gets the coordinates for a city using the OpenCage Geocoding API.
        """
        params = {
            "q": city,
            "key": self.geocode_api_key,
            "limit": 1
        }
        response = requests.get(self.geocode_url, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching coordinates: {response.status_code}")
            return None, None
        
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']
            return location['lat'], location['lng']
        else:
            print("No results found for the specified city.")
            return None, None

    def get_places_by_interest(self, lat, lon, interest, budget):
        """
        Calls Foursquare API to get places by interest within budget.
        """
        headers = {
            "Accept": "application/json",
            "Authorization": self.api_key
        }
        
        params = {
            "ll": f"{lat},{lon}",
            "query": interest,
            "limit": 5,  # Limit the number of results per interest
            "radius": 5000  # Radius in meters; adjust based on user preferences
        }
        
        response = requests.get(self.base_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching data from Foursquare API: {response.status_code}")
            return []
        
        # Parse the response
        places = response.json().get('results', [])
        filtered_places = []
        
        for place in places:
            name = place.get('name')
            address = place.get('location', {}).get('formatted_address', 'Address not available')
            price = place.get('price', 0)  # Assumes Foursquare API includes price data
            
            # Filter based on budget if price information is available
            if budget and price > budget:
                continue
            
            filtered_places.append({
                "name": name,
                "address": address,

                "category": interest
            })
        
        return filtered_places

    def sort_itinerary(self, itinerary):
        """
        Sorts itinerary items based on custom logic, e.g., proximity or type of attraction.
        This is a placeholder and can be enhanced based on additional requirements.
        """
        # Example: Sort by name for simplicity
        return sorted(itinerary, key=lambda x: x['name'])

class WeatherAgent:
    """Fetches weather information and provides recommendations based on the forecast."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://dataservice.accuweather.com"

    def get_location_key(self, city):
        """Retrieves the location key for a given city using the AccuWeather Locations API."""
        endpoint = f"{self.base_url}/locations/v1/cities/search"
        params = {"apikey": self.api_key, "q": city}
        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            print(f"Error fetching location key: {response.status_code}")
            return None

        locations = response.json()
        if not locations:
            print("No location found for the specified city.")
            return None

        return locations[0].get("Key")

    def fetch_weather(self, city, date):
        """Fetches the weather forecast for a specified city and date."""
        location_key = self.get_location_key(city)
        if not location_key:
            return {"error": "Could not retrieve location key for the specified city."}

        endpoint = f"{self.base_url}/forecasts/v1/daily/5day/{location_key}"
        params = {"apikey": self.api_key, "metric": True}
        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            print(f"Error fetching weather data: {response.status_code}")
            return {"error": "Could not retrieve weather data from AccuWeather."}

        forecast_data = response.json()
        for forecast in forecast_data.get("DailyForecasts", []):
            try:
                forecast_date = datetime.strptime(forecast["Date"], "%Y-%m-%dT%H:%M:%S%z").date()
                if forecast_date == date.date():
                    return {
                        "date": str(forecast_date),
                        "min_temperature": forecast["Temperature"]["Minimum"]["Value"],
                        "max_temperature": forecast["Temperature"]["Maximum"]["Value"],
                        "day_condition": forecast["Day"]["IconPhrase"],
                        "night_condition": forecast["Night"]["IconPhrase"],
                        "recommendation": self.get_recommendation(forecast["Day"]["IconPhrase"])
                    }
            except Exception as e:
                print(f"Error parsing forecast data: {e}")

        return {"error": "Weather data not available for the specified date."}

    def get_recommendation(self, condition):
        """Provides a recommendation based on the weather condition."""
        recommendations = {
            "Rain": "It's likely to rain. Bring an umbrella and consider indoor activities.",
            "Sunny": "The weather is clear. Great for outdoor activities!",
            "Snow": "Expect snow. Dress warmly and consider indoor activities.",
            "Cloudy": "It's cloudy. You may want to bring a light jacket.",
            "Thunderstorms": "Thunderstorms expected. Stay indoors for safety.",
            "Partly sunny": "Partly sunny. A good day for mixed activities."
        }
        return recommendations.get(condition, "No specific recommendation.")
class MapGenerationAgent:
    """Generates a visual map of the itinerary with marked places."""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="map_generation_agent")

    def generate_map(self, itinerary, start_location=None):
        """
        Generates an interactive map with itinerary points marked.
        """
        # Set the initial location for the map as the first item in the itinerary or a default location
        if start_location:
            map_location = start_location
        elif itinerary:
            # Check if the first item in itinerary has 'latitude' and 'longitude' keys
            first_place = itinerary[0]
            if 'latitude' in first_place and 'longitude' in first_place:
                map_location = (first_place['latitude'], first_place['longitude'])
            else:
                print("Latitude and longitude not found for the first place. Using default location.")
                map_location = (0, 0)  # Default to lat/lon (0, 0)
        else:
            map_location = (0, 0)  # Default location if no itinerary
        
        # Create the map centered at the initial location
        travel_map = folium.Map(location=map_location, zoom_start=13)

        # Add starting location marker, if available
        if start_location:
            folium.Marker(
                start_location, popup="Starting Point", icon=folium.Icon(color="blue")
            ).add_to(travel_map)

        # Mark each place in the itinerary on the map
        for place in itinerary:
            # Check for coordinates in each place
            if 'latitude' in place and 'longitude' in place:
                folium.Marker(
                    [place["latitude"], place["longitude"]],
                    popup=place.get("name", "Unnamed Place"),
                    icon=folium.Icon(color="red")
                ).add_to(travel_map)
            else:
                print(f"Skipping place '{place.get('name', 'Unnamed Place')}' due to missing coordinates.")
        
        # Optionally, add a travel path between points
        coordinates = [(place["latitude"], place["longitude"]) for place in itinerary if 'latitude' in place and 'longitude' in place]
        if coordinates:
            folium.PolyLine(coordinates, color="green", weight=2.5, opacity=1).add_to(travel_map)

        return travel_map

    

class NewsAgent:
    """Fetches news or events that could affect the itinerary."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_news(self, city):
        """
        Fetches recent news or events happening in the city.
        
        Args:
            city (str): The city for which to fetch news.

        Returns:
            list: A list of headlines or events in the city.
        """
        # Define the date range for recent news (last 7 days)
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        params = {
            "q": city,
            "from": from_date,
            "to": to_date,
            "sortBy": "relevancy",
            "apiKey": self.api_key
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            print(f"Error fetching news: {response.status_code}")
            return ["Error fetching news data."]

        news_data = response.json()
        headlines = [article["title"] for article in news_data.get("articles", [])]

        return headlines[:5]  # Return top 5 relevant news headlines
    

class MemoryAgent:
    """Stores and recalls user preferences in a Neo4j graph database using LLM-generated triplets."""

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def close(self):
        """Closes the Neo4j driver connection."""
        self.driver.close()

    def parse_triplets_with_llm(self, text):
        """
        Uses a mocked LLM to parse text and return a list of triplets in the format (Entity1, Relationship, Entity2).
        
        Args:
            text (str): The text to parse for triplets.

        Returns:
            list: A list of triplets, where each triplet is a tuple (Entity1, Relationship, Entity2).
        """
        # Mocked response to simulate LLM-generated triplets.
        if "art" in text and "New York" in text:
            return [("User", "HAS_PREFERENCE", "Art"), ("User", "VISITS", "New York")]
        elif "food" in text:
            return [("User", "LIKES", "Food")]
        else:
            return [("User", "INTERESTED_IN", "General")]

    def store_triplets(self, user_id, text):
        """
        Uses the LLM to generate triplets from the text and stores them in the Neo4j database.

        Args:
            user_id (str): The unique identifier for the user.
            text (str): The user input text to parse and store as memory triplets.
        """
        # Generate triplets based on the input text using LLM (mocked here).
        triplets = self.parse_triplets_with_llm(text)

        # Store each triplet in Neo4j
        with self.driver.session() as session:
            for entity1, relationship, entity2 in triplets:
                session.write_transaction(self._store_triplet, user_id, entity1, relationship, entity2)

    @staticmethod
    def _store_triplet(tx, user_id, entity1, relationship, entity2):
        """
        Creates or updates a triplet relationship in the Neo4j database, including a User node.
        
        Args:
            tx: The Neo4j transaction object.
            user_id (str): The unique identifier for the user.
            entity1 (str): The first entity in the triplet.
            relationship (str): The relationship between entities.
            entity2 (str): The second entity in the triplet.
        """
        # Store the user as a distinct node and connect it to the triplet
        tx.run("""
            MERGE (u:User {user_id: $user_id})
            MERGE (e1:Entity {name: $entity1})
            MERGE (e2:Entity {name: $entity2})
            MERGE (u)-[:PREFERS]->(e1)
            MERGE (e1)-[r:RELATES {type: $relationship}]->(e2)
        """, user_id=user_id, entity1=entity1, relationship=relationship, entity2=entity2)

    def recall_triplets(self, user_id):
        """
        Recalls all stored triplets for a given user from the Neo4j database.

        Args:
            user_id (str): The unique identifier for the user.

        Returns:
            list: A list of triplets representing the user's preferences.
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_triplets, user_id)
            return [(record["entity1"], record["relationship"], record["entity2"]) for record in result]

    @staticmethod
    def _get_triplets(tx, user_id):
        """
        Retrieves stored triplets for a given user from Neo4j.

        Args:
            tx: The Neo4j transaction object.
            user_id (str): The unique identifier for the user.

        Returns:
            list: Query result containing triplets.
        """
        query = """
            MATCH (u:User {user_id: $user_id})-[:PREFERS]->(e1:Entity)-[r]->(e2:Entity)
            RETURN e1.name AS entity1, r.type AS relationship, e2.name AS entity2
        """
        result = tx.run(query, user_id=user_id)
        return list(result)

# Initialize FastAPI app
app = FastAPI()

# Set up global variables and configurations
OLLAMA_MODEL_NAME = "YOUR API KEY"
OLLAMA_API_URL = "YOUR API KEY"
geocode_api_key = "YOUR API KEY"
weather_api_key = "YOUR API KEY"
foursquare_api_key = "YOUR API KEY"
news_api_key = "YOUR API KEY"
memory_db_uri = "YOUR API KEY"
memory_db_user = "YOUR API KEY"
memory_db_password = "YOUR API KEY"


# Initialize agents with API keys
weather_agent = WeatherAgent(api_key=weather_api_key)
news_agent = NewsAgent(api_key=news_api_key)
itinerary_agent = ItineraryGenerationAgent(api_key=foursquare_api_key, geocode_api_key=geocode_api_key)
memory_agent = MemoryAgent(uri=memory_db_uri, user=memory_db_user, password=memory_db_password)
map_agent = MapGenerationAgent()



# Initialize FastAPI app
app = FastAPI()

# Set up global variables and configurations
# Set up global variables and configurations
OLLAMA_MODEL_NAME = "llama3.2"
OLLAMA_API_URL = "http://localhost:11434/v1/completions"  # Update this to match the correct endpoint

MAX_RETRIES = 3  # Maximum number of retries for Ollama API requests
RETRY_DELAY = 2  # Delay in seconds between retries
chat_history = {}

# Request Model
class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[str] = None

# Helper function to get response from LLM
def get_ollama_response(user_id: str, message: str, chat_history: list[str]):
    # Build chat history context
    history_context = "\n".join(chat_history)

    # Include chat history in the guiding prompt
    guiding_prompt = (
        f"{history_context}\nUser: {message}\n\n"
        "You are a helpful assistant. Please continue the conversation based on the context provided above."
    )

    payload = {"model": "llama3.2", "prompt": guiding_prompt}
    response = requests.post("http://localhost:11434/v1/completions", json=payload)
    data = response.json()
    return data["choices"][0]["text"] if "choices" in data and data["choices"] else "No response from Ollama."

# Main Chat Endpoint
@app.post("/chat")
@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles chat requests, managing interaction with various agents based on specific keywords."""
    user_input = request.message
    user_id = request.user_id

    # Retrieve chat history from Neo4j using MemoryAgent
    chat_history = memory_agent.recall_triplets(user_id)
    chat_history_formatted = [
        f"User: {record[0]}\nAssistant: {record[2]}" for record in chat_history
    ]

    # If there is no chat history, ask for preferences
    if not chat_history:
        response_message = (
            "To get started, could you please share your city, interests, and budget? "
            "For example, you could say, 'I'd like to explore art and food in New York with a budget of $200.'"
        )
        memory_agent.store_triplets(user_id, user_input)  # Updated to match the method signature
        return {"message": response_message}

    # Use the LLM to decide on the next steps
    try:
        # Call the LLM with the chat history
        ollama_response = get_ollama_response(user_id, user_input, chat_history_formatted)

        # Based on the LLM's response, decide if an agent should be called
        if "itinerary" in ollama_response.lower():
            city = next((record[2] for record in chat_history if record[1] == "VISITS"), None)
            interests = next((record[2] for record in chat_history if record[1] == "HAS_PREFERENCE"), [])
            budget = next((record[2] for record in chat_history if record[1] == "BUDGET"), None)
            
            if not city:
                response_message = "It seems like you haven't mentioned the city you'd like to visit. Could you please specify the city for your itinerary?"
            else:
                # Generate itinerary with relevant details
                user_preferences = {"city": city, "interests": interests, "budget": budget}
                itinerary = itinerary_agent.generate_itinerary(user_preferences)
                
                if itinerary:
                    # Format the itinerary for display
                    formatted_itinerary = "\n".join([
                        f"**{place['name']}** - {place['address']} (Category: {place['category']}, Price: {place['price']})"
                        for place in itinerary
                    ])
                    response_message = f"Here are some itinerary suggestions for {city}:\n\n{formatted_itinerary}"
                else:
                    response_message = "I'm sorry, I couldn't find any itinerary suggestions based on your preferences."

            memory_agent.store_triplets(user_id, user_input)  # Updated to match the method signature
            return {"message": response_message}

        elif "weather" in ollama_response.lower():
            city = next((record[2] for record in chat_history if record[1] == "VISITS"), None)
            if not city:
                response_message = "I need to know the city to provide a weather forecast. Could you please specify the city?"
            else:
                weather_info = weather_agent.fetch_weather(city, datetime.now())
                response_message = "Here's the weather forecast."
            memory_agent.store_triplets(user_id, user_input)  # Updated to match the method signature
            return {"message": response_message, "weather": weather_info}

        elif "map" in ollama_response.lower():
            travel_map = map_agent.generate_map([])
            response_message = "Here's a map for your itinerary."
            memory_agent.store_triplets(user_id, user_input)  # Updated to match the method signature
            return {"message": response_message, "map": travel_map._repr_html_()}

        # Default response from LLM
        memory_agent.store_triplets(user_id, user_input)  # Updated to match the method signature
        return {"message": ollama_response}

    except Exception as e:
        print(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
