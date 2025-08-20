# a population of beetles!
import random
import pandas as pd

generations = 5
num_children = 3
mutation_rate = .1
bid = 1
# bottleneck generation will be f3,
# bottle neck survivors = 5

colors = ['red', 'green', 'blue'] # the colors of beetles
size = ['small', 'med', 'large'] # the size of the bettle
antennae = ['short', 'long'] # antennae length
resistance = ['low', 'high'] # how well beetles can surivive enviromental factors

# create a population

beetles = [{
    'id': 'B0',
    'parent_id': None,
    'color': random.choice(colors),
    'size': random.choice(size),
    'antennae': random.choice(antennae),
    'resistance': random.choice(resistance),
    'generation': 0,
    'survived': 1  # founder beetle will always survive
}]

#return mutated trait with some probability.
def mutate_trait(traits, current_value):
    if random.random() < mutation_rate:
        options = [t for t in traits if t != current_value]
        return random.choice(options)
    return current_value

# simulates a population bottleneck
def bottleneck_generation(beetles_list, survivors=5):
    current_gen = max(b['generation'] for b in beetles_list)
    current_gen_beetles = [b for b in beetles_list if b['generation'] == current_gen]
    kept = random.sample(current_gen_beetles, min(survivors, len(current_gen_beetles)))
    ids_to_keep = set(b['id'] for b in kept)
    return [b for b in beetles_list if b['generation'] != current_gen or b['id'] in ids_to_keep]

for gen in range(1, generations + 1):
    new_beetles = []

    parents = [b for b in beetles if b['generation'] == gen - 1 and b['survived'] == 1]

    for parent in parents:
        for _ in range(num_children):
            beetle_id = f'B{bid}'
            new_beetle = {
                'id': beetle_id,
                'parent_id': parent['id'],
                'color': mutate_trait(colors, parent['color']),
                'size': mutate_trait(size, parent['size']),
                'antennae': mutate_trait(size, parent['antennae']),
                'resistance': mutate_trait(resistance, parent['resistance']),
                'generation': gen,
                'survived': 1  # all surivive until bottleneck
            }
            bid = bid+1
            new_beetles.append(new_beetle)

    beetles.extend(new_beetles)

    if gen == 3:
        beetles = bottleneck_generation(beetles, 5)
        # beetles that died
        current_gen = gen
        survivors = {b['id'] for b in beetles if b['generation'] == current_gen}
        for b in beetles:
            if b['generation'] == current_gen and b['id'] not in survivors:
                b['survived'] = 0


df = pd.DataFrame(beetles)
df.to_csv("beetles.csv", index=False)