## IEEE-9-Bus_system-Load_Flow_Analysis

This repository contains the implementation of load flow analysis for the IEEE 9-bus system using the Newton-Raphson method. The IEEE 9-bus system is a standard test case in power system studies, and this implementation aims to provide insights into the load flow analysis process.

### Files Included

- `ieee_9_bus_data.py`: Contains the data for the IEEE 9-bus system, including bus data, line data, and generator data.
- `Newton_raphson_method.py`: Implements the Newton-Raphson method for load flow analysis.
- `load_flow_analysis.py`: Main script to perform load flow analysis using the Newton-Raphson method on the IEEE 9-bus system.
- `results/`: Directory to store the output results of the load flow analysis.

### Usage

1. Clone the repository:
   ```
   git clone https://github.com/Dineth14/IEEE-9-bus-system-Load_Flow_Analysis.git
   ```
   
2. Navigate to the cloned directory:
   ```
   cd IEEE-9-bus-system-Load_Flow_Analysis
   3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   
4. Run the load flow analysis:
   ```
   python load_flow_analysis.py
    ```
5. View the results in the `results/` directory.

### Note
- Ensure that you have Python installed on your system.
- The implementation is for educational purposes and may require further enhancements for practical applications.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or suggestions.

### Author

Dineth Perera
- GitHub: [Dineth14](https://github.com/Dineth14)