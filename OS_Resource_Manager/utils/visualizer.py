"""
Visualization Module
Generates charts and graphs for analysis
"""

import os
from typing import Dict

# Try to import matplotlib, if not available, provide fallback
try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class Visualizer:
    """Handles data visualization and chart generation"""
    
    def __init__(self):
        self.output_dir = "output/charts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def plot_scheduling_comparison(self, results: Dict):
        """Generate comparison chart for scheduling algorithms"""
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️  Matplotlib not installed. Chart generation skipped.")
            self._generate_text_chart(results, "scheduling")
            return
        
        algorithms = list(results.keys())
        avg_waiting = [results[algo]['avg_waiting_time'] for algo in algorithms]
        avg_turnaround = [results[algo]['avg_turnaround_time'] for algo in algorithms]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Waiting Time comparison
        ax1.bar(algorithms, avg_waiting, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Average Waiting Time (ms)')
        ax1.set_title('Average Waiting Time Comparison')
        ax1.grid(axis='y', alpha=0.3)
        
        # Turnaround Time comparison
        ax2.bar(algorithms, avg_turnaround, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
        ax2.set_xlabel('Algorithm')
        ax2.set_ylabel('Average Turnaround Time (ms)')
        ax2.set_title('Average Turnaround Time Comparison')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/scheduling_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_memory_comparison(self, results: Dict):
        """Generate comparison chart for memory allocation algorithms"""
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️  Matplotlib not installed. Chart generation skipped.")
            self._generate_text_chart(results, "memory")
            return
        
        algorithms = list(results.keys())
        allocated = [results[algo]['allocated_memory'] for algo in algorithms]
        fragmentation = [results[algo]['external_fragmentation'] for algo in algorithms]
        success_rate = [results[algo]['success_rate'] for algo in algorithms]
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
        
        # Allocated Memory comparison
        ax1.bar(algorithms, allocated, color=['#3498db', '#e74c3c', '#2ecc71'])
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Allocated Memory (KB)')
        ax1.set_title('Memory Allocation Comparison')
        ax1.grid(axis='y', alpha=0.3)
        
        # Fragmentation comparison
        ax2.bar(algorithms, fragmentation, color=['#3498db', '#e74c3c', '#2ecc71'])
        ax2.set_xlabel('Algorithm')
        ax2.set_ylabel('External Fragmentation (KB)')
        ax2.set_title('Fragmentation Comparison')
        ax2.grid(axis='y', alpha=0.3)
        
        # Success Rate comparison
        ax3.bar(algorithms, success_rate, color=['#3498db', '#e74c3c', '#2ecc71'])
        ax3.set_xlabel('Algorithm')
        ax3.set_ylabel('Success Rate (%)')
        ax3.set_title('Allocation Success Rate')
        ax3.set_ylim(0, 100)
        ax3.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/memory_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_text_chart(self, results: Dict, chart_type: str):
        """Generate simple text-based chart when matplotlib is not available"""
        filename = f"{self.output_dir}/{chart_type}_comparison.txt"
        
        with open(filename, 'w') as f:
            f.write(f"{'='*60}\n")
            f.write(f"{chart_type.upper()} ALGORITHM COMPARISON (Text Format)\n")
            f.write(f"{'='*60}\n\n")
            
            for algo, result in results.items():
                f.write(f"\n{algo}:\n")
                f.write(f"{'='*40}\n")
                for key, value in result.items():
                    if isinstance(value, (int, float)):
                        f.write(f"  {key}: {value:.2f}\n")
        
        print(f"📊 Text chart saved to {filename}")
