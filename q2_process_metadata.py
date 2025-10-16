# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.

#!/usr/bin/env python3

def parse_config(filepath: str) -> dict:
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
    with open(filepath, 'r') as file:
        content = file.readlines()

    config = {}
    for i in content:
        k, v = i.split('=')
        config[k] = int(v)

    return config


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
    valid_result = {}

    if (config.get('sample_data_rows', 0) > 0) and type(config.get('sample_data_rows', 0)) == int:
        valid_result['sample_data_rows'] = True
    else:
        valid_result['sample_data_rows'] = False

    if (config.get('sample_data_min', 0) >= 1) and type(config.get('sample_data_min', 0)) == int:
        valid_result['sample_data_min'] = True
    else:
        valid_result['sample_data_min'] = False

    if (config.get('sample_data_max', 0) > config.get('sample_data_min', 0)) and type(config.get('sample_data_max', 0)) == int:
        valid_result['sample_data_max'] = True
    else:
        valid_result['sample_data_max'] = False
        
    return valid_result


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
    # TODO: Use random module with config-specified range
    min = config.get('sample_data_min', 0)
    max = config.get('sample_data_max', 0)
    num = config.get('sample_data_rows', 0)

    import random

    with open(filename, 'w') as file:
        for i in range(num):
            file.write(str(random.randint(min, max)) + "\n")


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
    # TODO: Calculate stats
    stats = {}

    stats['mean'] = round(sum(data)/len(data), 1)
    stats['median'] = data[len(data)//2]
    stats['sum'] = sum(data)
    stats['count'] = len(data)

    return stats


if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # TODO: Read the generated file and calculate statistics
    # TODO: Save statistics to output/statistics.txt

    config = parse_config('q2_config.txt')
    # print(config['sample_data_rows'])

    validation = validate_config(config)
    # print(validation['sample_data_rows'])

    generate_sample_data('data/sample_data.csv', config)

    # Read the generated data
    with open('data/sample_data.csv', 'r') as file:
        dat = file.readlines()
    
    # convert the data from string to int
    statistics = calculate_statistics([int(i) for i in dat])
    # print(statistics['count'])

    # Write the summary statistics to output/statistics.txt
    with open('output/statistics.txt', 'w') as outfile:
        outfile.write("===== Summary Statistics =====\n")
        outfile.write(f"Mean: {statistics['mean']}\n")
        outfile.write(f"Median: {statistics['median']}\n")
        outfile.write(f"Sum: {statistics['sum']}\n")
        outfile.write(f"Count: {statistics['count']}\n")