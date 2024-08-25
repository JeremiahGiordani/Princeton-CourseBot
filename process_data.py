import json

def preprocess_course_data(course_data):
    for course in course_data:
        # Split the 'distribution area' field into a list of values
        if 'distribution area' in course:
            course['distribution area'] = [area.strip() for area in course['distribution area'].split(' or ')]
    return course_data


# Load course details from the JSON file
with open("course_details.json", "r") as infile:
    course_details = json.load(infile)

course_details = preprocess_course_data(course_details)

# Save the data to a JSON file
with open("course_details.json", "w") as outfile:
    json.dump(course_details, outfile, indent=4)  # indent=4 makes the JSON file pretty-printed for readability