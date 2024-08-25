from elasticsearch import Elasticsearch
import json
import elastic_search_variables

client = Elasticsearch(cloud_id=elastic_search_variables.get_cloud_id(), api_key=elastic_search_variables.get_api_key())

index_name = "courses"

def search(query):
        # Perform the search using the extracted query
    search_results = client.search(index="courses", body=query)
    
    # Initialize a string to store the results
    results_string = ""

    # Iterate over the search results and append them to the results_string
    for hit in search_results['hits']['hits']:
        course_details = hit["_source"]
        
        # Format course details into a readable string format
        course_info = f"Course ID: {course_details.get('courseid', 'N/A')}\n"
        course_info += f"Course Name: {course_details.get('course name', 'N/A')}\n"
        course_info += f"Department: {course_details.get('department', 'N/A')}\n"
        course_info += f"Course Code: {course_details.get('course code', 'N/A')}\n"
        course_info += f"Distribution Area: {course_details.get('distribution area', 'N/A')}\n"
        course_info += f"Description: {course_details.get('description', 'N/A')}\n"
        course_info += f"Assignments: {course_details.get('assignments', 'N/A')}\n"
        course_info += f"Grading: {course_details.get('grading', 'N/A')}\n"
        course_info += "-" * 40 + "\n"  # Separator for readability
        
        # Append the formatted course info to the results_string
        results_string += course_info
    
    return results_string