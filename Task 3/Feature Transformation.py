import unittest


def time_difference(hour1, hour2):

    #Calculating the difference between two times
    difference = abs(hour1 - hour2)

    #Determining whether these time values refer to the same day or not
    if hour1 > hour2:
        cyclic_difference = 24 - difference
        return min(difference, cyclic_difference)
    else:
        return difference


#Tests
class Test(unittest.TestCase):

    #Test for the difference between two days
    def test_cyclic_feature(self):
        self.assertEqual(time_difference(23, 1), 2)

    #When the input time is the same, the output must be 0
    def test_same_time(self):
        self.assertEqual(time_difference(22, 22), 0)

    #Couple of regular test cases
    def test_different_times(self):
        self.assertEqual(time_difference(5, 19), 14)
        self.assertEqual(time_difference(0, 12), 12)
        self.assertEqual(time_difference(9, 22), 13)
        self.assertEqual(time_difference(6, 8), 2)
        self.assertEqual(time_difference(20, 23), 3)


#Running tests
if __name__ == '__main__':
    unittest.main()