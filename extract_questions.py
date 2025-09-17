import requests
import json
import os

def extract():
    api_url = "https://the-trivia-api.com/v2/questions"
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()

        questions_dir = os.path.join(curr_dir, "resources", "questions.json")
        with open(questions_dir, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Questions successfully extracted")

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")

if __name__ == '__main__':
    extract()