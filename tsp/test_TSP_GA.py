import unittest
import random
from randomaccessfile import randomaccessfile
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
        print(best.chromosome)
        min_distance = self.brute_force_tsp([1,2,3,4,5], data, [])
        print("min_distance= " + str(min_distance))

    def test_tsp_ga_with_big_data(self):
        city_encoding = {0:"Bakersfield", 1:"Barstow", 2:"Carlsbad", 3:"Eureka", 4:"Fresno", 5:"Lake Tahoe, So."}
        data = [[0, 129,206,569,107,360,284,144,115,162,200,231,288,226,436,272,174,231,297,252,118,146,258,347,121,227,200],
                [0, 0,  153,696,236,395,155,139,130,291,329,360,417,123,565,401, 71,176,426,381,247,225,387,476,250,356,329],
                [0, 0,    0,777,315,780,312, 82, 93,370,406,428,496,116,644,480,827, 23,505,460,293,188,466,565,329,435,408],
                [0, 0,    0,  0,462,398,797,713,694,407,369,388,291,795,150,314, 43,800,272,317,504,609,349,222,544,356,488],
                [0, 0,    0,  0,  0,388,408,251,222, 55, 93,152,181,333,329,185,281,338,190,145,137,242,151,240, 82,120, 93],
                [0, 0,    0,  0,  0,  0,466,479,456,194,156,266,195,435,249,107,436,542,192,197,197,492,229,199,335,131,133],
                [0, 0,    0,  0,  0,  0,  0,314,302,446,484,504,567,276,640,587,228,332,568,524,414,354,524,610,408,510,435],
                [0, 0,    0,  0,  0,  0,  0,  0, 29,306,344,364,432,112,580,416, 68,105,441,396,229,124,402,491,265,371,344],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,277,315,335,403,111,551,387, 59,116,412,367,200, 95,373,462,236,342,315],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0, 37,118,126,388,274,110,336,393,135,114,192,297,118,185,137, 65, 81],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,153, 88,426,236, 72,374,431, 97, 82,230,335,114,147,175, 27,119],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,111,446,325,185,394,451,116, 71,135,240, 45,166,234,140,199],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,514,214, 87,462,519,  9, 40,227,332, 72, 59,263, 75,207],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,682,498, 52,139,523,478,311,206,484,573,347,453,426],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,164,610,667,223,254,411,546,286,251,411,209,355],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,446,503, 87,114,301,406,146,103,247, 45,191],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,105,471,426,259,254,432,521,295,401,374],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,528,483,316,211,489,578,352,458,431],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 45,232,337, 77, 50,272, 69,195],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,187,292, 32, 95,227, 69,195],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,105,180,282,174,256,230],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,285,387,287,361,335],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,127,233,101,199],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,322,134,266],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,202,175],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,146],
                [0, 0,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
                ]
        row , col = len(data), len(data[0])
        for i in range(row):
            for j in range(i, col):
                data[j][i] = data[i][j]

        ##3681
        ##[24, 19, 12, 11, 17, 2, 1, 7, 13, 21, 20, 5, 26, 9, 4, 10, 25, 15, 22, 18, 23, 14, 3, 16, 8, 6]


        def tsp_calculation():
            minimum = 10 ** 9
            minium_chromosome = None
            for i in range(100):
                g = Genetic_TSP(data, city_number=27)

                best = g.run(500)
                if minimum > best.fitness:
                    minimum = best.fitness
                    minium_chromosome = best.chromosome

            return (minimum, minium_chromosome)
        ans = 10 ** 9
        ans_chromosome = None
        for i in range(100):
            min_one, chromosome = tsp_calculation()
            ans = min(ans, min_one)

            print(min_one)
            print(chromosome)

        print(ans)


if __name__ == '__main__':
    unittest.main()
