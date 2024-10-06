import sys
from collections import defaultdict

def calculate_score(distances, hits):
    total_hits = sum(hits)
    weighted_distance = sum(d * h for d, h in zip(distances, hits)) / total_hits
    score = total_hits / weighted_distance
    return score, total_hits, weighted_distance

names = defaultdict(lambda: {'distances': [], 'hits': [], 'id': None})

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 4:
        continue  # Skip lines that don't have 4 parts
    hits, name, id, distance = parts
    names[name]['distances'].append(float(distance))
    names[name]['hits'].append(int(hits))
    names[name]['id'] = id  # Assume the ID is the same for all entries of a name

results = []
for name, data in names.items():
    score, total_hits, avg_distance = calculate_score(data['distances'], data['hits'])
    results.append((score, total_hits, avg_distance, data['id'], name))

# Sort by score in descending order
results.sort(reverse=True)

# Print results
print("Score\tHits\tAvg Distance\tID\tName")
for score, total_hits, avg_distance, id, name in results:
    print(f"{score:.2f}\t{total_hits}\t{avg_distance:.2f}\t{id}\t{name}")
