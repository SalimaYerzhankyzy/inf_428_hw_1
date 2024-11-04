import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def aggregated_threat_score(departments):
    total_score = 0
    total_importance = 0

    for department in departments:
        users = department['users']
        importance = department['importance']
        average_threat_score = np.mean(users)

        # Calculating average threat score based on importance
        priority_threat_score = average_threat_score * importance
        total_score += priority_threat_score
        total_importance += importance

    if total_importance == 0:
        return 0

    aggregated_score = total_score / total_importance

    # Normalization the aggregated score (range 0 - 90)
    return min(max(0, aggregated_score), 90)


#Tests
class Test(unittest.TestCase):

    #If departments importance is zero. Should return a score as 0
    def test_zero_importance(self):
        departments = [
            {'users': generate_random_data(30, 10, 10), 'importance': 0},
            {'users': generate_random_data(10, 10, 10), 'importance': 0}
        ]
        score = aggregated_threat_score(departments)
        self.assertEqual(score, 0)

    # All the same threat scores and importance
    def test_same_input(self):
        departments = [
            {'users': generate_random_data(50, 10, 10), 'importance': 3},
            {'users': generate_random_data(50, 10, 10), 'importance': 3},
            {'users': generate_random_data(50, 10, 10), 'importance': 3}
        ]
        score = aggregated_threat_score(departments)
        self.assertTrue(0 <= score <= 90)

    #If one departments threat score is high and others less
    def test_threat_score(self):
        departments = [
            {'users': generate_random_data(90, 10, 10), 'importance': 5},
            {'users': generate_random_data(10, 10, 10), 'importance': 1}
        ]
        score = aggregated_threat_score(departments)
        self.assertTrue(0 <= score <= 90)

    #Everything at the high peak
    def test_high_input(self):
        departments = [
            {'users': generate_random_data(90, 10, 10), 'importance': 4},
            {'users': generate_random_data(80, 10, 10), 'importance': 5}
        ]
        score = aggregated_threat_score(departments)
        self.assertTrue(0 <= score <= 90)

    #Different mixed input values
    def test_mixed(self):
        departments = [
            {'users': generate_random_data(30, 10, 10), 'importance': 1},
            {'users': generate_random_data(70, 10, 10), 'importance': 4}
        ]
        score = aggregated_threat_score(departments)
        self.assertTrue(0 <= score <= 90)


# Running tests
if __name__ == '__main__':
    unittest.main()
