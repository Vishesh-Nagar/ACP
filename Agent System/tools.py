# Tool functions for agent interactions.

import os
import requests
import time
from dotenv import load_dotenv
from typing import Optional
import logging

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def get_weather(city: str) -> dict:
    """Retrieve current weather for a specified city using WeatherAPI.com."""

    logging.info(f"weather agent called for city: {city}")

    api_key = os.getenv("WEATHERAPI_KEY")
    if not api_key:
        return {"status": "error", "error_message": "WEATHERAPI_KEY not set in .env file."}

    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            logging.info(f"data: {data}")
            current = data.get("current", {})
            condition = current.get("condition", {}).get("text")
            temp_c = current.get("temp_c")

            if condition and temp_c is not None:
                report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_c}°C."
                return {"status": "success", "report": report}
            else:
                return {"status": "error", "error_message": "Unexpected API response structure."}

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return {"status": "error", "error_message": str(e)}
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            return {"status": "error", "error_message": f"Unexpected error: {e}"}
    
def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    logging.info("say_hello tool called")
    name = "Vishesh"
    return "Hello {name}! How can I assist you today?".format(name=name)



def translate_english_to_spanish(text: str) -> dict:
    """Translates English text to Spanish using a dictionary, with fallback indication.

    Args:
        text (str): The English text to translate.

    Returns:
        dict: A dictionary with 'translated' (str) and 'complete' (bool) keys.
              'translated' contains the translated text, 'complete' indicates if all words were translated.
    """
    logging.info(f"translate_english_to_spanish called with text: {text}")

    # Simple mock translations for demonstration
    translations = {
        "hello": "hola",
        "world": "mundo",
        "how are you": "cómo estás",
        "thank you": "gracias",
        "goodbye": "adiós",
        "please": "por favor",
        "yes": "sí",
        "no": "no",
        "i love you": "te amo",
        "what is your name": "cuál es tu nombre",
    }

    # Simple word-by-word translation (for demo purposes)
    words = text.lower().split()
    translated_words = []
    all_translated = True
    for word in words:
        if word in translations:
            translated_words.append(translations[word])
        else:
            translated_words.append(word)  # Keep original if not found
            all_translated = False

    translated_text = " ".join(translated_words).capitalize()

    return {"translated": translated_text, "complete": all_translated}
