# OS Lab Tasks - LAB2

This folder contains 4 Python implementations for Operating System concepts:

## Task Files

### 1. task1_system_calls.py
**System Calls and Process Creation**
- Creates child processes using multiprocessing
- Displays Process IDs and Parent Process IDs
- Executes Windows commands from child process
- Demonstrates file operations (create, write, read, close)
- Tests NUL device access
- Handles errors with clear error messages

**Run with:** `python task1_system_calls.py`

### 2. task2_fcfs_sjf_simple.py
**FCFS and SJF Scheduling Algorithms**
- Interactive input for Process ID, Arrival Time, Burst Time
- Input validation with default test data option
- Implements First Come First Serve (FCFS) scheduling
- Implements non-preemptive Shortest Job First (SJF) scheduling
- Shows CPU idle intervals and execution order
- Displays comparison table for both algorithms

**Run with:** `python task2_fcfs_sjf_simple.py`

### 3. task3_priority_rr_simple.py
**Priority and Round Robin Scheduling**
- Interactive input for Process ID, Arrival Time, Burst Time, Priority
- Priority convention: lower number = higher priority
- Implements non-preemptive Priority Scheduling
- Implements Round Robin with configurable time quantum
- Maintains FIFO ready queue for Round Robin
- Shows execution slices and performance comparison

**Run with:** `python task3_priority_rr_simple.py`

### 4. task4_simple.py
**Scheduling Metrics, Threading, and IPC**
- Calculates Completion Time, Turnaround Time, Waiting Time, Response Time
- Generates text-based Gantt charts
- Demonstrates Python threading with worker threads
- Shows Inter-Process Communication using Pipe and Queue
- Explains scheduling results, thread benefits, and IPC limitations

**Run with:** `python task4_simple.py`

## Dependencies

All tasks use only standard Python libraries - no additional installations required.

## Usage Instructions

1. **Interactive Tasks**: Tasks 2 and 3 accept user input. Follow the prompts to enter process data, or press Enter to use default test data.

2. **Automatic Tasks**: Tasks 1 and 4 run automatically with predefined data and demonstrate all required features.

3. **Cross-Platform**: All tasks work on both Windows and Linux systems with automatic OS detection.

## Features Demonstrated

- ✅ Process creation and management
- ✅ File system operations
- ✅ Scheduling algorithm implementations
- ✅ CPU scheduling metrics calculation
- ✅ Text-based Gantt charts
- ✅ Multi-threading demonstration
- ✅ Inter-process communication
- ✅ Error handling and input validation
- ✅ College-appropriate code complexity

## Sample Output

Each task provides clear output showing:
- Process execution details
- Algorithm comparisons
- Performance metrics
- Text-based visual representations
- Thread and IPC demonstrations
- Educational explanations

All tasks are designed for college lab requirements with appropriate complexity and clear documentation.