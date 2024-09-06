# Princeton Course Recommendation Chatbot

This repository contains a Princeton Course Recommendation Chatbot that uses OpenAI's GPT-4 API and Elasticsearch to help students find courses based on their preferences. The system scrapes course data from the Princeton registrar's website, indexes it using Elasticsearch, and interacts with users through a Flask web application.

## Running Instructions

To run the chatbot, follow these steps:

### 1. Set Up API Keys

You will need to create two files: `api_key.py` and `elastic_search_variables.py`. These files store your OpenAI and Elasticsearch API keys.

- **Create `api_key.py`:**

  In this file, define a method called `get_api_key()` that returns your OpenAI API key.

  ```python
  def get_api_key():
      return "your_openai_api_key_here"
  ```

- **Create `elastic_search_variables.py`:**

  In this file, define two methods: `get_api_key()` and `get_cloud_id()`.

  - `get_api_key()` should return your Elasticsearch API key.
  - `get_cloud_id()` should return your Elasticsearch cloud ID.

  ```python
  def get_api_key():
      return "your_elasticsearch_api_key_here"

  def get_cloud_id():
      return "your_elasticsearch_cloud_id_here"
  ```

### 2. Run the Application

Once the API keys are set up, you can start the Flask app by running the following command:

```bash
python user.py
```

This will launch the chatbot web application, where users can interact with the system to find courses.

## Data Scraping

The `data_scrape.py` script is responsible for scraping all relevant course data from the Princeton registrar's website. 

### Instructions:

- **Chrome Driver Setup:**  
  You need to replace the placeholder `'path_to_chrome_driver'` in the script with the actual path to your ChromeDriver executable.

- **Run the Script:**

  ```bash
  python data_scrape.py
  ```

- **Output:**  
  The script scrapes all course details and saves them in the file `course_details.json`.

## Data Indexing

We use Elasticsearch to index the scraped course data.

### Instructions:

- **Index the Data:**

  Run the `elastic_index.py` script to read the course JSON data from `course_details.json` and index it in your Elasticsearch cloud.

  ```bash
  python elastic_index.py
  ```

## Chatbot

The chatbot is implemented as a Flask web application. It integrates with OpenAI's GPT-4 API to interact with users and Elasticsearch to perform course searches.

### Key Components:

- **`user.py`:**  
  This script handles the Flask app's logic, processing user interactions, and coordinating API requests.

- **`chatbot.py`:**  
  Manages the communication with the OpenAI API, generating responses based on user inputs.

- **`elastic_search.py`:**  
  Handles search queries within Elasticsearch, retrieving courses that match the user's preferences.

### Frontend:

The web interface is served by the Flask app and uses the HTML template obtained from a public GitHub repository (username: wuup; [link](https://github.com/wuup/gpt4-chatbot)).
