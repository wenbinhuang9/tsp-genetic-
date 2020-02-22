
import random
class Indivisual():
    def __init__(self, gene):
        self.gene = gene
        self.fitness = None
## todo do the final test
## todo add selection rate?
class Genetic_TSP():
    ## the curcuit always begins from the 0 city
    def __init__(self, city_distance_data = None,
                 city_number = 27, population_count = 10,
                 cross_rate = 0.8, mutation_rate = 0.1):
        self.city_distance_data = city_distance_data
        self.city_number = city_number
        self.cross_rate = cross_rate
        self.mutation_rate = mutation_rate
        self.population_count = population_count
        self.init_population_randomly(city_number, population_count)
        self.k = 7
        self.population = []

    def init_population_randomly(self, city_num, population_count):
        for i in range(population_count):
            gene = range(1, city_num)
            random.shuffle(gene)
            ind = self.gen_indivisual(gene)
            self.population.append(ind)


    def cal_tsp_distance(self, gene):
        distance = 0
        previous_city_no = 0
        for cur_city_no in gene:
            distance += self.city_distance_data[previous_city_no][cur_city_no]
            previous_city_no = cur_city_no

        distance += self.city_distance_data[previous_city_no][0]

        return distance

    def fitness(self, indivisual):
        indivisual.fitness = self.cal_tsp_distance(indivisual.gene)

    def cal_k_lowest_indivisual_chosen(self):
        self.population.sort(key=lambda x: x.fitness)
        return self.population[:self.k + 1]


    def select(self):
        k_lowest_indivisual_chosen = self.cal_k_lowest_indivisual_chosen()
        new_population = []

        for i in range(self.population_count):
            r = random.randrange(0, self.k)
            new_population.append(k_lowest_indivisual_chosen[r])

        return new_population

    def gen_crossover_position(self, gen_len):
        start = random.randrange(0, gen_len)
        end = random.randrange(start, gen_len)
        return (start, end)

    def get_parent_random(self):
        idx = random.randrange(0, self.population_count)

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
        ## todo bug here
        for i in range(0, start):
            if child[i] in replace_gene_set:
                if origin_gene_idx >= len(origin_gene):
                    print("here")
                child[i] = origin_gene[origin_gene_idx]
                origin_gene_idx += 1

        for i in range(end, len(child)):
            if child[i] in replace_gene_set:
                if origin_gene_idx >= len(origin_gene):
                    print("here")
                child[i] = origin_gene[origin_gene_idx]
                origin_gene_idx += 1

        if self.is_valid_child(child) == False:
            print("here")
        return child

    def is_valid_child(self, gene):
        s = set(gene)
        return len(gene) == len(s)
    def next_generation(self):
        self.population = self.select()

        new_generation = []
        for i in range(self.population_count/2):
            child1, chil2 = self.crossover()
            new_generation.extend([child1, chil2])

        for indivisual in new_generation:
            self.mutation(indivisual)

        self.population = new_generation

    def gen_indivisual(self, child_gene):
        i = Indivisual(child_gene)
        i.fitness = self.cal_tsp_distance(child_gene)

        return i
    def crossover(self):
        r = random.uniform(0, 1)

        parent1 = self.get_parent_random()
        parent2 = self.get_parent_random()
        if r > self.cross_rate:
            return (parent1, parent2)

        parent1_gene = parent1.gene
        parent2_gene = parent2.gene

        start, end = self.gen_crossover_position(len(parent1_gene))
        child1 = self.gen_new_child(parent1_gene, start, end, parent2_gene[start:end])
        child2 = self.gen_new_child(parent2_gene, start, end, parent1_gene[start:end])

        return (self.gen_indivisual(child1), self.gen_indivisual(child2))

    def mutation(self, indivisual):
        r = random.uniform(0, 1)
        if r < self.mutation_rate:
            start, end = self.gen_crossover_position(len(indivisual.gene))

            indivisual.gene[start], indivisual.gene[end] = indivisual.gene[end], indivisual.gene[start]

    def best(self):
        return self.cal_k_lowest_indivisual_chosen()[0]

    def run(self, iteration_times):
        i = 0
        while i < iteration_times:
            self.next_generation()
            i += 1

        return self.best()