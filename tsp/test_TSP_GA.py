import unittest
import random
from tsp_genetic import Genetic_TSP
class MyTestCase(unittest.TestCase):



    def test_cross_over(self):
        parent1 = [3,4,8,2,7,1,6,5]
        parent2 = [4,2,5,1,6,8,3,7]
        correct_child1 = [3,4,2,1,6,8,7,5]
        correct_child2 = [4,6,5,2,7,1,3,8]
        start = 3
        end =  6
        g = Genetic_TSP(9)

        child1 = g.gen_new_child(parent1, start, end, parent2[start:end])
        self.assertEqual(all([correct_child1[i] == child1[i] for i in range(len(correct_child1))]), True)

        child2 = g.gen_new_child(parent2, start, end, parent1[start:end])
        self.assertEqual(all([correct_child2[i] == child2[i] for i in range(len(correct_child2))]), True)


    def cal_tsp_distance(self, gene, city_distance_data):
        distance = 0
        previous_city_no = 0
        for cur_city_no in gene:
            distance += city_distance_data[previous_city_no][cur_city_no]
            previous_city_no = cur_city_no

        distance += city_distance_data[previous_city_no][0]

        return distance

    def brute_force_tsp(self, city, data, permutation):
        if len(city) == 0:
            return self.cal_tsp_distance(permutation, data)
        distance = 10**9
        for gene in city:
            city_copy = city[:]
            permutation_copy = permutation[:]
            permutation_copy.append(gene)
            city_copy.remove(gene)
            res = self.brute_force_tsp(city_copy, data, permutation_copy)
            distance = min(res, distance)

        return distance

    def test_tsp_ga_with_small_data(self):
        city_encoding = {0:"Bakersfield", 1:"Barstow", 2:"Carlsbad", 3:"Eureka", 4:"Fresno", 5:"Lake Tahoe, So."}
        data = [[  0,129,206,569,107,360],
                [129, 0,153,696,236,395],
                [206,153, 0,777,315,780],
                [569,696,777, 0,462,398],
                [107,236,315, 462,0,388],
                [360,395,780,398,388, 0]]

        g = Genetic_TSP(data, city_number = 6)

        best = g.run(500)
        print(best.fitness)
        print(best.gene)
        min_distance = self.brute_force_tsp([1,2,3,4,5], data, [])
        print("min_distance= " + str(min_distance))


    ## todo continues to fill the data
    def test_tsp_ga_with_big_data(self):
        city_encoding = {0:"Bakersfield", 1:"Barstow", 2:"Carlsbad", 3:"Eureka", 4:"Fresno", 5:"Lake Tahoe, So."}
        data = [[0, 129,206,569,107,360,284,144,115,162,200,231,288,226,436,272,174,231,297,252,118,146,258,347,121,227,200],
                [0, 0,  153,696,236,395,155,139,130,291,329,360,417,123,565,401, 71,176,426,381,247,225,387,476,250,356,329],
                [0, 0,    0,777,315,780,312, 82, 93,370,406,428,496,116,644,480,827, 23,505,460,293,188,466,565,329,435,408],
                [0, 0,    0,  0,462,398,797,713,694,407,369,388,291,795,150,314, 43,800,272,317,504,609,349,222,544,356,488],
                [107,236,315,462,0,388],
                [360,395,780,398,388, 0]]

        g = Genetic_TSP(data, city_number = 6)

        best = g.run(500)
        print(best.fitness)
        print(best.gene)
        min_distance = self.brute_force_tsp([1,2,3,4,5], data, [])
        print("min_distance= " + str(min_distance))

if __name__ == '__main__':
    unittest.main()
