#!/usr/bin/env python3
"""
Task 3: Classical Synchronization Problems
- Producer-Consumer with circular buffer
- Readers-Writers with protected reader count  
- Dining Philosophers with deadlock prevention
- All use finite iterations and proper synchronization
"""

import threading
import time
import random
from collections import deque

# Global control for demonstrations
running = True

class ProducerConsumerBuffer:
    """Circular buffer for Producer-Consumer problem"""
    
    def __init__(self, size=5):
        self.buffer = [None] * size
        self.size = size
        self.count = 0
        self.in_ptr = 0
        self.out_ptr = 0
        
        # Synchronization primitives
        self.mutex = threading.Lock()
        self.empty_slots = threading.Semaphore(size)  # Available slots
        self.full_slots = threading.Semaphore(0)     # Items available
        
    def produce(self, item, producer_id):
        """Producer adds item to buffer"""
        # Wait for empty slot
        self.empty_slots.acquire()
        
        # Critical section - add to buffer
        with self.mutex:
            self.buffer[self.in_ptr] = item
            print(f"Producer-{producer_id}: Added '{item}' at position {self.in_ptr}")
            print(f"   Buffer: {[x if x is not None else 'Empty' for x in self.buffer]}")
            
            self.in_ptr = (self.in_ptr + 1) % self.size
            self.count += 1
        
        # Signal that item is available
        self.full_slots.release()
    
    def consume(self, consumer_id):
        """Consumer removes item from buffer"""
        # Wait for available item
        self.full_slots.acquire()
        
        # Critical section - remove from buffer
        with self.mutex:
            item = self.buffer[self.out_ptr]
            self.buffer[self.out_ptr] = None
            print(f"Consumer-{consumer_id}: Removed '{item}' from position {self.out_ptr}")
            print(f"   Buffer: {[x if x is not None else 'Empty' for x in self.buffer]}")
            
            self.out_ptr = (self.out_ptr + 1) % self.size
            self.count -= 1
        
        # Signal that slot is available
        self.empty_slots.release()
        return item

def producer_worker(buffer, producer_id, items_to_produce):
    """Producer thread function"""
    print(f"Producer-{producer_id} started (Thread ID: {threading.get_ident()})")
    
    for i in range(items_to_produce):
        item = f"Item-{producer_id}-{i+1}"
        buffer.produce(item, producer_id)
        time.sleep(random.uniform(0.1, 0.3))  # Simulate production time
    
    print(f"Producer-{producer_id} finished")

def consumer_worker(buffer, consumer_id, items_to_consume):
    """Consumer thread function"""
    print(f"Consumer-{consumer_id} started (Thread ID: {threading.get_ident()})")
    
    for i in range(items_to_consume):
        item = buffer.consume(consumer_id)
        print(f"Consumer-{consumer_id}: Processing '{item}'")
        time.sleep(random.uniform(0.1, 0.3))  # Simulate processing time
    
    print(f"Consumer-{consumer_id} finished")

def demonstrate_producer_consumer():
    """Demonstrate Producer-Consumer problem"""
    print("\n" + "="*60)
    print("PRODUCER-CONSUMER PROBLEM")
    print("="*60)
    print("Setup: Circular buffer (size=5), 2 producers, 2 consumers")
    
    # Create buffer
    buffer = ProducerConsumerBuffer(size=5)
    
    # Create threads
    threads = []
    items_each = 3
    
    # Producers
    for i in range(2):
        thread = threading.Thread(target=producer_worker, args=(buffer, i+1, items_each))
        threads.append(thread)
    
    # Consumers  
    for i in range(2):
        thread = threading.Thread(target=consumer_worker, args=(buffer, i+1, items_each))
        threads.append(thread)
    
    # Start all threads
    print("\nStarting threads...")
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    print("\n✅ Producer-Consumer completed successfully!")
    print(f"Final buffer state: {[x if x is not None else 'Empty' for x in buffer.buffer]}")

class ReadersWritersResource:
    """Shared resource for Readers-Writers problem"""
    
    def __init__(self):
        self.data = "Initial shared data"
        self.reader_count = 0
        
        # Synchronization primitives
        self.reader_mutex = threading.Lock()  # Protects reader_count
        self.write_mutex = threading.Lock()   # Controls writer access
        
    def start_reading(self, reader_id):
        """Reader acquires read access"""
        with self.reader_mutex:
            self.reader_count += 1
            print(f"Reader-{reader_id}: Starting read (Total readers: {self.reader_count})")
            
            # First reader locks out writers
            if self.reader_count == 1:
                self.write_mutex.acquire()
                print(f"   First reader locked out writers")
    
    def finish_reading(self, reader_id):
        """Reader releases read access"""
        with self.reader_mutex:
            self.reader_count -= 1
            print(f"Reader-{reader_id}: Finished read (Total readers: {self.reader_count})")
            
            # Last reader allows writers
            if self.reader_count == 0:
                self.write_mutex.release()
                print(f"   Last reader allowed writers")
    
    def read_data(self, reader_id):
        """Read operation"""
        self.start_reading(reader_id)
        
        # Critical section - reading
        print(f"Reader-{reader_id}: Reading data = '{self.data}'")
        time.sleep(random.uniform(0.1, 0.2))  # Simulate reading time
        
        self.finish_reading(reader_id)
    
    def write_data(self, writer_id, new_data):
        """Write operation"""
        print(f"Writer-{writer_id}: Requesting write access...")
        
        # Acquire exclusive access
        with self.write_mutex:
            print(f"Writer-{writer_id}: Got exclusive access")
            old_data = self.data
            self.data = new_data
            print(f"Writer-{writer_id}: Changed data from '{old_data}' to '{new_data}'")
            time.sleep(random.uniform(0.1, 0.2))  # Simulate writing time
            print(f"Writer-{writer_id}: Finished writing")

