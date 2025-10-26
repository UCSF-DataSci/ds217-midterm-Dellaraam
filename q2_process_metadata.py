# TODO: Add shebang line: 
#!/usr/bin/env python3
import random
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.


def parse_config(file) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    # TODO: Read file, split on '=', create dict
    with open(file) as file:
        lines = file.readlines()
        configs = {}
        for line in lines: 
            l = line.strip().split('=')
            configs[l[0]] = int(l[1])
        return configs
    pass

def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    # TODO: Implement with if/elif/else
    if config['sample_data_rows'] > 0: return True
    elif config['sample_data_min'] >= 1: return True
    elif config['sample_data_max'] > config['sample_data_min']: return True
    else: return False 
    pass


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    # TODO: Parse config values (convert strings to int)
    # TODO: Generate random numbers and save to file
    with open(filename, 'w') as file:
        for i in range(config['sample_data_rows']):
            file.write(f'{random.randint(18, 75)}\n')
    # TODO: Use random module with config-specified range
    pass


def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    data2 = []
    with open(data) as file:
        for line in file:
            data2.append(int(line))
    stats = {}
    # TODO: Calculate stats
    sum = 0
    mid = len(data)//2
    for datum in data2:
        sum += datum
    stats['mean'] = sum/len(data2)
    stats['sum'] = sum 
    if len(data) % 2 != 0:
        stats['median'] = data2[mid]
    else:
        stats['median'] = (data2[mid] + data2[mid-1])//2
    return stats
    pass


if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    config = parse_config('q2_config.txt')
    validation = validate_config(config)
    generate_sample_data('data/sample_data.csv', config)
    # TODO: Read the generated file and calculate statistics
    stats = calculate_statistics('data/sample_data.csv')
    # TODO: Save statistics to output/statistics.txt
    with open('output/statistcs.txt', 'w') as file:
        file.write(f'{stats}')
    pass
