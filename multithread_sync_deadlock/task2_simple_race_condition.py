#!/usr/bin/env python3
"""
Task 2: Race Condition, Lock and Semaphore - Simple Version
- Simple shared counter demonstration
- Show race condition without protection
- Fix with Lock and Semaphore
- Easy to understand results
"""

import threading
import time

# Shared data
shared_counter = 0

# Synchronization objects
counter_lock = threading.Lock()
semaphore = threading.Semaphore(1)

def reset_counter():
    """Reset shared counter"""
    global shared_counter
    shared_counter = 0

def worker_unprotected(worker_id, increments):
    """Worker without synchronization - causes race condition"""
    global shared_counter
    
    print(f"Worker-{worker_id} starting (Thread ID: {threading.get_ident()})")
    
    for i in range(increments):
        # Race condition: read-modify-write without protection
        temp = shared_counter
        time.sleep(0.001)  # Small delay to increase race chance
        shared_counter = temp + 1
    
    print(f"Worker-{worker_id} completed")

def worker_with_lock(worker_id, increments):
    """Worker with Lock protection"""
    global shared_counter
    
    print(f"Lock Worker-{worker_id} starting (Thread ID: {threading.get_ident()})")
    
    for i in range(increments):
        # Protected with lock
        with counter_lock:
            temp = shared_counter
            time.sleep(0.001)
            shared_counter = temp + 1
    
    print(f"Lock Worker-{worker_id} completed")

def worker_with_semaphore(worker_id, increments):
    """Worker with Semaphore protection"""
    global shared_counter
    
    print(f"Semaphore Worker-{worker_id} starting (Thread ID: {threading.get_ident()})")
    
    for i in range(increments):
        # Protected with semaphore
        semaphore.acquire()
        try:
            temp = shared_counter
            time.sleep(0.001)
            shared_counter = temp + 1
        finally:
            semaphore.release()
    
    print(f"Semaphore Worker-{worker_id} completed")
def test_unprotected():
    """Test unprotected version"""
    print("\n" + "="*50)
    print("UNPROTECTED VERSION (Race Condition)")
    print("="*50)
    
    reset_counter()
    threads = []
    num_threads = 3
    increments_each = 10
    
    start_time = time.time()
    
    # Create threads
    for i in range(num_threads):
        thread = threading.Thread(target=worker_unprotected, args=(i+1, increments_each))
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    expected = num_threads * increments_each
    actual = shared_counter
    
    print(f"\nResults:")
    print(f"Expected counter: {expected}")
    print(f"Actual counter:   {actual}")
    print(f"Difference:       {abs(expected - actual)}")
    print(f"Execution time:   {end_time - start_time:.3f}s")
    
    if actual != expected:
        print("🚨 RACE CONDITION DETECTED!")
    else:
        print("✅ No race detected (may vary in different runs)")
    
    return end_time - start_time, actual, expected

def test_with_lock():
    """Test lock-based version"""
    print("\n" + "="*50)
    print("LOCK-BASED VERSION (Protected)")
    print("="*50)
    
    reset_counter()
    threads = []
    num_threads = 3
    increments_each = 10
    
    start_time = time.time()
    
    # Create threads
    for i in range(num_threads):
        thread = threading.Thread(target=worker_with_lock, args=(i+1, increments_each))
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    expected = num_threads * increments_each
    actual = shared_counter
    
    print(f"\nResults:")
    print(f"Expected counter: {expected}")
    print(f"Actual counter:   {actual}")
    print(f"Difference:       {abs(expected - actual)}")
    print(f"Execution time:   {end_time - start_time:.3f}s")
    
    if actual == expected:
        print("✅ LOCK SYNCHRONIZATION SUCCESSFUL!")
    else:
        print("❌ Lock failed")
    
    return end_time - start_time, actual, expected
