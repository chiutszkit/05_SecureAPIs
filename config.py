import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_CONFIG = {
    'nasa': {
        'api_key': os.getenv('NASA_API_KEY'),
        'base_url': 'https://api.nasa.gov/neo/rest/v1/feed'
    }
}

# Add more API configurations here as needed
# Example:
# API_CONFIG['weather'] = {
#     'api_key': 'your_weather_api_key',
#     'base_url': 'https://api.weather.com/...'
# }