#!/usr/bin/env python3
"""
Task 2: FCFS and SJF Scheduling - Simple College Lab Version
"""

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def get_processes():
    """Get process data from user"""
    processes = []
    print("Enter process details (or press Enter to use default data):")
    
    # Try to get user input
    try:
        n = input("Number of processes: ").strip()
        if not n:
            # Use default data if no input
            print("Using default test data:")
            default_processes = [
                Process("P1", 0, 8),
                Process("P2", 1, 4), 
                Process("P3", 2, 9),
                Process("P4", 3, 5)
            ]
            return default_processes
        
        n = int(n)
        for i in range(n):
            print(f"\nProcess {i+1}:")
            pid = input("Process ID: ") or f"P{i+1}"
            at = float(input("Arrival Time: "))
            bt = float(input("Burst Time: "))
            processes.append(Process(pid, at, bt))
    
    except:
        print("Invalid input. Using default data:")
        return [
            Process("P1", 0, 8),
            Process("P2", 1, 4),
            Process("P3", 2, 9), 
            Process("P4", 3, 5)
        ]
    
    return processes

def fcfs_scheduling(processes):
    """First Come First Serve scheduling"""
    print("\n=== FCFS SCHEDULING ===")
    
    # Sort by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    
    print("Execution Order:")
    print(f"{'Process':<10} {'Start':<8} {'End':<8}")
    print("-" * 30)
    
    for p in processes:
        # If CPU is idle
        if current_time < p.arrival_time:
            print(f"{'IDLE':<10} {current_time:<8} {p.arrival_time:<8}")
            current_time = p.arrival_time
        
        # Execute process
        start_time = current_time
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        
        print(f"{p.pid:<10} {start_time:<8} {current_time:<8}")
    
    return processes

def sjf_scheduling(original_processes):
    """Shortest Job First (non-preemptive) scheduling"""
    print("\n=== SJF SCHEDULING ===")
    
    # Make copy of processes
    processes = [Process(p.pid, p.arrival_time, p.burst_time) for p in original_processes]
    
    current_time = 0
    completed = []
    remaining = processes[:]
    
    print("Execution Order:")
    print(f"{'Process':<10} {'Start':<8} {'End':<8} {'Reason'}")
    print("-" * 50)
    
    while remaining:
        # Get available processes
        available = [p for p in remaining if p.arrival_time <= current_time]
        
        if not available:
            # CPU idle - move to next arrival
            next_arrival = min(p.arrival_time for p in remaining)
            print(f"{'IDLE':<10} {current_time:<8} {next_arrival:<8} CPU idle")
            current_time = next_arrival
            continue
        
        # Select shortest job
        selected = min(available, key=lambda x: x.burst_time)
        
        # Execute
        start_time = current_time
        current_time += selected.burst_time
        selected.completion_time = current_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time
        
        print(f"{selected.pid:<10} {start_time:<8} {current_time:<8} Shortest job")
        
        completed.append(selected)
        remaining.remove(selected)
    
    return completed

def display_results(fcfs_processes, sjf_processes):
    """Display comparison results"""
    print("\n=== RESULTS COMPARISON ===")
    
    print(f"{'Process':<8} {'AT':<6} {'BT':<6} {'FCFS CT':<8} {'FCFS TAT':<9} {'FCFS WT':<8} {'SJF CT':<7} {'SJF TAT':<8} {'SJF WT':<7}")
    print("-" * 70)
    
    for i in range(len(fcfs_processes)):
        f = fcfs_processes[i]
        s = sjf_processes[i] 
        print(f"{f.pid:<8} {f.arrival_time:<6} {f.burst_time:<6} {f.completion_time:<8} {f.turnaround_time:<9} {f.waiting_time:<8} {s.completion_time:<7} {s.turnaround_time:<8} {s.waiting_time:<7}")
    
    # Calculate averages
    fcfs_avg_tat = sum(p.turnaround_time for p in fcfs_processes) / len(fcfs_processes)
    fcfs_avg_wt = sum(p.waiting_time for p in fcfs_processes) / len(fcfs_processes)
    
    sjf_avg_tat = sum(p.turnaround_time for p in sjf_processes) / len(sjf_processes)
    sjf_avg_wt = sum(p.waiting_time for p in sjf_processes) / len(sjf_processes)
    
    print(f"\nAverage Times:")
    print(f"FCFS - Average TAT: {fcfs_avg_tat:.2f}, Average WT: {fcfs_avg_wt:.2f}")
    print(f"SJF  - Average TAT: {sjf_avg_tat:.2f}, Average WT: {sjf_avg_wt:.2f}")

def main():
    print("=" * 50)
    print("Task 2: FCFS and SJF Scheduling")
    print("=" * 50)
    
    # Get process data
    original_processes = get_processes()
    
    print("\nOriginal Process Data:")
    print(f"{'Process':<10} {'Arrival Time':<15} {'Burst Time'}")
    print("-" * 40)
    for p in original_processes:
        print(f"{p.pid:<10} {p.arrival_time:<15} {p.burst_time}")
    
    # Run FCFS
    fcfs_processes = fcfs_scheduling([Process(p.pid, p.arrival_time, p.burst_time) for p in original_processes])
    
    # Run SJF
    sjf_processes = sjf_scheduling(original_processes)
    
    # Display results
    display_results(fcfs_processes, sjf_processes)
    
    print("\n" + "=" * 50)
    print("Task 2 Complete!")
    print("Demonstrated:")
    print("✓ Process input and validation")
    print("✓ FCFS scheduling")
    print("✓ SJF scheduling") 
    print("✓ CPU idle time handling")
    print("✓ Performance comparison")
    print("=" * 50)

if __name__ == "__main__":
    main()