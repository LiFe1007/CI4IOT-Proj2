import random
import pandas as pd
import numpy as np
from deap import algorithms, base, creator, tools

# Load the distance matrix from an Excel file
dist_df = pd.read_excel("Project3_DistancesMatrix.xlsx", sheet_name="Sheet1", index_col=0)
distance_matrix = dist_df.to_numpy()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("indices", random.sample, range(len(distance_matrix)), len(distance_matrix))
# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# Define the fitness function
def fitness(path):
    # Calculate the sum of distances between consecutive positions
    dist = 0
    for i in range(len(path) - 1):
        dist += distance_matrix[path[i]][path[i + 1]]
    return dist,


toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == "__main__":
    # Initialize the population
    pop = toolbox.population(n=300)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    cxpb, mutpb, ngen = 0.5, 0.2, 1000

    # Run the GA
    for g in range(ngen):
        print("-- Generation %i --" % g)

        # Select the next generation
        offspring = toolbox.select(pop, len(pop))
        # Apply crossover and mutation
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the fitness of the offspring
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit

        # Replace the old population with the offspring
        pop[:] = offspring

    # Sort the population by fitness
    pop = sorted(pop, key=lambda ind: ind.fitness.values)

    # Print the best individual (path)
    print("Path: ", pop[0])
    print("Fitness: ", pop[0].fitness.values[0])
