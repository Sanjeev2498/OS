# Technical Analysis: All 4 Tasks - What's Used and How It Works

## Quick Reference Summary

| Task | Main Concepts | Key Primitives | Purpose |
|------|---------------|----------------|---------|
| **Task 1** | Thread Creation | `Thread()`, `start()`, `join()`, `Lock()` | Create and manage worker threads |
| **Task 2** | Race Conditions | `Lock()`, `Semaphore()`, `with` statement | Demonstrate and fix data races |
| **Task 3** | Classical Problems | `Lock()`, `Semaphore(count)` | Solve synchronization challenges |
| **Task 4** | Deadlock Handling | `acquire(timeout)`, Banker's Algorithm | Prevent, detect, and recover from deadlocks |

---

## TASK 1: Thread Creation, Models and Benefits

### What's Used:

```python
import threading  # Python's threading library
import time       # For timing measurements
import math       # For prime calculations
```

### Core Components:

#### 1. **threading.Thread()**
```python
thread = threading.Thread(
    target=cpu_intensive_task,  # Function to run
    args=(task_id, data_chunk),  # Function arguments
    name="Worker-1"              # Thread name (optional)
)
```
**What it does**: Creates a new thread object but doesn't start it yet

#### 2. **thread.start()**
```python
thread.start()
```
**What it does**: Tells OS to begin executing the thread's target function

#### 3. **thread.join()**
```python
thread.join()  # Wait here until thread finishes
```
**What it does**: Blocks current thread until this thread completes

#### 4. **threading.Lock()**
```python
progress_lock = threading.Lock()

with progress_lock:  # Acquire lock, auto-release when done
    progress_data[task_id] = ...
```
**What it does**: Prevents multiple threads from modifying shared data simultaneously

### How It Works:

```
MAIN THREAD                    WORKER THREADS
    |                                |
    |--- Create Thread-1 ----------→ Thread-1 created (not running)
    |--- Create Thread-2 ----------→ Thread-2 created (not running)
    |--- Create Thread-3 ----------→ Thread-3 created (not running)
    |                                |
    |--- Start Thread-1 -----------→ Thread-1 RUNNING (calculating primes)
    |--- Start Thread-2 -----------→ Thread-2 RUNNING (calculating primes)
    |--- Start Thread-3 -----------→ Thread-3 RUNNING (calculating primes)
    |                                |
    |--- Join Thread-1 (WAIT) ------→ Thread-1 finishes
    |← Thread-1 done ----------------┘
    |                                |
    |--- Join Thread-2 (WAIT) ------→ Thread-2 finishes
    |← Thread-2 done ----------------┘
    |                                |
    |--- Join Thread-3 (WAIT) ------→ Thread-3 finishes
    |← Thread-3 done ----------------┘
    |
    |--- All threads complete!
    |--- Continue execution
```

### Threading Models Explained:

#### 1. **User-Level Threads**
- Managed by user-space library (not OS)
- Fast to create and switch
- **Problem**: If one blocks, all block
- **Example**: Green threads in old Python versions

#### 2. **Kernel-Level Threads**
- Managed by OS kernel
- True parallelism on multi-core CPUs
- **Python uses this!** (`threading` module creates OS threads)
- Slower to create/switch than user-level

#### 3. **Hybrid Model (M:N)**
- M user threads mapped to N kernel threads
- Best of both worlds
- Complex to implement

### Python's GIL (Global Interpreter Lock):

```
CPU Core 1: [Thread-1 executes] → [GIL] ← [Thread-2 waits]
                                     ↓
CPU Core 2:                      [GIL switches]
                                     ↓
CPU Core 1: [Thread-1 waits] ← [GIL] → [Thread-2 executes]
```

**Why Limited Speedup?**
- Only ONE thread can execute Python code at a time
- GIL prevents true CPU parallelism for Python code
- Better for I/O-bound tasks (network, disk) than CPU-bound

---

## TASK 2: Race Conditions, Locks and Semaphores

### What's Used:

```python
import threading
import time

# Synchronization primitives
counter_lock = threading.Lock()           # Mutex for mutual exclusion
semaphore = threading.Semaphore(1)       # Binary semaphore (like a lock)
```

