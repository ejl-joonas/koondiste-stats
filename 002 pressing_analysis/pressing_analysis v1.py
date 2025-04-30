import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors

# Import the previously created momentum_analysis module
# (assuming it's in the same directory)
from momentum_analysis import load_dartfish_data, preprocess_data

def classify_pressing_zones(df):
    """
    Classify pressing zones based on the Dartfish data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed Dartfish data
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with classified pressing zones
    """
    # Create a copy to avoid modifying the original
    pressing_df = df.copy()
    
    # Extract pressing events (where Pressing column is not empty)
    pressing_events = pressing_df[pressing_df['Pressing'].notna()].copy()
    
    # Map pressing types to zones (based on your zoning system)
    zone_mapping = {
        'HIGHPRESS': 'Offensive',
        'MIDPRESS': 'Pre-Offensive',
        'LOWPRESS': 'Pre-Defensive'
    }
    
    # Apply the mapping
    pressing_events['Pressing_Zone'] = pressing_events['Pressing'].map(zone_mapping)
    
    # Map team possession to attacking/defending team
    pressing_events['Pressing_Team'] = pressing_events['Põhimoment'].apply(
        lambda x: 'OPP Pressing' if x.startswith('AA') else 'EST Pressing' if x.startswith('DD') else 'Transition'
    )
    
    # Map outcome to success/failure
    pressing_events['Pressing_Success'] = pressing_events['Outcome'].apply(
        lambda x: True if x == 'POS' else False
    )
    
    # Add field position details if available
    if 'Field Position' in pressing_events.columns:
        # Parse field positions (like M3, L2/1, R2/2)
        pressing_events['Field_Side'] = pressing_events['Field Position'].str[0]
        pressing_events['Field_Depth'] = pressing_events['Field Position'].str[1]
        
    return pressing_events

def calculate_pressing_metrics(pressing_events):
    """
    Calculate effectiveness metrics for pressing.
    
    Parameters:
    -----------
    pressing_events : pd.DataFrame
        DataFrame with pressing events
        
    Returns:
    --------
    dict
        Dictionary with pressing metrics
    """
    metrics = {}
    
    # Overall pressing metrics
    total_presses = pressing_events.shape[0]
    successful_presses = pressing_events['Pressing_Success'].sum()
    
    metrics['total_presses'] = total_presses
    metrics['successful_presses'] = successful_presses
    metrics['success_rate'] = round((successful_presses / total_presses) * 100, 1) if total_presses > 0 else 0
    
    # Pressing by zone
    zone_metrics = pressing_events.groupby('Pressing').agg(
        total=('Pressing_Success', 'count'),
        successful=('Pressing_Success', 'sum')
    )
    zone_metrics['success_rate'] = (zone_metrics['successful'] / zone_metrics['total'] * 100).round(1)
    metrics['zone_metrics'] = zone_metrics
    
    # Pressing by team
    team_metrics = pressing_events.groupby('Pressing_Team').agg(
        total=('Pressing_Success', 'count'),
        successful=('Pressing_Success', 'sum')
    )
    team_metrics['success_rate'] = (team_metrics['successful'] / team_metrics['total'] * 100).round(1)
    metrics['team_metrics'] = team_metrics
    
    # Pressing by half
    half_metrics = pressing_events.groupby('Poolaeg').agg(
        total=('Pressing_Success', 'count'),
        successful=('Pressing_Success', 'sum')
    )
    half_metrics['success_rate'] = (half_metrics['successful'] / half_metrics['total'] * 100).round(1)
    metrics['half_metrics'] = half_metrics
    
    # Pressing by zone and team
    zone_team_metrics = pressing_events.groupby(['Pressing_Team', 'Pressing']).agg(
        total=('Pressing_Success', 'count'),
        successful=('Pressing_Success', 'sum')
    )
    zone_team_metrics['success_rate'] = (zone_team_metrics['successful'] / zone_team_metrics['total'] * 100).round(1)
    metrics['zone_team_metrics'] = zone_team_metrics
    
    # Calculate PPDA (Passes Per Defensive Action) - if we have pass data
    if 'KEEPPOS' in pressing_events['Result'].values:
        passes = pressing_events[pressing_events['Result'] == 'KEEPPOS'].shape[0]
        defensive_actions = pressing_events[(pressing_events['Pressing_Success']) & 
                                          (pressing_events['Result'] != 'KEEPPOS')].shape[0]
        
        metrics['ppda'] = round(passes / defensive_actions, 2) if defensive_actions > 0 else float('inf')
    
    return metrics