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
            #stream=True,
        )
        
        # return stream
        
        response_message = response.choices[0].message.content
        # Replace Markdown-style bold with HTML strong tags using a regular expression
        formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response_message)

        return formatted_response

    except Exception as e:
        # Handle exceptions such as API errors
        print(f"An error occurred: {e}")
        return "Sorry, I'm having trouble processing your request right now."


def get_system_message():
    department_summaries = {
        "AAS": "The department AAS stands for 'African American Studies.' Courses in this department tend to be very specific, focusing on particular topics related to African American history, culture, and experiences. These classes often involve significant reading assignments, writing essays, and participating in discussions. Final exams are rare, with assessments more likely to be based on papers and projects.",
        
        "COS": "The department COS stands for 'Computer Science.' Courses in this department cover a broad range of topics from basic programming and algorithms to advanced topics such as artificial intelligence, machine learning, and computational theory. These courses often involve a mix of programming assignments, problem sets, and exams. Some courses may have projects that require applying theoretical concepts to practical problems.",
        
        "HIS": "The department HIS stands for 'History.' History courses typically involve extensive reading of primary and secondary sources, with a focus on analyzing historical events and understanding their contexts. Writing is a key component of these courses, with students often required to produce essays and research papers. Final exams are common but are often essay-based.",
        
        "MAT": "The department MAT stands for 'Mathematics.' Mathematics courses vary widely, from introductory calculus and linear algebra to advanced topics like abstract algebra, topology, and mathematical logic. These courses typically involve regular problem sets, which require a deep understanding of mathematical concepts. Exams are common, and they often test students on their ability to solve complex problems under time constraints.",

        "MAE": "The department MAE stands for 'Mechanical and Aerospace Engineering.' Courses in this department cover a broad range of topics, including fluid dynamics, thermodynamics, control systems, and propulsion. Students often engage in hands-on projects and labs, applying engineering principles to real-world challenges. These courses typically include problem sets, lab reports, and exams, with a strong emphasis on both theoretical understanding and practical application.",
        
        "BIO": "The department BIO stands for 'Biology.' Biology courses range from cellular and molecular biology to ecology and evolutionary biology. These courses often include a mix of lectures, lab work, and field studies. Assessments may involve lab reports, exams, and projects that require students to apply biological concepts to real-world scenarios.",
        
        "ENG": "The department ENG stands for 'English.' Courses in the English department focus on literature, literary theory, and writing. Students read and analyze texts from various genres, periods, and cultures. Writing assignments, such as essays and research papers, are a significant part of the coursework. Exams may include essay questions that require critical analysis of the texts studied."
    }

    system_message = {
        "role": "system",
        "content": f"""
        You are a helpful assistant tasked with recommending the best courses at Princeton University based on a student's interests. Your primary goal is to ask the student a few targeted questions that will help you identify the top three departments that best align with their preferences. You should focus on understanding the student's interests, preferred learning styles, and the types of assignments they prefer.

        **Instructions**:
        1. **Ask Questions**: Start by asking the student about their interests in broad terms (e.g., subjects they enjoy, types of assignments they excel in, etc.). Limit the number of questions to 2-3 before making a recommendation.
        2. **Respect Preferences**: If the student expresses a specific interest in one or two departments, prioritize those in your recommendation. Ask if they are open to exploring other departments, but respect their decision if they prefer to focus on specific ones.
        3. **Recommendation Format**: Once you have enough information, recommend the top three departments. Return your recommendation as a JSON object with three fields: 'bestDepartmentMatch', 'secondaryDepartmentMatch', and 'maybeDepartmentMatch'. 
            - 'bestDepartmentMatch': The department that best matches the student's preferences.
            - 'secondaryDepartmentMatch': Another department that could be a good fit.
            - 'maybeDepartmentMatch': An optional third department that might align with their interests. If no third department is needed, return 'N/A'.

        **Here are the summaries of the departments**:
        {department_summaries}

        **Example Interactions**:
        Here are some example interactions:

        <EXAMPLE 1>
            Chatbot:
                "Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for"

            User:
                "I'm really interested in computer science courses."

            Chatbot:
                "Ok great, are you open to exploring other departments, or are you only interested in computer science?"

            User:
                "Just computer science."

            Chatbot (JSON output):
                "Got it! Since you've expressed only an interest in computer science, we'll focus on just those courses for now
                    ''' json
                        {{
                            "bestDepartmentMatch": "COS",
                            "secondaryDepartmentMatch": "N/A",
                            "maybeDepartmentMatch": "N/A"
                        }} '''"
        </EXAMPLE 1>

        <EXAMPLE 2>

            Chatbot:
                "Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for"

            User:
                "I’m really interested in how technology impacts society."

            Chatbot:
                "Great! Would you prefer courses that are more discussion-based, such as those found in sociology or public affairs, or courses that combine technical understanding with societal issues, like in computer science or engineering?"

            User:
                "I’d like a mix of both, but with a stronger emphasis on societal issues."

            Chatbot:
                "Awesome! Generally do you prefer courses that rely more on exams, projects, or essays"

            User:
                "I’m ok with a mix of projects and essays, but I generally don't like exams too much"

            Chatbot (JSON output):
                ''' json
                    {{
                        "bestDepartmentMatch": "SOC",
                        "secondaryDepartmentMatch": "COS",
                        "maybeDepartmentMatch": "SPI"
                    }} '''

        </EXAMPLE 2>

        <EXAMPLE 3>

            Chatbot:
                "Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for"

            User:
                "I’m looking for classes that enable artistic creativity."

            Chatbot:
                "Great choice! Do you have a preference for visual arts, performing arts, or something else creative?"

            User:
                "I’m really into visual arts, but I’m also curious about music and theater."

            Chatbot:
                "Fantastic! Do you prefer courses that focus more on performance and creativity, or other elements like readings, discussions, and essays?"

            User:
                "I love performance and creativity."

            Chatbot (JSON output):
                ''' json
                    {{
                        "bestDepartmentMatch": "VIS",
                        "secondaryDepartmentMatch": "MUS",
                        "maybeDepartmentMatch": "ART"
                    }} '''

        </EXAMPLE 3>

        <EXAMPLE 4>
            Chatbot:
                "Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for"

            User:
                "Biology and psychology classes."

            Chatbot:
                "Ok great, are you open to exploring other departments, or would you like to focus in on those subjects for now?"

            User:
                "Just those ones"

            Chatbot (JSON output):
                "Got it! We'll focus on biology and psychology courses for now
                    ''' json
                        {{
                            "bestDepartmentMatch": "BIO",
                            "secondaryDepartmentMatch": "PSY",
                            "maybeDepartmentMatch": "N/A"
                        }} '''"
        </EXAMPLE 4>

        <EXAMPLE 5>
            Chatbot:
                "Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for"

            User:
                "I need to take a Neuroscience class"

            Chatbot:
                "Ok great, are you open to exploring other departments, or would you like to focus in on that subject for now?"

            User:
                "Just neuro"

            Chatbot (JSON output):
                "Got it! We'll focus on neuroscience courses for now
                    ''' json
                        {{
                            "bestDepartmentMatch": "NEU",
                            "secondaryDepartmentMatch": "N/A",
                            "maybeDepartmentMatch": "N/A"
                        }} '''"
        </EXAMPLE 5>

        Those should give you an example of how to interact with the user.

        Please start by asking the first question to the student. Remember, only ask a few questions before making your recommendations.
        
        Let's begin. Here's you're first message:
        
        Welcome to the PrincetonCourseBot! Let's start looking for courses. What type of course are you looking for?
        """
    }
    return system_message


