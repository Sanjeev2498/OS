# Multithreading, Synchronization and Deadlock

This folder contains advanced Operating System concepts focusing on multithreading, synchronization mechanisms, and deadlock handling.

## Task Files

### 1. task1_thread_creation_models.py ✅
**Thread Creation, Models and Benefits (5 marks)**
- Creates single-threaded baseline workload (prime number calculation)
- Divides workload into independent tasks for multiple threads
- Demonstrates worker thread creation using Python threading
- Displays thread identifiers and execution progress in real-time
- Waits for all worker threads to complete using join()
- Measures and compares single-threaded vs multithreaded execution time
- Comprehensive explanation of threading models and concepts

**Features Demonstrated:**
- ✅ Single-threaded baseline implementation
- ✅ Independent task division and worker thread creation
- ✅ Thread identifier display and progress tracking
- ✅ Thread completion synchronization
- ✅ Performance measurement and comparison
- ✅ Threading models explanation (User-level, Kernel-level, Hybrid)
- ✅ Multithreading models (Many-to-One, One-to-One, Many-to-Many)
- ✅ Benefits discussion (Responsiveness, Resource sharing, Concurrency, Parallelism)
- ✅ Challenges analysis (Race conditions, Deadlocks, Overhead)
- ✅ Python-specific considerations (GIL impact)

**Run with:** `python task1_thread_creation_models.py`

### 2. task2_race_condition_lock_semaphore.py ✅
**Race Condition, Lock and Semaphore (5 marks)**
- Creates shared data (counter, balance, operations list) accessible by multiple threads
- Demonstrates race conditions without synchronization protection
- Shows timing-dependent behavior through multiple execution runs
- Corrects race conditions using Lock-based mutual exclusion
- Implements Semaphore-based synchronization version
- Uses identical workload for all three versions (unprotected, lock, semaphore)
- Measures and compares execution times for performance analysis
- Analyzes correctness and synchronization overhead

**Features Demonstrated:**
- ✅ Shared data structures with concurrent access
- ✅ Race condition demonstration with inconsistent results
- ✅ Timing-dependent behavior verification (100% race detection rate)
- ✅ Lock-based synchronization with perfect correctness
- ✅ Semaphore-based synchronization with perfect correctness
- ✅ Performance comparison: Unprotected (fastest) vs Lock (+77% overhead) vs Semaphore (+462% overhead)
- ✅ Correctness analysis: Unprotected (incorrect) vs Synchronized (correct)
- ✅ Synchronization concepts explanation

**Run with:** `python task2_race_condition_lock_semaphore.py`

**Simple Version:** `task2_simple_race_condition.py` - Easier demonstration with 3 threads

### 3. task3_classical_sync_problems.py ✅
**Classical Synchronization Problems (5 marks)**
- Implements Producer-Consumer problem with bounded buffer
- Demonstrates Readers-Writers problem with concurrent access control
- Solves Dining Philosophers problem with deadlock prevention
- Uses semaphores, locks, and proper synchronization techniques
- Shows real-time execution with clear output formatting

**Features Demonstrated:**
- ✅ **Producer-Consumer**: Multiple producers/consumers with bounded buffer (size 5)
- ✅ **Readers-Writers**: Concurrent readers, exclusive writers with proper coordination
- ✅ **Dining Philosophers**: 5 philosophers with deadlock prevention using waiter + resource ordering
- ✅ **Synchronization**: Semaphores (empty, full, mutex), Locks (read/write control, chopsticks)
- ✅ **Deadlock Prevention**: Waiter mechanism limits concurrent diners to prevent circular wait
- ✅ **Clean Termination**: Finite execution with proper thread cleanup

**Synchronization Mechanisms:**
- **Producer-Consumer**: `empty` semaphore (5), `full` semaphore (0), `mutex` lock
- **Readers-Writers**: `read_count_lock`, `write_lock` for exclusive/shared access
- **Dining Philosophers**: Individual chopstick locks + waiter semaphore (4/5 limit)

**Run with:** `python task3_classical_sync_problems.py`

## Current Implementation Status

