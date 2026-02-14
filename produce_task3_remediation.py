
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from E21291_LoadFlow import get_ieee_9_bus_data, build_y_bus, newton_raphson

def run_sensitivity_remediation():
    print("Running Task 3 Remediation: Sensitivity Analysis")
    
    # 1. Setup Base Case
    num_buses, bus_types, P_base, Q_base, V_init, branch_data = get_ieee_9_bus_data()
    Y_bus = build_y_bus(num_buses, branch_data)
    
    # Identify Load Buses (Type 1)
    load_buses = np.where(bus_types == 1)[0]
    
    cases = {
        'Base Case': {'P_factor': 1.0, 'Q_factor': 1.0},
        'P_minus_10%': {'P_factor': 0.9, 'Q_factor': 1.0},
        'P_plus_10%': {'P_factor': 1.1, 'Q_factor': 1.0},
        'Q_minus_10%': {'P_factor': 1.0, 'Q_factor': 0.9},
        'Q_plus_10%': {'P_factor': 1.0, 'Q_factor': 1.1}
    }
    
    results = {}
    
    # 2. Run Simulations
    for case_name, factors in cases.items():
        print(f"  Simulating {case_name}...")
        
        P_spec = P_base.copy()
        Q_spec = Q_base.copy()
        
        # Apply factors to Loads only (Loads are negative in P_spec/Q_spec)
        # Verify: If P_load = -1.25, P_minus_10% should be -1.25 * 0.9 = -1.125 (Lower load)
        # Wait, "Vary P/Q by -10%". Does that mean Load * 0.9 or Load * 1.1?
        # Usually "-10%" means "10% less load".
        
        for bus_idx in load_buses:
            P_spec[bus_idx] *= factors['P_factor']
            Q_spec[bus_idx] *= factors['Q_factor']
            
        V_final, _, _, _ = newton_raphson(Y_bus, P_spec, Q_spec, V_init, bus_types, verbose=False)
        results[case_name] = np.abs(V_final)
        
    # 3. Generate Raw Tables (CSV)
    df = pd.DataFrame(results)
    df.insert(0, 'Bus', np.arange(1, 10))
    
    # Save for Report
    df.to_csv('outputs/tables/task3_voltage_sensitivity_raw.csv', index=False, float_format='%.4f')
    print("  Saved raw data to outputs/tables/task3_voltage_sensitivity_raw.csv")
    
    # 4. Generate Plot (Voltage Profile)
    plt.figure(figsize=(12, 7))
    
    # Plot lines
    plt.plot(df['Bus'], df['Base Case'], 'k-o', linewidth=2, label='Base Case')
    
    plt.plot(df['Bus'], df['P_minus_10%'], 'g--', marker='v', label='P - 10% (Light P Load)')
    plt.plot(df['Bus'], df['P_plus_10%'], 'g-', marker='^', label='P + 10% (Heavy P Load)')
    
    plt.plot(df['Bus'], df['Q_minus_10%'], 'r--', marker='v', label='Q - 10% (Light Q Load)')
    plt.plot(df['Bus'], df['Q_plus_10%'], 'r-', marker='^', label='Q + 10% (Heavy Q Load)')
    
    plt.xlabel('Bus Number', fontsize=12)
    plt.ylabel('Voltage Magnitude (pu)', fontsize=12)
    plt.title('Impact of Active (P) vs Reactive (Q) Load Variations on Voltage Profile', fontsize=14)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=10)
    plt.xticks(np.arange(1, 10))
    
    # Highlight Load Buses
    for bus_idx in load_buses:
        plt.axvline(x=bus_idx+1, color='gray', alpha=0.1)
        
    plt.tight_layout()
    plt.savefig('Report/task3_sensitivity_profiles.png', dpi=300)
    print("  Generated plot Report/task3_sensitivity_profiles.png")

if __name__ == "__main__":
    run_sensitivity_remediation()
