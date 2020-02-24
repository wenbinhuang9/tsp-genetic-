import random

## my best answer 3513
class Individual():
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = None

class Genetic_TSP():
    ## the curcuit always begins from the 0 city
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