### Core Components:

#### 1. **Lock (Mutex)**
```python
# Method 1: Manual acquire/release
lock.acquire()  # Block until lock is available
# Critical section
lock.release()  # Release lock

# Method 2: Context manager (RECOMMENDED)
with lock:
    # Critical section (auto-released even if exception occurs)
    shared_counter += 1
```

**What it does**: Ensures only ONE thread can execute critical section at a time

#### 2. **Semaphore**
```python
semaphore = threading.Semaphore(3)  # Initial count = 3

semaphore.acquire()  # Decrement count (wait if 0)
# Critical section (max 3 threads can be here)
semaphore.release()  # Increment count
```

**What it does**: 
- Maintains a counter
- `acquire()`: Decrement counter, block if 0
- `release()`: Increment counter, wake waiting threads

### How Race Conditions Happen:

```
TIME    THREAD-1 (Unprotected)         THREAD-2 (Unprotected)         COUNTER
----    ----------------------         ----------------------         -------
t0      temp = counter (reads 0)                                      0
t1                                     temp = counter (reads 0)       0
t2      counter = temp + 1 (writes 1)                                 1
t3                                     counter = temp + 1 (writes 1)  1 ← WRONG!
                                                                     Should be 2!
```

**The Problem**: Both read OLD value before either writes NEW value

### How Locks Fix It:

```
TIME    THREAD-1 (Protected)           THREAD-2 (Protected)           COUNTER
----    --------------------           --------------------           -------
t0      lock.acquire() ✓                                              0
t1      temp = counter (reads 0)                                      0
t2                                     lock.acquire() BLOCKED ⏸       0
t3      counter = temp + 1 (writes 1)                                 1
t4      lock.release()                                                1
t5                                     lock.acquire() ✓               1
t6                                     temp = counter (reads 1)       1
t7                                     counter = temp + 1 (writes 2)  2 ← CORRECT!
t8                                     lock.release()                 2
```

**The Solution**: Only one thread can be in critical section at a time

### Lock vs Semaphore:

| Feature | Lock | Semaphore(1) |
|---------|------|--------------|
| **Purpose** | Mutual exclusion | Resource counting |
| **Binary** | Yes (locked/unlocked) | Can be binary |
| **Owner** | Thread that acquired it | No specific owner |
| **Release** | Only owner can release | Any thread can release |
| **Performance** | Faster | Slower (more overhead) |
| **Use Case** | Protecting shared data | Controlling resource pool |

### Why Timing-Dependent?

```python
# This makes race condition more visible:
temp = shared_counter
time.sleep(0.0001)  # ← Context switch more likely here!
shared_counter = temp + 1
```

Without sleep, race might not occur every time (depends on thread scheduling)

---

## TASK 3: Classical Synchronization Problems

### What's Used:

```python
import threading
from collections import deque  # For circular buffer

# Multiple synchronization primitives
mutex = threading.Lock()                 # Binary protection
empty_slots = threading.Semaphore(5)     # Counting semaphore
full_slots = threading.Semaphore(0)      # Counting semaphore
waiter = threading.Semaphore(4)          # Limit concurrent access
```

---

### Problem 1: Producer-Consumer

#### Synchronization Mechanism:

```python
class Buffer:
    mutex = Lock()              # Protects buffer structure
    empty = Semaphore(5)        # Counts empty slots (initially 5)
    full = Semaphore(0)         # Counts full slots (initially 0)
```

#### How Producer Works:

```
1. empty.acquire()    ← Wait if buffer full (empty = 0)
   └─ Decrement empty count
   
2. with mutex:        ← Get exclusive access to buffer
   └─ Add item to buffer
   └─ Update pointers
   
3. full.release()     ← Signal item available
   └─ Increment full count
   └─ Wake up waiting consumer
```

#### How Consumer Works:

```
1. full.acquire()     ← Wait if buffer empty (full = 0)
   └─ Decrement full count
   
2. with mutex:        ← Get exclusive access to buffer
   └─ Remove item from buffer
   └─ Update pointers
   
3. empty.release()    ← Signal slot available
   └─ Increment empty count
   └─ Wake up waiting producer
```

