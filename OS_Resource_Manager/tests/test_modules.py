"""
Test Cases for OS Resource Manager Modules
Tests scheduling, memory, and deadlock modules
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from scheduler import ProcessScheduler
from memory import MemoryManager
from deadlock import DeadlockHandler

def test_scheduler():
    """Test Process Scheduling Module"""
    print("\n" + "="*60)
    print("TEST 1: PROCESS SCHEDULING MODULE")
    print("="*60)
    
    scheduler = ProcessScheduler()
    
    # Test 1: Load sample data
    print("\n✓ Test 1.1: Load sample data")
    scheduler.load_sample_data()
    assert scheduler.has_processes(), "Failed: No processes loaded"
    print(f"  Loaded {len(scheduler.processes)} processes")
    
    # Test 2: FCFS algorithm
    print("\n✓ Test 1.2: FCFS Algorithm")
    result = scheduler.fcfs()
    assert result['avg_waiting_time'] >= 0, "Failed: Invalid waiting time"
    print(f"  Avg Waiting Time: {result['avg_waiting_time']:.2f}")
    print(f"  Avg Turnaround Time: {result['avg_turnaround_time']:.2f}")
    
    # Test 3: SJF algorithm
    print("\n✓ Test 1.3: SJF Algorithm")
    result = scheduler.sjf()
    assert result['avg_waiting_time'] >= 0, "Failed: Invalid waiting time"
    print(f"  Avg Waiting Time: {result['avg_waiting_time']:.2f}")
    
    # Test 4: Round Robin
    print("\n✓ Test 1.4: Round Robin Algorithm")
    result = scheduler.round_robin(2)
    assert result['avg_waiting_time'] >= 0, "Failed: Invalid waiting time"
    print(f"  Avg Waiting Time: {result['avg_waiting_time']:.2f}")
    
    print("\n✅ All scheduling tests passed!")

def test_memory():
    """Test Memory Management Module"""
    print("\n" + "="*60)
    print("TEST 2: MEMORY MANAGEMENT MODULE")
    print("="*60)
    
    memory = MemoryManager()
    
    # Test 1: Load sample data
    print("\n✓ Test 2.1: Load sample data")
    memory.load_sample_data()
    assert memory.has_data(), "Failed: No memory data loaded"
    print(f"  Loaded {len(memory.blocks)} blocks and {len(memory.processes)} processes")
    
    # Test 2: First Fit
    print("\n✓ Test 2.2: First Fit Algorithm")
    result = memory.first_fit()
    assert result['total_memory'] > 0, "Failed: Invalid total memory"
    print(f"  Allocated: {result['allocated_memory']} KB")
    print(f"  Success Rate: {result['success_rate']:.2f}%")
    
    # Test 3: Best Fit
    print("\n✓ Test 2.3: Best Fit Algorithm")
    result = memory.best_fit()
    assert result['success_rate'] >= 0, "Failed: Invalid success rate"
    print(f"  Fragmentation: {result['external_fragmentation']} KB")
    
    # Test 4: Worst Fit
    print("\n✓ Test 2.4: Worst Fit Algorithm")
    result = memory.worst_fit()
    assert result['allocated_memory'] >= 0, "Failed: Invalid allocation"
    print(f"  Free Memory: {result['free_memory']} KB")
    
    print("\n✅ All memory tests passed!")

def test_deadlock():
    """Test Deadlock Handling Module"""
    print("\n" + "="*60)
    print("TEST 3: DEADLOCK HANDLING MODULE")
    print("="*60)
    
    deadlock = DeadlockHandler()
    
    # Test 1: Load sample data
    print("\n✓ Test 3.1: Load sample data")
    deadlock.load_sample_data()
    assert deadlock.has_data(), "Failed: No deadlock data loaded"
    print(f"  Loaded {deadlock.num_processes} processes and {deadlock.num_resources} resources")
    
    # Test 2: Banker's Algorithm
    print("\n✓ Test 3.2: Banker's Algorithm")
    result = deadlock.bankers_algorithm()
    print(f"  Safe State: {result['is_safe']}")
    if result['is_safe']:
        print(f"  Safe Sequence: {' → '.join(result['safe_sequence'])}")
    
    # Test 3: Need Matrix Calculation
    print("\n✓ Test 3.3: Need Matrix Calculation")
    assert len(deadlock.need) == deadlock.num_processes, "Failed: Invalid need matrix"
    print(f"  Need matrix size: {len(deadlock.need)} x {len(deadlock.need[0])}")
    
    # Test 4: Deadlock Detection
    print("\n✓ Test 3.4: Deadlock Detection")
    result = deadlock.detect_deadlock()
    print(f"  Deadlock Exists: {result['deadlock_exists']}")
    
    print("\n✅ All deadlock tests passed!")

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "="*60)
    print("TEST 4: EDGE CASES AND ERROR HANDLING")
    print("="*60)
    
    # Test 1: Empty process list
    print("\n✓ Test 4.1: Empty process list")
    scheduler = ProcessScheduler()
    assert not scheduler.has_processes(), "Failed: Should have no processes"
    print("  Correctly handles empty list")
    
    # Test 2: Single process
    print("\n✓ Test 4.2: Single process")
    scheduler.set_processes([{'pid': 'P1', 'arrival': 0, 'burst': 5, 'priority': 1}])
    result = scheduler.fcfs()
    assert result['avg_waiting_time'] == 0, "Failed: Single process should have 0 wait"
    print("  Correctly handles single process")
    
    # Test 3: Large memory request
    print("\n✓ Test 4.3: Insufficient memory")
    memory = MemoryManager()
    memory.set_data([100, 200], [{'pid': 'P1', 'size': 500}])
    result = memory.first_fit()
    assert result['success_rate'] < 100, "Failed: Should not allocate"
    print("  Correctly handles insufficient memory")
    
    print("\n✅ All edge case tests passed!")

def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*70)
    print("        OS RESOURCE MANAGER - MODULE TESTING")
    print("="*70)
    
    try:
        test_scheduler()
        test_memory()
        test_deadlock()
        test_edge_cases()
        
        print("\n" + "="*70)
        print("         ✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("="*70)
        print("\nTest Summary:")
        print("  ✓ Process Scheduling: 4/4 tests passed")
        print("  ✓ Memory Management: 4/4 tests passed")
        print("  ✓ Deadlock Handling: 4/4 tests passed")
        print("  ✓ Edge Cases: 3/3 tests passed")
        print("\n  Total: 15/15 tests passed (100%)")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
