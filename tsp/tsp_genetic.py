import random

##------------- implement code ------##
class Individual():
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = None

class Genetic_TSP():
    def __init__(self, city_distance_data = None,
                 city_number = 27, population_length = 10,
                 cross_rate = 0.8, mutation_rate = 0.1, kth_selection = 7):
        ##tuning arguments
        self.kth_selection = kth_selection
        self.cross_rate = cross_rate
        self.mutation_rate = mutation_rate
        self.population_length = population_length

        ## city distance data
        self.city_distance_data = city_distance_data
        self.city_number = city_number

        ## population initialization
        self.population = []
        ## store all generations
        self.generations = []
        self.init_population(city_number, population_length)

    def selection(self):
        k_lowest_individual_chosen = self.cal_k_lowest_individual_chosen()
        new_population = []

        for i in range(self.population_length):
            r = random.randrange(0, self.kth_selection)
            new_population.append(k_lowest_individual_chosen[r])

        return new_population

    def crossover(self):
        r = random.uniform(0, 1)

        parent1 = self.get_parent_random()
        parent2 = self.get_parent_random()
        if r > self.cross_rate:
            return (parent1, parent2)

        parent1_chromosome = parent1.chromosome
        parent2_chromosome = parent2.chromosome

        start, end = self.gen_crossover_position(len(parent1_chromosome))
        child1 = self.gen_new_child(parent1_chromosome, start, end, parent2_chromosome[start:end])
        child2 = self.gen_new_child(parent2_chromosome, start, end, parent1_chromosome[start:end])

        return (self.gen_individual(child1), self.gen_individual(child2))

    def mutation(self, indivisual):
        r = random.uniform(0, 1)
        if r < self.mutation_rate:
            start, end = self.gen_crossover_position(len(indivisual.chromosome))

            indivisual.chromosome[start], indivisual.chromosome[end] = indivisual.chromosome[end], indivisual.chromosome[start]

    def next_generation(self):
        self.population = self.selection()

        new_generation = []
        for i in range(self.population_length / 2):
            child1, child2 = self.crossover()
            new_generation.extend([child1, child2])

        for individual in new_generation:
            self.mutation(individual)

        self.population = new_generation

    def run(self, iteration_times):
        i = 0
        while i < iteration_times:
            self.next_generation()
            i += 1

        return self.best()

    def best(self):
        return self.cal_k_lowest_individual_chosen()[0]

    def init_population(self, city_num, population_count):
        for i in range(population_count):
            chromosome = range(1, city_num)
            ## randomize chromosome
            random.shuffle(chromosome)
            ind = self.gen_individual(chromosome)
            self.population.append(ind)

    def cal_tsp_distance(self, chromosome):
        distance = 0
        previous_city_no = 0
        for cur_city_no in chromosome:
            distance += self.city_distance_data[previous_city_no][cur_city_no]
            previous_city_no = cur_city_no

        distance += self.city_distance_data[previous_city_no][0]

        return distance

    def fitness(self, individual):
        individual.fitness = self.cal_tsp_distance(individual.chromosome)

    def cal_k_lowest_individual_chosen(self):
        self.population.sort(key=lambda x: x.fitness)
        return self.population[:self.kth_selection + 1]

    def gen_crossover_position(self, chromosome_len):
        start = random.randrange(0, chromosome_len)
        end = random.randrange(start, chromosome_len)
        return (start, end)

    def get_parent_random(self):
        idx = random.randrange(0, self.population_length)

        return self.population[idx]

    def gen_new_child(self, parent, start, end, replace_gene):
        replace_gene_set = set(replace_gene)
        origin_gene = parent[start: end]
        remove_val = []
        for city_no in origin_gene:
            if city_no in replace_gene_set:
                remove_val.append(city_no)
        for val in remove_val:
            origin_gene.remove(val)

        child = parent[:start]
        child.extend(replace_gene)
        child.extend(parent[end:])
        origin_gene_idx = 0
        for i in range(0, start):
            if child[i] in replace_gene_set:
                child[i] = origin_gene[origin_gene_idx]
                origin_gene_idx += 1

        for i in range(end, len(child)):
            if child[i] in replace_gene_set:
                child[i] = origin_gene[origin_gene_idx]
                origin_gene_idx += 1

        return child

    def gen_individual(self, chromosome):
        individual = Individual(chromosome)
        self.fitness(individual)

        return individual


