def visualize_set_pieces(set_pieces, set_piece_metrics):
    """
    Create visualizations for set piece statistics.
    
    Parameters:
    -----------
    set_pieces : pd.DataFrame
        DataFrame with set piece events
    set_piece_metrics : dict
        Dictionary with set piece metrics
        
    Returns:
    --------
    tuple
        Figure and axis objects
    """
    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Set pieces by type
    sp_types = set_piece_metrics['set_pieces_by_type']
    
    # Sort by frequency
    sorted_types = sorted(sp_types.items(), key=lambda x: x[1], reverse=True)
    types, counts = zip(*sorted_types)
    
    axs[0, 0].bar(types, counts)
    axs[0, 0].set_title('Set Pieces by Type', fontsize=14)
    axs[0, 0].set_xlabel('Set Piece Type')
    axs[0, 0].set_ylabel('Count')
    
    # Add data labels
    for i, count in enumerate(counts):
        axs[0, 0].text(i, count + 0.5, str(count), ha='center')
    
    # 2. Set piece outcomes
    outcome_dist = set_piece_metrics['outcome_distribution']
    
    # Sort by severity (goals, shots, entries, etc.)
    outcome_order = ['Goal', 'Shot on Target', 'Shot off Target', 'Entry', 
                    'Maintained Possession', 'Lost Possession', 'Other']
    sorted_outcomes = [(k, outcome_dist.get(k, 0)) for k in outcome_order if k in outcome_dist]
    
    outcomes, outcome_counts = zip(*sorted_outcomes)
    
    # Create color map based on outcome
    outcome_colors = ['green', 'yellowgreen', 'yellow', 'orange', 'lightblue', 'red', 'gray']
    colors = [outcome_colors[outcome_order.index(o)] for o in outcomes]
    
    axs[0, 1].bar(outcomes, outcome_counts, color=colors)
    axs[0, 1].set_title('Set Piece Outcomes', fontsize=14)
    axs[0, 1].set_xlabel('Outcome')
    axs[0, 1].set_ylabel('Count')
    axs[0, 1].tick_params(axis='x', rotation=45)
    
    # Add data labels
    for i, count in enumerate(outcome_counts):
        axs[0, 1].text(i, count + 0.5, str(count), ha='center')
    
    # 3. Success rate by type
    if 'success_rate_by_type' in set_piece_metrics:
        type_metrics = set_piece_metrics['success_rate_by_type']
        
        if 'success_rate' in type_metrics:
            types = []
            rates = []
            
            for sp_type in sorted(type_metrics['success_rate'].keys()):
                types.append(sp_type)
                rates.append(type_metrics['success_rate'][sp_type])
            
            axs[1, 0].bar(types, rates)
            axs[1, 0].set_title('Set Piece Success Rate by Type', fontsize=14)
            axs[1, 0].set_xlabel('Set Piece Type')
            axs[1, 0].set_ylabel('Success Rate (%)')
            axs[1, 0].set_ylim(0, 100)
            
            # Add data labels
            for i, rate in enumerate(rates):
                axs[1, 0].text(i, rate + 3, f"{rate}%", ha='center')
    
    # 4. Conversion rates by type
    if 'conversion_rates' in set_piece_metrics:
        conv_rates = set_piece_metrics['conversion_rates']
        
        types = []
        shot_rates = []
        goal_rates = []
        
        for sp_type in sorted(conv_rates.keys()):
            types.append(sp_type)
            shot_rates.append(conv_rates[sp_type]['shot_rate'])
            goal_rates.append(conv_rates[sp_type]['goal_rate'])
        
        bar_width = 0.35
        x = np.arange(len(types))
        
        axs[1, 1].bar(x - bar_width/2, shot_rates, bar_width, label='Shot Rate', color='blue')
        axs[1, 1].bar(x + bar_width/2, goal_rates, bar_width, label='Goal Rate', color='green')
        
        axs[1, 1].set_title('Set Piece Conversion Rates', fontsize=14)
        axs[1, 1].set_xlabel('Set Piece Type')
        axs[1, 1].set_ylabel('Rate (%)')
        axs[1, 1].set_xticks(x)
        axs[1, 1].set_xticklabels(types)
        axs[1, 1].legend()
        
        # Add data labels
        for i, rate in enumerate(shot_rates):
            axs[1, 1].text(i - bar_width/2, rate + 1, f"{rate}%", ha='center', fontsize=8)
        
        for i, rate in enumerate(goal_rates):
            axs[1, 1].text(i + bar_width/2, rate + 1, f"{rate}%", ha='center', fontsize=8)
    
    plt.tight_layout()
    
    return fig, axs

