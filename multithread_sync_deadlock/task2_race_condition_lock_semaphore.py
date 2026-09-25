#!/usr/bin/env python3
"""
Task 2: Race Condition, Lock and Semaphore
- Create shared data/counter accessible by multiple threads
- Demonstrate race condition without protection
- Show timing-dependent behavior through multiple executions
- Fix race condition using Lock mechanism
- Implement Semaphore-based version
- Compare execution times and correctness
- Analyze synchronization overhead
"""

import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor
import statistics

# Shared data structures
shared_counter = 0
shared_balance = 1000.0
shared_data = {"counter": 0, "operations": []}

# Synchronization primitives
counter_lock = threading.Lock()
balance_lock = threading.Lock()
data_lock = threading.Lock()
semaphore = threading.Semaphore(1)  # Binary semaphore (mutex equivalent)

# Results storage
execution_results = {
    "unprotected": [],
    "lock_based": [],
    "semaphore_based": []
}

def reset_shared_data():
    """Reset all shared data to initial values"""
    global shared_counter, shared_balance, shared_data
    shared_counter = 0
    shared_balance = 1000.0
    shared_data = {"counter": 0, "operations": []}

def worker_unprotected(worker_id, iterations):
    """
    Worker function without synchronization - demonstrates race condition
    """
    global shared_counter, shared_balance, shared_data
    
    print(f"Unprotected Worker-{worker_id} (Thread ID: {threading.get_ident()}) starting...")
    
    for i in range(iterations):
        # Race condition 1: Counter increment
        temp_counter = shared_counter
        time.sleep(0.0001)  # Simulate processing time to increase chance of race
        shared_counter = temp_counter + 1
        
        # Race condition 2: Balance operations
        if i % 2 == 0:
            # Deposit operation
            temp_balance = shared_balance
            time.sleep(0.0001)
            shared_balance = temp_balance + 10.0
        else:
            # Withdrawal operation  
            temp_balance = shared_balance
            time.sleep(0.0001)
            shared_balance = temp_balance - 5.0
        
        # Race condition 3: Shared data structure
        temp_data = shared_data["counter"]
        time.sleep(0.0001)
        shared_data["counter"] = temp_data + 1
        shared_data["operations"].append(f"Worker-{worker_id}-Op-{i}")
    
    print(f"Unprotected Worker-{worker_id} completed")

def worker_lock_based(worker_id, iterations):
    """
    Worker function with Lock-based synchronization
    """
    global shared_counter, shared_balance, shared_data
    
    print(f"Lock-based Worker-{worker_id} (Thread ID: {threading.get_ident()}) starting...")
    
    for i in range(iterations):
        # Protected counter increment
        with counter_lock:
            temp_counter = shared_counter
            time.sleep(0.0001)
            shared_counter = temp_counter + 1
        
        # Protected balance operations
        with balance_lock:
            if i % 2 == 0:
                temp_balance = shared_balance
                time.sleep(0.0001)
                shared_balance = temp_balance + 10.0
            else:
                temp_balance = shared_balance
                time.sleep(0.0001)
                shared_balance = temp_balance - 5.0
        
        # Protected data structure access
        with data_lock:
            temp_data = shared_data["counter"]
            time.sleep(0.0001)
            shared_data["counter"] = temp_data + 1
            shared_data["operations"].append(f"Worker-{worker_id}-Op-{i}")
    
    print(f"Lock-based Worker-{worker_id} completed")

def worker_semaphore_based(worker_id, iterations):
    """
    Worker function with Semaphore-based synchronization
    """
    global shared_counter, shared_balance, shared_data
    
    print(f"Semaphore-based Worker-{worker_id} (Thread ID: {threading.get_ident()}) starting...")
    
    for i in range(iterations):
        # Semaphore-protected operations
        semaphore.acquire()
        try:
            # Counter increment
            temp_counter = shared_counter
            time.sleep(0.0001)
            shared_counter = temp_counter + 1
            
            # Balance operations
            if i % 2 == 0:
                temp_balance = shared_balance
                time.sleep(0.0001)
                shared_balance = temp_balance + 10.0
            else:
                temp_balance = shared_balance
                time.sleep(0.0001)
                shared_balance = temp_balance - 5.0
            
            # Data structure access
            temp_data = shared_data["counter"]
            time.sleep(0.0001)
            shared_data["counter"] = temp_data + 1
            shared_data["operations"].append(f"Worker-{worker_id}-Op-{i}")
            
        finally:
            semaphore.release()
    
    print(f"Semaphore-based Worker-{worker_id} completed")

