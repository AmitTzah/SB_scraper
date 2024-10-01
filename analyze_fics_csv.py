import csv
from operator import itemgetter

def parse_number(value):
    """Parse a string number that may contain commas, 'K', or 'N/A'."""
    if isinstance(value, str):
        value = value.replace(',', '').strip()
        if value.lower() == 'n/a':
            return 0  # Return 0 for 'N/A' values
        if value.lower().endswith('k'):
            return float(value[:-1]) * 1000
    try:
        return float(value)
    except ValueError:
        print(f"Warning: Could not convert '{value}' to float. Using 0 instead.")
        return 0

def calculate_ratio(row):
    """Calculate the followers-to-views ratio for a row."""
    watchers = parse_number(row['watchers'])
    views = parse_number(row['views'])
    
    if views == 0:
        return 0  # Avoid division by zero
    
    return watchers / views

def sort_fictions_by_ratio(input_file, output_file):
    # Read the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fictions = list(reader)
    
    # Calculate ratio and add it to each fiction
    for fiction in fictions:
        fiction['ratio'] = calculate_ratio(fiction)
    
    # Sort fictions by ratio in descending order
    sorted_fictions = sorted(fictions, key=itemgetter('ratio'), reverse=True)
    
    # Write sorted fictions to the output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'watchers', 'views', 'ratio', 'replies', 'likes', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for fiction in sorted_fictions:
            writer.writerow({
                'title': fiction['title'],
                'watchers': fiction['watchers'],
                'views': fiction['views'],
                'ratio': f"{fiction['ratio']:.6f}",
                'replies': fiction['replies'],
                'likes': fiction['likes'],
                'tags': fiction['tags']
            })

if __name__ == "__main__":
    input_file = 'spacebattles_fictions.csv'
    output_file = 'sorted_fictions_by_ratio.csv'
    sort_fictions_by_ratio(input_file, output_file)
    print(f"Sorted fictions have been saved to {output_file}")