def create_pressing_heatmap(pressing_events):
    """
    Create a heatmap visualization of pressing activities on the pitch.
    
    Parameters:
    -----------
    pressing_events : pd.DataFrame
        DataFrame with pressing events
        
    Returns:
    --------
    tuple
        Figure and axis objects
    """
    # Create a pitch figure
    fig, ax = plot_pitch_with_pressing_zones()
    
    # Pitch dimensions
    pitch_length, pitch_width = 105, 68
    
    # If we have field position data
    if 'Field_Side' in pressing_events.columns and 'Field_Depth' in pressing_events.columns:
        # Map field positions to x,y coordinates
        side_mapping = {'L': 0.2, 'M': 0.5, 'R': 0.8}  # Left, Middle, Right positions (normalized)
        depth_mapping = {'1': 0.15, '2': 0.5, '3': 0.85}  # Defensive to offensive (normalized)
        
        # Extract coordinates
        x_coords = []
        y_coords = []
        colors = []
        
        for _, event in pressing_events.iterrows():
            if pd.notna(event['Field_Side']) and pd.notna(event['Field_Depth']):
                # Get base coordinates
                x_base = depth_mapping.get(event['Field_Depth'], 0.5)
                y_base = side_mapping.get(event['Field_Side'], 0.5)
                
                # Add some jitter for better visualization
                x = x_base * pitch_length + np.random.normal(0, 3)
                y = y_base * pitch_width + np.random.normal(0, 3)
                
                x_coords.append(x)
                y_coords.append(y)
                
                # Color by pressing type
                if event['Pressing'] == 'HIGHPRESS':
                    colors.append('red')
                elif event['Pressing'] == 'MIDPRESS':
                    colors.append('yellow')
                else:
                    colors.append('blue')
        
        # Plot the pressing events
        ax.scatter(x_coords, y_coords, c=colors, alpha=0.7, s=100, edgecolors='black')
        
        # Add annotations for the number of pressing events in each zone
        high_press_count = pressing_events[pressing_events['Pressing'] == 'HIGHPRESS'].shape[0]
        mid_press_count = pressing_events[pressing_events['Pressing'] == 'MIDPRESS'].shape[0]
        low_press_count = pressing_events[pressing_events['Pressing'] == 'LOWPRESS'].shape[0]
        
        ax.text(pitch_length * 0.15, -2, f"Low Press: {low_press_count}", ha='center', fontsize=10)
        ax.text(pitch_length * 0.5, -2, f"Mid Press: {mid_press_count}", ha='center', fontsize=10)
        ax.text(pitch_length * 0.85, -2, f"High Press: {high_press_count}", ha='center', fontsize=10)
    
    else:
        # If we don't have field position data, create a simplified visualization
        # Create a grid to represent pressing zones
        grid_x, grid_y = np.mgrid[0:pitch_length:30j, 0:pitch_width:20j]
        positions = np.vstack([grid_x.ravel(), grid_y.ravel()])
        
        # Count events in each pressing zone
        high_press = pressing_events[pressing_events['Pressing'] == 'HIGHPRESS']
        mid_press = pressing_events[pressing_events['Pressing'] == 'MIDPRESS']
        low_press = pressing_events[pressing_events['Pressing'] == 'LOWPRESS']
        
        # Create kernel density estimation based on the counts
        values = np.zeros_like(grid_x)
        
        # Assign higher density to areas based on press counts
        # (This is a simplified approach without actual positional data)
        values[20:, :] += high_press.shape[0] / 100  # High press in offensive third
        values[10:20, :] += mid_press.shape[0] / 100  # Mid press in middle third
        values[:10, :] += low_press.shape[0] / 100  # Low press in defensive third
        
        # Add some random noise to make it look more natural
        values += np.random.normal(0, 0.1, values.shape)
        values = np.maximum(0, values)  # Ensure non-negative
        
        # Generate the heatmap
        heatmap = ax.imshow(
            values.T,
            extent=[0, pitch_length, 0, pitch_width],
            origin='lower',
            cmap='hot',
            alpha=0.6,
            vmin=0
        )
        
        # Add a colorbar
        plt.colorbar(heatmap, ax=ax, label='Pressing Intensity')
    
    ax.set_title('Pressing Activity Heatmap', fontsize=16)
    
    return fig, ax