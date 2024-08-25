import json

# Load your course JSON data
with open('course_details.json', 'r') as file:
    course_data = json.load(file)

# Function to determine the level based on the course code
def extract_level(course_code):
    # Extract the level as the fifth character in the course code (the hundreds value)
    level = None
    # Since some courses have multiple codes, we take the first one to determine the level
    if course_code:
        first_course_code = course_code.split(';')[0].strip()
        if len(first_course_code) >= 5 and first_course_code[4].isdigit():
            level = int(first_course_code[4])
    return level

# Iterate through each course and add the level field
for course in course_data:
    course_code = course.get('course code', '')
    course['level'] = f"{extract_level(course_code)}"

# Save the updated course data back to the JSON file
with open('course_details.json', 'w') as file:
    json.dump(course_data, file, indent=4)

print("Course levels have been successfully added to the JSON file.")
