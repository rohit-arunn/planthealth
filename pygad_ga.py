import pygad
import numpy as np
import pandas as pd
from packing_ld1 import grid_based_pack
from genetic_alg_2 import calculate_weight_penalty, evaluate_fitness




df = pd.read_parquet("flight_ICN_to_BUD.parquet")


# Boxes is a list of dictionaries where each dictionary represents one box
boxes = [] 
for idx, row in df.iterrows():
    box_id = (
        row['mstdocnum'], row['docowridr'], row['dupnum'],
        row['seqnum'], row['ratlinsernum'], row['dimsernum']
    ) 
    length = float(row['pcslen']) 
    width = float(row['pcswid'])
    height = float(row['pcshgt']) 
    numpcs = int(row['dim_numpcs'])
    weight = float(row['dim_wgt']) 

    boxes.append({
        'box_id': box_id,
        'dimensions': (length, width, height),
        'number' : numpcs, 
        'weight': weight

    })



solution_placements = {}



# Define the fitness function
def fitness_function(ga_instance,solution, solution_idx):


    fitness_value, placed_boxes = evaluate_fitness(boxes)
    solution_placements[solution_idx] = placed_boxes
    # Objective: Maximize the sum of squares of the solution elementss
    return fitness_value

# Problem parameters
num_generations = 10  # Number of generations
num_parents_mating = 4  # Number of parents for mating
sol_per_pop = 8  # Population size
num_genes = 5  # Number of genes (variables in the solution)
mutation_type = "random"
crossover_type = "two_points"

# Define the range of values for each gene 
gene_space = {'low': -10, 'high': 10}

# Initialize the GA
ga_instance = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    fitness_func=fitness_function,
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    mutation_type=mutation_type,
    crossover_type=crossover_type,
    gene_space=gene_space
)

# Run the GA
ga_instance.run()

# Get the best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Best solution:", solution)
print("Fitness value of the best solution:", solution_fitness)
print("idx is - ", solution_idx)
           
           
# Plot the fitness progress  
ga_instance.plot_fitness()



