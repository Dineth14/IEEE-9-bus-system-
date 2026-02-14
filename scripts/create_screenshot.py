
import matplotlib.pyplot as plt
import textwrap

def generate_screenshot():
    # Read the output file
    try:
        with open('outputs/final_execution.txt', 'r', encoding='utf-16') as f:
            content = f.read()
    except UnicodeError:
        try:
            with open('outputs/final_execution.txt', 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeError:
             with open('outputs/final_execution.txt', 'r', encoding='latin-1') as f:
                content = f.read()

    # Filter content to fit on one "screen" or take important parts
    # We want the top part (Header + Student ID) and bottom part (Conclusion)
    lines = content.split('\n')
    
    # Select key lines to show in screenshot
    selected_lines = []
    
    # Header
    selected_lines.extend(lines[:25]) 
    selected_lines.append("... [Checking Convergence] ...")
    
    # Find results section
    try:
        res_idx = [i for i, s in enumerate(lines) if "FINAL RESULTS" in s][0]
        selected_lines.extend(lines[res_idx:res_idx+20])
    except IndexError:
        pass
        
    selected_lines.append("... [Line Flows Truncated] ...")
    
    # Footer (Timing and Student ID repetition if any)
    selected_lines.extend(lines[-15:])
    
    text_to_render = "\n".join(selected_lines)
    
    # Setup plot
    fig = plt.figure(figsize=(12, 10), facecolor='#1e1e1e') # Dark background
    ax = plt.gca()
    ax.set_facecolor('#1e1e1e')
    
    # Remove axes
    ax.axis('off')
    
    # Add text
    plt.text(0.02, 0.98, text_to_render, 
             color='#cccccc',      # Light gray text
             fontfamily='monospace',
             fontsize=10,
             va='top', ha='left')
             
    # Save
    plt.savefig('Report/execution_proof.png', bbox_inches='tight', facecolor='#1e1e1e', dpi=150)
    print("Screenshot generated: Report/execution_proof.png")

if __name__ == "__main__":
    generate_screenshot()
