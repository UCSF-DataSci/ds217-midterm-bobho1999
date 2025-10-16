# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Loaded data

    Example:
        >>> df = load_data('data/clinical_trial_raw.csv')
        >>> df.shape
        (10000, 18)
    """
    return pd.read_csv(filepath)


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.

    Args:
        df: Input DataFrame
        remove_duplicates: Whether to drop duplicate rows
        sentinel_value: Value to replace with NaN (e.g., -999, -1)

    Returns:
        pd.DataFrame: Cleaned data

    Example:
        >>> df_clean = clean_data(df, sentinel_value=-999)
    """
    if remove_duplicates:
        df_clean = df.drop_duplicates()
        df_clean = df_clean.replace(sentinel_value, np.nan)
    else:
        df_clean = df.replace(sentinel_value, np.nan)

    return df_clean

def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.

    Args:
        df: Input DataFrame

    Returns:
        pd.Series: Count of missing values for each column

    Example:
        >>> missing = detect_missing(df)
        >>> missing['age']
        15
    """
    return df.isnull().sum()


def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.

    Args:
        df: Input DataFrame
        column: Column name to fill
        strategy: Fill strategy - 'mean', 'median', or 'ffill'

    Returns:
        pd.DataFrame: DataFrame with filled values

    Example:
        >>> df_filled = fill_missing(df, 'age', strategy='median')
    """
    if strategy == 'mean':
        df[column] = df[column].fillna(df[column].mean())
    elif strategy == 'median':
        df[column] = df[column].fillna(df[column].median())
    elif strategy == 'ffill':
        df[column] = df[column].ffill() 

    return df

def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.

    Args:
        df: Input DataFrame
        filters: List of filter dictionaries, each with keys:
                'column', 'condition', 'value'
                Conditions: 'equals', 'greater_than', 'less_than', 'in_range', 'in_list'

    Returns:
        pd.DataFrame: Filtered data

    Examples:
        >>> # Single filter
        >>> filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Multiple filters applied in order
        >>> filters = [
        ...     {'column': 'age', 'condition': 'greater_than', 'value': 18},
        ...     {'column': 'age', 'condition': 'less_than', 'value': 65},
        ...     {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
        ... ]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Range filter example
        >>> filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
        >>> df_filtered = filter_data(df, filters)
    """
    df_filtered = df.copy()

    for f in filters:
        if f['condition'] == 'equals':
            df_filtered = df_filtered[df_filtered[f['column']] == f['value']]
        elif f['condition'] == 'greater_than':
            df_filtered = df_filtered[df_filtered[f['column']] > f['value']]
        elif f['condition'] == 'less_than':
            df_filtered = df_filtered[df_filtered[f['column']] < f['value']]
        elif f['condition'] == 'in_range':
            df_filtered = df_filtered[df_filtered[f['column']].between(f['value'][0], f['value'][1])]
        elif f['condition'] == 'in_list':
            df_filtered = df_filtered[df_filtered[f['column']].isin(f['value'])]
    
    return df_filtered

def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.

    Args:
        df: Input DataFrame
        type_map: Dict mapping column names to target types
                  Supported types: 'datetime', 'numeric', 'category', 'string'

    Returns:
        pd.DataFrame: DataFrame with converted types

    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """

    for colname, colType in type_map.items():
        if colname not in df.columns:
            raise ValueError(f"Error: Column {colname} not in the dataframe")
        else:
            if colType == 'datetime':
                df[colname] = pd.to_datetime(df[colname], errors='coerce')
            elif colType == 'numeric':
                df[colname] = pd.to_numeric(df[colname], errors='coerce')
            elif colType == 'category':
                df[colname] = df[colname].astype('category')
            elif colType == 'string':
                df[colname] = df[colname].astype('string')
            else:
                raise ValueError("Data type not supported. Must be one of ['datetime', 'numeric', 'category', 'string']")
        
    return df



def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: List of bin edges
        labels: List of bin labels
        new_column: Name for new binned column (default: '{column}_binned')

    Returns:
        pd.DataFrame: DataFrame with new binned column

    Example:
        >>> df_binned = create_bins(
        ...     df,
        ...     column='age',
        ...     bins=[0, 18, 35, 50, 65, 100],
        ...     labels=['<18', '18-34', '35-49', '50-64', '65+']
        ... )
    """
    if new_column == None:
        colname = column+"_binned"
        df[colname] = pd.cut(df[column], bins=bins, labels=labels)
    else:
        df[new_column] = pd.cut(df[column], bins=bins, labels=labels)
    
    return df


def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: aggregation_function(s)}
                  If None, uses .describe() on numeric columns

    Returns:
        pd.DataFrame: Grouped and aggregated data

    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """
    if agg_dict == None:
        return df.describe()
    else:
        return df.groupby(group_col, observed=True).agg(agg_dict)




if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")
    
    # TODO: Add simple test example here
    # Example:
    # test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    # print("Test DataFrame created:", test_df.shape)
    # print("Test detect_missing:", detect_missing(test_df))

    # Create testing dataframe
    print("==============================")
    print("Preparing testing dataframe...")
    test_df = pd.DataFrame({'age': [25, 30, 35, 50, 60], 
                            'bmi': [25, -999, 28, 30, 19], 
                            'site': ['Site A', 'Site B', 'Site C', 'Site C', 'Site B']})
    
    # Test clean_data 
    print("\n=== Testing clean data ===")
    df_clean = clean_data(test_df)
    print("Cleaned data:", df_clean)

    # Testing detect_missing 
    print("\n=== Test detect_missing ===")
    print(detect_missing(df_clean))
    
    # Test fill_missing
    print("\n=== Testing fill_missing ===")
    df_filled = fill_missing(df_clean, 'bmi', strategy='ffill')
    print(df_filled)

    # Test filter_data
    print("\n=== Testing filter_data 1 ===")
    filters = [{'column': 'age', 'condition': 'greater_than', 'value': 18}, 
               {'column': 'age', 'condition': 'less_than', 'value': 29},
               {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
               ]
    print(filter_data(df_filled, filters))

    print("\n=== Testing filter_data 2 ===")
    filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 31]}]
    print(filter_data(df_filled, filters))

    # Test create_bins
    print("\n=== Testing create_bins ===")
    df_binned = create_bins(
        df_filled,
        column='age',
        bins=[0, 18, 35, 50, 65, 100],
        labels=['<18', '18-34', '35-49', '50-64', '65+']
        )
    print(df_binned)

    # Test transform_types
    print("\n=== Testing transform_types ===")
    type_map = {
        'age': 'numeric',
        'site': 'category'
        }
    df_typed = transform_types(df_filled, type_map)
    print(df_typed.dtypes)

    # Test transform_types
    print("\n=== Testing summarize_by_group ===")
    # Simple summary
    print("=== Simple summary ===")
    print(summarize_by_group(df_filled, 'site'))

    # Custom aggregations
    print("\n=== Custom aggregations ===")
    summary = summarize_by_group(
        df_filled,
        'site',
        {'age': ['mean', 'std'], 'bmi': 'mean'}
        )
    print(summary)