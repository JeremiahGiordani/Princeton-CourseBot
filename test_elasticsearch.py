from elasticsearch import Elasticsearch
import json
import elastic_search_variables

# Connect to your Elasticsearch cluster
client = Elasticsearch(cloud_id=elastic_search_variables.get_cloud_id(), api_key=elastic_search_variables.get_api_key())

index_name = "courses"

def pretty_print(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

def test_search_prompt():
    query = {
        "query": {
        "bool": {
            "must": [
                {
                    "bool": {
                        "should": [
                            {
                                "multi_match": {
                                    "query": "biological sciences",
                                    "fields": ["course name", "description"]
                                }
                            },
                            {
                                "multi_match": {
                                    "query": "technology and society",
                                    "fields": ["course name", "description"]
                                }
                            }
                        ]
                    }
                },
                {
                    "multi_match": {
                        "query": "project",
                        "fields": ["grading", "assignments"]
                    }
                }
            ],
            "must_not": [
                {
                    "multi_match": {
                        "query": "exam",
                        "fields": ["grading", "assignments"]
                    }
                }
            ],
            "filter": [
                {
                    "terms": {
                        "department": [
                            "SPI",
                            "COS"
                        ]
                    }
                }
            ]
        }
    }
    }

    results = client.search(index=index_name, body=query)
    print("Testing the query")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")

if __name__ == "__main__":
    # test the provided query
    print("=" * 50)
    print("Test 8")
    test_search_prompt()