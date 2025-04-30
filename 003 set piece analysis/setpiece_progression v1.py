import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle, Circle
import matplotlib.colors as mcolors
from collections import defaultdict
import re

# Import the previously created modules
# (assuming they're in the same directory)
from momentum_analysis import load_dartfish_data, preprocess_data

def identify_set_pieces(df):
    """
    Identify and categorize set pieces from the Dartfish data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed Dartfish data
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with identified set pieces
    """
    # Create a copy to avoid modifying the original
    setpiece_df = df.copy()
    
    # Set piece types to look for in the data
    set_piece_patterns = [
        'STAN_CORNER',    # Corner kicks
        'STAN_FK',        # Direct free kicks
        'STAN_FKDIRECT'   # Direct free kicks on/off target
        'STAN_KICKOFF',   # Kickoffs
        'FK_OPEN',        # Open play free kicks
        'THROWIN_OPEN'    # Open play throw-ins
        'STAN_THROWIN'    # Long throw-ins
        'STAN_PENALTY'    # Penalties
        'GK_OPENSHORT'    # Goalkick short
        'GK_OPENLONG'     # Goalkick long
    ]
    
    # Create pattern for matching set pieces using regex (case insensitive)
    pattern = '|'.join(set_piece_patterns)
    
    # Filter rows that contain set piece information
    # First check 'Standard last/4' column
    standard_mask = setpiece_df['Standard last/4'].notna() & setpiece_df['Standard last/4'].str.contains(pattern, case=False, regex=True)
    
    # Then check 'Opening' column
    opening_mask = setpiece_df['Opening'].notna() & setpiece_df['Opening'].str.contains(pattern, case=False, regex=True)
    
    # Also check 'Name' column which often contains the set piece type
    name_mask = setpiece_df['Name'].notna() & setpiece_df['Name'].str.contains(pattern, case=False, regex=True)
    
    # Combine all masks
    all_set_pieces = setpiece_df[standard_mask | opening_mask | name_mask].copy()
    
    # Categorize set pieces
    def categorize_set_piece(row):
        for column in ['Standard last/4', 'Opening', 'Name']:
            if pd.notna(row[column]):
                if 'STAN_CORNER' in row[column]:
                    return 'Corners'
                elif 'STAN_FK' in row[column]:
                    return 'Direct free kicks'
                elif 'FK_OPEN' in row[column]:
                    return 'Opening free kicks'
                elif 'STAN_FKDIRECT' in row[column]:
                    return Direct free kicks on/off target
                elif 'STAN_KICKOFF' in row[column]:
                    return 'Kickoffs'
                elif 'THROWIN_OPEN' in row[column]:
                    return 'Throw-ins'
                elif 'STAN_THROWIN' in row[column]:
                    return 'Direct throw-ins'
                elif 'GK_OPENSHORT' in row[column]:
                    return 'Goalkick (short)'
                elif 'GK_OPENLONG' in row[column]:
                    return 'Goalkick (long)'
                elif '
        return 'Other'
    
    # Apply categorization
    all_set_pieces['Set_Piece_Type'] = all_set_pieces.apply(categorize_set_piece, axis=1)
    
    # Identify the team taking the set piece
    all_set_pieces['Taking_Team'] = all_set_pieces['Põhimoment'].apply(
        lambda x: 'Estonia' if x.startswith('AA') else 'Georgia' if x.startswith('DD') else 'Unknown'
    )
    
    # Identify outcome of the set piece
    all_set_pieces['Outcome_Category'] = all_set_pieces['Result'].apply(
        lambda x: 'Goal' if x == 'SHOTGOAL' 
                  else 'Shot on Target' if x == 'SHOTON' 
                  else 'Shot off Target' if x == 'SHOTOFF'
                  else 'Shot blocked' if x == 'SHOTBLOCK'
                  else 'Entry' if x == 'ENTRY'
                  else 'Maintained Possession' if x == 'KEEPPOS' or x == 'WINOPENSTAN'
                  else 'Lost Possession' if x == '-' or pd.isna(x)
                  else 'Other'
    )
    
    # Determine if the set piece was positive or negative
    all_set_pieces['Was_Successful'] = all_set_pieces['Outcome'].apply(
        lambda x: True if x == 'POS' else False
    )
    
    # Additional field for direct shot attempts from set pieces
    shot_results = ['SHOTGOAL', 'SHOTON', 'SHOTOFF', 'SHOTBLOCK']
    all_set_pieces['Direct_Shot'] = all_set_pieces['Result'].isin(shot_results)
    
    # Calculate elapsed game time in minutes (for plotting)
    all_set_pieces['Match_Minute'] = (all_set_pieces['Match_Time_sec'] / 60).round(1)
    
    return all_set_pieces

