import itertools
import os
import threading
import time
import pandas as pd
import requests
from csv_settings import categories, delete_keywords, keywords


def should_delete(description):
    # Convert description to upper case once for efficiency
    description_upper = description.upper()
    return any(keyword.upper() in description_upper for keyword in delete_keywords)


def csv_categorize(
    input_folder: str,
    output_folder: str,
    csv_file: str
):
    # Start spinner
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        file_path = os.path.join(input_folder, csv_file)

        data = pd.read_csv(file_path)

        data = data[~data['Description'].apply(should_delete)]

        # ! do categorize here
        data['Category'] = data['Description'].apply(categorize_spending)

        # Prepare JSON output path and save JSON
        json_file = csv_file.replace('.csv', '.json')
        json_path = os.path.join(output_folder, json_file)
        data.to_json(json_path, orient='records', indent=4)

        print(f"Processed {csv_file} to {json_path}")
    finally:
        # Stop spinner
        spinner_thread.do_run = False
        spinner_thread.join()


def categorize_spending(description):
    # Load  from a JSON file

    # Iterate over the keyword to category mapping
    for keyword, category in keywords.items():
        # Use upper case for case insensitive matching
        if keyword in description.upper():
            return category

    # If no direct match, fallback to LLM categorization
    return call_llm_to_categorize(description)


def call_llm_to_categorize(desc):
    prompt = f"""
            Please categorize this spending: '{desc}' with {categories}.
            Response only one of the category text.
            No explanation No extra text no special character.
        """

    url = 'http://localhost:11434/api/generate'
    body = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        result = response.json()
        assign = result.get('response')
        # print finish categorize
        print(f'{desc} Category {assign}')

        return result.get('response', 'Uncategorized')
    else:
        return 'Error'

# Modification to the spinner function to check for an exit condition


def spinner():
    spinner_icons = itertools.cycle(['-', '\\', '|', '/'])
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print(next(spinner_icons), end='\r', flush=True)
        time.sleep(0.1)
