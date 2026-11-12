"""
Deadlock Handling Module
Implements Banker's Algorithm and deadlock detection
"""

from typing import List, Dict, Tuple
import copy

class DeadlockHandler:
    """Handles deadlock detection and prevention using Banker's Algorithm"""
    
    def __init__(self):
        self.num_processes = 0
        self.num_resources = 0
        self.allocation = []
        self.maximum = []
        self.available = []
        self.need = []
    
    def has_data(self):
        """Check if deadlock data is loaded"""
        return self.num_processes > 0 and self.num_resources > 0
    
    def set_data(self, allocation: List[List[int]], maximum: List[List[int]], available: List[int]):
        """Set deadlock data"""
        self.allocation = [row[:] for row in allocation]
        self.maximum = [row[:] for row in maximum]
        self.available = available[:]
        self.num_processes = len(allocation)
        self.num_resources = len(available)
        self._calculate_need()
    
    def load_sample_data(self):
        """Load sample deadlock data (Banker's Algorithm example)"""
        allocation = [
            [0, 1, 0],  # P0
            [2, 0, 0],  # P1
            [3, 0, 2],  # P2
            [2, 1, 1],  # P3
            [0, 0, 2],  # P4
        ]
        
        maximum = [
            [7, 5, 3],  # P0
            [3, 2, 2],  # P1
            [9, 0, 2],  # P2
            [2, 2, 2],  # P3
            [4, 3, 3],  # P4
        ]
        
        available = [3, 3, 2]
        
        self.set_data(allocation, maximum, available)
    
    def _calculate_need(self):
        """Calculate Need matrix: Need = Maximum - Allocation"""
        self.need = []
        for i in range(self.num_processes):
            need_row = []
            for j in range(self.num_resources):
                need_row.append(self.maximum[i][j] - self.allocation[i][j])
            self.need.append(need_row)
    
    def bankers_algorithm(self) -> Dict:
        """Run Banker's Algorithm to check for safe state"""
        work = self.available[:]
        finish = [False] * self.num_processes
        safe_sequence = []
        
        # Try to find a safe sequence
        while len(safe_sequence) < self.num_processes:
            found = False
            
            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if Need[i] <= Work
                    can_allocate = all(self.need[i][j] <= work[j] for j in range(self.num_resources))
                    
                    if can_allocate:
                        # Process can finish
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        
                        finish[i] = True
                        safe_sequence.append(f'P{i}')
                        found = True
                        break
            
            if not found:
                # No process can proceed - unsafe state
                return {
                    'is_safe': False,
                    'safe_sequence': [],
                    'allocation': self.allocation,
                    'maximum': self.maximum,
                    'need': self.need,
                    'available': self.available
                }
        
        # Safe state found
        return {
            'is_safe': True,
            'safe_sequence': safe_sequence,
            'allocation': self.allocation,
            'maximum': self.maximum,
            'need': self.need,
            'available': self.available
        }
    
    def detect_deadlock(self) -> Dict:
        """Detect if system is in deadlock"""
        # Use Banker's algorithm result
        result = self.bankers_algorithm()
        
        deadlocked_processes = []
        if not result['is_safe']:
            # Find which processes cannot complete
            work = self.available[:]
            finish = [False] * self.num_processes
            
            # Mark processes that can finish
            changed = True
            while changed:
                changed = False
                for i in range(self.num_processes):
                    if not finish[i]:
                        can_allocate = all(self.need[i][j] <= work[j] for j in range(self.num_resources))
                        if can_allocate:
                            for j in range(self.num_resources):
                                work[j] += self.allocation[i][j]
                            finish[i] = True
                            changed = True
            
            # Processes that couldn't finish are deadlocked
            deadlocked_processes = [f'P{i}' for i in range(self.num_processes) if not finish[i]]
        
        return {
            'deadlock_exists': not result['is_safe'],
            'deadlocked_processes': deadlocked_processes
        }
    
    def print_matrix(self, matrix: List[List[int]]):
        """Print a matrix in formatted way"""
        if not matrix:
            print("  (empty)")
            return
        
        # Header
        print(f"  {'Process':<10}", end="")
        for j in range(len(matrix[0])):
            print(f"R{j:<3}", end=" ")
        print()
        print("  " + "-" * (10 + len(matrix[0]) * 4))
        
        # Data
        for i, row in enumerate(matrix):
            print(f"  P{i:<9}", end="")
            for val in row:
                print(f"{val:<4}", end="")
            print()
