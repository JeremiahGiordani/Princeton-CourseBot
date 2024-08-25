from elasticsearch import Elasticsearch
import json
import elastic_search_variables

# Connect to your Elasticsearch cluster
client = Elasticsearch(cloud_id=elastic_search_variables.get_cloud_id(), api_key=elastic_search_variables.get_api_key())

index_name = "courses"

def pretty_print(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

def search_by_department(department):
    query = {
        "query": {
            "term": {
                "department": department
            }
        }
    }
    results = client.search(index=index_name, body=query)
    print(f"Search results for department '{department}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")


def search_by_department_and_distribution(department, distribution_area):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"department": department}},
                    {"term": {"distribution area": distribution_area}}
                ]
            }
        }
    }
    results = client.search(index=index_name, body=query)
    print(f"Search results for department '{department}' with distribution area '{distribution_area}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")


def full_text_search(field, text):
    query = {
        "query": {
            "match": {
                field: text
            }
        }
    }
    results = client.search(index=index_name, body=query)
    print(f"Full-text search results for '{text}' in field '{field}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")

def full_text_multi_search(field_one, field_two, text):
    query = {
        "query": {
            "multi_match": {
                "query": text,
                "fields": [field_one, field_two]
            }
        }
    }

    results = client.search(index=index_name, body=query)
    print(f"Full-text search results for '{text}' in fields '{field_one}' and '{field_two}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")


def full_text_exclusion_search(field_one, field_two, include_text, exclude_text):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {
                        "query": include_text,
                        "fields": [field_one, field_two]
                    }}
                ],
                "must_not": [
                    {"multi_match": {
                        "query": exclude_text,
                        "fields": [field_one, field_two]
                    }}
                ]
            }
        }
    }

    results = client.search(index=index_name, body=query)
    print(f"Search results for '{include_text}' in fields '{field_one}' and '{field_two}', excluding '{exclude_text}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")


def department_and_text_search(department, field_one, field_two, text):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"department": department}},
                    {"multi_match": {
                        "query": text,
                        "fields": [field_one, field_two]
                    }}
                ]
            }
        }
    }

    results = client.search(index=index_name, body=query)
    print(f"Search results for '{text}' in fields '{field_one}' and '{field_two}' within department '{department}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")


def complex_search(text, no_final_exam, requirement):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"course name": text}},
                    {"term": {"distribution area": requirement}},
                    {"terms": {"department": ["AAS"]}},
                    {"multi_match": {
                        "query": "final project",
                        "fields": ["assignments", "grading"]
                    }},
                ],
                "must_not": [
                    {"multi_match": {
                        "query": "exam",
                        "fields": ["assignments", "grading"]
                    }},
                ]
            }
        }
    }

    results = client.search(index=index_name, body=query)
    print(f"Complex search results for '{text}' with no '{no_final_exam}' and satisfying requirement '{requirement}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")

def complex_search_working(text, no_final_exam, requirement):
    query = {
        "query": {
            "bool": {
                "must": [
                    # {"match": {"course name": text}},
                    # {"match": {"description": text}},
                    {"multi_match": {
                        "query": "final project",
                        "fields": ["assignments", "grading"]
                    }},
                    {"multi_match": {
                        "query": text,
                        "fields": ["course name", "description"]
                    }},
                    # {"multi_match": {
                    #     "query": "humanities",
                    #     "fields": ["course name", "description", "department"]
                    # }},
                ],
                # "should": [
                #     {"terms": {"department": ["AAS", "AFS"]}},
                # ],
                "must_not": [
                    {"match": {"grading": "exam"}},
                ],
                "filter": [
                    {"term": {"distribution area": requirement}},
                    {"terms": {"department": ["AAS", "AFS"]}},
                ],
            }
        }
    }
    query = {'query': {'bool': {'must': [{'bool': {'should': [{'multi_match': {'query': 'computer science', 'fields': ['course name', 'description']}}]}}, {'multi_match': {'query': 'project', 'fields': ['grading', 'assignments']}}], 'must_not': [{'multi_match': {'query': 'exam', 'fields': ['grading', 'assignments']}}], 'filter': [{'terms': {'department': ['COS']}}]}}}
    results = client.search(index=index_name, body=query)
    print(f"Complex search results for '{text}' with no '{no_final_exam}' and satisfying requirement '{requirement}':")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")

def test_search_prompt(text, no_final_exam, requirement):
    query = {
        # "query": {
        #     "bool": {
        #         "must": [
        #             {
        #                 "bool": {
        #                     "should": [
        #                     {
        #                         "multi_match": {
        #                             "query": "science",
        #                             "fields": ["course name", "description"]
        #                         }
        #                     },
        #                     {
        #                         "multi_match": {
        #                             "query": "technology",
        #                             "fields": ["course name", "description"]
        #                         }
        #                     }
        #                     ]
        #                 }
        #             },
        #             {
        #                 "multi_match": {
        #                     "query": "exam",
        #                     "fields": ["grading", "assignments"]
        #                 }
        #             },
        #             {
        #                 "multi_match": {
        #                     "query": "project",
        #                     "fields": ["grading", "assignments"]
        #                 }
        #             }
        #         ],
        #         "must_not": [
        #             # {
        #             #     "multi_match": {
        #             #         "query": "project",
        #             #         "fields": ["grading", "assignments"]
        #             #     }
        #             # }
        #         ],
        #         "filter": [
        #             # {"terms": {"distribution area": ["COS"]}},
        #             # {"terms": {"department": ["QCR"]}},
        #         ]
        #     }
        # }
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

    query = {'query': {'bool': {'must': [{'bool': {'should': [{'multi_match': {'query': 'science', 'fields': ['course name', 'description']}}]}}, {'multi_match': {'query': 'project', 'fields': ['grading', 'assignments']}}], 'filter': [{'terms': {'department': ['COS']}}]}}}

    query = {'query': {'bool': {'must': [{'multi_match': {'query': 'introduction', 'fields': ['course name', 'description']}}, {'term': {'department': 'COS'}}]}}}

    results = client.search(index=index_name, body=query)
    print("Testing the query")
    for hit in results['hits']['hits']:
        pretty_print(hit["_source"])
    print("\n")

if __name__ == "__main__":
    # Test 1: Search by department
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")
    # print("Test 1")
    # search_by_department("COS")
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")

    # Test 2: Search by department and distribution area
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")
    # print("Test 2")
    # search_by_department_and_distribution("GHP", "SA")
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")

    # Test 3: Full-text search in course name
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")
    # print("Test 3")
    # full_text_multi_search("course name", "description", "Intro to Computer Science")
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")
    # # Test 4: Full-text search in description
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")
    # print("Test 4")
    # full_text_multi_search("course name", "description", "machine learning")
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")

    # Test 5: Full-text search in assignments
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")
    # print("Test 5")
    # full_text_search("assignments", "final project")
    # print("\n" + "-"*50 + "\n")
    # print("\n" + "-"*50 + "\n")

    # Test 6: Search for "final project" but exclude "final exam"
    # print("=" * 50)
    # print("Test 6")
    # full_text_exclusion_search("assignments", "grading", "final project", "final exam")

    # # Test 7: Search for "Introduction to Computer Science" in COS department
    # print("=" * 50)
    # print("Test 7")
    # department_and_text_search("COS", "course name", "description", "Introduction to Computer Science")

    # # Test 8: Search for courses matching text, no final exam, and satisfying QCR requirement
    print("=" * 50)
    print("Test 8")
    test_search_prompt("African American Studies", "final exam", "CD")

    # test_distribution_area_query("CD")

    # search_by_department_and_distribution("AAS", "CD")