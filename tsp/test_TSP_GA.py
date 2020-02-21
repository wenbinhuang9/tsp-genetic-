import unittest

from tsp_genetic import Genetic_TSP
class MyTestCase(unittest.TestCase):

    def test_cross_over(self):
        parent1 = [3,4,8,2,7,1,6,5]
        parent2 = [4,2,5,1,6,8,3,7]
        correct_child1 = [3,4,2,1,6,8,7,5]
        correct_child2 = [4,6,5,2,7,1,3,8]
        start = 3
        end =  6
        g = Genetic_TSP()

        child1 = g.gen_new_child(parent1, start, end, parent2[start:end])
        self.assertEqual(all([correct_child1[i] == child1[i] for i in range(len(correct_child1))]), True)

        child2 = g.gen_new_child(parent2, start, end, parent1[start:end])
        self.assertEqual(all([correct_child2[i] == child2[i] for i in range(len(correct_child2))]), True)

if __name__ == '__main__':
    unittest.main()