def run_unprotected_version(num_threads=5, iterations_per_thread=100):
    """
    Run unprotected version to demonstrate race conditions
    """
    print(f"\n{'='*60}")
    print("UNPROTECTED VERSION (Race Condition Demonstration)")
    print(f"{'='*60}")
    
    reset_shared_data()
    start_time = time.time()
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker_unprotected,
            args=(i+1, iterations_per_thread),
            name=f"UnprotectedWorker-{i+1}"
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Calculate expected vs actual results
    expected_counter = num_threads * iterations_per_thread
    expected_balance = 1000.0 + (num_threads * iterations_per_thread * 2.5)  # +10-5 = +5 per 2 ops = +2.5 per op
    expected_operations = num_threads * iterations_per_thread
    
    print(f"\nResults Analysis:")
    print(f"Expected counter value: {expected_counter}")
    print(f"Actual counter value:   {shared_counter}")
    print(f"Counter difference:     {abs(expected_counter - shared_counter)}")
    
    print(f"Expected balance:       {expected_balance:.2f}")
    print(f"Actual balance:         {shared_balance:.2f}")
    print(f"Balance difference:     {abs(expected_balance - shared_balance):.2f}")
    
    print(f"Expected operations:    {expected_operations}")
    print(f"Actual operations:      {shared_data['counter']}")
    print(f"Operations difference:  {abs(expected_operations - shared_data['counter'])}")
    
    print(f"Execution time:         {execution_time:.4f} seconds")
    
    # Check for race condition
    race_detected = (shared_counter != expected_counter or 
                    abs(shared_balance - expected_balance) > 0.01 or
                    shared_data['counter'] != expected_operations)
    
    if race_detected:
        print("🚨 RACE CONDITION DETECTED! Results are inconsistent.")
    else:
        print("✅ No race condition detected in this run (may vary).")
    
    return {
        "execution_time": execution_time,
        "expected": {"counter": expected_counter, "balance": expected_balance, "operations": expected_operations},
        "actual": {"counter": shared_counter, "balance": shared_balance, "operations": shared_data['counter']},
        "race_detected": race_detected
    }

def run_lock_based_version(num_threads=5, iterations_per_thread=100):
    """
    Run Lock-based version with proper synchronization
    """
    print(f"\n{'='*60}")
    print("LOCK-BASED VERSION (Proper Synchronization)")
    print(f"{'='*60}")
    
    reset_shared_data()
    start_time = time.time()
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker_lock_based,
            args=(i+1, iterations_per_thread),
            name=f"LockWorker-{i+1}"
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Calculate expected vs actual results
    expected_counter = num_threads * iterations_per_thread
    expected_balance = 1000.0 + (num_threads * iterations_per_thread * 2.5)
    expected_operations = num_threads * iterations_per_thread
    
    print(f"\nResults Analysis:")
    print(f"Expected counter value: {expected_counter}")
    print(f"Actual counter value:   {shared_counter}")
    print(f"Counter difference:     {abs(expected_counter - shared_counter)}")
    
    print(f"Expected balance:       {expected_balance:.2f}")
    print(f"Actual balance:         {shared_balance:.2f}")
    print(f"Balance difference:     {abs(expected_balance - shared_balance):.2f}")
    
    print(f"Expected operations:    {expected_operations}")
    print(f"Actual operations:      {shared_data['counter']}")
    print(f"Operations difference:  {abs(expected_operations - shared_data['counter'])}")
    
    print(f"Execution time:         {execution_time:.4f} seconds")
    
    # Verify correctness
    correct = (shared_counter == expected_counter and 
              abs(shared_balance - expected_balance) < 0.01 and
              shared_data['counter'] == expected_operations)
    
    if correct:
        print("✅ SYNCHRONIZATION SUCCESSFUL! All results are correct.")
    else:
        print("❌ Synchronization failed - unexpected results.")
    
    return {
        "execution_time": execution_time,
        "expected": {"counter": expected_counter, "balance": expected_balance, "operations": expected_operations},
        "actual": {"counter": shared_counter, "balance": shared_balance, "operations": shared_data['counter']},
        "correct": correct
    }

