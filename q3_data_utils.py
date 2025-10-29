# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


def load_data(file:str) -> pd.DataFrame:
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
    df = pd.read_csv(file)
    return df
    pass


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
    if remove_duplicates == True:
        df = df.drop_duplicates(inplace=True)
    if sentinel_value == -999:
        df = df.replace(sentinel_value, np.nan,inplace=True)
    return df
    pass


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
    count = df.isnull().sum()
    return count
    pass


def fill_missing(df: pd.DataFrame, column: str, strategy: str) -> pd.DataFrame:
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
    df_filled = df.copy()
    if strategy == "median":
        df_filled[column] = df[column].fillna(df[column].median())
    elif strategy == "mean":
        df_filled[column] = df[column].fillna(df[column].mean())
    elif strategy == "ffill":
        df_filled[column] = df[column].fillna(method='ffill')
    else:
        df_filled[column] = df[column]
    return df_filled
    pass


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
        col = f['column']
        if f['condition'] == 'equals':
            df_filtered = df_filtered[df_filtered[col] == int(f['value'])]
        elif f['condition'] == 'greater_than':
            df_filtered = df_filtered[df_filtered[col] > int(f['value'])]
        elif f['condition'] == 'less_than':
            df_filtered = df_filtered[df_filtered[col] < int(f['value'])]
        elif f['condition'] == 'in_range':
            df_filtered = df_filtered[(df_filtered[col] >= int(f['value'][0])) & (df_filtered[col] <= int(f['value'][1]))]
        elif f['condition'] == 'in_list':
            df_filtered = df_filtered[df_filtered[col].isin(f['value'])]
        else: 
            return False
    return df_filtered
    pass


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
    df_transform = df.copy()
    for col,type in type_map.items():
        if type == "datetime":
            df_transform[col] = pd.to_datetime(df[col])
        elif type == "numeric":
            df_transform[col] = pd.to_numeric(df_transform[col])
        elif type == "category":
            df_transform[col] = df_transform[col].astype("category")
        elif type == "string":
            df_transform[col] = df_transform[col].astype("string")
        else:
            return False
    return df_transform
    pass


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
    df_bins = df.copy()
    df_bins[new_column] = pd.cut(df_bins[column], labels=labels, bins=bins)
    return df_bins
    pass


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
        group_data = df.groupby(group_col).describe()
    else:
        group_data = df.groupby(group_col).agg(agg_dict)
    return group_data 
    pass




if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    
    print("  - load_data()")
    df = load_data('data/clinical_trial_raw.csv')
    """
    df2 = load_data('test_paper')
    print(df2)
    df2_filled = fill_missing(df2, 'col2', strategy='mean')
    print(df2_filled)
    print(detect_missing(df2_filled['col2']))
    """
    print(df.shape)

    print("  - clean_data()")
    df_clean = clean_data(df, sentinel_value=-999)
    print(df_clean.shape)

    print("  - detect_missing()")
    missing = detect_missing(df_clean)
    print(missing['cholesterol_total'])

    print("  - fill_missing()")
    df_filled = fill_missing(df, 'cholesterol_total', strategy='median')
    print(detect_missing(df_filled['cholesterol_total']))
    print("  - filter_data()")
    filters = [
        {'column': 'age', 'condition': 'greater_than', 'value': 18},
        {'column': 'age', 'condition': 'less_than', 'value': 65},
        {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
    ]
    df_filtered = filter_data(df, filters)
    print(df_filtered['age'])
    print("  - transform_types()")
    type_map = {
        'enrollment_date': 'datetime',
        'age': 'numeric',
        'site': 'category'
    }
    df_typed = transform_types(df, type_map)
    print(df_typed)
    print("  - create_bins()")
    df_binned = create_bins(df,column='age',bins=[0, 18, 35, 50, 65, 100],labels=['<18', '18-34', '35-49', '50-64', '65+'])
    print(df_binned)
    print("  - summarize_by_group()")
    summary = summarize_by_group(df, 'site')
    # TODO: Add simple test example here
    # Example:
    # test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    # print("Test DataFrame created:", test_df.shape)
    # print("Test detect_missing:", detect_missing(test_df))