def load_dartfish_data(first_half_path, second_half_path):
    try:
        first_half = pd.read_csv(first_half_path, sep=';', encoding='utf-8-sig')
        second_half = pd.read_csv(second_half_path, sep=';', encoding='utf-8-sig')
        return pd.concat([first_half, second_half], ignore_index=True)
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        raise
    
    """
    Load and combine Dartfish CSV data from first and second half files.
    
    Parameters:
    -----------
    first_half_path : str
        Path to the first half CSV file
    second_half_path : str
        Path to the second half CSV file
        
    Returns:
    --------
    pd.DataFrame
        Combined dataframe with both halves
    """
    # Load both halves, handling the BOM character in the first column
    first_half = pd.read_csv(first_half_path, sep=';', encoding='utf-8-sig')
    second_half = pd.read_csv(second_half_path, sep=';', encoding='utf-8-sig')
    
    # Combine the data
    combined_data = pd.concat([first_half, second_half], ignore_index=True)
    
    return combined_data

def preprocess_data(df):
    """
    Preprocess the Dartfish data for momentum analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw Dartfish data
        
    Returns:
    --------
    pd.DataFrame
        Preprocessed dataframe
    """
    # Convert milliseconds to seconds for easier interpretation
    df['Position_sec'] = df['Position'] / 1000
    df['Duration_sec'] = df['Duration'] / 1000
    
    # Calculate end position
    df['End_Position_sec'] = df['Position_sec'] + df['Duration_sec']
    
    # Convert Poolaeg (half) to numeric if it contains period notation (e.g. "1.")
    df['Half'] = df['Poolaeg'].str.replace('.', '').astype(int)
    
    # Create absolute match time - adding 45 minutes (2700 seconds) for second half
    df['Match_Time_sec'] = df['Position_sec']
    df.loc[df['Half'] == 2, 'Match_Time_sec'] += 2700  # Add 45 minutes for second half
    
    # Create 5-minute interval labels (0-5, 5-10, etc.)
    df['Interval'] = (df['Match_Time_sec'] // 300).astype(int)
    df['Interval_Label'] = df['Interval'].apply(lambda x: f"{x*5}-{(x+1)*5}")
    
    return df