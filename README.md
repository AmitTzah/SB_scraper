# SpaceBattles Fiction Analyzer

This project consists of two Python scripts designed to scrape and analyze fiction data from the SpaceBattles forums. It focuses on original fiction within a specific word count range and calculates engagement metrics. It's useful for comparing your story against other stories of similalr length.

## Scripts

1. `fetch_threads_info_from_url.py`: Scrapes fiction data from SpaceBattles forums.
2. `analyze_fics_csv.py`: Analyzes the scraped data and sorts fictions based on a follower-to-view ratio.

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - beautifulsoup4
  - csv (built-in)

## Usage

### Step 1: Fetch Fiction Data

Run the `fetch_threads_info_from_url.py` script to scrape fiction data from SpaceBattles:

```
python fetch_threads_info_from_url.py
```

This will create a CSV file named `spacebattles_fictions.csv` with the scraped data.

### Step 2: Analyze Fiction Data

Run the `analyze_fics_csv.py` script to analyze and sort the fiction data:

```
python analyze_fics_csv.py
```

This will create a new CSV file named `sorted_fictions_by_ratio.csv` with the analyzed and sorted data.

## Output

- `spacebattles_fictions.csv`: Contains raw scraped data including title, replies, views, likes, tags, and watcher count for each fiction.
- `sorted_fictions_by_ratio.csv`: Contains analyzed data sorted by the follower-to-view ratio, which can be used as an engagement metric.

## Customization

You can modify the `base_url` and `params` variables in `fetch_threads_info_from_url.py` to scrape different sections of the SpaceBattles forums or adjust the word count range.

## Notes

- This project is for educational purposes only. Be respectful of the SpaceBattles website and follow their terms of service.
- The scripts include delays between requests to avoid overwhelming the server. Please be considerate and do not remove these delays.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or bug fixes.

## License

[MIT License](https://opensource.org/licenses/MIT)