#### State Diagram:

```
EMPTY = 5, FULL = 0  [_____|_____|_____|_____|_____]  Buffer empty

Producer adds item:
EMPTY = 4, FULL = 1  [ITEM1|_____|_____|_____|_____]

Producer adds another:
EMPTY = 3, FULL = 2  [ITEM1|ITEM2|_____|_____|_____]

Consumer removes item:
EMPTY = 4, FULL = 1  [_____|ITEM2|_____|_____|_____]

... and so on ...
```

**Why This Works**:
- `empty` semaphore prevents buffer overflow
- `full` semaphore prevents buffer underflow
- `mutex` prevents simultaneous modifications

---

### Problem 2: Readers-Writers

#### Synchronization Mechanism:

```python
reader_count = 0                  # Tracks active readers
reader_mutex = Lock()             # Protects reader_count
write_mutex = Lock()              # Controls writer access
```

#### How Readers Work:

```
START READING:
1. with reader_mutex:
     reader_count += 1
     if reader_count == 1:     ← FIRST reader
        write_mutex.acquire()   ← Lock out all writers
        
2. READ DATA (No lock needed! Multiple readers can be here)

3. with reader_mutex:
     reader_count -= 1
     if reader_count == 0:     ← LAST reader
        write_mutex.release()   ← Allow writers again
```

#### How Writers Work:

```
1. with write_mutex:           ← Wait if ANY reader active
   WRITE DATA                  ← Exclusive access (no readers, no writers)
```

#### State Examples:

```
State 1: No activity
  reader_count = 0
  write_mutex = unlocked
  
State 2: Reader-1 starts
  Reader-1: reader_count = 1, acquires write_mutex
  
State 3: Reader-2 starts (while Reader-1 still reading)
  Reader-2: reader_count = 2
  Both read simultaneously! ✓
  
State 4: Writer-1 tries to write
  Writer-1: BLOCKED on write_mutex (readers active)
  
State 5: Reader-1 finishes
  reader_count = 1 (still not zero)
  Writer-1: Still BLOCKED
  
State 6: Reader-2 finishes
  reader_count = 0, releases write_mutex
  Writer-1: Unblocked! Gets exclusive access
```

**Key Insight**: 
- First reader locks out writers
- Last reader allows writers
- Multiple readers don't block each other

---

### Problem 3: Dining Philosophers

#### The Classic Deadlock Scenario:

```
Philosopher 0: Picks up fork 0
Philosopher 1: Picks up fork 1
Philosopher 2: Picks up fork 2
Philosopher 3: Picks up fork 3
Philosopher 4: Picks up fork 4

Now everyone needs their right fork:
Philosopher 0: Wants fork 1 (held by Phil-1) ⏸
Philosopher 1: Wants fork 2 (held by Phil-2) ⏸
Philosopher 2: Wants fork 3 (held by Phil-3) ⏸
Philosopher 3: Wants fork 4 (held by Phil-4) ⏸
Philosopher 4: Wants fork 0 (held by Phil-0) ⏸

DEADLOCK! Everyone waits forever in a circle.
```

#### Deadlock Prevention Strategy 1: Waiter Mechanism

```python
waiter = Semaphore(4)  # Only 4 can try to eat at once

def eat():
    waiter.acquire()       # Request permission
    get_left_fork()
    get_right_fork()
    EAT
    put_down_forks()
    waiter.release()       # Release permission
```

**How it prevents deadlock**:
```
If only 4 philosophers can attempt eating:
  Phil-0: Has fork 0
  Phil-1: Has fork 1
  Phil-2: Has fork 2
  Phil-3: Has fork 3
  Phil-4: WAITING (waiter blocked)
  
Phil-0 wants fork 1: Gets it! (Phil-1 blocked elsewhere)
Phil-0 can now EAT and release forks
Others can proceed...
```

**At least ONE philosopher will succeed** (pigeonhole principle)

#### Deadlock Prevention Strategy 2: Resource Ordering

```python
def eat(philosopher_id):
    left_fork = philosopher_id
    right_fork = (philosopher_id + 1) % 5
    
    # Always acquire lower-numbered fork first
    first = min(left_fork, right_fork)
    second = max(left_fork, right_fork)
    
    forks[first].acquire()
    forks[second].acquire()
    EAT
    forks[second].release()
    forks[first].release()
```

