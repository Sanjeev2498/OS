#!/usr/bin/env python3
"""
Task 1: Thread Creation, Models and Benefits
- Create single-threaded baseline workload
- Divide workload into independent tasks
- Create multiple worker threads
- Display thread identifiers and execution progress
- Wait for all threads to complete
- Measure and compare execution times
- Explain threading models and concepts
"""

import threading
import time
import random
import math

# Shared data structure to track progress
progress_lock = threading.Lock()
progress_data = {}

def cpu_intensive_task(task_id, data_chunk, result_dict):
    """
    CPU-intensive task: Calculate prime numbers in a range
    """
    thread_id = threading.get_ident()
    thread_name = threading.current_thread().name
    
    print(f"Thread {thread_name} (ID: {thread_id}) starting task {task_id}")
    
    # Update progress
    with progress_lock:
        progress_data[task_id] = {"status": "started", "thread_id": thread_id, "progress": 0}
    
    start_range, end_range = data_chunk
    primes = []
    
    # Calculate primes in the given range
    for num in range(start_range, end_range + 1):
        if num > 1:
            is_prime = True
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        
        # Update progress periodically
        if (num - start_range) % 100 == 0:
            progress = ((num - start_range) / (end_range - start_range)) * 100
            with progress_lock:
                progress_data[task_id]["progress"] = progress
            print(f"Thread {thread_name}: Task {task_id} - {progress:.1f}% complete")
    
    # Store result
    result_dict[task_id] = {
        "thread_id": thread_id,
        "thread_name": thread_name,
        "range": (start_range, end_range),
        "primes_count": len(primes),
        "primes": primes[:10]  # Store first 10 primes for verification
    }
    
    # Update final progress
    with progress_lock:
        progress_data[task_id]["status"] = "completed"
        progress_data[task_id]["progress"] = 100
    
    print(f"Thread {thread_name}: Task {task_id} COMPLETED - Found {len(primes)} primes")
    
    # Simulate some additional processing time
    time.sleep(0.1)

def single_threaded_baseline():
    """
    Single-threaded baseline implementation
    """
    print("=" * 60)
    print("SINGLE-THREADED BASELINE")
    print("=" * 60)
    
    # Define workload: find primes in ranges
    workload = [
        (1, 1000),
        (1001, 2000),
        (2001, 3000),
        (3001, 4000),
        (4001, 5000)
    ]
    
    results = {}
    start_time = time.time()
    
    print(f"Main Thread ID: {threading.get_ident()}")
    print(f"Processing {len(workload)} tasks sequentially...")
    
    for i, data_chunk in enumerate(workload):
        task_id = f"Task-{i+1}"
        print(f"\nProcessing {task_id}: range {data_chunk}")
        cpu_intensive_task(task_id, data_chunk, results)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n{'='*40}")
    print("SINGLE-THREADED RESULTS:")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Tasks completed: {len(results)}")
    
    total_primes = sum(result["primes_count"] for result in results.values())
    print(f"Total primes found: {total_primes}")
    
    return execution_time, results

def multithreaded_implementation():
    """
    Multithreaded implementation with worker threads
    """
    print("\n" + "=" * 60)
    print("MULTITHREADED IMPLEMENTATION")
    print("=" * 60)
    
    # Clear progress data
    global progress_data
    progress_data = {}
    
    # Define the same workload
    workload = [
        (1, 1000),
        (1001, 2000),
        (2001, 3000),
        (3001, 4000),
        (4001, 5000)
    ]
    
    results = {}
    threads = []
    
    print(f"Main Thread ID: {threading.get_ident()}")
    print(f"Creating {len(workload)} worker threads...")
    
    start_time = time.time()
    
    # Create and start worker threads
    for i, data_chunk in enumerate(workload):
        task_id = f"Task-{i+1}"
        thread = threading.Thread(
            target=cpu_intensive_task,
            args=(task_id, data_chunk, results),
            name=f"Worker-{i+1}"
        )
        threads.append(thread)
        print(f"Created thread: {thread.name}")
    
    # Start all threads
    print(f"\nStarting {len(threads)} threads...")
    for thread in threads:
        thread.start()
        print(f"Started thread: {thread.name} (ID will be assigned on execution)")
    
    print(f"\nAll threads started! Waiting for completion...")
    
    # Monitor progress
    while any(thread.is_alive() for thread in threads):
        time.sleep(0.5)
        with progress_lock:
            active_tasks = [task for task, info in progress_data.items() 
                          if info["status"] != "completed"]
            if active_tasks:
                print(f"Active tasks: {len(active_tasks)} - {', '.join(active_tasks)}")
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
        print(f"Thread {thread.name} joined successfully")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n{'='*40}")
    print("MULTITHREADED RESULTS:")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Tasks completed: {len(results)}")
    print(f"Threads used: {len(threads)}")
    
    # Display thread information
    print(f"\nThread Execution Details:")
    print(f"{'Task':<10} {'Thread Name':<15} {'Thread ID':<15} {'Range':<15} {'Primes':<10}")
    print("-" * 75)
    
    for task_id, result in results.items():
        print(f"{task_id:<10} {result['thread_name']:<15} {result['thread_id']:<15} "
              f"{str(result['range']):<15} {result['primes_count']:<10}")
    
    total_primes = sum(result["primes_count"] for result in results.values())
    print(f"\nTotal primes found: {total_primes}")
    
    return execution_time, results