##------------- test test test code ------------##
## my best answer 2471
def test_tsp_ga_with_big_data():
    city_encoding = {0: "Bakersfield", 1: "Barstow", 2: "Carlsbad", 3: "Eureka", 4: "Fresno", 5: "Lake Tahoe, So."}
    data = [[0, 129, 206, 569, 107, 360, 284, 144, 115, 162, 200, 231, 288, 226, 436, 272, 174, 231, 297, 252, 118, 146,
             258, 347, 121, 227, 200],
            [0, 0, 153, 696, 236, 395, 155, 139, 130, 291, 329, 360, 417, 123, 565, 401, 71, 176, 426, 381, 247, 225,
             387, 476, 250, 356, 329],
            [0, 0, 0, 777, 315, 780, 312, 82, 93, 370, 406, 428, 496, 116, 644, 480, 827, 23, 505, 460, 293, 188, 466,
             565, 329, 435, 408],
            [0, 0, 0, 0, 462, 398, 797, 713, 694, 407, 369, 388, 291, 795, 150, 314, 43, 800, 272, 317, 504, 609, 349,
             222, 544, 356, 488],
            [0, 0, 0, 0, 0, 388, 408, 251, 222, 55, 93, 152, 181, 333, 329, 185, 281, 338, 190, 145, 137, 242, 151, 240,
             82, 120, 93],
            [0, 0, 0, 0, 0, 0, 466, 479, 456, 194, 156, 266, 195, 435, 249, 107, 436, 542, 192, 197, 197, 492, 229, 199,
             335, 131, 133],
            [0, 0, 0, 0, 0, 0, 0, 314, 302, 446, 484, 504, 567, 276, 640, 587, 228, 332, 568, 524, 414, 354, 524, 610,
             408, 510, 435],
            [0, 0, 0, 0, 0, 0, 0, 0, 29, 306, 344, 364, 432, 112, 580, 416, 68, 105, 441, 396, 229, 124, 402, 491, 265,
             371, 344],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 277, 315, 335, 403, 111, 551, 387, 59, 116, 412, 367, 200, 95, 373, 462, 236,
             342, 315],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 118, 126, 388, 274, 110, 336, 393, 135, 114, 192, 297, 118, 185, 137, 65,
             81],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 153, 88, 426, 236, 72, 374, 431, 97, 82, 230, 335, 114, 147, 175, 27,
             119],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 111, 446, 325, 185, 394, 451, 116, 71, 135, 240, 45, 166, 234, 140,
             199],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 514, 214, 87, 462, 519, 9, 40, 227, 332, 72, 59, 263, 75, 207],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 682, 498, 52, 139, 523, 478, 311, 206, 484, 573, 347, 453, 426],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 164, 610, 667, 223, 254, 411, 546, 286, 251, 411, 209, 355],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 446, 503, 87, 114, 301, 406, 146, 103, 247, 45, 191],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 105, 471, 426, 259, 254, 432, 521, 295, 401, 374],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 528, 483, 316, 211, 489, 578, 352, 458, 431],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 232, 337, 77, 50, 272, 69, 195],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 187, 292, 32, 95, 227, 69, 195],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 105, 180, 282, 174, 256, 230],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 285, 387, 287, 361, 335],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 233, 101, 199],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 322, 134, 266],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 202, 175],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
    row, col = len(data), len(data[0])
    for i in range(row):
        for j in range(i, col):
            data[j][i] = data[i][j]


    best_score = 10**9

    while best_score > 2700:
        g = Genetic_TSP(data, city_number=27, population_length = 500, kth_selection = 300)
        best = g.run(500)
        best_score = best.fitness
        print(best.fitness)

    print("best score is " + str(best.fitness))
    print("city permutation is")
    print(best.chromosome)

## run test code here
test_tsp_ga_with_big_data()