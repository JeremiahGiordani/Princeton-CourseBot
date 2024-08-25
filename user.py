import chatbot
import elastic_search
import json
from pprint import pprint
from flask import Flask, render_template, request, jsonify
from markupsafe import Markup

app = Flask(__name__)

system_message = chatbot.get_alternative_system_message_rag()

# Initialize messages list with the system message
messages = []
messages.append(system_message)


# Print the initial welcome message to the user
# print("Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for?")

@app.route('/')
def index():
    system_message = chatbot.get_alternative_system_message_rag()
    global messages
    # Initialize messages list with the system message
    messages = []
    messages.append(system_message)
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    user_input = request.form['input']

    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)
    # print("\n" + "-"*50 + "\n")  # Add a separator
    # for message in messages:
    #     pprint(message)
    # print("\n" + "-"*50 + "\n")

    response = chatbot.get_response(messages)
    # print("\n" + "-"*50 + "\n")
    # print(response)
    # print("\n" + "-"*50 + "\n")
    if 'json' in response.lower():
        print("JSON DETECTED")
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

        additional_notice = "None"

        # if not courses:
        #     query = remove_filters(query)
        #     additional_notice = "There are no courses in the particular department (if specified) and requirement (if specified) that the user is looking for. Be sure to let them know, before recommending courses that you were unable to find courses filtered based on either of these, if they provided them."
        #     courses = elastic_search.search(query)
        
        # if not courses:
        #     query = remove_must_not(query)
        #     additional_notice += " In addition, there are no courses based on the specification from the user that excluded the types of assignments and grading that they were looking for. Be sure to let them know, before recommending courses that you were unable to find courses filtered based on the assignment and grading structure that they were looking for."
        #     courses = elastic_search.search(query)

        while not courses:
            chatbot_response = {"role": "assistant", "content": response}
            messages.append(chatbot_response)
            system_notice = {"role": "system", "content": "Unfortunately, the query that you sent did not return any courses. Please try again, and relax some of the conditions in the query, while still attempting to return the most useful and relevant courses. In addition, when you make your recommendation, be sure to let the user know that you couldn't find any courses that strictly adhered to their request, but that these are the most similar matches."}
            messages.append(system_notice)
            response = chatbot.get_response(messages)
            query = parse_json(response)
            print("\n" + "-"*50 + "\n")
            print("This is the NEW query")
            print(query)
            print("\n" + "-"*50 + "\n")
            courses = elastic_search.search(query)
            print("\n" + "-"*50 + "\n")
            print("These are the NEW courses")
            print(courses)
            print("\n" + "-"*50 + "\n")

        system_notice = {"role": "system", "content": f"Great, the query that you sent returned the following courses. Use this to make three recommendations (or as many courses as listed below). When you recommend a course, list the course name and the course code. Then, give a brief description of the course. Then, give a description of the grading and assignment structure of the course. Then, give a brief description as to why the course is a good fit. In all, you should keep your summaries brief. \n IMPORTANT INSTRUCTION: If you receive three or more courses, only recommend three. If you recieve less than three, only recommend those ones. You MUST ONLY RECOMMEND A COURSE AMONG THE LIST BELOW! Do NOT recommend any courses that are not on the list below. In addition, there may be duplicates. Do not recommend the same course twice. \n\n Courses: {courses}\n\n Now, please give your recommendations:"}
        messages.append(system_notice)

        response = chatbot.get_response(messages)

        # # Remove the first list element from 'messages'
        # messages.pop(0)

        # # New system message
        # initial_system_message = {
        #     "role": "system",
        #     "content": (
        #         f"You are a helpful assistant, helping students find courses that align with their interests and goals. You will be provided with a list of courses that may be suitable for the student. You will ask a series of questions to narrow down the recommended courses. Once you have asked enough questions that you feel like you can make a recommendation, you will recommend three courses that you feel would be the most suitable, listing the course name and the course code. Then you will give a brief description of the course. Then, you will give some details on the grading and assignments in the course. Then you will explain why the course would be a good fit for the student. These should all be brief. \n\n Here is a list of courses that the user might be interested in: {courses}\n\n In addition, there may be some additional notices: {additional_notice}\n\n Now, we'll begin. <begin conversation> \n\n Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for?"
        #     )
        # }
        # # print(initial_system_message)

        # # Prepend the new system message to the 'messages' list
        # messages.insert(0, initial_system_message)

        # # Get the new response from the chatbot
        # response = chatbot.get_response(messages)

    chatbot_response = {"role": "assistant", "content": response}
    messages.append(chatbot_response)
    # print(messages)

    # print("\n" + "-"*50 + "\n")  # Add a separator
    # for message in messages:
    #     pprint(message)
    # print("\n" + "-"*50 + "\n")  # Add a separator

    if response.startswith("Error"):
        return jsonify({'response_type': 'error', 'response': Markup(response)})
    else:
        return jsonify({'response_type': 'success', 'response': Markup(response)})

def remove_filters(query):
    # Check if the query has the expected structure
    if "query" in query and "bool" in query["query"]:
        # Access the 'bool' section
        bool_query = query["query"]["bool"]
        
        # Replace the 'filter' field with an empty list if it exists
        if "filter" in bool_query:
            bool_query["filter"] = []
    
    # Return the modified query
    return query

def remove_must_not(query):
    # Check if the query has the expected structure
    if "query" in query and "bool" in query["query"]:
        # Access the 'bool' section
        bool_query = query["query"]["bool"]
        
        # Replace the 'filter' field with an empty list if it exists
        if "filter" in bool_query:
            bool_query["must_not"] = []
    
    # Return the modified query
    return query
    
def parse_json(response):
    try:
        # Extract the JSON part of the response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_string = response[json_start:json_end]

        # Parse the JSON
        courses_json = json.loads(json_string)

        # Extract the department codes into a list
        # department_codes = [
        #     department_data.get("query"),
        # ]
        # Extract the query from the JSON response
        query = courses_json.get("query", {})
        query = {"query": query}
        

        # Filter out any 'N/A' values from the list
        # department_codes = [code for code in department_codes if code != "N/A"]

        # print("Extracted department codes:", department_codes)
        # return department_codes
        return query

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)


def load_course_details_for_departments(departments, file_path='course_details.json'):
    try:
        with open(file_path, 'r') as file:
            all_courses = json.load(file)
            # Filter courses that match the selected departments
            filtered_courses = [course for course in all_courses if course["department"] in departments]
            return filtered_courses
    except FileNotFoundError as e:
        print("Error: Course details file not found.", e)
        return []
    except json.JSONDecodeError as e:
        print("Error decoding course details JSON.", e)
        return []

if __name__ == '__main__':
    app.run(debug=True)

