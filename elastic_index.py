from elasticsearch import Elasticsearch
import json
import elastic_search_variables

client = Elasticsearch(cloud_id=elastic_search_variables.get_cloud_id(), api_key=elastic_search_variables.get_api_key())


# Create the index with the defined mapping
index_name = "courses"
print("Deleting index:")
print(client.indices.delete(index=index_name, ignore=[400, 404]))

print("\n" + "-"*50 + "\n")


# Define the mapping
mapping = {
    "mappings": {
        "properties": {
            "courseid": {
                "type": "keyword"
            },
            "department": {
                "type": "keyword"
            },
            "course name": {
                "type": "text",
                "analyzer": "standard"
            },
            "course code": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "distribution area": {
                "type": "keyword"  # No change needed; keyword supports arrays
            },
            "description": {
                "type": "text",
                "analyzer": "standard"
            },
            "assignments": {
                "type": "text",
                "analyzer": "standard"
            },
            "grading": {
                "type": "text",
                "analyzer": "standard"
            },
            "level": {
                "type": "text",
                "analyzer": "standard"
            }
        }
    }
}

print("Creating index")
print(client.indices.create(index=index_name, body=mapping))

print("\n" + "-"*50 + "\n")

# Load course details from the JSON file
with open("course_details.json", "r") as infile:
    course_details = json.load(infile)

total_courses = len(course_details)

# Index the processed course data with progress printing
for i, course in enumerate(course_details, start=1):
    client.index(index=index_name, document=course)
    print(f"Indexing course {i} / {total_courses}")

print("\n" + "-"*50 + "\n")
print("Total number of indexed courses")
print(client.count(index=index_name))