#!/usr/bin/env python3
"""
Task 4: Metrics, Threading and IPC - Simple College Lab Version
"""

import threading
import multiprocessing
import time

# Simple process class
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0
        self.response = 0

def calculate_metrics():
    """Simple scheduling metrics calculation"""
    print("=" * 40)
    print("SCHEDULING METRICS CALCULATION")
    print("=" * 40)
    
    # Sample data
    processes = [
        Process("P1", 0, 8),
        Process("P2", 1, 4),
        Process("P3", 2, 9),
        Process("P4", 3, 5)
    ]
    
    # Simple FCFS calculation
    current_time = 0
    for p in processes:
        if current_time < p.arrival:
            current_time = p.arrival
        
        p.response = current_time - p.arrival
        current_time += p.burst
        p.completion = current_time
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst
    
    # Display results
    print(f"{'Process':<8} {'AT':<6} {'BT':<6} {'CT':<6} {'TAT':<6} {'WT':<6} {'RT':<6}")
    print("-" * 50)
    
    total_tat = 0
    total_wt = 0
    total_rt = 0
    
    for p in processes:
        print(f"{p.pid:<8} {p.arrival:<6} {p.burst:<6} {p.completion:<6} "
              f"{p.turnaround:<6} {p.waiting:<6} {p.response:<6}")
        total_tat += p.turnaround
        total_wt += p.waiting
        total_rt += p.response
    
    n = len(processes)
    print(f"\nAverages:")
    print(f"Average Turnaround Time: {total_tat/n:.2f}")
    print(f"Average Waiting Time: {total_wt/n:.2f}")
    print(f"Average Response Time: {total_rt/n:.2f}")
    
    return processes

def create_text_gantt(processes):
    """Simple text-based Gantt chart"""
    print(f"\n=== GANTT CHART ===")
    
    # Show execution timeline
    print("Execution Timeline:")
    print(f"{'Process':<10} {'Start':<8} {'End':<8} {'Duration':<10}")
    print("-" * 40)
    
    current = 0
    for p in processes:
        if current < p.arrival:
            print(f"{'IDLE':<10} {current:<8} {p.arrival:<8} {p.arrival - current:<10}")
            current = p.arrival
        
        print(f"{p.pid:<10} {current:<8} {p.completion:<8} {p.burst:<10}")
        current = p.completion
    
    # Visual representation
    print(f"\nVisual Timeline:")
    timeline = ""
    current = 0
    for p in processes:
        if current < p.arrival:
            timeline += "IDLE "
            current = p.arrival
        timeline += f"{p.pid} "
        current = p.completion
    print(timeline)

def worker_thread(thread_id, data, results):
    """Simple worker thread function"""
    print(f"Thread {thread_id} started (Thread ID: {threading.get_ident()})")
    
    # Simulate some work
    total = 0
    for item in data:
        time.sleep(0.1)  # Simulate work
        result = item * 2  # Simple calculation
        total += result
        print(f"Thread {thread_id}: {item} * 2 = {result}")
    
    # Store result
    results[thread_id] = {
        'thread_id': threading.get_ident(),
        'total': total,
        'items': len(data)
    }
    
    print(f"Thread {thread_id} completed. Total: {total}")

def demonstrate_threading():
    """Simple threading demonstration"""
    print("\n" + "=" * 40)
    print("THREADING DEMONSTRATION")
    print("=" * 40)
    
    # Data for threads
    data1 = [1, 2, 3, 4, 5]
    data2 = [6, 7, 8, 9, 10]
    data3 = [11, 12, 13, 14, 15]
    
    results = {}
    threads = []
    
    print(f"Main Thread ID: {threading.get_ident()}")
    
    # Create threads
    thread1 = threading.Thread(target=worker_thread, args=(1, data1, results))
    thread2 = threading.Thread(target=worker_thread, args=(2, data2, results))
    thread3 = threading.Thread(target=worker_thread, args=(3, data3, results))
    
    threads = [thread1, thread2, thread3]
    
    # Start threads
    print("Starting threads...")
    for t in threads:
        t.start()
    
    # Wait for completion
    print("Waiting for threads...")
    for t in threads:
        t.join()
    
    # Show results
    print(f"\nThread Results:")
    print(f"{'Thread':<8} {'Thread ID':<12} {'Items':<8} {'Total':<8}")
    print("-" * 40)
    
    for tid, result in results.items():
        print(f"{tid:<8} {result['thread_id']:<12} {result['items']:<8} {result['total']:<8}")
    
    print(f"\nBenefits of Threading:")
    print("✓ Concurrent execution")
    print("✓ Better CPU utilization")
    print("✓ Parallel processing")

