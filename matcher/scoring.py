import json
import os
import click
from collections import defaultdict

def calculate_score(distances, hits):
    total_hits = sum(hits)
    weighted_distance = sum(d * h for d, h in zip(distances, hits)) / total_hits
    score = total_hits / weighted_distance
    return score, total_hits, weighted_distance

@click.command()
@click.option('--performers-file', default='./performers.json', help='Path to the performers JSON file')
@click.argument('data-directory', type=click.Path(exists=True))
def process_data(performers_file, data_directory):
    # Load performers data
    with open(performers_file, 'r') as f:
        performers = json.load(f)

    names = defaultdict(lambda: {'distances': [], 'hits': [], 'id': None})

    # Process all JSON files in the specified directory
    for filename in os.listdir(data_directory):
        if filename.endswith('.json'):
            with open(os.path.join(data_directory, filename), 'r') as f:
                data = json.load(f)
                for item in data:
                    id = item['id']
                    distance = item['distance']
                    hits = item['hits']
                    name = performers.get(id, id)  # Use ID as name if not found in performers
                    names[name]['distances'].append(float(distance))
                    names[name]['hits'].append(int(hits))
                    names[name]['id'] = id

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

if __name__ == '__main__':
    process_data()