def compare_performance(single_time, multi_time):
    """
    Compare single-threaded vs multithreaded performance
    """
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    speedup = single_time / multi_time if multi_time > 0 else 0
    efficiency = speedup / 5 * 100  # 5 threads used
    
    print(f"Single-threaded execution time: {single_time:.2f} seconds")
    print(f"Multithreaded execution time:   {multi_time:.2f} seconds")
    print(f"Speedup:                        {speedup:.2f}x")
    print(f"Efficiency:                     {efficiency:.1f}%")
    
    if speedup > 1:
        improvement = ((single_time - multi_time) / single_time) * 100
        print(f"Performance improvement:        {improvement:.1f}%")
        print("✓ Multithreading provided performance benefit")
    else:
        print("⚠ Multithreading did not improve performance")
        print("  (This can happen due to GIL, overhead, or task nature)")

def explain_threading_concepts():
    """
    Brief explanation of threading models and concepts
    """
    print("\n" + "=" * 50)
    print("THREADING CONCEPTS SUMMARY")
    print("=" * 50)
    
    print("\n🔹 THREAD MODELS:")
    print("   • User-level: Fast switching, library-managed")
    print("   • Kernel-level: OS-managed, true parallelism") 
    print("   • Hybrid: M:N mapping, balanced approach")
    
    print("\n🔸 MULTITHREADING MODELS:")
    print("   • Many-to-One: Multiple user → single kernel thread")
    print("   • One-to-One: Direct mapping, higher overhead")
    print("   • Many-to-Many: Flexible mapping, complex")

def explain_threading_benefits_challenges():
    """
    Brief explanation of threading benefits and challenges
    """
    print("\n✅ THREADING BENEFITS:")
    print("   • Responsiveness: Non-blocking execution")
    print("   • Resource Sharing: Efficient memory usage")
    print("   • Concurrency: Simultaneous task progress")
    print("   • Parallelism: Multi-core utilization")
    
    print("\n❌ THREADING CHALLENGES:")
    print("   • Race Conditions: Shared data conflicts")
    print("   • Deadlocks: Circular waiting scenarios")
    print("   • Overhead: Context switching costs")
    print("   • Python GIL: Limits CPU parallelism")

def main():
    """
    Main function to demonstrate thread creation, models and benefits
    """
    print("=" * 70)
    print("TASK 1: THREAD CREATION, MODELS AND BENEFITS")
    print("=" * 70)
    
    print("\nDemonstration Workload:")
    print("• Task: Find all prime numbers in different ranges")
    print("• CPU-intensive computation suitable for threading comparison")
    print("• Same workload used for both single and multithreaded versions")
    
    # Run single-threaded baseline
    single_time, single_results = single_threaded_baseline()
    
    # Run multithreaded implementation
    multi_time, multi_results = multithreaded_implementation()
    
    # Compare performance
    compare_performance(single_time, multi_time)
    
    # Explain concepts
    explain_threading_concepts()
    explain_threading_benefits_challenges()
    
    print("\n" + "=" * 70)
    print("TASK 1 COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    print("\n📊 DEMONSTRATION SUMMARY:")
    print(f"✓ Single-threaded baseline: {single_time:.2f}s")
    print(f"✓ Multithreaded implementation: {multi_time:.2f}s")
    print(f"✓ Thread identifiers and progress displayed")
    print(f"✓ All worker threads completed successfully")
    print(f"✓ Performance comparison provided")
    print(f"✓ Threading models and concepts explained")
    print(f"✓ Benefits and challenges discussed")
    
    return {
        "single_threaded_time": single_time,
        "multithreaded_time": multi_time,
        "speedup": single_time / multi_time if multi_time > 0 else 0,
        "threads_used": 5,
        "total_primes": sum(result["primes_count"] for result in multi_results.values())
    }

if __name__ == "__main__":
    results = main()
    
    # Additional verification
    print(f"\n🔍 VERIFICATION:")
    print(f"   Speedup achieved: {results['speedup']:.2f}x")
    print(f"   Threads utilized: {results['threads_used']}")
    print(f"   Total computation: {results['total_primes']} prime numbers found")
    
    if results['speedup'] > 1:
        print("   ✅ Multithreading provided measurable benefit")
    else:
        print("   ⚠️  Limited speedup due to Python GIL for CPU-bound tasks")
        print("   💡 Consider I/O-bound tasks for better threading benefits")