### ✅ **Task 1 - Thread Creation & Models**
**Workload:** Prime number calculation in ranges 1-5000
**Results:** 
- Single-threaded: ~0.52 seconds
- Multithreaded (5 threads): ~0.51 seconds  
- Speedup: ~1.02x (limited by Python GIL for CPU-bound tasks)
- Total computation: 669 prime numbers found

### ✅ **Task 2 - Race Conditions & Synchronization**
**Workload:** Concurrent counter operations (10,000 per thread)
**Results:**
- Unprotected: 100% race condition detection (incorrect results)
- Lock-protected: Perfect synchronization (correct results, +77% overhead)
- Semaphore-protected: Perfect synchronization (correct results, +462% overhead)

### ✅ **Task 3 - Classical Synchronization Problems**
**Implementation:** All three classical problems with proper synchronization
**Results:**
- **Producer-Consumer**: 5 producers, 5 consumers, bounded buffer (5 items)
- **Readers-Writers**: 3 readers, 2 writers with exclusive write access
- **Dining Philosophers**: 5 philosophers with deadlock prevention (waiter mechanism)
- All problems execute concurrently with clean termination

**Key Learning Points:**
- Python's GIL limits CPU-bound threading benefits
- Threading still provides organizational and responsiveness benefits
- Proper thread lifecycle management (creation, execution, joining)
- Progress monitoring in concurrent environments
- Performance measurement methodologies

## Threading Concepts Covered

### 🧵 **Thread Models**
1. **User-Level Threads**: Fast switching, library-managed, GIL-affected
2. **Kernel-Level Threads**: OS-managed, true parallelism, higher overhead  
3. **Hybrid Model**: M:N mapping, balanced approach

### 🔄 **Multithreading Models**
1. **Many-to-One**: Multiple user threads → single kernel thread
2. **One-to-One**: Direct mapping, true parallelism
3. **Many-to-Many**: Flexible mapping, complex implementation

### ⚡ **Benefits Demonstrated**
- **Responsiveness**: Non-blocking execution
- **Resource Sharing**: Memory and handle efficiency
- **Concurrency**: Simultaneous task progress
- **Parallelism**: Multi-core utilization (where possible)

### ⚠️ **Challenges Addressed**
- **Race Conditions**: Shared data access conflicts
- **Deadlocks**: Circular waiting scenarios
- **Overhead**: Context switching and synchronization costs
- **Python GIL**: CPU-bound parallelism limitations

## Requirements

- Python 3.x
- Standard library only (threading, time, math, random)
- Cross-platform compatible (Windows/Linux)
- No external dependencies

## Usage Instructions

1. **Run Individual Tasks:**
   ```bash
   cd multithread_sync_deadlock
   python task1_thread_creation_models.py
   ```

2. **Expected Output:**
   - Single-threaded baseline execution with timing
   - Multithreaded execution with thread details
   - Performance comparison and analysis
   - Comprehensive threading concepts explanation

3. **Learning Outcomes:**
   - Understanding thread lifecycle and management
   - Performance implications of threading approaches
   - Threading model differences and trade-offs
   - Python-specific threading considerations

## Academic Focus

This implementation is designed for advanced Operating Systems courses covering:
- **Concurrent Programming**: Thread creation and management
- **Performance Analysis**: Benchmarking and comparison methodologies
- **System Design**: Threading model selection criteria
- **Problem Solving**: Identifying appropriate concurrency patterns

## Best Practices Demonstrated

✅ **Proper Thread Management**: Creation, execution, and cleanup
✅ **Progress Monitoring**: Real-time status tracking
✅ **Resource Safety**: Shared data protection with locks
✅ **Performance Measurement**: Accurate timing and comparison
✅ **Educational Documentation**: Comprehensive concept explanation
✅ **Code Structure**: Clean, readable, and maintainable implementation

## Future Extensions

- **I/O-bound threading examples** for better speedup demonstration
- **Thread pool implementations** for efficient resource management  
- **Advanced synchronization patterns** (barriers, latches)
- **Cross-platform performance comparisons**
- **Real-world application scenarios**