def run_semaphore_based_version(num_threads=5, iterations_per_thread=100):
    """
    Run Semaphore-based version with semaphore synchronization
    """
    print(f"\n{'='*60}")
    print("SEMAPHORE-BASED VERSION (Semaphore Synchronization)")
    print(f"{'='*60}")
    
    reset_shared_data()
    start_time = time.time()
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker_semaphore_based,
            args=(i+1, iterations_per_thread),
            name=f"SemaphoreWorker-{i+1}"
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Calculate expected vs actual results
    expected_counter = num_threads * iterations_per_thread
    expected_balance = 1000.0 + (num_threads * iterations_per_thread * 2.5)
    expected_operations = num_threads * iterations_per_thread
    
    print(f"\nResults Analysis:")
    print(f"Expected counter value: {expected_counter}")
    print(f"Actual counter value:   {shared_counter}")
    print(f"Counter difference:     {abs(expected_counter - shared_counter)}")
    
    print(f"Expected balance:       {expected_balance:.2f}")
    print(f"Actual balance:         {shared_balance:.2f}")
    print(f"Balance difference:     {abs(expected_balance - shared_balance):.2f}")
    
    print(f"Expected operations:    {expected_operations}")
    print(f"Actual operations:      {shared_data['counter']}")
    print(f"Operations difference:  {abs(expected_operations - shared_data['counter'])}")
    
    print(f"Execution time:         {execution_time:.4f} seconds")
    
    # Verify correctness
    correct = (shared_counter == expected_counter and 
              abs(shared_balance - expected_balance) < 0.01 and
              shared_data['counter'] == expected_operations)
    
    if correct:
        print("✅ SEMAPHORE SYNCHRONIZATION SUCCESSFUL! All results are correct.")
    else:
        print("❌ Semaphore synchronization failed - unexpected results.")
    
    return {
        "execution_time": execution_time,
        "expected": {"counter": expected_counter, "balance": expected_balance, "operations": expected_operations},
        "actual": {"counter": shared_counter, "balance": shared_balance, "operations": shared_data['counter']},
        "correct": correct
    }

def demonstrate_timing_dependency(runs=5):
    """
    Demonstrate timing-dependent behavior by running unprotected version multiple times
    """
    print(f"\n{'='*70}")
    print("TIMING-DEPENDENT BEHAVIOR DEMONSTRATION")
    print(f"{'='*70}")
    
    print(f"Running unprotected version {runs} times to show variability...")
    
    results = []
    for run in range(runs):
        print(f"\n--- Run {run + 1} ---")
        result = run_unprotected_version(num_threads=3, iterations_per_thread=50)
        results.append(result)
    
    print(f"\n{'='*50}")
    print("TIMING DEPENDENCY ANALYSIS")
    print(f"{'='*50}")
    
    print(f"{'Run':<5} {'Counter':<10} {'Balance':<12} {'Operations':<12} {'Race?':<8} {'Time(s)':<10}")
    print("-" * 65)
    
    counter_values = []
    balance_values = []
    operation_values = []
    race_count = 0
    
    for i, result in enumerate(results):
        counter_val = result['actual']['counter']
        balance_val = result['actual']['balance']
        ops_val = result['actual']['operations']
        race = "Yes" if result['race_detected'] else "No"
        exec_time = result['execution_time']
        
        print(f"{i+1:<5} {counter_val:<10} {balance_val:<12.2f} {ops_val:<12} {race:<8} {exec_time:<10.4f}")
        
        counter_values.append(counter_val)
        balance_values.append(balance_val)
        operation_values.append(ops_val)
        
        if result['race_detected']:
            race_count += 1
    
    expected_counter = results[0]['expected']['counter']
    expected_balance = results[0]['expected']['balance']
    expected_ops = results[0]['expected']['operations']
    
    print(f"\nExpected values:")
    print(f"Counter: {expected_counter}, Balance: {expected_balance:.2f}, Operations: {expected_ops}")
    
    print(f"\nVariability Analysis:")
    print(f"Counter values range: {min(counter_values)} - {max(counter_values)}")
    print(f"Balance values range: {min(balance_values):.2f} - {max(balance_values):.2f}")
    print(f"Operations range: {min(operation_values)} - {max(operation_values)}")
    print(f"Race conditions detected: {race_count}/{runs} runs ({race_count/runs*100:.1f}%)")
    
    if len(set(counter_values)) > 1 or len(set(balance_values)) > 1 or len(set(operation_values)) > 1:
        print("🚨 TIMING-DEPENDENT BEHAVIOR CONFIRMED!")
        print("   Results vary between runs due to race conditions.")
    else:
        print("ℹ️  No variation detected in this test (may need more iterations or threads)")

