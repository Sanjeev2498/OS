# OS Resource Manager - Integrated Application

**An integrated Python application simulating major OS resource-management functions**

## 📋 Project Overview

This project implements a comprehensive Operating System resource management simulator that demonstrates:
- **Process Scheduling** (FCFS, SJF, Priority, Round Robin)
- **Memory Management** (First Fit, Best Fit, Worst Fit)
- **Deadlock Handling** (Banker's Algorithm, Deadlock Detection)
- **Performance Analysis** (Algorithm comparison with charts)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Optional: matplotlib (for chart generation)

### Installation

1. **Clone or Download the Project**
   ```bash
   cd OS_Resource_Manager
   ```

2. **Install Optional Dependencies** (for charts)
   ```bash
   pip install matplotlib
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## 📖 How to Use

### Main Menu Options

1. **Process Scheduling**
   - Load sample data or enter custom processes
   - Run FCFS, SJF, Priority, or Round Robin algorithms
   - View Gantt charts and performance metrics

2. **Memory Management**
   - Load sample memory blocks and processes
   - Compare First Fit, Best Fit, and Worst Fit algorithms
   - Analyze fragmentation and allocation success rates

3. **Deadlock Handling**
   - Use Banker's Algorithm for safe state verification
   - Detect potential deadlocks
   - View resource allocation matrices

4. **Analysis & Comparison**
   - Compare all algorithms side-by-side
   - Generate performance charts
   - Export results to files

## 📂 Project Structure

```
OS_Resource_Manager/
├── main.py                      # Main application entry point
├── modules/
│   ├── scheduler.py             # Process scheduling algorithms
│   ├── memory.py                # Memory allocation algorithms
│   └── deadlock.py              # Deadlock handling algorithms
├── utils/
│   ├── visualizer.py            # Chart generation
│   └── logger.py                # Activity logging
├── data/
│   ├── processes_sample.txt     # Sample process data
│   └── memory_sample.txt        # Sample memory data
├── output/
│   ├── charts/                  # Generated charts
│   └── system.log               # Activity log
└── README.md                    # This file
```

## 🎯 Features

### Process Scheduling
- **FCFS**: First Come First Serve (non-preemptive)
- **SJF**: Shortest Job First (non-preemptive)
- **Priority**: Priority-based scheduling
- **Round Robin**: Time quantum-based preemptive scheduling

**Metrics Calculated:**
- Average Waiting Time
- Average Turnaround Time
- CPU Utilization
- Throughput

### Memory Management
- **First Fit**: Allocate to first available block
- **Best Fit**: Allocate to smallest sufficient block
- **Worst Fit**: Allocate to largest block

**Metrics Calculated:**
- Memory Utilization
- External Fragmentation
- Allocation Success Rate

### Deadlock Handling
- **Banker's Algorithm**: Safe state verification
- **Deadlock Detection**: Identify deadlocked processes
- **Resource Allocation**: Matrix-based representation

## 📊 Sample Output

### Scheduling Comparison
```
Algorithm      Avg Wait    Avg Turnaround    CPU Util%    Throughput
-----------------------------------------------------------------------
FCFS           10.20       21.40            85.50        0.23
SJF            6.80        18.00            90.20        0.25
Priority       8.40        19.60            88.00        0.24
Round Robin    11.60       22.80            83.00        0.22
```

### Memory Allocation Comparison
```
Algorithm      Allocated    Free    Fragment    Success%
---------------------------------------------------------
First Fit      1167        533     88          100.00
Best Fit       1167        533     71          100.00
Worst Fit      1167        533     179         100.00
```

## 🧪 Testing

The application includes built-in sample data for testing:
- 5 sample processes with varying arrival times, burst times, and priorities
- 5 memory blocks with different sizes
- 4 processes requiring memory allocation
- Banker's Algorithm example with 5 processes and 3 resource types

## 📝 Input Format

### Process Data
```
ProcessID, ArrivalTime, BurstTime, Priority
P1, 0, 5, 2
P2, 1, 3, 1
```

### Memory Data
```
Memory Blocks (KB): 100, 500, 200, 300, 600
Processes: P1:212, P2:417, P3:112, P4:426
```

## 🎓 Educational Value

This project demonstrates:
- Algorithm implementation and comparison
- Data structure usage
- Modular programming design
- User interface development
- Performance metrics analysis
- Visualization techniques

## 🐛 Troubleshooting

**Issue**: Charts not generating
- **Solution**: Install matplotlib: `pip install matplotlib`

**Issue**: Module not found error
- **Solution**: Run from the OS_Resource_Manager directory

**Issue**: Permission denied for log file
- **Solution**: Ensure write permissions in the output directory

## 📧 Support

For issues or questions, refer to the inline help (Option 6 in Main Menu) or check the system logs in `output/system.log`.

## 📄 License

This project is created for educational purposes as part of Operating Systems coursework.

---

**Author**: OS Lab Project  
**Version**: 1.0  
**Last Updated**: 2024
