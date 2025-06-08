import os

from dotenv import load_dotenv

load_dotenv()


class Secrets:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_base_url = os.getenv("GEMINI_BASE_URL")
        self.gemini_api_model = os.getenv("GEMINI_API_MODEL")

        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")
        self.openrouter_model1 = os.getenv("OPENROUTER_MODEL1")
        self.openrouter_model2 = os.getenv("OPENROUTER_MODEL2")

        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.weather_base_url = os.getenv("WEATHER_BASE_URL")

        self.joke_api_base_url = os.getenv("JOKE_BASE_URL")

        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.news_base_url = os.getenv("NEWS_BASE_URL")

        self.currency_exchange_api_key = os.getenv("CURRENCY_EXCHANGE_API_KEY")
        self.currency_exchange_base_url = os.getenv("CURRENCY_EXCHANGE_URL")
