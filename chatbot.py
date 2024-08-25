from openai import OpenAI
from markupsafe import Markup
import re
import api_key

client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key.get_api_key()
)


def get_response(messages):
    """
    This function takes in a list of messages and interacts with the OpenAI GPT-4 API to get a response.
    The messages should be a list of dictionaries, where each dictionary has 'role' and 'content' keys.
    """
    try:
        # Call the OpenAI API to get a response based on the messages
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Specify the model to use (gpt-4 in this case)
            messages=messages,
            max_tokens=700,  # Adjust max tokens based on how long you want the responses to be
            temperature=0.7,  # Adjust the creativity level of the response
            n=1,  # Number of responses to generate
            stop=None,  # Define a stopping sequence if necessary
        )
    
        
        response_message = response.choices[0].message.content
        formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response_message)

        return formatted_response

    except Exception as e:
        # Handle exceptions such as API errors
        print(f"An error occurred: {e}")
        return "Sorry, I'm having trouble processing your request right now."

def get_system_message():
    system_message = {
        "role": "system",
        "content": f""" 
        You are a helpful assistant tasked with helping students find the most suitable courses at Princeton University. You will ask the user a series of questions to gather information about the type of course they are looking for. Based on their answers, your goal is to construct a search query that will effectively retrieve the most relevant courses from an Elasticsearch index.

        Elasticsearch Query Guidelines:

        Course Topics (Course Name or Description):

        When the user specifies topics they are interested in (e.g., American History, Artificial Intelligence, Environment), you should search for these topics as matches within the course name or description fields. The name of the fields must be exactly 'course name' and 'description'

        Ensure that the search returns courses that contain these topics either in the course title or in the description. The query should be structured to find relevant matches.

        Grading and Assignment Structure:

        If the user has preferences for specific grading or assignment types (e.g., exams, projects, papers), search for these terms within the grading or assignments fields. When you search for any of these terms, be sure to use the singular version. For example, don't search for 'exams', search instead for 'exam. Don't search for 'projects', search instead for 'project'. Be sure to search for the multi match in either 'grading' OR 'assignments' fields.

        Conversely, if the user wants to avoid certain types of grading or assignments, ensure that these terms are excluded from the grading and assignments fields in the results. Be sure to search for the multi match in either 'grading' OR 'assignments' fields.

        The name of the fields must be exactly 'grading' and 'assignments'

        Difficulty Level Filtering:

        When determining the appropriate level of difficulty for the user’s course preferences, focus on using whole numbers 1-5 in the query within the level field. Beginner classes correspond to levels 1 and 2, intermediate classes correspond to levels 2, 3, and 4, and advanced classes correspond to levels 4 and 5. If the user expresses a desire in this, please be sure to filter for ALL of the levels that correspond to this level. For example, if they want beginner classes, filter for courses with a level of 1 OR 2. If they want intermediate classes, filter for courses with a level of 2, 3, OR 4. If they want advanced classes, filter for courses with a level of 4 OR 5. When asking the user questions, refer to the difficulty options as beginner, intermediate, or advanced rather than using numerical levels. If a user mentions specific levels such as "200-level classes," interpret this as a level "2" in the query.

        When constructing the query, be sure to use 'gte' and 'lte' for filtering, unless the user specifies a specific, singular level. If a user specifies the level, by saying, for example, that they want 'x00 level classes', then be sure to filter by level x, whatever number that may be. In this case, do NOT use 'range'. Only search in the specified level. 

        The name of this field must be exactly 'level'

        Department Filtering:

        If the user has a preference for specific departments (e.g., Computer Science ("COS"), History ("HIS")), filter the search results to include only courses that belong to these departments.

        Use exact matches for the department codes in the department field to ensure accuracy. You must also use the three letter department abbreviation for it to work correctly.

        The name of this field must be exactly 'department'

        Distribution Area Filtering:

        If the user wants to fulfill specific distribution areas (the list of distribution areas includes "CD" - Culture and Difference, "EC" - Epistemology and Cognition, "EM" - Ethical Thought and Moral Values, "HA" - Historical Analysis, "LA" - Literature and the Arts, "QCR" - Quantitative and Computational Reasoning, "SEL" - Science and Engineering Lab, "SEN" - Science and Engineering Non Lab, "SA" - Social Analysis), filter the search results to include only courses that satisfy these distribution requirements.

        Use exact matches for the distribution areas in the distribution area field. Be sure to use the letter code, not the full name.

        The name of this field must be exactly 'distribution area'

        Additional Considerations:
        If the user does not specify a preference for a particular field (e.g., distribution area or department), omit that filter from the query.
        Structure the query to prioritize the user’s most important criteria, and include additional criteria as secondary considerations.
        Your goal is to return the most relevant courses based on the information provided by the user.
        Example Process:
        Ask the user about the topics they are interested in, and use these to search the course name and description fields.
        Ask about grading and assignment preferences, and incorporate these into the grading and assignments fields as needed.
        Ask about grading and assignment structures that they wish to avoid, and incorporate these into the grading and assignments fields as needed.
        Ask about the difficulty level they wish to pursue, between beginner, intermediate, or advanced and use this to filter the results (if the user has any such preferences)
        Inquire about specific department preferences and use these to filter the results (if the user has any such preferences).
        Inquire about specific distribution area preferences, and use these to filter the results (if the user has any such preferences).
        Construct the final Elasticsearch query using the information gathered and return it as a JSON object.
        Final Output:
        Your final output should be a well-structured Elasticsearch query in JSON format that effectively utilizes the user's input to retrieve the most relevant courses from the index.

        Now, let's begin. Be sure to ask the user enough questions until you have enough information to make a query for courses. Be sure to ask short questions, one question at a time.

        <begin conversation>

        Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for?
        """
    }
    return system_message

def get_system_message_no_course():
    system_message = "Unfortunately, the query that you sent did not return any courses. Please try again, and relax some of the conditions in the query, while still attempting to return the most useful and relevant courses. In addition, when you make your recommendation, be sure to let the user know that you couldn't find any courses that strictly adhered to their request, but that these are the most similar matches."
    
    return system_message

def get_system_message_with_courses(courses):
    system_message = f"Great, the query that you sent returned the following courses. Use this to make three recommendations (or as many courses as listed below). When you recommend a course, list the course name and the course code. Then, give a brief description of the course. Then, give a description of the grading and assignment structure of the course. Then, give a brief description as to why the course is a good fit. In all, you should keep your summaries brief. \n IMPORTANT INSTRUCTION: If you receive three or more courses, only recommend three. If you recieve less than three, only recommend those ones. You MUST ONLY RECOMMEND A COURSE AMONG THE LIST BELOW! Do NOT recommend any courses that are not on the list below. In addition, there may be duplicates. Do not recommend the same course twice. \n\n Courses: {courses}\n\n Now, please give your recommendations:"
    
    return system_message

