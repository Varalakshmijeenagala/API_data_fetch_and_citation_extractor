# Citation Extractor

This Python script fetches data from an API endpoint, identifies whether the response for each response-sources pair came from any of the sources, and lists down the sources from which the response was formed. It then saves the citations to a JSON file.

## Requirements

- Python 3.x
- `requests` library
- `re` module
- `json` module
- `string` module

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Varalakshmijeenagala/beyond_chats_assesment.git
```

2. Install the Required Python Packages
```bash
pip install -r requirements.txt
```

## Usage
1. Navigate to the Project directory
2. Run the Python Script in the terminal
```bash
python main.py
```
3. The Citation will be saved to 'citations_output.json'.

## Configuration
Adjust the API_URL and PAGE_SIZE constants in the script according to your API endpoint and page size requirements.
