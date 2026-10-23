# Final Submission: Multithreading, Synchronization and Deadlock

**Course:** Operating Systems  
**Lab:** Advanced Threading Concepts  
**Total Marks:** 20 (4 tasks × 5 marks each)

## ✅ Task 1: Thread Creation, Models and Benefits (5 marks)
**File:** `task1_thread_creation_models.py`

### Implementation Features:
- Single-threaded baseline (prime calculation 1-5000)
- Multithreaded implementation with 5 worker threads
- Real-time progress monitoring with thread IDs
- Performance comparison and timing analysis
- Comprehensive threading concepts explanation

### Results:
- Single-threaded: ~0.52 seconds (669 primes found)
- Multithreaded: ~0.51 seconds (669 primes found)
- Demonstrates proper thread lifecycle management

### Concepts Covered:
- User-level vs Kernel-level threads
- Threading models (Many-to-One, One-to-One, Many-to-Many)
- Benefits: Responsiveness, Resource sharing, Concurrency, Parallelism
- Python GIL implications for CPU-bound tasks

---

## ✅ Task 2: Race Condition, Lock and Semaphore (5 marks)
**Files:** 
- `task2_race_condition_lock_semaphore.py` (comprehensive)
- `task2_simple_race_condition.py` (simplified version)

### Implementation Features:
- Race condition demonstration (100% detection rate)
- Lock-based synchronization with mutex protection
- Semaphore-based synchronization for resource management
- Performance comparison between all three approaches
- Shared data protection mechanisms

### Results:
- **Unprotected:** Race conditions with incorrect results
- **Lock-protected:** Perfect synchronization (+77% overhead)
- **Semaphore-protected:** Perfect synchronization (+462% overhead)

### Synchronization Mechanisms:
- Threading.Lock for mutual exclusion
- Threading.Semaphore for counting semaphore
- Proper critical section protection

---

## ✅ Task 3: Classical Synchronization Problems (5 marks)
**File:** `task3_classical_sync_problems.py`

### Three Classical Problems Implemented:

#### 1. Producer-Consumer Problem
- **Setup:** 5 producers, 5 consumers, bounded buffer (size 5)
- **Synchronization:** `empty` semaphore, `full` semaphore, `mutex` lock
- **Features:** Real-time buffer monitoring, proper blocking/unblocking

#### 2. Readers-Writers Problem  
- **Setup:** 3 readers, 2 writers with shared data access
- **Synchronization:** `read_count_lock`, `write_lock` for exclusive control
- **Features:** Multiple concurrent readers, exclusive writer access

#### 3. Dining Philosophers Problem
- **Setup:** 5 philosophers with chopsticks as shared resources
- **Deadlock Prevention:** Waiter semaphore (limit 4/5) + resource ordering
- **Features:** No deadlock, no starvation, proper resource management

### Synchronization Techniques:
- **Semaphores:** For counting and binary synchronization
- **Locks:** For mutual exclusion and critical sections
- **Deadlock Prevention:** Waiter mechanism prevents circular wait

---

## ✅ Task 4: Deadlock Handling and Banker's Algorithm (5 marks)
**File:** `task4_deadlock_bankers_algorithm.py`

### Implementation Features:
- Controlled circular-wait deadlock scenario (4 threads, 4 resources)
- Identification of all four necessary deadlock conditions
- Deadlock prevention using resource ordering strategy
- Complete Banker's Algorithm implementation
- Need matrix calculation from Allocation and Maximum matrices
- Safe state detection with safe sequence generation
- Unsafe state detection and reporting
- Deadlock detection using timeout mechanism
- Recovery strategies (resource release, thread termination)

### Three Main Parts:

#### Part 1: Circular-Wait Deadlock
- **Deadlock Scenario**: T0→R0→R1, T1→R1→R2, T2→R2→R3, T3→R3→R0 (circular chain)
- **Four Conditions Identified**:
  1. **Mutual Exclusion**: Locks held exclusively by one thread
  2. **Hold and Wait**: Threads hold resources while waiting for others
  3. **No Preemption**: Resources released voluntarily only
  4. **Circular Wait**: Circular dependency chain creates deadlock
- **Prevention**: Resource ordering (always acquire in ascending order) breaks circular wait

#### Part 2: Banker's Algorithm
- **Example 1 (Safe State)**: 5 processes, 3 resource types
  - Safe Sequence Found: P1 → P3 → P0 → P2 → P4
  - All processes can complete without deadlock
- **Example 2 (Unsafe State)**: 4 processes, 3 resource types
  - No safe sequence exists (insufficient resources)
  - System reports unsafe state, requests denied

#### Part 3: Deadlock Detection & Recovery
- **Detection**: Timeout-based mechanism (acquire with timeout)
- **Recovery**: Automatic resource release upon deadlock detection
- **Strategies**: Resource release, retry capability, thread termination option

### Banker's Algorithm Details:
- **Input Matrices**:
  - Allocation[i][j]: Currently allocated resources
  - Maximum[i][j]: Maximum resource needs
  - Available[j]: Currently available resources
- **Calculated Matrix**:
  - Need[i][j] = Maximum[i][j] - Allocation[i][j]
- **Safety Algorithm**:
  - Iteratively find processes where Need[i] ≤ Available
  - Simulate completion and resource release
  - Generate safe sequence or report unsafe state

### Results:
- **Deadlock Created**: Circular wait successfully demonstrated
- **Prevention Success**: Resource ordering eliminated deadlock (100%)
- **Safe State**: Correctly identified with valid safe sequence
- **Unsafe State**: Correctly detected when resources insufficient
- **Detection**: Timeout mechanism caught deadlock (3/3 threads)
- **Recovery**: All threads released resources and terminated cleanly

---

## Technical Specifications

### Environment:
- **Language:** Python 3.x
- **Libraries:** threading, time, math, random (standard library only)
- **Platform:** Cross-platform compatible (Windows/Linux)
- **Execution:** All programs terminate cleanly with proper thread cleanup

### Key Learning Outcomes:
1. **Thread Management:** Creation, execution, synchronization, cleanup
2. **Race Condition Handling:** Detection, prevention, correction techniques
3. **Classical Problems:** Industry-standard synchronization solutions
4. **Performance Analysis:** Overhead measurement and comparison
5. **Deadlock Prevention:** Practical avoidance strategies

### Code Quality:
- ✅ Clean, readable, and well-documented code
- ✅ Proper error handling and resource management
- ✅ Real-time output with clear formatting
- ✅ Educational comments explaining concepts
- ✅ Finite execution with graceful termination

## Execution Instructions

```bash
# Run all tasks individually
python task1_thread_creation_models.py
python task2_race_condition_lock_semaphore.py  
python task2_simple_race_condition.py
python task3_classical_sync_problems.py
python task4_deadlock_bankers_algorithm.py
```

## Expected Learning Assessment

Each task demonstrates mastery of core OS threading concepts:

- **Task 1:** Understanding threading models and benefits
- **Task 2:** Race condition identification and prevention
- **Task 3:** Classical synchronization problem solutions
- **Task 4:** Deadlock handling, prevention, avoidance, detection, and recovery

**Total Implementation:** 5 complete Python files (including simplified version) with comprehensive threading and deadlock demonstrations suitable for advanced Operating Systems coursework.