def visualize_set_piece_distribution(set_pieces):
    """
    Create a visualization of set piece distribution across the match.
    
    Parameters:
    -----------
    set_pieces : pd.DataFrame
        DataFrame with set piece events
        
    Returns:
    --------
    tuple
        Figure and axis objects
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Group set pieces by type and calculate counts per interval
    sp_by_minute = set_pieces.groupby(['Match_Minute', 'Set_Piece_Type']).size().unstack(fill_value=0)
    
    # Plot cumulative set pieces over time
    sp_by_minute.plot(kind='area', stacked=True, ax=ax, alpha=0.7)
    
    # Add vertical line at half time (45 minutes)
    ax.axvline(x=45, color='black', linestyle='--', alpha=0.7)
    ax.text(45, ax.get_ylim()[1]*0.9, 'Half-Time', ha='center', va='center', rotation=90)
    
    # Customize the plot
    ax.set_title('Set Piece Distribution Over Match Time', fontsize=16)
    ax.set_xlabel('Match Time (minutes)')
    ax.set_ylabel('Cumulative Set Pieces')
    ax.legend(title='Set Piece Type')
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3)
    
    return fig, ax

def visualize_progression_metrics(progression_metrics):
    """
    Create visualizations for progression metrics.
    
    Parameters:
    -----------
    progression_metrics : dict
        Dictionary with progression metrics
        
    Returns:
    --------
    tuple
        Figure and axis objects
    """
    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Progression types
    prog_types = progression_metrics['progression_types']
    
    # Sort by frequency
    sorted_types = sorted(prog_types.items(), key=lambda x: x[1], reverse=True)
    types, counts = zip(*sorted_types)
    
    axs[0, 0].bar(types, counts)
    axs[0, 0].set_title('Progression Types', fontsize=14)
    axs[0, 0].set_xlabel('Progression Type')
    axs[0, 0].set_ylabel('Count')
    axs[0, 0].tick_params(axis='x', rotation=90)
    
    # 2. Sequence types
    seq_types = progression_metrics['sequence_types']
    
    # Sort by frequency
    sorted_seq_types = sorted(seq_types.items(), key=lambda x: x[1], reverse=True)
    seq_names, seq_counts = zip(*sorted_seq_types)
    
    axs[0, 1].bar(seq_names, seq_counts)
    axs[0, 1].set_title('Sequence Types', fontsize=14)
    axs[0, 1].set_xlabel('Sequence Type')
    axs[0, 1].set_ylabel('Count')
    axs[0, 1].tick_params(axis='x', rotation=45)
    
    # Add data labels
    for i, count in enumerate(seq_counts):
        axs[0, 1].text(i, count + 0.5, str(count), ha='center')
    
    # 3. Efficiency by sequence type
    if 'efficiency_by_type' in progression_metrics:
        eff_metrics = progression_metrics['efficiency_by_type']
        
        if 'shot_rate' in eff_metrics and 'goal_rate' in eff_metrics:
            seq_types = []
            shot_rates = []
            goal_rates = []
            
            for seq_type in eff_metrics['shot_rate'].keys():
                seq_types.append(seq_type)
                shot_rates.append(eff_metrics['shot_rate'][seq_type])
                goal_rates.append(eff_metrics['goal_rate'][seq_type])
            
            bar_width = 0.35
            x = np.arange(len(seq_types))
            
            axs[1, 0].bar(x - bar_width/2, shot_rates, bar_width, label='Shot Rate', color='blue')
            axs[1, 0].bar(x + bar_width/2, goal_rates, bar_width, label='Goal Rate', color='green')
            
            axs[1, 0].set_title('Efficiency by Sequence Type', fontsize=14)
            axs[1, 0].set_xlabel('Sequence Type')
            axs[1, 0].set_ylabel('Rate (%)')
            axs[1, 0].set_xticks(x)
            axs[1, 0].set_xticklabels(seq_types)
            axs[1, 0].tick_params(axis='x', rotation=45)
            axs[1, 0].legend()
    
    # 4. Sequence outcomes
    seq_outcomes = progression_metrics['sequence_outcomes']
    
    # Sort by severity
    outcome_order = ['Goal', 'Shot on Target', 'Shot off Target', 'Entry', 
                     'Maintained Possession', 'Lost Possession', 'Other']
    sorted_outcomes = [(k, seq_outcomes.get(k, 0)) for k in outcome_order if k in seq_outcomes]
    
    if sorted_outcomes:  # Check if outcomes exist
        outcomes, outcome_counts = zip(*sorted_outcomes)
        
        # Create color map based on outcome
        outcome_colors = ['green', 'yellowgreen', 'yellow', 'orange', 'lightblue', 'red', 'gray']
        colors = [outcome_colors[outcome_order.index(o)] for o in outcomes]
        
        axs[1, 1].bar(outcomes, outcome_counts, color=colors)
        axs[1, 1].set_title('Sequence Outcomes', fontsize=14)
        axs[1, 1].set_xlabel('Outcome')
        axs[1, 1].set_ylabel('Count')
        axs[1, 1].tick_params(axis='x', rotation=45)
        
        # Add data labels
        for i, count in enumerate(outcome_counts):
            axs[1, 1].text(i, count + 0.5, str(count), ha='center')
    
    plt.tight_layout()
    
    return fig, axs

def visualize_progression_flow(sequences_df):
    """
    Create a Sankey diagram to visualize the flow of progressions.
    
    Parameters:
    -----------
    sequences_df : pd.DataFrame
        DataFrame with progression sequences
        
    Returns:
    --------
    tuple
        Figure and axis objects
    """
    # This is a simplified approach as true Sankey diagrams require more complex libraries
    # In practice, you might want to use plotly or other Sankey-specific tools
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Count sequences by team and outcome
    team_outcome_counts = sequences_df.groupby(['Team', 'Final_Outcome']).size().reset_index(name='Count')
    
    # Filter for main outcomes to keep the chart readable
    main_outcomes = ['Goal', 'Shot on Target', 'Shot off Target', 'Entry', 'Lost Possession']
    team_outcome_counts = team_outcome_counts[team_outcome_counts['Final_Outcome'].isin(main_outcomes)]
    
    # Set up positions
    teams = team_outcome_counts['Team'].unique()
    outcomes = team_outcome_counts['Final_Outcome'].unique()
    
    # Team positions (left side)
    team_y_positions = {team: idx * 10 for idx, team in enumerate(teams)}
    
    # Outcome positions (right side)
    outcome_y_positions = {outcome: idx * 10 for idx, outcome in enumerate(outcomes)}
    
    # Draw connections
    max_count = team_outcome_counts['Count'].max()
    
    for _, row in team_outcome_counts.iterrows():
        team = row['Team']
        outcome = row['Final_Outcome']
        count = row['Count']
        
        # Line width based on count
        linewidth = 1 + (count / max_count) * 10
        
        # Line color based on outcome
        if outcome == 'Goal':
            color = 'green'
        elif outcome in ['Shot on Target', 'Shot off Target']:
            color = 'yellow'
        elif outcome == 'Entry':
            color = 'orange'
        else:
            color = 'red'
        
        # Draw the connection
        ax.plot(
            [0, 1],  # x coordinates (left to right)
            [team_y_positions[team], outcome_y_positions[outcome]],  # y coordinates
            linewidth=linewidth,
            color=color,
            alpha=0.7
        )
        
        # Add count text
        midpoint_x = 0.5
        midpoint_y = (team_y_positions[team] + outcome_y_positions[outcome]) / 2
        ax.text(midpoint_x, midpoint_y, str(count), ha='center', va='center', 
               bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
    
    # Add team labels (left side)
    for team, y_pos in team_y_positions.items():
        ax.text(-0.05, y_pos, team, ha='right', va='center', fontsize=12, 
               bbox=dict(facecolor='lightblue', alpha=0.7, boxstyle='round'))
    
    # Add outcome labels (right side)
    for outcome, y_pos in outcome_y_positions.items():
        ax.text(1.05, y_pos, outcome, ha='left', va='center', fontsize=12,
               bbox=dict(facecolor='lightgreen', alpha=0.7, boxstyle='round'))
    
    # Configure axes
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(min(list(team_y_positions.values()) + list(outcome_y_positions.values())) - 5,
               max(list(team_y_positions.values()) + list(outcome_y_positions.values())) + 5)
    ax.axis('off')
    
    # Add title
    ax.set_title('Progression Flow: Teams to Outcomes', fontsize=16)
    
    return fig, ax