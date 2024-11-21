import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def aggregated_threat_score(departments):
    department_scores = []

    # Calculating threat score of each department and normalizing it based on department size(users amount)
    for department in departments:
        users = department['users']
        mean_threat = np.mean(users)
        variance_threat = np.var(users)

        department_scores.append(mean_threat + variance_threat)

    # Normalization the aggregated score (range 0 - 90)
    aggregated_score = np.mean(department_scores)
    return min(max(0, int(aggregated_score)), 90)


#Tests
class Test(unittest.TestCase):

    # All departments has similar threat scores
    def test_similar_threat_score(self):
        departments = [
            {'users': generate_random_data(40, 5, 30)},
            {'users': generate_random_data(37, 5, 30)},
            {'users': generate_random_data(43, 5, 30)}
        ]
        score = aggregated_threat_score(departments)
        print(f"Test Similar Threat Score: Computed Score = {score}")
        self.assertTrue(30 <= score <= 50)

    # One department has a high threat score(outlier)
    def test_outlier_department(self):
        departments = [
            {'users': generate_random_data(20, 10, 30)},
            {'users': generate_random_data(10, 10, 30)},
            {'users': generate_random_data(80, 10, 30)}
        ]
        score = aggregated_threat_score(departments)
        print(f"Test Outlier Department: Computed Score = {score}")
        self.assertTrue(score > 50)

    # Users with really high scores inside one of the departments (other departments have a low score)
    def test_outlier_users(self):
        departments = [
            {'users': generate_random_data(20, 10, 30)},
            {'users': generate_random_data(10, 10, 30)},
            {'users': np.append(generate_random_data(15, 10, 25), [90, 90, 90, 90, 90])} # five users with high score
        ]
        score = aggregated_threat_score(departments)
        print(f"Test Outlier Users: Computed Score = {score}")
        self.assertTrue(70 <= score <= 90)

    # Departments with varying numbers of users
    def test_varying_users_amount(self):
        departments = [
            {'users': generate_random_data(80, 10, 10)},
            {'users': generate_random_data(45, 10, 200)},
            {'users': generate_random_data(50, 10, 20)}
        ]
        score = aggregated_threat_score(departments)
        print(f"Test Varying Users Amount: Computed Score = {score}")
        self.assertTrue(score >= 70)


#Running tests
if __name__ == '__main__':
    unittest.main()
