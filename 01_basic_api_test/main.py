import requests
import dotenv
import os

dotenv.load_dotenv()

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

headers = {
        'Content-Type': 'application/json'
        }
requestResponse = requests.get(f"https://api.tiingo.com/api/test?token={TIINGO_API_KEY}",
                                    headers=headers)
print(requestResponse.json())