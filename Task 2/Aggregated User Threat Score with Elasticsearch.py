import csv
import os
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import unittest

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "threat_scores"

# Step 1: Create Elasticsearch index with mappings
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        mappings = {
            "mappings": {
                "properties": {
                    "department": {"type": "keyword"},
                    "user_id": {"type": "integer"},
                    "score": {"type": "float"}
                }
            }
        }
        es.indices.create(index=INDEX_NAME, body=mappings)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

# Step 2: Generate random data and save to CSV
def generate_and_save_data():
    csv_file = "threat_scores.csv"
    if not os.path.exists(csv_file):
        data = []
        departments = ["Engineering", "Marketing", "Finance", "HR", "Science"]
        for department in departments:
            for user_id in range(np.random.randint(10, 200)):
                score = np.random.uniform(0, 90)  # Generate random scores
                data.append([department, user_id, score])

        # Save data to CSV
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["department", "user_id", "score"])
            writer.writerows(data)
        print("Data saved to CSV.")
    else:
        print("CSV file already exists.")

# Step 3: Populate Elasticsearch index from CSV
def populate_index_from_csv():
    csv_file = "threat_scores.csv"
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            actions = [
                {
                    "_index": INDEX_NAME,
                    "_source": {
                        "department": row["department"],
                        "user_id": int(row["user_id"]),
                        "score": float(row["score"])
                    }
                }
                for row in reader
            ]
        bulk(es, actions)
        print("Elasticsearch index populated.")
    else:
        print("CSV file not found. Generate data first.")

# Step 4: Read data from Elasticsearch for calculations
def fetch_department_scores():
    query = {
        "size": 10000,
        "query": {
            "match_all": {}
        }
    }
    results = es.search(index=INDEX_NAME, body=query)
    data = {}
    for hit in results["hits"]["hits"]:
        department = hit["_source"]["department"]
        score = hit["_source"]["score"]
        if department not in data:
            data[department] = []
        data[department].append(score)
    return data

def aggregated_threat_score_from_es():
    department_scores = fetch_department_scores()
    aggregated_scores = []

    for department, scores in department_scores.items():
        mean_threat = np.mean(scores)
        variance_threat = np.var(scores)
        aggregated_scores.append(mean_threat + variance_threat)

    aggregated_score = np.mean(aggregated_scores)
    return min(max(0, int(aggregated_score)), 90)

# Tests
class TestWithElasticsearch(unittest.TestCase):
    def setUp(self):
        create_index()
        generate_and_save_data()
        populate_index_from_csv()

    # All departments has similar threat scores
    def test_similar_threat_score(self):
        departments = [
            {'users': np.random.uniform(30, 50, 30)},
            {'users': np.random.uniform(30, 50, 30)},
            {'users': np.random.uniform(30, 50, 30)}
        ]
        score = aggregated_threat_score_from_es()
        print(f"Test Similar Threat Score: Computed Score = {score}")
        self.assertTrue(30 <= score <= 50)

    # One department has a high threat score(outlier)
    def test_outlier_department(self):
        departments = [
            {'users': np.random.uniform(10, 20, 30)},
            {'users': np.random.uniform(10, 20, 30)},
            {'users': np.random.uniform(70, 90, 30)}
        ]
        score = aggregated_threat_score_from_es()
        print(f"Test Outlier Department: Computed Score = {score}")
        self.assertTrue(score > 50)

    # Users with really high scores inside one of the departments (other departments have a low score)
    def test_outlier_users(self):
        departments = [
            {'users': np.random.uniform(10, 20, 30)},
            {'users': np.random.uniform(10, 20, 30)},
            {'users': np.append(np.random.uniform(10, 20, 25), [90, 90, 90, 90, 90])}  # five users with high score
        ]
        score = aggregated_threat_score_from_es()
        print(f"Test Outlier Users: Computed Score = {score}")
        self.assertTrue(70 <= score <= 90)

    # Departments with varying numbers of users
    def test_varying_users_amount(self):
        departments = [
            {'users': np.random.uniform(60, 90, 10)},
            {'users': np.random.uniform(30, 50, 200)},
            {'users': np.random.uniform(40, 60, 20)}
        ]
        score = aggregated_threat_score_from_es()
        print(f"Test Varying Users Amount: Computed Score = {score}")
        self.assertTrue(score >= 70)

if __name__ == "__main__":
    unittest.main()