def calculate_set_piece_metrics(set_pieces):
    """
    Calculate effectiveness metrics for set pieces.
    
    Parameters:
    -----------
    set_pieces : pd.DataFrame
        DataFrame with identified set pieces
        
    Returns:
    --------
    dict
        Dictionary with set piece metrics
    """
    metrics = {}
    
    # Total set pieces
    metrics['total_set_pieces'] = set_pieces.shape[0]
    
    # Set pieces by type
    metrics['set_pieces_by_type'] = set_pieces['Set_Piece_Type'].value_counts().to_dict()
    
    # Set pieces by team
    metrics['set_pieces_by_team'] = set_pieces['Taking_Team'].value_counts().to_dict()
    
    # Success rate by type
    type_success = set_pieces.groupby('Set_Piece_Type').agg(
        total=('Set_Piece_Type', 'count'),
        successful=('Was_Successful', 'sum')
    )
    type_success['success_rate'] = (type_success['successful'] / type_success['total'] * 100).round(1)
    metrics['success_rate_by_type'] = type_success.to_dict()
    
    # Success rate by team
    team_success = set_pieces.groupby('Taking_Team').agg(
        total=('Taking_Team', 'count'),
        successful=('Was_Successful', 'sum')
    )
    team_success['success_rate'] = (team_success['successful'] / team_success['total'] * 100).round(1)
    metrics['success_rate_by_team'] = team_success.to_dict()
    
    # Outcome distribution
    metrics['outcome_distribution'] = set_pieces['Outcome_Category'].value_counts().to_dict()
    
    # Shots from set pieces
    metrics['shots_from_set_pieces'] = set_pieces['Direct_Shot'].sum()
    metrics['shot_rate_from_set_pieces'] = round((set_pieces['Direct_Shot'].sum() / metrics['total_set_pieces']) * 100, 1)
    
    # Goals from set pieces
    metrics['goals_from_set_pieces'] = set_pieces[set_pieces['Outcome_Category'] == 'Goal'].shape[0]
    
    # Set pieces by half
    half_set_pieces = set_pieces.groupby('Half').size()
    metrics['set_pieces_first_half'] = half_set_pieces.get(1, 0)
    metrics['set_pieces_second_half'] = half_set_pieces.get(2, 0)
    
    # Set pieces by interval
    metrics['set_pieces_by_interval'] = set_pieces.groupby('Interval_Label').size().to_dict()
    
    # Calculate conversion rates by type (percent leading to shots or goals)
    conversion_rates = {}
    for sp_type in set_pieces['Set_Piece_Type'].unique():
        type_data = set_pieces[set_pieces['Set_Piece_Type'] == sp_type]
        
        total = type_data.shape[0]
        if total == 0:
            continue
            
        shots = type_data['Direct_Shot'].sum()
        goals = type_data[type_data['Outcome_Category'] == 'Goal'].shape[0]
        
        conversion_rates[sp_type] = {
            'shot_rate': round((shots / total) * 100, 1) if total > 0 else 0,
            'goal_rate': round((goals / total) * 100, 1) if total > 0 else 0,
            'goals_per_shot': round((goals / shots) * 100, 1) if shots > 0 else 0
        }
    
    metrics['conversion_rates'] = conversion_rates
    
    return metrics