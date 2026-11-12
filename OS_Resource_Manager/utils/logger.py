"""
Logging Module
Handles system activity logging
"""

import os
from datetime import datetime

class Logger:
    """Handles application logging"""
    
    def __init__(self):
        self.log_file = "output/system.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.log("=" * 70)
        self.log("Logger initialized")
    
    def log(self, message: str):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"⚠️  Logging error: {e}")
    
    def get_logs(self, lines: int = 50):
        """Get last N lines from log file"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
                return [line.strip() for line in all_lines[-lines:]]
        except Exception as e:
            print(f"⚠️  Error reading logs: {e}")
            return []