def reader_worker(resource, reader_id, read_count):
    """Reader thread function"""
    print(f"Reader-{reader_id} started (Thread ID: {threading.get_ident()})")
    
    for i in range(read_count):
        resource.read_data(reader_id)
        time.sleep(random.uniform(0.05, 0.15))
    
    print(f"Reader-{reader_id} finished")

def writer_worker(resource, writer_id, write_count):
    """Writer thread function"""
    print(f"Writer-{writer_id} started (Thread ID: {threading.get_ident()})")
    
    for i in range(write_count):
        new_data = f"Data from Writer-{writer_id}-{i+1}"
        resource.write_data(writer_id, new_data)
        time.sleep(random.uniform(0.1, 0.2))
    
    print(f"Writer-{writer_id} finished")

def demonstrate_readers_writers():
    """Demonstrate Readers-Writers problem"""
    print("\n" + "="*60)
    print("READERS-WRITERS PROBLEM")
    print("="*60)
    print("Setup: 3 readers, 2 writers, protected reader count")
    
    # Create shared resource
    resource = ReadersWritersResource()
    
    threads = []
    
    # Create readers
    for i in range(3):
        thread = threading.Thread(target=reader_worker, args=(resource, i+1, 2))
        threads.append(thread)
    
    # Create writers
    for i in range(2):
        thread = threading.Thread(target=writer_worker, args=(resource, i+1, 2))
        threads.append(thread)
    
    # Start all threads
    print(f"\nInitial data: '{resource.data}'")
    print("Starting threads...")
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    print(f"\n✅ Readers-Writers completed successfully!")
    print(f"Final data: '{resource.data}'")

class DiningPhilosophers:
    """Dining Philosophers problem with deadlock prevention"""
    
    def __init__(self, num_philosophers=5):
        self.num_philosophers = num_philosophers
        self.forks = [threading.Lock() for _ in range(num_philosophers)]
        
        # Deadlock prevention: Waiter mechanism (max N-1 can eat simultaneously)
        self.waiter = threading.Semaphore(num_philosophers - 1)
        
        # State tracking
        self.philosopher_states = ["THINKING"] * num_philosophers
        self.state_lock = threading.Lock()
    
    def get_fork_ids(self, philosopher_id):
        """Get left and right fork IDs"""
        left_fork = philosopher_id
        right_fork = (philosopher_id + 1) % self.num_philosophers
        return left_fork, right_fork
    
    def set_state(self, philosopher_id, state):
        """Update philosopher state safely"""
        with self.state_lock:
            self.philosopher_states[philosopher_id] = state
            self.print_state()
    
    def print_state(self):
        """Print current state of all philosophers"""
        states = " | ".join([f"P{i}:{state:<8}" for i, state in enumerate(self.philosopher_states)])
        print(f"   State: {states}")
    
    def think(self, philosopher_id):
        """Philosopher thinking"""
        self.set_state(philosopher_id, "THINKING")
        print(f"Philosopher-{philosopher_id}: Thinking...")
        time.sleep(random.uniform(0.1, 0.3))
    
    def eat(self, philosopher_id):
        """Philosopher eating with deadlock prevention"""
        left_fork, right_fork = self.get_fork_ids(philosopher_id)
        
        print(f"Philosopher-{philosopher_id}: Hungry, requesting waiter permission...")
        
        # Waiter controls access (prevents all from picking up forks simultaneously)
        self.waiter.acquire()
        try:
            self.set_state(philosopher_id, "HUNGRY")
            print(f"Philosopher-{philosopher_id}: Got waiter permission")
            
            # Resource ordering: always acquire lower numbered fork first (prevents circular wait)
            first_fork = min(left_fork, right_fork)
            second_fork = max(left_fork, right_fork)
            
            print(f"Philosopher-{philosopher_id}: Acquiring fork {first_fork}...")
            self.forks[first_fork].acquire()
            print(f"Philosopher-{philosopher_id}: Got fork {first_fork}")
            
            print(f"Philosopher-{philosopher_id}: Acquiring fork {second_fork}...")
            self.forks[second_fork].acquire()
            print(f"Philosopher-{philosopher_id}: Got fork {second_fork}")
            
            # Eating
            self.set_state(philosopher_id, "EATING")
            print(f"Philosopher-{philosopher_id}: EATING with forks {left_fork} and {right_fork}")
            time.sleep(random.uniform(0.2, 0.4))
            
            # Release forks
            self.forks[first_fork].release()
            self.forks[second_fork].release()
            print(f"Philosopher-{philosopher_id}: Released both forks")
            
        finally:
            # Release waiter permission
            self.waiter.release()
            print(f"Philosopher-{philosopher_id}: Released waiter permission")

