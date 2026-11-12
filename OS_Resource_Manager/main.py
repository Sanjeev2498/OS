#!/usr/bin/env python3
"""
OS RESOURCE MANAGER - Integrated Application
Simulates major OS resource-management functions

Author: Operating Systems Lab Project
Version: 1.0
"""

import sys
import os
from datetime import datetime

# Add modules directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from scheduler import ProcessScheduler
from memory import MemoryManager
from deadlock import DeadlockHandler
from visualizer import Visualizer
from logger import Logger

class OSResourceManager:
    """Main integrated application for OS resource management simulation"""
    
    def __init__(self):
        self.scheduler = ProcessScheduler()
        self.memory = MemoryManager()
        self.deadlock = DeadlockHandler()
        self.visualizer = Visualizer()
        self.logger = Logger()
        
        # Log application start
        self.logger.log("OS Resource Manager started")
        
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("=" * 70)
        print(" " * 15 + "OS RESOURCE MANAGER")
        print(" " * 10 + "Integrated Resource Management Simulator")
        print("=" * 70)
        print()
    
    def print_main_menu(self):
        """Display main menu"""
        self.print_header()
        print("Main Menu:")
        print("-" * 70)
        print("  1. Process Scheduling (CPU Scheduling Algorithms)")
        print("  2. Memory Management (Allocation Algorithms)")
        print("  3. Deadlock Handling (Banker's Algorithm)")
        print("  4. Analysis & Comparison (Compare Algorithms)")
        print("  5. View Logs (System Activity Log)")
        print("  6. Help & Documentation")
        print("  0. Exit Application")
        print("-" * 70)
    
    def process_scheduling_menu(self):
        """Process scheduling submenu"""
        while True:
            self.clear_screen()
            self.print_header()
            print("MODULE 1: PROCESS SCHEDULING")
            print("-" * 70)
            print("  1. FCFS (First Come First Serve)")
            print("  2. SJF (Shortest Job First)")
            print("  3. Priority Scheduling")
            print("  4. Round Robin")
            print("  5. Load Sample Data")
            print("  6. Enter Custom Data")
            print("  0. Back to Main Menu")
            print("-" * 70)
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.run_fcfs()
            elif choice == '2':
                self.run_sjf()
            elif choice == '3':
                self.run_priority()
            elif choice == '4':
                self.run_round_robin()
            elif choice == '5':
                self.load_sample_processes()
            elif choice == '6':
                self.enter_custom_processes()
            else:
                print("\n❌ Invalid choice! Press Enter to continue...")
                input()
    
    def memory_management_menu(self):
        """Memory management submenu"""
        while True:
            self.clear_screen()
            self.print_header()
            print("MODULE 2: MEMORY MANAGEMENT")
            print("-" * 70)
            print("  1. First Fit Algorithm")
            print("  2. Best Fit Algorithm")
            print("  3. Worst Fit Algorithm")
            print("  4. Load Sample Data")
            print("  5. Enter Custom Data")
            print("  0. Back to Main Menu")
            print("-" * 70)
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.run_first_fit()
            elif choice == '2':
                self.run_best_fit()
            elif choice == '3':
                self.run_worst_fit()
            elif choice == '4':
                self.load_sample_memory()
            elif choice == '5':
                self.enter_custom_memory()
            else:
                print("\n❌ Invalid choice! Press Enter to continue...")
                input()
    
    def deadlock_handling_menu(self):
        """Deadlock handling submenu"""
        while True:
            self.clear_screen()
            self.print_header()
            print("MODULE 3: DEADLOCK HANDLING")
            print("-" * 70)
            print("  1. Banker's Algorithm (Safe State Check)")
            print("  2. Deadlock Detection")
            print("  3. Resource Allocation Graph")
            print("  4. Load Sample Data")
            print("  5. Enter Custom Data")
            print("  0. Back to Main Menu")
            print("-" * 70)
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.run_bankers_algorithm()
            elif choice == '2':
                self.run_deadlock_detection()
            elif choice == '3':
                self.show_resource_graph()
            elif choice == '4':
                self.load_sample_deadlock()
            elif choice == '5':
                self.enter_custom_deadlock()
            else:
                print("\n❌ Invalid choice! Press Enter to continue...")
                input()
    
    def analysis_menu(self):
        """Analysis and comparison menu"""
        while True:
            self.clear_screen()
            self.print_header()
            print("MODULE 4: ANALYSIS & COMPARISON")
            print("-" * 70)
            print("  1. Compare Scheduling Algorithms")
            print("  2. Compare Memory Allocation Algorithms")
            print("  3. Generate Performance Charts")
            print("  4. Export Results to File")
            print("  5. View Summary Statistics")
            print("  0. Back to Main Menu")
            print("-" * 70)
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.compare_scheduling()
            elif choice == '2':
                self.compare_memory()
            elif choice == '3':
                self.generate_charts()
            elif choice == '4':
                self.export_results()
            elif choice == '5':
                self.view_statistics()
            else:
                print("\n❌ Invalid choice! Press Enter to continue...")
                input()
    
    def run_fcfs(self):
        """Run FCFS scheduling algorithm"""
        print("\n" + "=" * 70)
        print("RUNNING: FCFS (First Come First Serve) Scheduling")
        print("=" * 70)
        
        if not self.scheduler.has_processes():
            print("\n⚠️  No processes loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.scheduler.fcfs()
        self.display_scheduling_result(result, "FCFS")
        self.logger.log("FCFS scheduling executed")
        
        input("\nPress Enter to continue...")
    
    def run_sjf(self):
        """Run SJF scheduling algorithm"""
        print("\n" + "=" * 70)
        print("RUNNING: SJF (Shortest Job First) Scheduling")
        print("=" * 70)
        
        if not self.scheduler.has_processes():
            print("\n⚠️  No processes loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.scheduler.sjf()
        self.display_scheduling_result(result, "SJF")
        self.logger.log("SJF scheduling executed")
        
        input("\nPress Enter to continue...")
    
    def run_priority(self):
        """Run Priority scheduling algorithm"""
        print("\n" + "=" * 70)
        print("RUNNING: Priority Scheduling")
        print("=" * 70)
        
        if not self.scheduler.has_processes():
            print("\n⚠️  No processes loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.scheduler.priority()
        self.display_scheduling_result(result, "Priority")
        self.logger.log("Priority scheduling executed")
        
        input("\nPress Enter to continue...")
    
    def run_round_robin(self):
        """Run Round Robin scheduling algorithm"""
        print("\n" + "=" * 70)
        print("RUNNING: Round Robin Scheduling")
        print("=" * 70)
        
        if not self.scheduler.has_processes():
            print("\n⚠️  No processes loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        try:
            quantum = int(input("Enter time quantum (default 2): ") or "2")
            result = self.scheduler.round_robin(quantum)
            self.display_scheduling_result(result, f"Round Robin (Quantum={quantum})")
            self.logger.log(f"Round Robin scheduling executed with quantum={quantum}")
        except ValueError:
            print("\n❌ Invalid quantum value!")
        
        input("\nPress Enter to continue...")
    
    def display_scheduling_result(self, result, algorithm_name):
        """Display scheduling results"""
        print(f"\n{'='*70}")
        print(f"RESULTS: {algorithm_name}")
        print(f"{'='*70}")
        
        # Gantt Chart
        print("\nGantt Chart:")
        print(result['gantt_chart'])
        
        # Process Details Table
        print("\nProcess Details:")
        print(f"{'Process':<10} {'Arrival':<10} {'Burst':<10} {'Waiting':<10} {'Turnaround':<12} {'Completion':<12}")
        print("-" * 70)
        
        for process in result['processes']:
            print(f"{process['pid']:<10} {process['arrival']:<10} {process['burst']:<10} "
                  f"{process['waiting']:<10} {process['turnaround']:<12} {process['completion']:<12}")
        
        # Statistics
        print(f"\n{'='*70}")
        print("Performance Metrics:")
        print(f"  Average Waiting Time:     {result['avg_waiting_time']:.2f} ms")
        print(f"  Average Turnaround Time:  {result['avg_turnaround_time']:.2f} ms")
        print(f"  CPU Utilization:          {result['cpu_utilization']:.2f}%")
        print(f"  Throughput:               {result['throughput']:.2f} processes/unit")
        print(f"{'='*70}")
    
    def run_first_fit(self):
        """Run First Fit memory allocation"""
        print("\n" + "=" * 70)
        print("RUNNING: First Fit Memory Allocation")
        print("=" * 70)
        
        if not self.memory.has_data():
            print("\n⚠️  No memory data loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.memory.first_fit()
        self.display_memory_result(result, "First Fit")
        self.logger.log("First Fit memory allocation executed")
        
        input("\nPress Enter to continue...")
    
    def run_best_fit(self):
        """Run Best Fit memory allocation"""
        print("\n" + "=" * 70)
        print("RUNNING: Best Fit Memory Allocation")
        print("=" * 70)
        
        if not self.memory.has_data():
            print("\n⚠️  No memory data loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.memory.best_fit()
        self.display_memory_result(result, "Best Fit")
        self.logger.log("Best Fit memory allocation executed")
        
        input("\nPress Enter to continue...")
    
    def run_worst_fit(self):
        """Run Worst Fit memory allocation"""
        print("\n" + "=" * 70)
        print("RUNNING: Worst Fit Memory Allocation")
        print("=" * 70)
        
        if not self.memory.has_data():
            print("\n⚠️  No memory data loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.memory.worst_fit()
        self.display_memory_result(result, "Worst Fit")
        self.logger.log("Worst Fit memory allocation executed")
        
        input("\nPress Enter to continue...")
    
    def display_memory_result(self, result, algorithm_name):
        """Display memory allocation results"""
        print(f"\n{'='*70}")
        print(f"RESULTS: {algorithm_name}")
        print(f"{'='*70}")
        
        print("\nMemory Allocation Table:")
        print(f"{'Process':<12} {'Size':<12} {'Block':<12} {'Status':<15} {'Fragment':<12}")
        print("-" * 70)
        
        for allocation in result['allocations']:
            print(f"{allocation['process']:<12} {allocation['size']:<12} "
                  f"{allocation['block']:<12} {allocation['status']:<15} "
                  f"{allocation['fragment']:<12}")
        
        print(f"\n{'='*70}")
        print("Memory Statistics:")
        print(f"  Total Memory:             {result['total_memory']} KB")
        print(f"  Allocated Memory:         {result['allocated_memory']} KB")
        print(f"  Free Memory:              {result['free_memory']} KB")
        print(f"  External Fragmentation:   {result['external_fragmentation']} KB")
        print(f"  Allocation Success Rate:  {result['success_rate']:.2f}%")
        print(f"{'='*70}")
    
    def run_bankers_algorithm(self):
        """Run Banker's Algorithm"""
        print("\n" + "=" * 70)
        print("RUNNING: Banker's Algorithm (Safe State Check)")
        print("=" * 70)
        
        if not self.deadlock.has_data():
            print("\n⚠️  No deadlock data loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.deadlock.bankers_algorithm()
        self.display_deadlock_result(result)
        self.logger.log("Banker's Algorithm executed")
        
        input("\nPress Enter to continue...")
    
    def run_deadlock_detection(self):
        """Run deadlock detection"""
        print("\n" + "=" * 70)
        print("RUNNING: Deadlock Detection")
        print("=" * 70)
        
        if not self.deadlock.has_data():
            print("\n⚠️  No deadlock data loaded! Please load sample data or enter custom data.")
            input("\nPress Enter to continue...")
            return
        
        result = self.deadlock.detect_deadlock()
        
        print(f"\n{'='*70}")
        if result['deadlock_exists']:
            print("⚠️  DEADLOCK DETECTED!")
            print(f"Deadlocked Processes: {', '.join(result['deadlocked_processes'])}")
        else:
            print("✅ NO DEADLOCK - System is safe")
        print(f"{'='*70}")
        
        self.logger.log("Deadlock detection executed")
        input("\nPress Enter to continue...")
    
    def display_deadlock_result(self, result):
        """Display Banker's Algorithm results"""
        print(f"\n{'='*70}")
        print("BANKER'S ALGORITHM RESULTS")
        print(f"{'='*70}")
        
        # Display matrices
        print("\nAllocation Matrix:")
        self.deadlock.print_matrix(result['allocation'])
        
        print("\nMaximum Matrix:")
        self.deadlock.print_matrix(result['maximum'])
        
        print("\nNeed Matrix:")
        self.deadlock.print_matrix(result['need'])
        
        print(f"\nAvailable Resources: {result['available']}")
        
        # Safe state result
        print(f"\n{'='*70}")
        if result['is_safe']:
            print("✅ SYSTEM IS IN SAFE STATE")
            print(f"Safe Sequence: {' → '.join(result['safe_sequence'])}")
        else:
            print("⚠️  SYSTEM IS IN UNSAFE STATE")
            print("Deadlock may occur - request should be denied")
        print(f"{'='*70}")
    
    def load_sample_processes(self):
        """Load sample process data"""
        self.scheduler.load_sample_data()
        print("\n✅ Sample process data loaded successfully!")
        print(f"   Loaded {len(self.scheduler.processes)} processes")
        self.logger.log("Sample process data loaded")
        input("\nPress Enter to continue...")
    
    def load_sample_memory(self):
        """Load sample memory data"""
        self.memory.load_sample_data()
        print("\n✅ Sample memory data loaded successfully!")
        print(f"   Memory blocks: {len(self.memory.blocks)}")
        print(f"   Processes: {len(self.memory.processes)}")
        self.logger.log("Sample memory data loaded")
        input("\nPress Enter to continue...")
    
    def load_sample_deadlock(self):
        """Load sample deadlock data"""
        self.deadlock.load_sample_data()
        print("\n✅ Sample deadlock data loaded successfully!")
        print(f"   Processes: {self.deadlock.num_processes}")
        print(f"   Resource types: {self.deadlock.num_resources}")
        self.logger.log("Sample deadlock data loaded")
        input("\nPress Enter to continue...")
    
    def enter_custom_processes(self):
        """Enter custom process data"""
        print("\n" + "=" * 70)
        print("ENTER CUSTOM PROCESS DATA")
        print("=" * 70)
        print("Enter process details (leave blank to finish)")
        
        try:
            processes = []
            while True:
                pid = input(f"\nProcess ID (or Enter to finish): ").strip()
                if not pid:
                    break
                
                arrival = int(input("  Arrival Time: "))
                burst = int(input("  Burst Time: "))
                priority = int(input("  Priority (1-10): "))
                
                processes.append({
                    'pid': pid,
                    'arrival': arrival,
                    'burst': burst,
                    'priority': priority
                })
            
            if processes:
                self.scheduler.set_processes(processes)
                print(f"\n✅ {len(processes)} processes loaded successfully!")
                self.logger.log(f"Custom process data loaded: {len(processes)} processes")
            else:
                print("\n⚠️  No processes entered")
        
        except ValueError:
            print("\n❌ Invalid input! Please enter numeric values.")
        
        input("\nPress Enter to continue...")
    
    def enter_custom_memory(self):
        """Enter custom memory data"""
        print("\n" + "=" * 70)
        print("ENTER CUSTOM MEMORY DATA")
        print("=" * 70)
        
        try:
            # Memory blocks
            print("\nEnter memory block sizes (leave blank to finish):")
            blocks = []
            while True:
                size = input(f"  Block {len(blocks)+1} size (KB, or Enter to finish): ").strip()
                if not size:
                    break
                blocks.append(int(size))
            
            # Processes
            print("\nEnter process sizes (leave blank to finish):")
            processes = []
            while True:
                size = input(f"  Process {len(processes)+1} size (KB, or Enter to finish): ").strip()
                if not size:
                    break
                processes.append({'pid': f'P{len(processes)+1}', 'size': int(size)})
            
            if blocks and processes:
                self.memory.set_data(blocks, processes)
                print(f"\n✅ Memory data loaded successfully!")
                print(f"   Blocks: {len(blocks)}, Processes: {len(processes)}")
                self.logger.log(f"Custom memory data loaded")
            else:
                print("\n⚠️  Incomplete data")
        
        except ValueError:
            print("\n❌ Invalid input! Please enter numeric values.")
        
        input("\nPress Enter to continue...")
    
    def enter_custom_deadlock(self):
        """Enter custom deadlock data"""
        print("\n" + "=" * 70)
        print("ENTER CUSTOM DEADLOCK DATA")
        print("=" * 70)
        print("(This is complex - consider using sample data)")
        input("\nPress Enter to continue...")
    
    def compare_scheduling(self):
        """Compare all scheduling algorithms"""
        print("\n" + "=" * 70)
        print("COMPARING SCHEDULING ALGORITHMS")
        print("=" * 70)
        
        if not self.scheduler.has_processes():
            print("\n⚠️  No processes loaded! Please load sample data first.")
            input("\nPress Enter to continue...")
            return
        
        # Run all algorithms
        results = {
            'FCFS': self.scheduler.fcfs(),
            'SJF': self.scheduler.sjf(),
            'Priority': self.scheduler.priority(),
            'Round Robin': self.scheduler.round_robin(2)
        }
        
        # Display comparison table
        print("\nComparison Table:")
        print(f"{'Algorithm':<15} {'Avg Wait':<12} {'Avg Turnaround':<15} {'CPU Util%':<12} {'Throughput':<12}")
        print("-" * 70)
        
        for algo, result in results.items():
            print(f"{algo:<15} {result['avg_waiting_time']:<12.2f} "
                  f"{result['avg_turnaround_time']:<15.2f} "
                  f"{result['cpu_utilization']:<12.2f} "
                  f"{result['throughput']:<12.2f}")
        
        # Generate chart
        self.visualizer.plot_scheduling_comparison(results)
        print("\n✅ Comparison chart saved to output/charts/scheduling_comparison.png")
        
        self.logger.log("Scheduling algorithms compared")
        input("\nPress Enter to continue...")
    
    def compare_memory(self):
        """Compare memory allocation algorithms"""
        print("\n" + "=" * 70)
        print("COMPARING MEMORY ALLOCATION ALGORITHMS")
        print("=" * 70)
        
        if not self.memory.has_data():
            print("\n⚠️  No memory data loaded! Please load sample data first.")
            input("\nPress Enter to continue...")
            return
        
        # Run all algorithms
        results = {
            'First Fit': self.memory.first_fit(),
            'Best Fit': self.memory.best_fit(),
            'Worst Fit': self.memory.worst_fit()
        }
        
        # Display comparison table
        print("\nComparison Table:")
        print(f"{'Algorithm':<15} {'Allocated':<12} {'Free':<12} {'Fragment':<12} {'Success%':<12}")
        print("-" * 70)
        
        for algo, result in results.items():
            print(f"{algo:<15} {result['allocated_memory']:<12} "
                  f"{result['free_memory']:<12} "
                  f"{result['external_fragmentation']:<12} "
                  f"{result['success_rate']:<12.2f}")
        
        # Generate chart
        self.visualizer.plot_memory_comparison(results)
        print("\n✅ Comparison chart saved to output/charts/memory_comparison.png")
        
        self.logger.log("Memory algorithms compared")
        input("\nPress Enter to continue...")
    
    def generate_charts(self):
        """Generate all charts"""
        print("\n📊 Generating charts...")
        
        if self.scheduler.has_processes():
            self.compare_scheduling()
        
        if self.memory.has_data():
            self.compare_memory()
        
        print("\n✅ All charts generated!")
        input("\nPress Enter to continue...")
    
    def export_results(self):
        """Export results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/results_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("OS RESOURCE MANAGER - RESULTS EXPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            f.write("Results exported successfully\n")
        
        print(f"\n✅ Results exported to {filename}")
        self.logger.log(f"Results exported to {filename}")
        input("\nPress Enter to continue...")
    
    def view_statistics(self):
        """View summary statistics"""
        print("\n" + "=" * 70)
        print("SUMMARY STATISTICS")
        print("=" * 70)
        print("\n📊 System activity summary will be displayed here")
        print("(Feature in development)")
        input("\nPress Enter to continue...")
    
    def show_resource_graph(self):
        """Show resource allocation graph"""
        print("\n📊 Resource Allocation Graph")
        print("(Feature in development)")
        input("\nPress Enter to continue...")
    
    def view_logs(self):
        """View system logs"""
        self.clear_screen()
        self.print_header()
        print("SYSTEM ACTIVITY LOG")
        print("=" * 70)
        
        logs = self.logger.get_logs()
        if logs:
            for log in logs[-20:]:  # Show last 20 entries
                print(log)
        else:
            print("No logs available")
        
        print("=" * 70)
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """Show help and documentation"""
        self.clear_screen()
        self.print_header()
        print("HELP & DOCUMENTATION")
        print("=" * 70)
        print("""
This integrated application simulates major OS resource management functions:

1. PROCESS SCHEDULING
   - Manages CPU allocation to processes
   - Algorithms: FCFS, SJF, Priority, Round Robin
   - Metrics: Waiting time, Turnaround time, CPU utilization

2. MEMORY MANAGEMENT
   - Manages memory allocation to processes
   - Algorithms: First Fit, Best Fit, Worst Fit
   - Metrics: Fragmentation, Success rate

3. DEADLOCK HANDLING
   - Prevents and detects deadlocks
   - Uses Banker's Algorithm for safety
   - Shows safe sequences

4. ANALYSIS & COMPARISON
   - Compares algorithm performance
   - Generates charts and visualizations
   - Exports results for reporting

For detailed documentation, see README.md
        """)
        print("=" * 70)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                self.clear_screen()
                self.print_main_menu()
                
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '0':
                    print("\n👋 Thank you for using OS Resource Manager!")
                    self.logger.log("Application closed")
                    break
                elif choice == '1':
                    self.process_scheduling_menu()
                elif choice == '2':
                    self.memory_management_menu()
                elif choice == '3':
                    self.deadlock_handling_menu()
                elif choice == '4':
                    self.analysis_menu()
                elif choice == '5':
                    self.view_logs()
                elif choice == '6':
                    self.show_help()
                else:
                    print("\n❌ Invalid choice! Press Enter to continue...")
                    input()
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted by user")
            self.logger.log("Application interrupted")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            self.logger.log(f"Error: {e}")
            input("\nPress Enter to continue...")


def main():
    """Entry point"""
    print("\n🚀 Starting OS Resource Manager...")
    print("Loading modules...\n")
    
    try:
        app = OSResourceManager()
        app.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check that all modules are installed correctly.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