def sender_process(conn, msg_queue):
    """Simple sender process for IPC"""
    print(f"Sender Process started (PID: {multiprocessing.current_process().pid})")
    
    # Send via Pipe
    messages = ["Hello via Pipe", "Message 2", "Goodbye Pipe"]
    for msg in messages:
        conn.send(f"PIPE: {msg}")
        print(f"Sent via pipe: {msg}")
        time.sleep(0.1)
    conn.close()
    
    # Send via Queue
    queue_msgs = ["Hello via Queue", "Queue message", "Queue end"]
    for msg in queue_msgs:
        msg_queue.put(f"QUEUE: {msg}")
        print(f"Sent via queue: {msg}")
        time.sleep(0.1)
    
    msg_queue.put(None)  # End marker
    print("Sender process finished")

def receiver_process(conn, msg_queue):
    """Simple receiver process for IPC"""
    print(f"Receiver Process started (PID: {multiprocessing.current_process().pid})")
    
    received = []
    
    # Receive from Pipe with timeout
    print("Receiving from pipe...")
    try:
        for i in range(3):  # Expect 3 messages
            if conn.poll(2):  # 2 second timeout
                msg = conn.recv()
                received.append(msg)
                print(f"Received: {msg}")
    except Exception as e:
        print(f"Pipe receive error: {e}")
    finally:
        conn.close()
    
    # Receive from Queue with timeout
    print("Receiving from queue...")
    try:
        while True:
            try:
                msg = msg_queue.get(timeout=2)  # 2 second timeout
                if msg is None:
                    break
                received.append(msg)
                print(f"Received: {msg}")
            except:
                break
    except Exception as e:
        print(f"Queue receive error: {e}")
    
    print(f"Receiver got {len(received)} messages")
    return received

def demonstrate_ipc():
    """Simple IPC demonstration"""
    print("\n" + "=" * 40)
    print("INTER-PROCESS COMMUNICATION")
    print("=" * 40)
    
    # Create IPC mechanisms
    parent_conn, child_conn = multiprocessing.Pipe()
    msg_queue = multiprocessing.Queue()
    
    print("IPC Methods: Pipe and Queue")
    print(f"Main Process PID: {multiprocessing.current_process().pid}")
    
    # Create processes
    sender = multiprocessing.Process(target=sender_process, args=(child_conn, msg_queue))
    receiver = multiprocessing.Process(target=receiver_process, args=(parent_conn, msg_queue))
    
    # Start processes
    print("\nStarting processes...")
    sender.start()
    receiver.start()
    
    # Wait for completion
    sender.join()
    receiver.join()
    
    print(f"\nProcess Summary:")
    print(f"Sender PID: {sender.pid}")
    print(f"Receiver PID: {receiver.pid}")
    
    print(f"\nIPC Analysis:")
    print("PIPE:")
    print("  + Fast, direct communication")
    print("  - Limited to related processes")
    
    print("QUEUE:")
    print("  + Multiple senders/receivers")
    print("  - Serialization overhead")
    
    print("\nLimitations:")
    print("- Pipes: blocking operations, limited scope")
    print("- Queues: memory usage, no message confirmation")

def main():
    print("=" * 50)
    print("Task 4: Metrics, Threading and IPC")
    print("=" * 50)
    
    # Calculate metrics
    processes = calculate_metrics()
    
    # Create Gantt chart
    create_text_gantt(processes)
    
    # Threading demo
    demonstrate_threading()
    
    # IPC demo
    demonstrate_ipc()
    
    print("\n" + "=" * 50)
    print("Task 4 Complete!")
    print("Demonstrated:")
    print("✓ Scheduling metrics (CT, TAT, WT, RT)")
    print("✓ Average calculations")
    print("✓ Gantt chart generation")
    print("✓ Multi-threading")
    print("✓ Inter-process communication")
    print("✓ Benefits and limitations explained")
    print("=" * 50)

if __name__ == "__main__":
    main()