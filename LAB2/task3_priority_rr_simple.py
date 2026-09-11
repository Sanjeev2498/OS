#!/usr/bin/env python3
"""
Task 3: Priority and Round Robin Scheduling - Simple College Lab Version
"""

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = -1

def get_processes():
    """Get process data with priority"""
    print("Priority Convention: Lower number = Higher priority")
    print("Enter process details (or press Enter to use default):")
    
    try:
        n = input("Number of processes: ").strip()
        if not n:
            print("Using default data:")
            return [
                Process("P1", 0, 8, 3),
                Process("P2", 1, 4, 1),
                Process("P3", 2, 9, 4),
                Process("P4", 3, 5, 2)
            ]
        
        processes = []
        n = int(n)
        for i in range(n):
            print(f"\nProcess {i+1}:")
            pid = input("Process ID: ") or f"P{i+1}"
            at = float(input("Arrival Time: "))
            bt = float(input("Burst Time: "))
            priority = int(input("Priority (lower=higher): "))
            processes.append(Process(pid, at, bt, priority))
        
        return processes
    
    except:
        print("Invalid input. Using default data:")
        return [
            Process("P1", 0, 8, 3),
            Process("P2", 1, 4, 1), 
            Process("P3", 2, 9, 4),
            Process("P4", 3, 5, 2)
        ]

def get_time_quantum():
    """Get time quantum for Round Robin"""
    try:
        quantum = input("Enter time quantum for Round Robin: ").strip()
        return float(quantum) if quantum else 2.0
    except:
        print("Invalid input. Using default quantum = 2")
        return 2.0

def priority_scheduling(processes):
    """Non-preemptive Priority Scheduling"""
    print("\n=== PRIORITY SCHEDULING ===")
    print("Priority Convention: Lower number = Higher priority")
    
    current_time = 0
    completed = []
    remaining = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in processes]
    
    print(f"{'Process':<10} {'Start':<8} {'End':<8} {'Priority':<10}")
    print("-" * 40)
    
    while remaining:
        # Get available processes
        available = [p for p in remaining if p.arrival_time <= current_time]
        
        if not available:
            # CPU idle
            next_arrival = min(p.arrival_time for p in remaining)
            print(f"{'IDLE':<10} {current_time:<8} {next_arrival:<8} {'--'}")
            current_time = next_arrival
            continue
        
        # Select highest priority (lowest number)
        selected = min(available, key=lambda x: (x.priority, x.arrival_time))
        
        # Execute
        start_time = current_time
        current_time += selected.burst_time
        selected.completion_time = current_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time
        
        print(f"{selected.pid:<10} {start_time:<8} {current_time:<8} {selected.priority:<10}")
        
        completed.append(selected)
        remaining.remove(selected)
    
    return completed

def round_robin_scheduling(processes, quantum):
    """Round Robin Scheduling"""
    print(f"\n=== ROUND ROBIN (Quantum = {quantum}) ===")
    
    current_time = 0
    ready_queue = []
    completed = []
    remaining = sorted([Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in processes], 
                      key=lambda x: x.arrival_time)
    next_index = 0
    
    print("Execution slices:")
    print(f"{'Process':<10} {'Start':<8} {'End':<8} {'Remaining':<10}")
    print("-" * 40)
    
    while ready_queue or next_index < len(remaining):
        # Add newly arrived processes
        while next_index < len(remaining) and remaining[next_index].arrival_time <= current_time:
            ready_queue.append(remaining[next_index])
            next_index += 1
        
        if not ready_queue:
            # CPU idle
            next_arrival = remaining[next_index].arrival_time
            print(f"{'IDLE':<10} {current_time:<8} {next_arrival:<8} {'--'}")
            current_time = next_arrival
            continue
        
        # Get next process (FIFO)
        current_process = ready_queue.pop(0)
        
        # Set response time on first execution
        if current_process.response_time == -1:
            current_process.response_time = current_time - current_process.arrival_time
        
        # Execute for quantum or remaining time
        exec_time = min(quantum, current_process.remaining_time)
        start_time = current_time
        current_time += exec_time
        current_process.remaining_time -= exec_time
        
        print(f"{current_process.pid:<10} {start_time:<8} {current_time:<8} {current_process.remaining_time:<10}")
        
        # Add newly arrived during execution
        while next_index < len(remaining) and remaining[next_index].arrival_time <= current_time:
            ready_queue.append(remaining[next_index])
            next_index += 1
        
        # Check if completed
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed.append(current_process)
        else:
            # Add back to queue
            ready_queue.append(current_process)
    
    return completed

def display_results(processes, priority_processes, rr_processes, quantum):
    """Display comparison results"""
    print("\n=== RESULTS COMPARISON ===")
    
    print(f"Time Quantum: {quantum}")
    print(f"{'Process':<8} {'AT':<6} {'BT':<6} {'Prio':<6} {'Prio CT':<8} {'Prio TAT':<9} {'RR CT':<7} {'RR TAT':<8} {'RR RT':<7}")
    print("-" * 70)
    
    # Create lookup dictionaries
    prio_dict = {p.pid: p for p in priority_processes}
    rr_dict = {p.pid: p for p in rr_processes}
    
    for p in processes:
        prio_p = prio_dict[p.pid]
        rr_p = rr_dict[p.pid]
        print(f"{p.pid:<8} {p.arrival_time:<6} {p.burst_time:<6} {p.priority:<6} "
              f"{prio_p.completion_time:<8} {prio_p.turnaround_time:<9} "
              f"{rr_p.completion_time:<7} {rr_p.turnaround_time:<8} {rr_p.response_time:<7}")
    
    # Averages
    prio_avg = sum(p.turnaround_time for p in priority_processes) / len(priority_processes)
    rr_avg = sum(p.turnaround_time for p in rr_processes) / len(rr_processes)
    
    print(f"\nAverage Turnaround Time:")
    print(f"Priority: {prio_avg:.2f}")
    print(f"Round Robin: {rr_avg:.2f}")

def main():
    print("=" * 50)
    print("Task 3: Priority and Round Robin Scheduling")
    print("=" * 50)
    
    # Get inputs
    processes = get_processes()
    quantum = get_time_quantum()
    
    print("\nProcess Data:")
    print(f"{'Process':<8} {'AT':<6} {'BT':<6} {'Priority'}")
    print("-" * 30)
    for p in processes:
        print(f"{p.pid:<8} {p.arrival_time:<6} {p.burst_time:<6} {p.priority}")
    
    # Run algorithms
    priority_processes = priority_scheduling(processes)
    rr_processes = round_robin_scheduling(processes, quantum)
    
    # Show results
    display_results(processes, priority_processes, rr_processes, quantum)
    
    print("\n" + "=" * 50)
    print("Task 3 Complete!")
    print("Demonstrated:")
    print("✓ Priority scheduling (lower number = higher priority)")
    print("✓ Round Robin with time quantum")
    print("✓ FIFO ready queue")
    print("✓ Response time calculation")
    print("✓ Performance comparison")
    print("=" * 50)

if __name__ == "__main__":
    main()