**How it prevents deadlock**:
```
Philosopher 0: Acquires fork 0, then fork 1
Philosopher 1: Acquires fork 1, then fork 2
Philosopher 2: Acquires fork 2, then fork 3
Philosopher 3: Acquires fork 3, then fork 4
Philosopher 4: Acquires fork 0, then fork 4  ← DIFFERENT ORDER!

No circular dependency! Phil-4 needs fork 0 first,
but Phil-0 already has it. Phil-0 completes, releases forks,
then Phil-4 can proceed.
```

**Breaks the circular wait condition!**

---

## TASK 4: Deadlock Handling & Banker's Algorithm

### What's Used:

```python
import threading
import time
from typing import List, Tuple

# Timeout-based deadlock detection
resource.acquire(timeout=2.0)  # Wait max 2 seconds

# Data structures for Banker's Algorithm
allocation = [[...], [...]]    # 2D list
maximum = [[...], [...]]       # 2D list
available = [...]              # 1D list
```

---

### Part 1: Four Conditions for Deadlock

#### 1. **Mutual Exclusion**
```python
lock = threading.Lock()
# Only ONE thread can hold lock at a time
```

#### 2. **Hold and Wait**
```python
lock1.acquire()  # Holding lock1
# ... doing work ...
lock2.acquire()  # Now waiting for lock2 (while still holding lock1)
```

#### 3. **No Preemption**
```python
# Lock can only be released by thread that acquired it
# OS cannot forcibly take it away
lock.release()  # Only this thread can do this
```

#### 4. **Circular Wait**
```python
Thread-0: Holds R0, waits for R1
Thread-1: Holds R1, waits for R2
Thread-2: Holds R2, waits for R0  ← Circle closes!
```

**Deadlock happens ONLY when ALL FOUR are present!**

### Deadlock Prevention: Break ONE Condition

#### Break Mutual Exclusion:
- Make resources sharable (not always possible)
- Example: Read-only files

#### Break Hold and Wait:
```python
# Acquire all resources at once, or none
with lock1, lock2, lock3:
    # Work with all resources
```

#### Break No Preemption:
```python
# Use timeouts
if not lock.acquire(timeout=1.0):
    # Release everything and retry
    release_all_locks()
```

#### Break Circular Wait:
```python
# Resource ordering (always acquire in order)
first = min(res1, res2)
second = max(res1, res2)
resources[first].acquire()
resources[second].acquire()
```

---

### Part 2: Banker's Algorithm

#### Data Structures:

```python
# Example: 3 processes, 3 resource types
Allocation = [
    [0, 1, 0],  # P0 currently has 0 of R0, 1 of R1, 0 of R2
    [2, 0, 0],  # P1 currently has 2 of R0, 0 of R1, 0 of R2
    [3, 0, 2],  # P2 currently has 3 of R0, 0 of R1, 2 of R2
]

Maximum = [
    [7, 5, 3],  # P0 needs max: 7 of R0, 5 of R1, 3 of R2
    [3, 2, 2],  # P1 needs max: 3 of R0, 2 of R1, 2 of R2
    [9, 0, 2],  # P2 needs max: 9 of R0, 0 of R1, 2 of R2
]

Available = [3, 3, 2]  # Currently available: 3 of R0, 3 of R1, 2 of R2

# Calculate Need
Need[i][j] = Maximum[i][j] - Allocation[i][j]
```

#### Algorithm Pseudocode:

```python
def is_safe_state():
    Work = Available.copy()  # Working copy
    Finish = [False] * num_processes
    safe_sequence = []
    
    while not all(Finish):
        # Find a process that can finish
        found = False
        for i in range(num_processes):
            if not Finish[i]:
                # Can this process complete with available resources?
                if Need[i] <= Work:  # All resource types
                    # Yes! Simulate completion
                    Work += Allocation[i]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
        
        if not found:
            # No process can proceed - UNSAFE!
            return False, []
    
    # All processes finished - SAFE!
    return True, safe_sequence
```

