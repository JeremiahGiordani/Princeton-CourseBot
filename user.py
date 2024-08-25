import chatbot
import elastic_search
import json
from pprint import pprint
from flask import Flask, render_template, request, jsonify
from markupsafe import Markup

app = Flask(__name__)

system_message = chatbot.get_system_message()

# Initialize messages list with the system message
messages = []
messages.append(system_message)

@app.route('/')
def index():
    system_message = chatbot.get_system_message()
    global messages
    # Reset messages list with the system message
    messages = []
    messages.append(system_message)
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    user_input = request.form['input']

    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)

    response = chatbot.get_response(messages)

    if 'json' in response.lower():
        query = parse_json(response)
        print("\n" + "-"*50 + "\n")
        print("This is the query")
        print(query)
        print("\n" + "-"*50 + "\n")

        # Perform the search using the extracted query
        courses = elastic_search.search(query)
        print("\n" + "-"*50 + "\n")
        print("These are the courses")
        print(courses)
        print("\n" + "-"*50 + "\n")

        while not courses:
            # add the response to the chat history
            chatbot_response = {"role": "assistant", "content": response}
            messages.append(chatbot_response)

            # add a system notice about how there were no courses
            system_notice = {"role": "system", "content": chatbot.get_system_message_no_course()}
            messages.append(system_notice)

            # get a new query
            response = chatbot.get_response(messages)
            query = parse_json(response)

            print("\n" + "-"*50 + "\n")
            print("This is the NEW query")
            print(query)
            print("\n" + "-"*50 + "\n")

            # search based on the new query
            courses = elastic_search.search(query)
            print("\n" + "-"*50 + "\n")
            print("These are the NEW courses")
            print(courses)
            print("\n" + "-"*50 + "\n")

        # create a system notice with the courses and append to the conversation history
        system_notice = {"role": "system", "content": chatbot.get_system_message_with_courses(courses)}
        messages.append(system_notice)

        # get generation
        response = chatbot.get_response(messages)

    chatbot_response = {"role": "assistant", "content": response}
    messages.append(chatbot_response)

    # return the response to the frontend
    if response.startswith("Error"):
        return jsonify({'response_type': 'error', 'response': Markup(response)})
    else:
        return jsonify({'response_type': 'success', 'response': Markup(response)})
    
def parse_json(response):
    try:
        # Extract the JSON part of the response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_string = response[json_start:json_end]

        # Parse the JSON
        courses_json = json.loads(json_string)

        query = courses_json.get("query", {})
        query = {"query": query}
        
        return query

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

if __name__ == '__main__':
    app.run(debug=True)

