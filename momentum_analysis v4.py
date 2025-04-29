def plot_momentum_chart(momentum_df, team_stats):
    """
    Create a visualization of the momentum throughout the match.
    
    Parameters:
    -----------
    momentum_df : pd.DataFrame
        Dataframe with momentum data by interval
    team_stats : dict
        Dictionary with team statistics
        
    Returns:
    --------
    None (displays plot)
    """
    # Create a figure with two subplots (momentum line and momentum bars)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[2, 1], sharex=True)
    
    # Line plot for cumulative momentum
    sns.lineplot(
        data=momentum_df, 
        x=momentum_df.index, 
        y='Cumulative_Momentum', 
        ax=ax1, 
        marker='o',
        color='blue',
        linewidth=2
    )
    
    # Add a horizontal line at y=0
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    
    # Bar plot for interval momentum
    bars = ax2.bar(
        momentum_df.index, 
        momentum_df['Momentum_Score'], 
        color=momentum_df['Momentum_Score'].apply(lambda x: 'green' if x > 0 else 'red')
    )
    
    # Customize the plots
    ax1.set_title('Match Momentum Analysis: Estonia vs Georgia (U17)', fontsize=16)
    ax1.set_ylabel('Cumulative Momentum', fontsize=12)
    ax2.set_xlabel('Match Time (5-minute intervals)', fontsize=12)
    ax2.set_ylabel('Interval Momentum', fontsize=12)
    
    # Add interval labels to x-axis
    plt.xticks(
        range(len(momentum_df)), 
        momentum_df['Interval_Label'], 
        rotation=45
    )
    
    # Add a vertical line at half-time (index 9, which is 45 minutes)
    ax1.axvline(x=8.5, color='black', linestyle='-', alpha=0.5)
    ax1.text(8.5, ax1.get_ylim()[1]*0.9, 'Half-Time', ha='center', va='center', rotation=90)
    ax2.axvline(x=8.5, color='black', linestyle='-', alpha=0.5)
    
    # Add match stats as a text box
    stats_text = (
        f"Estonia {team_stats['Estonia']['goals']} - {team_stats['Opponent']['goals']} Georgia\n"
        f"Shots (on/off): {team_stats['Estonia']['shots_on_target']}/{team_stats['Estonia']['shots_off_target']} - "
        f"{team_stats['Opponent']['shots_on_target']}/{team_stats['Opponent']['shots_off_target']}\n"
        f"Possession: {team_stats['Estonia']['possession_pct']}% - {team_stats['Opponent']['possession_pct']}%"
    )
    ax1.text(
        0.02, 0.95, stats_text, 
        transform=ax1.transAxes, 
        fontsize=10, 
        verticalalignment='top', 
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )
    
    plt.tight_layout()
    plt.show()
    
    return fig

def plot_pressing_effectiveness(df):
    """
    Create a visualization of pressing effectiveness by zone.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed Dartfish data
        
    Returns:
    --------
    None (displays plot)
    """
    # Filter for pressing events
    pressing_df = df[df['Pressing'].notna()]
    
    # Create a DataFrame for pressing analysis
    pressing_analysis = pd.DataFrame({
        'Team': ['Estonia' if team == 'AA' else 'Georgia' for team in pressing_df['Põhimoment'].str[:2]],
        'Zone': pressing_df['Pressing'],
        'Success': pressing_df['Outcome'] == 'POS'
    })
    
    # Group and calculate success rates
    pressing_stats = pressing_analysis.groupby(['Team', 'Zone']).agg(
        total=('Success', 'count'),
        successful=('Success', 'sum')
    ).reset_index()
    
    pressing_stats['success_rate'] = (pressing_stats['successful'] / pressing_stats['total'] * 100).round(1)
    
    # Plot the results
    plt.figure(figsize=(12, 6))
    
    # Bar chart of pressing success rate by zone
    sns.barplot(
        data=pressing_stats,
        x='Zone',
        y='success_rate',
        hue='Team',
        palette=['blue', 'red']
    )
    
    plt.title('Pressing Effectiveness by Zone', fontsize=16)
    plt.xlabel('Pressing Zone', fontsize=12)
    plt.ylabel('Success Rate (%)', fontsize=12)
    plt.ylim(0, 100)
    
    for i, row in enumerate(pressing_stats.itertuples()):
        plt.text(
            i % 3 + (0 if row.Team == 'Estonia' else 0.25), 
            row.success_rate + 3,
            f"{row.success_rate}%\n({row.successful}/{row.total})",
            ha='center'
        )
    
    plt.tight_layout()
    plt.show()