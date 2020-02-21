
import random
class Indivisual():
    def __init__(self, gene):
        self.gene = gene
        self.fitness = None

## todo do the final test 
class Genetic_TSP():
    ## the curcuit always begins from the 0 city
    def __init__(self, city_distance_data = None,
                 city_number = 27, population_count = 10,
                 cross_rate = 0.8, mutation_rate = 0.1):
        self.city_distance_data = city_distance_data
        self.city_number = city_number
        self.cross_rate = cross_rate
        self.mutation_rate = mutation_rate
        self.population = []
        self.population_count = population_count
        self.init_population_randomly(city_number, population_count)
        self.k = 7

    def init_population_randomly(self, city_num, population_count):
        for i in range(population_count):
            gene = range(1, city_num)
            random_gene = random.shuffle(gene)
            self.population.append(random_gene)


    def cal_tsp_distance(self, gene):
        distance = 0
        previous_city_no = 0
        for cur_city_no in gene:
            distance += self.city_distance_data[previous_city_no][cur_city_no]
            previous_city_no = cur_city_no

        distance += self.city_distance_data[previous_city_no][0]

    def fitness(self, indivisual):
        indivisual.fitness = self.cal_tsp_distance(indivisual.gene)

    def cal_k_lowest_indivisual_chosen(self):

        self.population.sort(key=lambda x: x.fitness)
        return self.population[:self.k]


    def select(self):
        k_lowest_indivisual_chosen = self.cal_k_lowest_indivisual_chosen()
        new_population = []

        for i in range(self.population_count):
            r = random.randrange(0, self.k)
            new_population.append(k_lowest_indivisual_chosen[r])

        return new_population

    def gen_crossover_position(self):
        start = random.randrange(0, self.city_number)
        end = random.randrange(start + 1, self.city_number)
        return (start, end)

    def get_parent_random(self):
        idx = random.randrange(0, self.population_count)

        return self.population[idx]

    def gen_new_child(self, parent, start, end, replace_gene):
        replace_gene_set = set(replace_gene)
        origin_gene = parent[start: end]
        for city_no in origin_gene:
            if city_no in replace_gene_set:
                origin_gene.remove(city_no)

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

    def next_generation(self):
        self.population = self.select()

        new_generation = []
        for i in range(self.city_number/2):
            child1, chil2 = self.crossover()
            new_generation.extend([child1, chil2])

        for indivisual in new_generation:
            self.mutation(indivisual)

        self.population = new_generation

    def crossover(self):
        r = random.uniform(0, 1)

        start, end = self.gen_crossover_position()
        parent1 = self.get_parent_random()
        parent2 = self.get_parent_random()
        if r > self.cross_rate:
            return (parent1, parent2)

        child1 = self.gen_new_child(parent1, start, end, parent2[start, end])
        child2 = self.gen_new_child(parent2, start, end, parent1[start, end])

        return (child1, child2)

    def mutation(self, indivisual):
        r = random.uniform(0, 1)
        if r < self.mutation_rate:
            start, end = self.gen_crossover_position()

            indivisual.gene[start], indivisual.gene[end] = indivisual.gene[end], indivisual.gene[start]

    def best(self):
        return self.cal_k_lowest_indivisual_chosen()[0]

    def run(self, iteration_times):
        ga = Genetic_TSP()

        i = 0
        while i < iteration_times:
            ga.next_generation()
            i += 1

        return ga.best()