def compare_all_versions():
    """
    Compare execution time and correctness of all three versions
    """
    print(f"\n{'='*70}")
    print("COMPREHENSIVE COMPARISON")
    print(f"{'='*70}")
    
    num_threads = 5
    iterations = 100
    
    print(f"Test configuration: {num_threads} threads, {iterations} iterations each")
    
    # Run each version
    unprotected_result = run_unprotected_version(num_threads, iterations)
    lock_result = run_lock_based_version(num_threads, iterations)
    semaphore_result = run_semaphore_based_version(num_threads, iterations)
    
    # Comparison table
    print(f"\n{'='*80}")
    print("PERFORMANCE AND CORRECTNESS COMPARISON")
    print(f"{'='*80}")
    
    print(f"{'Version':<20} {'Exec Time(s)':<15} {'Counter':<10} {'Balance':<12} {'Correct?':<10}")
    print("-" * 80)
    
    # Unprotected
    unp_correct = "No" if unprotected_result['race_detected'] else "Maybe"
    print(f"{'Unprotected':<20} {unprotected_result['execution_time']:<15.4f} "
          f"{unprotected_result['actual']['counter']:<10} "
          f"{unprotected_result['actual']['balance']:<12.2f} {unp_correct:<10}")
    
    # Lock-based
    lock_correct = "Yes" if lock_result['correct'] else "No"
    print(f"{'Lock-based':<20} {lock_result['execution_time']:<15.4f} "
          f"{lock_result['actual']['counter']:<10} "
          f"{lock_result['actual']['balance']:<12.2f} {lock_correct:<10}")
    
    # Semaphore-based
    sem_correct = "Yes" if semaphore_result['correct'] else "No"
    print(f"{'Semaphore-based':<20} {semaphore_result['execution_time']:<15.4f} "
          f"{semaphore_result['actual']['counter']:<10} "
          f"{semaphore_result['actual']['balance']:<12.2f} {sem_correct:<10}")
    
    # Overhead analysis
    base_time = unprotected_result['execution_time']
    lock_overhead = ((lock_result['execution_time'] - base_time) / base_time) * 100
    sem_overhead = ((semaphore_result['execution_time'] - base_time) / base_time) * 100
    
    print(f"\nSynchronization Overhead Analysis:")
    print(f"Lock overhead:      {lock_overhead:+.1f}% compared to unprotected")
    print(f"Semaphore overhead: {sem_overhead:+.1f}% compared to unprotected")
    
    if lock_overhead < sem_overhead:
        print("→ Lock-based synchronization is more efficient")
    elif sem_overhead < lock_overhead:
        print("→ Semaphore-based synchronization is more efficient")
    else:
        print("→ Both synchronization methods have similar overhead")

def explain_concepts():
    """
    Brief explanation of race conditions, locks, and semaphores
    """
    print(f"\n{'='*60}")
    print("SYNCHRONIZATION CONCEPTS SUMMARY")
    print(f"{'='*60}")
    
    print("\n🚨 RACE CONDITIONS:")
    print("   • Multiple threads accessing shared data simultaneously")
    print("   • Results depend on thread timing and execution order")
    print("   • Can cause data corruption and inconsistent state")
    print("   • Demonstrated by varying results across runs")
    
    print("\n🔒 LOCKS (MUTEX):")
    print("   • Mutual exclusion mechanism")
    print("   • Only one thread can hold lock at a time")
    print("   • Ensures atomic access to critical sections")
    print("   • Low overhead, fast performance")
    
    print("\n🚦 SEMAPHORES:")
    print("   • Counting synchronization primitive")
    print("   • Binary semaphore = mutex equivalent")
    print("   • Can control access to multiple resources")
    print("   • Slightly higher overhead than locks")
    
    print("\n💡 KEY INSIGHTS:")
    print("   • Synchronization trades performance for correctness")
    print("   • Unprotected code is fastest but unreliable")
    print("   • Proper synchronization ensures consistent results")
    print("   • Choose mechanism based on use case requirements")

def main():
    """
    Main function to demonstrate race conditions, locks, and semaphores
    """
    print("="*70)
    print("TASK 2: RACE CONDITION, LOCK AND SEMAPHORE")
    print("="*70)
    
    print("\nDemonstration Overview:")
    print("• Shared data: Counter, Balance, Operations list")
    print("• Multiple threads performing concurrent updates")
    print("• Comparison of unprotected vs synchronized versions")
    print("• Performance and correctness analysis")
    
    # Demonstrate timing-dependent behavior
    demonstrate_timing_dependency(runs=3)
    
    # Compare all versions
    compare_all_versions()
    
    # Explain concepts
    explain_concepts()
    
    print(f"\n{'='*70}")
    print("TASK 2 COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    print("\n📊 DEMONSTRATION SUMMARY:")
    print("✓ Race conditions demonstrated with timing dependency")
    print("✓ Lock-based synchronization implemented and tested")
    print("✓ Semaphore-based synchronization implemented and tested") 
    print("✓ Same workload used for all versions")
    print("✓ Execution times measured and compared")
    print("✓ Correctness and overhead analysis provided")
    print("✓ Synchronization concepts explained")

if __name__ == "__main__":
    main()