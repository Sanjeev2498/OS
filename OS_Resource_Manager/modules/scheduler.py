"""
Process Scheduling Module
Implements CPU scheduling algorithms: FCFS, SJF, Priority, Round Robin
"""

from typing import List, Dict
import copy

class ProcessScheduler:
    """Handles process scheduling algorithms"""
    
    def __init__(self):
        self.processes = []
        self.original_processes = []
    
    def has_processes(self):
        """Check if processes are loaded"""
        return len(self.processes) > 0
    
    def set_processes(self, processes: List[Dict]):
        """Set process list"""
        self.processes = copy.deepcopy(processes)
        self.original_processes = copy.deepcopy(processes)
    
    def load_sample_data(self):
        """Load sample process data"""
        sample_processes = [
            {'pid': 'P1', 'arrival': 0, 'burst': 5, 'priority': 2},
            {'pid': 'P2', 'arrival': 1, 'burst': 3, 'priority': 1},
            {'pid': 'P3', 'arrival': 2, 'burst': 8, 'priority': 3},
            {'pid': 'P4', 'arrival': 3, 'burst': 6, 'priority': 2},
            {'pid': 'P5', 'arrival': 4, 'burst': 4, 'priority': 1},
        ]
        self.set_processes(sample_processes)
    
    def fcfs(self) -> Dict:
        """First Come First Serve scheduling"""
        processes = copy.deepcopy(self.original_processes)
        processes.sort(key=lambda x: x['arrival'])
        
        current_time = 0
        gantt = []
        
        for process in processes:
            if current_time < process['arrival']:
                current_time = process['arrival']
            
            process['waiting'] = current_time - process['arrival']
            process['completion'] = current_time + process['burst']
            process['turnaround'] = process['completion'] - process['arrival']
            
            gantt.append(f"[{process['pid']}:{current_time}-{process['completion']}]")
            current_time = process['completion']
        
        return self._calculate_metrics(processes, gantt)
    
    def sjf(self) -> Dict:
        """Shortest Job First scheduling (Non-preemptive)"""
        processes = copy.deepcopy(self.original_processes)
        processes.sort(key=lambda x: (x['arrival'], x['burst']))
        
        current_time = 0
        completed = []
        remaining = processes.copy()
        gantt = []
        
        while remaining:
            # Get processes that have arrived
            available = [p for p in remaining if p['arrival'] <= current_time]
            
            if not available:
                current_time = min(p['arrival'] for p in remaining)
                continue
            
            # Pick shortest job
            process = min(available, key=lambda x: x['burst'])
            remaining.remove(process)
            
            process['waiting'] = current_time - process['arrival']
            process['completion'] = current_time + process['burst']
            process['turnaround'] = process['completion'] - process['arrival']
            
            gantt.append(f"[{process['pid']}:{current_time}-{process['completion']}]")
            current_time = process['completion']
            completed.append(process)
        
        return self._calculate_metrics(completed, gantt)
    
    def priority(self) -> Dict:
        """Priority scheduling (Lower number = Higher priority)"""
        processes = copy.deepcopy(self.original_processes)
        processes.sort(key=lambda x: (x['arrival'], x['priority']))
        
        current_time = 0
        completed = []
        remaining = processes.copy()
        gantt = []
        
        while remaining:
            # Get processes that have arrived
            available = [p for p in remaining if p['arrival'] <= current_time]
            
            if not available:
                current_time = min(p['arrival'] for p in remaining)
                continue
            
            # Pick highest priority (lowest number)
            process = min(available, key=lambda x: x['priority'])
            remaining.remove(process)
            
            process['waiting'] = current_time - process['arrival']
            process['completion'] = current_time + process['burst']
            process['turnaround'] = process['completion'] - process['arrival']
            
            gantt.append(f"[{process['pid']}:{current_time}-{process['completion']}]")
            current_time = process['completion']
            completed.append(process)
        
        return self._calculate_metrics(completed, gantt)
    
    def round_robin(self, quantum: int = 2) -> Dict:
        """Round Robin scheduling with time quantum"""
        processes = copy.deepcopy(self.original_processes)
        processes.sort(key=lambda x: x['arrival'])
        
        # Add remaining time field
        for p in processes:
            p['remaining'] = p['burst']
            p['waiting'] = 0
        
        current_time = 0
        queue = []
        completed = []
        gantt = []
        index = 0
        
        # Add first process to queue
        if processes:
            queue.append(processes[0])
            index = 1
        
        while queue or index < len(processes):
            if not queue:
                current_time = processes[index]['arrival']
                queue.append(processes[index])
                index += 1
                continue
            
            process = queue.pop(0)
            
            # Execute for quantum or remaining time
            exec_time = min(quantum, process['remaining'])
            start_time = current_time
            current_time += exec_time
            process['remaining'] -= exec_time
            
            gantt.append(f"[{process['pid']}:{start_time}-{current_time}]")
            
            # Add newly arrived processes to queue
            while index < len(processes) and processes[index]['arrival'] <= current_time:
                queue.append(processes[index])
                index += 1
            
            # If process not finished, add back to queue
            if process['remaining'] > 0:
                queue.append(process)
            else:
                process['completion'] = current_time
                process['turnaround'] = process['completion'] - process['arrival']
                process['waiting'] = process['turnaround'] - process['burst']
                completed.append(process)
        
        return self._calculate_metrics(completed, gantt)
    
    def _calculate_metrics(self, processes: List[Dict], gantt: List[str]) -> Dict:
        """Calculate performance metrics"""
        n = len(processes)
        
        total_waiting = sum(p['waiting'] for p in processes)
        total_turnaround = sum(p['turnaround'] for p in processes)
        
        avg_waiting = total_waiting / n if n > 0 else 0
        avg_turnaround = total_turnaround / n if n > 0 else 0
        
        # Calculate CPU utilization
        max_completion = max(p['completion'] for p in processes) if processes else 0
        total_burst = sum(p['burst'] for p in processes)
        cpu_utilization = (total_burst / max_completion * 100) if max_completion > 0 else 0
        
        # Calculate throughput
        throughput = n / max_completion if max_completion > 0 else 0
        
        # Format Gantt chart
        gantt_chart = " → ".join(gantt)
        
        return {
            'processes': processes,
            'gantt_chart': gantt_chart,
            'avg_waiting_time': avg_waiting,
            'avg_turnaround_time': avg_turnaround,
            'cpu_utilization': cpu_utilization,
            'throughput': throughput,
            'total_time': max_completion
        }