def philosopher_worker(dining, philosopher_id, eat_cycles):
    """Philosopher thread function"""
    print(f"Philosopher-{philosopher_id} started (Thread ID: {threading.get_ident()})")
    
    for cycle in range(eat_cycles):
        print(f"\n--- Philosopher-{philosopher_id}: Cycle {cycle + 1} ---")
        dining.think(philosopher_id)
        dining.eat(philosopher_id)
    
    dining.set_state(philosopher_id, "FINISHED")
    print(f"Philosopher-{philosopher_id} finished all cycles")

def demonstrate_dining_philosophers():
    """Demonstrate Dining Philosophers problem"""
    print("\n" + "="*60)
    print("DINING PHILOSOPHERS PROBLEM")
    print("="*60)
    print("Setup: 5 philosophers, deadlock prevention with waiter + resource ordering")
    
    # Create dining setup
    dining = DiningPhilosophers(num_philosophers=5)
    
    threads = []
    cycles_each = 2
    
    print(f"\nDeadlock Prevention Methods:")
    print(f"1. Waiter mechanism: Max 4 philosophers can try to eat simultaneously")
    print(f"2. Resource ordering: Always acquire lower-numbered fork first")
    print(f"\nInitial state:")
    dining.print_state()
    
    # Create philosopher threads
    for i in range(5):
        thread = threading.Thread(target=philosopher_worker, args=(dining, i, cycles_each))
        threads.append(thread)
    
    # Start all threads
    print(f"\nStarting {len(threads)} philosophers...")
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    print(f"\n✅ Dining Philosophers completed successfully!")
    print("Final state:")
    dining.print_state()

def discuss_concepts():
    """Discuss synchronization concepts"""
    print("\n" + "="*60)
    print("SYNCHRONIZATION CONCEPTS DISCUSSION")
    print("="*60)
    
    print("\n🔒 DEADLOCK:")
    print("   • Circular waiting for resources")
    print("   • Prevention: Resource ordering, waiter mechanism")
    print("   • Example: All philosophers pick up left fork simultaneously")
    
    print("\n⏳ STARVATION:")
    print("   • Thread never gets required resources")
    print("   • Can occur in readers-writers (writers may starve)")
    print("   • Solution: Fair scheduling, timeouts")
    
    print("\n⚖️  FAIRNESS:")
    print("   • Equal opportunity for all threads")
    print("   • Prevented starvation through bounded waiting")
    print("   • Example: Waiter ensures philosophers get turns")
    
    print("\n✅ CORRECTNESS:")
    print("   • Mutual exclusion maintained")
    print("   • No race conditions")
    print("   • Proper synchronization ensures correct results")
    
    print("\n🛡️  SOLUTIONS IMPLEMENTED:")
    print("   • Producer-Consumer: Semaphores for buffer control")
    print("   • Readers-Writers: Mutex for reader count protection")
    print("   • Dining Philosophers: Waiter + resource ordering")

def main():
    """Main function to demonstrate all classical problems"""
    print("="*70)
    print("TASK 3: CLASSICAL SYNCHRONIZATION PROBLEMS")
    print("="*70)
    
    print("\nDemonstration Overview:")
    print("• Producer-Consumer: Circular buffer with semaphores")
    print("• Readers-Writers: Protected reader count with exclusive writers")
    print("• Dining Philosophers: Deadlock prevention mechanisms")
    print("• All use finite iterations for guaranteed termination")
    
    # Demonstrate each problem
    demonstrate_producer_consumer()
    demonstrate_readers_writers()
    demonstrate_dining_philosophers()
    
    # Discuss concepts
    discuss_concepts()
    
    print(f"\n{'='*70}")
    print("TASK 3 COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    print("\n📊 DEMONSTRATION SUMMARY:")
    print("✓ Producer-Consumer with circular buffer implemented")
    print("✓ Readers-Writers with protected reader count")
    print("✓ Dining Philosophers with deadlock prevention")
    print("✓ Finite iterations ensure normal termination")
    print("✓ Shared resource states displayed throughout")
    print("✓ Synchronization concepts discussed")
    print("✓ Deadlock, starvation, fairness, and correctness addressed")

if __name__ == "__main__":
    main()