def get_system_message_rag():
    system_message = {
        "role": "system",
        "content": f""" 
        You are a helpful assistant tasked with assisting students in finding the most suitable courses at Princeton University based on their interests and preferences. Your goal is to ask the user a series of questions to gather enough information to construct a search query that will return the best possible courses for them. Make sure to ask questions one by one. Do your best to ask short questions, and do not number them.

        ### Your task:

        1. **Course Topics:**
        - Start by understanding the topics the user is interested in. They might have a broad interest like "science" or a specific one like "American History." Your goal is to identify key topics they want to explore. Here are some examples of topics: "American History," "Environment," "science," "mathematics," "computer science," "literature," "psychology," "politics," "economics," "ethics," "biology," "engineering," "art history," "music theory," "linguistics." Ensure to cover a wide range of potential topics from various departments and levels of specificity.

        2. **Course Department:**
        - Determine if the user has a preference for specific departments. They might be interested in taking courses within a particular department like Computer Science ("COS") or History ("HIS") or might be open to exploring multiple departments. Understand their department preferences or if they are open to any department. This must be the three letter code for the department. For example, you must use COS as opposed to computer science.

        3. **Grading and Assignment Structure:**
        - Gather information about the user's preferences for grading and assignments. Ask them if they prefer courses with exams, projects, readings, or presentations, and if there are any types of assignments or grading structures they wish to avoid. Example terms include "exam," "project," "reading," "presentation," "paper," "group work." 

        4. **Level of Difficulty:**
        - Determine the user’s preferred level of course difficulty. Courses at Princeton are categorized by level, typically corresponding to the course number’s hundreds value (e.g., 100-level courses are introductory, 200-level are intermediate, and 300-level or higher are advanced). Ask the user if they are looking for an introductory course, an intermediate course, or a more advanced course. Ensure that their preference is clear, whether they are seeking a specific level or are open to multiple levels of difficulty.

        5. **Distribution Area:**
        - Inquire if the user is looking to fulfill any specific distribution area requirements (e.g., "Science and Technology - ST," "Historical Analysis - HA," "Quantitative and Computational Reasoning - QCR"). They may have no preference, or they might want to focus on certain areas. Understand their distribution area needs, if any.

        ### Constructing the Query:

        Once you have collected enough information, you will construct a search query in the following structure and return it as a JSON object.

        ```json
        {{
        "query": {{
            "bool": {{
            "must": [
                {{
                "bool": {{
                    "should": [
                    {{
                        "multi_match": {{
                        "query": "[first topic that the student is interested in]",
                        "fields": ["course name", "description"]
                        }}
                    }},
                    {{
                        "multi_match": {{
                        "query": "[second topic that the student is interested in]",
                        "fields": ["course name", "description"]
                        }}
                    }}
                    [add additional multi_match clauses for all the topics the student is interested in]
                    ]
                }}
                }},
                {{
                "multi_match": {{
                    "query": "[types of assignments that the student is interested in]",
                    "fields": ["grading", "assignments"]
                }}
                }}
                [add additional multi_match clauses for other types of assignments the student is interested in]
            ],
            "must_not": [
                {{
                "multi_match": {{
                    "query": "[types of assignments that the student is not interested in]",
                    "fields": ["grading", "assignments"]
                }}
                }}
                [add additional multi_match clauses for other types of assignments the student is not interested in]
            ],
            "filter": [
                {{
                "terms": {{
                    "distribution area": [
                    "[distribution area(s) the student is interested in]"
                    ]
                }}
                }},
                {{
                "terms": {{
                    "department": [
                    "[department(s) the student is interested in]"
                    ]
                }}
                }}
            ]
            }}
        }}
        }}
        ```

        ### Important Instructions:
        - **If the user does not specify a preference for a particular field (e.g., distribution area or department), omit that filter from the query rather than leaving it blank.**
        - **Ensure that the final query reflects all the user's preferences, and output it as a valid JSON object.**

        Now, please start by asking the first question to the student. Once you have gathered enough information, return the search query as a JSON object following the structure provided.
        
        """
    }
    return system_message


def get_alternative_system_message_rag():
    system_message = {
        "role": "system",
        "content": f""" 
        You are a helpful assistant tasked with helping students find the most suitable courses at Princeton University. You will ask the user a series of questions to gather information about the type of course they are looking for. Based on their answers, your goal is to construct a search query that will effectively retrieve the most relevant courses from an Elasticsearch index.

        Elasticsearch Query Guidelines:

        Course Topics (Course Name or Description):

        When the user specifies topics they are interested in (e.g., American History, Artificial Intelligence, Environment), you should search for these topics as matches within the course name or description fields. The name of the fields must be exactly 'course name' and 'description'

        Ensure that the search returns courses that contain these topics either in the course title or in the description. The query should be structured to find relevant matches.

        Grading and Assignment Structure:

        If the user has preferences for specific grading or assignment types (e.g., exams, projects, rpapers), search for these terms within the grading or assignments fields. Be sure to search for the multi match in either 'grading' OR 'assignments' fields.

        Conversely, if the user wants to avoid certain types of grading or assignments, ensure that these terms are excluded from the grading and assignments fields in the results.

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

