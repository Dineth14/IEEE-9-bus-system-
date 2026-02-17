
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def generate_plots():
    # Ensure output directory exists
    os.makedirs('Report', exist_ok=True)

    # Data from PSS/E (Hardcoded from Report Table 4)
    # Buses 1 to 9
    psse_v = [1.0400, 1.0250, 1.0250, 1.0258, 0.9956, 1.0127, 1.0258, 1.0159, 1.0324]
    psse_ang = [0.00, 9.28, 4.66, -2.22, -3.99, -3.69, 3.72, 0.73, 1.97]
    
    # Data from My Program (Hardcoded from Report Table 4 for consistency, or could read CSV)
    # Values match PSS/E exactly for magnitude, slight diff for angle
    my_v = [1.0400, 1.0250, 1.0250, 1.0258, 0.9956, 1.0127, 1.0258, 1.0159, 1.0324]
    my_ang = [0.0000, 9.2800, 4.6648, -2.2168, -3.9888, -3.6874, 3.7197, 0.7275, 1.9667]
    
    buses = np.arange(1, 10)
    
    # Plot 1: Voltage Magnitude Comparison
    plt.figure(figsize=(10, 6))
    width = 0.35
    plt.bar(buses - width/2, psse_v, width, label='PSS/E', alpha=0.8)
    plt.bar(buses + width/2, my_v, width, label='My Program', alpha=0.8)
    
    plt.xlabel('Bus Number')
    plt.ylabel('Voltage Magnitude (pu)')
    plt.title('Comparison of Voltage Magnitudes: PSS/E vs Python')
    plt.xticks(buses)
    plt.ylim(0.95, 1.05) # Zoom in to show details like 0.9956
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig('Report/task2_voltage_mag_comparison.png', dpi=300)
    print("Generated Report/task2_voltage_mag_comparison.png")
    
    # Plot 2: Voltage Angle Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(buses, psse_ang, 'o-', label='PSS/E', markersize=8, linewidth=2)
    plt.plot(buses, my_ang, 'x--', label='My Program', markersize=8, linewidth=2)
    
    plt.xlabel('Bus Number')
    plt.ylabel('Voltage Angle (degrees)')
    plt.title('Comparison of Voltage Angles: PSS/E vs Python')
    plt.xticks(buses)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig('Report/task2_voltage_angle_comparison.png', dpi=300)
    print("Generated Report/task2_voltage_angle_comparison.png")

if __name__ == "__main__":
    generate_plots()
