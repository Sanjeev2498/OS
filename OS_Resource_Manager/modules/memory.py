"""
Memory Management Module
Implements memory allocation algorithms: First Fit, Best Fit, Worst Fit
"""

from typing import List, Dict
import copy

class MemoryManager:
    """Handles memory allocation algorithms"""
    
    def __init__(self):
        self.blocks = []
        self.processes = []
        self.original_blocks = []
        self.original_processes = []
    
    def has_data(self):
        """Check if memory data is loaded"""
        return len(self.blocks) > 0 and len(self.processes) > 0
    
    def set_data(self, blocks: List[int], processes: List[Dict]):
        """Set memory blocks and processes"""
        self.blocks = blocks.copy()
        self.processes = copy.deepcopy(processes)
        self.original_blocks = blocks.copy()
        self.original_processes = copy.deepcopy(processes)
    
    def load_sample_data(self):
        """Load sample memory data"""
        sample_blocks = [100, 500, 200, 300, 600]
        sample_processes = [
            {'pid': 'P1', 'size': 212},
            {'pid': 'P2', 'size': 417},
            {'pid': 'P3', 'size': 112},
            {'pid': 'P4', 'size': 426},
        ]
        self.set_data(sample_blocks, sample_processes)
    
    def first_fit(self) -> Dict:
        """First Fit memory allocation algorithm"""
        blocks = self.original_blocks.copy()
        processes = copy.deepcopy(self.original_processes)
        
        allocations = []
        
        for process in processes:
            allocated = False
            
            for i, block_size in enumerate(blocks):
                if block_size >= process['size']:
                    # Allocate process to this block
                    fragment = block_size - process['size']
                    blocks[i] = 0  # Mark as allocated
                    
                    allocations.append({
                        'process': process['pid'],
                        'size': process['size'],
                        'block': f'Block-{i+1}',
                        'status': 'Allocated',
                        'fragment': fragment
                    })
                    allocated = True
                    break
            
            if not allocated:
                allocations.append({
                    'process': process['pid'],
                    'size': process['size'],
                    'block': 'None',
                    'status': 'Not Allocated',
                    'fragment': 0
                })
        
        return self._calculate_metrics(allocations, self.original_blocks)
    
    def best_fit(self) -> Dict:
        """Best Fit memory allocation algorithm"""
        blocks = self.original_blocks.copy()
        processes = copy.deepcopy(self.original_processes)
        
        allocations = []
        
        for process in processes:
            best_idx = -1
            best_size = float('inf')
            
            # Find the smallest block that fits
            for i, block_size in enumerate(blocks):
                if block_size >= process['size'] and block_size < best_size:
                    best_idx = i
                    best_size = block_size
            
            if best_idx != -1:
                fragment = blocks[best_idx] - process['size']
                blocks[best_idx] = 0  # Mark as allocated
                
                allocations.append({
                    'process': process['pid'],
                    'size': process['size'],
                    'block': f'Block-{best_idx+1}',
                    'status': 'Allocated',
                    'fragment': fragment
                })
            else:
                allocations.append({
                    'process': process['pid'],
                    'size': process['size'],
                    'block': 'None',
                    'status': 'Not Allocated',
                    'fragment': 0
                })
        
        return self._calculate_metrics(allocations, self.original_blocks)
    
    def worst_fit(self) -> Dict:
        """Worst Fit memory allocation algorithm"""
        blocks = self.original_blocks.copy()
        processes = copy.deepcopy(self.original_processes)
        
        allocations = []
        
        for process in processes:
            worst_idx = -1
            worst_size = -1
            
            # Find the largest block that fits
            for i, block_size in enumerate(blocks):
                if block_size >= process['size'] and block_size > worst_size:
                    worst_idx = i
                    worst_size = block_size
            
            if worst_idx != -1:
                fragment = blocks[worst_idx] - process['size']
                blocks[worst_idx] = 0  # Mark as allocated
                
                allocations.append({
                    'process': process['pid'],
                    'size': process['size'],
                    'block': f'Block-{worst_idx+1}',
                    'status': 'Allocated',
                    'fragment': fragment
                })
            else:
                allocations.append({
                    'process': process['pid'],
                    'size': process['size'],
                    'block': 'None',
                    'status': 'Not Allocated',
                    'fragment': 0
                })
        
        return self._calculate_metrics(allocations, self.original_blocks)
    
    def _calculate_metrics(self, allocations: List[Dict], original_blocks: List[int]) -> Dict:
        """Calculate memory management metrics"""
        total_memory = sum(original_blocks)
        
        allocated_memory = sum(alloc['size'] for alloc in allocations if alloc['status'] == 'Allocated')
        free_memory = total_memory - allocated_memory
        
        external_fragmentation = sum(alloc['fragment'] for alloc in allocations if alloc['status'] == 'Allocated')
        
        total_processes = len(allocations)
        allocated_processes = sum(1 for alloc in allocations if alloc['status'] == 'Allocated')
        success_rate = (allocated_processes / total_processes * 100) if total_processes > 0 else 0
        
        return {
            'allocations': allocations,
            'total_memory': total_memory,
            'allocated_memory': allocated_memory,
            'free_memory': free_memory,
            'external_fragmentation': external_fragmentation,
            'success_rate': success_rate
        }
