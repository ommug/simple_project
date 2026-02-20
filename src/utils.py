"""
Utility functions for loading the data
"""

import json



def load_data(file_path: str) -> list:
    """
    Load the data from the file
    """
    with open(file_path, 'r') as file:
        return json.load(file)



if __name__ == "__main__":
    data = load_data("data/records.json")
    print(data)