def test_with_semaphore():
    """Test semaphore-based version"""
    print("\n" + "="*50)
    print("SEMAPHORE-BASED VERSION (Protected)")
    print("="*50)
    
    reset_counter()
    threads = []
    num_threads = 3
    increments_each = 10
    
    start_time = time.time()
    
    # Create threads
    for i in range(num_threads):
        thread = threading.Thread(target=worker_with_semaphore, args=(i+1, increments_each))
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    expected = num_threads * increments_each
    actual = shared_counter
    
    print(f"\nResults:")
    print(f"Expected counter: {expected}")
    print(f"Actual counter:   {actual}")
    print(f"Difference:       {abs(expected - actual)}")
    print(f"Execution time:   {end_time - start_time:.3f}s")
    
    if actual == expected:
        print("✅ SEMAPHORE SYNCHRONIZATION SUCCESSFUL!")
    else:
        print("❌ Semaphore failed")
    
    return end_time - start_time, actual, expected

def show_timing_dependency():
    """Show that unprotected version gives different results"""
    print("\n" + "="*50)
    print("TIMING DEPENDENCY DEMONSTRATION")
    print("="*50)
    
    print("Running unprotected version 3 times...")
    
    results = []
    for run in range(3):
        print(f"\n--- Run {run + 1} ---")
        time_taken, actual, expected = test_unprotected()
        results.append(actual)
    
    print(f"\n" + "="*30)
    print("TIMING DEPENDENCY RESULTS")
    print("="*30)
    print(f"Expected result: 30")
    print(f"Run 1 result: {results[0]}")
    print(f"Run 2 result: {results[1]}")
    print(f"Run 3 result: {results[2]}")
    
    if len(set(results)) > 1:
        print("🚨 DIFFERENT RESULTS ACROSS RUNS!")
        print("   This proves timing-dependent behavior.")
    else:
        print("ℹ️  Same results (race may not occur every time)")
def compare_all_versions():
    """Compare all three versions"""
    print("\n" + "="*50)
    print("FINAL COMPARISON")
    print("="*50)
    
    # Test each version
    unprotected_time, unp_actual, expected = test_unprotected()
    lock_time, lock_actual, expected = test_with_lock()
    sem_time, sem_actual, expected = test_with_semaphore()
    
    print(f"\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    print(f"{'Version':<15} {'Time(s)':<10} {'Result':<10} {'Correct?':<10}")
    print("-" * 50)
    print(f"{'Unprotected':<15} {unprotected_time:<10.3f} {unp_actual:<10} {'No' if unp_actual != expected else 'Maybe':<10}")
    print(f"{'Lock-based':<15} {lock_time:<10.3f} {lock_actual:<10} {'Yes' if lock_actual == expected else 'No':<10}")
    print(f"{'Semaphore':<15} {sem_time:<10.3f} {sem_actual:<10} {'Yes' if sem_actual == expected else 'No':<10}")
    
    print(f"\nOverhead Analysis:")
    print(f"Lock overhead: {((lock_time - unprotected_time) / unprotected_time * 100):+.1f}%")
    print(f"Semaphore overhead: {((sem_time - unprotected_time) / unprotected_time * 100):+.1f}%")

def explain_concepts():
    """Simple explanation of concepts"""
    print(f"\n" + "="*40)
    print("SIMPLE EXPLANATION")
    print("="*40)
    
    print("\n🚨 RACE CONDITION:")
    print("   Multiple threads change shared data at same time")
    print("   Results become unpredictable and wrong")
    print("   Like two people editing same document together")
    
    print("\n🔒 LOCK:")
    print("   Only one thread can use shared data at a time")
    print("   Other threads must wait their turn")
    print("   Guarantees correct results")
    
    print("\n🚦 SEMAPHORE:")
    print("   Similar to lock but more flexible")
    print("   Can control multiple resources")
    print("   Binary semaphore = lock equivalent")
    
    print("\n💡 KEY POINT:")
    print("   Synchronization makes code slower but correct")
    print("   Always use synchronization for shared data")

def main():
    """Main function"""
    print("="*50)
    print("SIMPLE RACE CONDITION DEMO")
    print("="*50)
    
    print("Demonstration: 3 threads, each adds 10 to counter")
    print("Expected result: 30")
    
    # Show timing dependency
    show_timing_dependency()
    
    # Compare all versions
    compare_all_versions()
    
    # Simple explanation
    explain_concepts()
    
    print(f"\n" + "="*50)
    print("DEMO COMPLETED!")
    print("="*50)
    print("✓ Race condition demonstrated")
    print("✓ Lock protection working")
    print("✓ Semaphore protection working")
    print("✓ Performance comparison shown")

if __name__ == "__main__":
    main()