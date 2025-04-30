def plot_pitch_with_pressing_zones():
    """
    Create a visualization of a soccer pitch with pressing zones.
    
    Returns:
    --------
    tuple
        Figure and axis objects for further customization
    """
    # Create a figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Draw the pitch (simplified version)
    # Pitch dimensions (in arbitrary units, keeping aspect ratio)
    pitch_length, pitch_width = 105, 68
    
    # Draw the pitch outline
    pitch_outline = Rectangle((0, 0), pitch_length, pitch_width, fill=False, color='black')
    ax.add_patch(pitch_outline)
    
    # Draw the halfway line
    ax.plot([pitch_length/2, pitch_length/2], [0, pitch_width], color='black')
    
    # Draw the center circle
    center_circle = plt.Circle((pitch_length/2, pitch_width/2), 9.15, fill=False, color='black')
    ax.add_patch(center_circle)
    
    # Draw the penalty areas
    penalty_area_left = Rectangle((0, pitch_width/2 - 20.16), 16.5, 40.32, fill=False, color='black')
    penalty_area_right = Rectangle((pitch_length - 16.5, pitch_width/2 - 20.16), 16.5, 40.32, fill=False, color='black')
    ax.add_patch(penalty_area_left)
    ax.add_patch(penalty_area_right)
    
    # Draw the goal areas
    goal_area_left = Rectangle((0, pitch_width/2 - 9.16), 5.5, 18.32, fill=False, color='black')
    goal_area_right = Rectangle((pitch_length - 5.5, pitch_width/2 - 9.16), 5.5, 18.32, fill=False, color='black')
    ax.add_patch(goal_area_left)
    ax.add_patch(goal_area_right)
    
    # Draw the pressing zones with transparency
    # High press zone (offensive third)
    high_press = Rectangle((pitch_length*2/3, 0), pitch_length/3, pitch_width, 
                           color='red', alpha=0.2, label='High Press (Offensive)')
    
    # Mid press zone (middle third)
    mid_press = Rectangle((pitch_length/3, 0), pitch_length/3, pitch_width, 
                         color='yellow', alpha=0.2, label='Mid Press (Pre-Offensive)')
    
    # Low press zone (defensive third)
    low_press = Rectangle((0, 0), pitch_length/3, pitch_width, 
                         color='blue', alpha=0.2, label='Low Press (Pre-Defensive)')
    
    ax.add_patch(high_press)
    ax.add_patch(mid_press)
    ax.add_patch(low_press)
    
    # Additional field zones
    # Add zones S1, S2, S3 as vertical thirds
    zone_s1 = plt.Line2D([pitch_length/3, pitch_length/3], [0, pitch_width], 
                        linestyle='--', color='black', linewidth=1.5)
    zone_s2 = plt.Line2D([pitch_length*2/3, pitch_length*2/3], [0, pitch_width], 
                        linestyle='--', color='black', linewidth=1.5)
    
    ax.add_artist(zone_s1)
    ax.add_artist(zone_s2)
    
    # Add text labels for zones
    ax.text(pitch_length/6, pitch_width + 2, 'S1', ha='center', fontsize=12)
    ax.text(pitch_length/2, pitch_width + 2, 'S2', ha='center', fontsize=12)
    ax.text(pitch_length*5/6, pitch_width + 2, 'S3', ha='center', fontsize=12)
    
    # Configure the axis
    ax.set_xlim(-5, pitch_length + 5)
    ax.set_ylim(-5, pitch_width + 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add a title
    ax.set_title('Soccer Pitch with Pressing Zones', fontsize=16)
    
    # Add a legend
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
    
    return fig, ax

def visualize_pressing_statistics(pressing_metrics):
    """
    Create visualizations for pressing statistics.
    
    Parameters:
    -----------
    pressing_metrics : dict
        Dictionary with pressing metrics
        
    Returns:
    --------
    tuple
        Figure and axis objects
    """
    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Pressing success rate by zone
    zone_metrics = pressing_metrics['zone_metrics'].reset_index()
    sns.barplot(x='Pressing', y='success_rate', data=zone_metrics, ax=axs[0, 0])
    axs[0, 0].set_title('Pressing Success Rate by Zone', fontsize=14)
    axs[0, 0].set_xlabel('Pressing Zone')
    axs[0, 0].set_ylabel('Success Rate (%)')
    axs[0, 0].set_ylim(0, 100)
    
    # Add data labels
    for i, row in enumerate(zone_metrics.itertuples()):
        axs[0, 0].text(i, row.success_rate + 3, 
                     f"{row.success_rate}%\n({row.successful}/{row.total})",
                     ha='center')
    
    # 2. Pressing count by team and zone
    zone_team = pressing_metrics['zone_team_metrics'].reset_index()
    palette = {"Estonia": "blue", "Georgia": "red"}
    
    sns.barplot(x='Pressing', y='total', hue='Pressing_Team', data=zone_team, 
               palette=palette, ax=axs[0, 1])
    axs[0, 1].set_title('Number of Pressing Actions by Team and Zone', fontsize=14)
    axs[0, 1].set_xlabel('Pressing Zone')
    axs[0, 1].set_ylabel('Count')
    
    # 3. Success rate by team
    team_metrics = pressing_metrics['team_metrics'].reset_index()
    sns.barplot(x='Pressing_Team', y='success_rate', data=team_metrics, 
               palette=palette, ax=axs[1, 0])
    axs[1, 0].set_title('Pressing Success Rate by Team', fontsize=14)
    axs[1, 0].set_xlabel('Team')
    axs[1, 0].set_ylabel('Success Rate (%)')
    axs[1, 0].set_ylim(0, 100)
    
    # Add data labels
    for i, row in enumerate(team_metrics.itertuples()):
        axs[1, 0].text(i, row.success_rate + 3, 
                      f"{row.success_rate}%\n({row.successful}/{row.total})",
                      ha='center')
    
    # 4. Pressing by half
    half_metrics = pressing_metrics['half_metrics'].reset_index()
    half_metrics['Half'] = half_metrics['Half'].map({1: '1st Half', 2: '2nd Half'})
    
    sns.barplot(x='Half', y='success_rate', data=half_metrics, ax=axs[1, 1])
    axs[1, 1].set_title('Pressing Success Rate by Half', fontsize=14)
    axs[1, 1].set_xlabel('Match Half')
    axs[1, 1].set_ylabel('Success Rate (%)')
    axs[1, 1].set_ylim(0, 100)
    
    # Add data labels
    for i, row in enumerate(half_metrics.itertuples()):
        axs[1, 1].text(i, row.success_rate + 3, 
                      f"{row.success_rate}%\n({row.successful}/{row.total})",
                      ha='center')
    
    plt.tight_layout()
    
    return fig, axs

def visualize_transition_statistics(transition_metrics):
    """
    Create visualizations for transition statistics.
    
    Parameters:
    -----------
    transition_metrics : dict
        Dictionary with transition metrics
        
    Returns:
    --------
    tuple
        Figure and axis objects
    """
    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Transitions by type
    transition_types = ['Estonia gained possession', 'Estonia lost possession']
    transition_counts = [transition_metrics['estonia_gained_possession'], 
                        transition_metrics['estonia_lost_possession']]
    
    axs[0, 0].bar(transition_types, transition_counts, color=['green', 'red'])
    axs[0, 0].set_title('Transition Types', fontsize=14)
    axs[0, 0].set_ylabel('Count')
    
    # Add data labels
    for i, count in enumerate(transition_counts):
        axs[0, 0].text(i, count + 1, str(count), ha='center')
    
    # 2. Transition outcomes
    outcome_labels = ['Resulted in Shot', 'Resulted in Entry', 'Other']
    outcome_counts = [
        transition_metrics['transitions_to_shots'],
        transition_metrics['transitions_to_entries'] - transition_metrics['transitions_to_shots'],
        transition_metrics['total_transitions'] - transition_metrics['transitions_to_entries']
    ]
    
    axs[0, 1].pie(outcome_counts, labels=outcome_labels, autopct='%1.1f%%',
                 colors=['green', 'yellow', 'gray'])
    axs[0, 1].set_title('Transition Outcomes', fontsize=14)
    
    # 3. Transitions by starting zone
    starting_zones = transition_metrics['transitions_by_starting_zone']
    
    # Sort zones (S1, S2, S3)
    if starting_zones:  # Check if not empty
        sorted_zones = sorted(starting_zones.items(), 
                             key=lambda x: ('S1', 'S2', 'S3').index(x[0]) if x[0] in ('S1', 'S2', 'S3') else 999)
        zone_names, zone_counts = zip(*sorted_zones)
        
        axs[1, 0].bar(zone_names, zone_counts)
        axs[1, 0].set_title('Transitions by Starting Zone', fontsize=14)
        axs[1, 0].set_xlabel('Starting Zone')
        axs[1, 0].set_ylabel('Count')
        
        # Add data labels
        for i, count in enumerate(zone_counts):
            axs[1, 0].text(i, count + 0.5, str(count), ha='center')
    else:
        axs[1, 0].text(0.5, 0.5, "No zone data available", ha='center', va='center')
        axs[1, 0].set_title('Transitions by Starting Zone', fontsize=14)
    
    # 4. Transitions by half
    half_labels = ['1st Half', '2nd Half']
    half_counts = [transition_metrics['transitions_first_half'], 
                  transition_metrics['transitions_second_half']]
    
    axs[1, 1].bar(half_labels, half_counts)
    axs[1, 1].set_title('Transitions by Half', fontsize=14)
    axs[1, 1].set_ylabel('Count')
    
    # Add data labels
    for i, count in enumerate(half_counts):
        axs[1, 1].text(i, count + 0.5, str(count), ha='center')
    
    plt.tight_layout()
    
    return fig, axs