#### Step-by-Step Example:

```
Initial: Available = [3, 3, 2]

Step 1: Check which process can run
  P0: Need [7,4,3] > Available [3,3,2] ✗
  P1: Need [1,2,2] ≤ Available [3,3,2] ✓  ← Can run!
  
  Simulate P1 completion:
  Available = [3,3,2] + Allocation_P1[2,0,0] = [5,3,2]
  Safe Sequence: [P1]

Step 2: Available = [5,3,2]
  P0: Need [7,4,3] > Available [5,3,2] ✗
  P2: Need [6,0,0] > Available [5,3,2] ✗
  P3: Need [0,1,1] ≤ Available [5,3,2] ✓  ← Can run!
  
  Simulate P3 completion:
  Available = [5,3,2] + Allocation_P3[2,1,1] = [7,4,3]
  Safe Sequence: [P1, P3]

Step 3: Available = [7,4,3]
  P0: Need [7,4,3] ≤ Available [7,4,3] ✓  ← Can run!
  
  Simulate P0 completion:
  Available = [7,4,3] + Allocation_P0[0,1,0] = [7,5,3]
  Safe Sequence: [P1, P3, P0]

... continue until all processes finish ...

Result: SAFE with sequence [P1, P3, P0, P2, P4]
```

#### When is it UNSAFE?

```
Available = [0, 0, 0]  # No resources available

Step 1: Check all processes
  P0: Need [7,4,3] > Available [0,0,0] ✗
  P1: Need [1,2,2] > Available [0,0,0] ✗
  P2: Need [6,0,0] > Available [0,0,0] ✗
  
No process can proceed!
Result: UNSAFE - deadlock possible
```

---

### Part 3: Deadlock Detection & Recovery

#### Detection Using Timeouts:

```python
def thread_function():
    resource1.acquire()  # Got first resource
    
    # Try to get second resource with timeout
    if resource2.acquire(timeout=2.0):
        # Success! Do work
        work()
        resource2.release()
    else:
        # Timeout! Possible deadlock detected
        print("DEADLOCK DETECTED!")
        # Initiate recovery
        recovery()
    
    resource1.release()
```

#### Recovery Strategy 1: Resource Release

```python
def recovery():
    # Release all held resources
    for resource in held_resources:
        resource.release()
    
    # Wait random time (avoid repeated deadlock)
    time.sleep(random.uniform(0.1, 0.5))
    
    # Retry operation
    retry()
```

#### Recovery Strategy 2: Thread Termination

```python
def detect_and_recover():
    if deadlock_detected():
        # Choose victim thread (e.g., lowest priority)
        victim = choose_victim_thread()
        
        # Terminate it
        victim.terminate()
        
        # Release its resources
        release_resources(victim)
```

#### Recovery Strategy 3: Rollback

```python
def transaction():
    checkpoint = save_state()
    
    try:
        acquire_resources()
        do_work()
        commit()
    except DeadlockException:
        # Rollback to checkpoint
        restore_state(checkpoint)
        release_all_resources()
```

---

## Summary of All Mechanisms

### Thread Management:
- **`Thread()`**: Create thread object
- **`start()`**: Begin execution
- **`join()`**: Wait for completion
- **`get_ident()`**: Get thread ID

### Synchronization:
- **`Lock()`**: Binary mutual exclusion
- **`Semaphore(n)`**: Counting semaphore (n slots)
- **`acquire()`**: Get resource (block if unavailable)
- **`release()`**: Free resource
- **`acquire(timeout=x)`**: Try with timeout (deadlock detection)
- **`with lock:`**: Context manager (auto-release)

### Patterns:
- **Producer-Consumer**: 2 semaphores + 1 lock
- **Readers-Writers**: 2 locks + counter
- **Dining Philosophers**: N locks + waiter semaphore + ordering
- **Banker's Algorithm**: Matrix operations for safety

### Deadlock:
- **Four Conditions**: All must be present
- **Prevention**: Break one condition
- **Avoidance**: Banker's Algorithm (safe states)
- **Detection**: Timeouts, resource graphs
- **Recovery**: Release, terminate, rollback

---

**All code uses Python 3.x standard library - no external dependencies required!**
