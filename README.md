# Operating System Lab Assignments

This repository contains college-level Operating System lab assignments implemented in Python.

## Repository Structure

### LAB1 - First Come First Serve (FCFS) Scheduling
- **FIFS.py** - FCFS scheduling algorithm implementation
- **os_system_calls** - Basic system calls demonstration

### LAB2 - Comprehensive OS Concepts
- **task1_system_calls.py** - System calls and process creation
- **task2_fcfs_sjf_simple.py** - FCFS and SJF scheduling algorithms
- **task3_priority_rr_simple.py** - Priority and Round Robin scheduling
- **task4_simple.py** - Scheduling metrics, threading, and IPC
- **README.md** - Detailed documentation for LAB2

## Features Implemented

### ✅ Process Scheduling Algorithms
- First Come First Serve (FCFS)
- Shortest Job First (SJF) - Non-preemptive
- Priority Scheduling - Non-preemptive
- Round Robin with configurable time quantum

### ✅ System Programming Concepts
- Process creation using multiprocessing
- Process IDs and Parent Process IDs
- File operations (create, read, write, delete)
- System interface access (/dev/null, NUL device)
- Error handling and validation

### ✅ Threading and IPC
- Python threading with concurrent execution
- Thread synchronization and communication
- Inter-Process Communication using:
  - Pipes (bidirectional communication)
  - Queues (FIFO message passing)

### ✅ Performance Analysis
- Scheduling metrics calculation:
  - Completion Time (CT)
  - Turnaround Time (TAT)
  - Waiting Time (WT)
  - Response Time (RT)
- Average performance comparisons
- Text-based Gantt chart generation

## Requirements

- Python 3.x
- Standard Python libraries only (no external dependencies)
- Cross-platform compatible (Windows/Linux)

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/Sanjeev2498/OS.git
   cd OS
   ```

2. Run individual tasks:
   ```bash
   # LAB1
   python LAB1/FIFS.py
   
   # LAB2
   python LAB2/task1_system_calls.py
   python LAB2/task2_fcfs_sjf_simple.py
   python LAB2/task3_priority_rr_simple.py
   python LAB2/task4_simple.py
   ```

3. Follow interactive prompts for process input or use default test data

## Academic Note

These implementations are designed for college-level Operating System courses with:
- Appropriate complexity for academic assignments
- Clear, educational code structure
- No external dependencies for easy deployment
- Comprehensive documentation and comments
- Cross-platform compatibility for different lab environments

## Author

**Sanjeev** - College OS Lab Assignments

## License

This project is for educational purposes.