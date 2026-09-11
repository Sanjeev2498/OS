#!/usr/bin/env python3
"""
Task 1: System Calls and Process Creation - Simple College Lab Version
"""

import os
import multiprocessing
import subprocess

def child_process_work():
    """Simple child process work - Cross-platform"""
    print("=== CHILD PROCESS ===")
    print(f"Child PID: {os.getpid()}")
    print(f"Parent PID: {os.getppid()}")
    
    # Execute simple commands
    print("\nExecuting commands from child:")
    try:
        # Directory listing - cross-platform
        if os.name == 'posix':  # Linux/Unix
            result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
        else:  # Windows
            result = subprocess.run(['dir'], shell=True, capture_output=True, text=True)
        
        print("Directory listing:")
        print(result.stdout[:100])  # Show first 100 characters
        
        # Show date - cross-platform
        if os.name == 'posix':  # Linux/Unix
            result = subprocess.run(['date'], capture_output=True, text=True)
        else:  # Windows
            result = subprocess.run(['date', '/t'], shell=True, capture_output=True, text=True)
        
        print(f"Current date: {result.stdout.strip()}")
        
    except Exception as e:
        print(f"Command error: {e}")
    
    print("Child process finished")
    return "Done"

def simple_file_operations():
    """Simple file operations demo"""
    print("\n=== FILE OPERATIONS ===")
    
    # 1. Create and write to file
    filename = "test_file.txt"
    print(f"1. Creating file: {filename}")
    
    try:
        # Write to file
        with open(filename, 'w') as f:
            f.write("Hello from OS Lab Task 1\n")
            f.write("This is a test file\n")
            f.write("File operations demo\n")
        print("   File created and written successfully")
        
        # Read from file
        print("2. Reading from file:")
        with open(filename, 'r') as f:
            content = f.read()
            print(f"   File content:\n{content}")
        
        # Delete file
        os.remove(filename)
        print("3. File deleted")
        
    except Exception as e:
        print(f"   Error: {e}")

def simple_interface_check():
    """Simple system interface check - Cross-platform"""
    print("\n=== SYSTEM INTERFACE CHECK ===")
    
    # Check null device - cross-platform
    try:
        print("1. Testing null device:")
        if os.name == 'posix':  # Linux/Unix
            with open('/dev/null', 'w') as null_dev:
                null_dev.write("Test message to /dev/null\n")
            print("   Successfully wrote to /dev/null")
        else:  # Windows
            with open('NUL', 'w') as nul:
                nul.write("Test message to NUL\n")
            print("   Successfully wrote to NUL device")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Try to access system info - cross-platform
    try:
        print("2. Getting system info:")
        if os.name == 'posix':  # Linux/Unix
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
        else:  # Windows
            result = subprocess.run(['systeminfo'], shell=True, capture_output=True, text=True)
        
        if result.stdout:
            # Show first few lines
            lines = result.stdout.split('\n')[:3]
            for line in lines:
                if line.strip():
                    print(f"   {line.strip()}")
    except Exception as e:
        print(f"   Error: {e}")

def simple_error_demo():
    """Simple error handling demo - Cross-platform"""
    print("\n=== ERROR HANDLING DEMO ===")
    
    # Test 1: File not found
    try:
        print("1. Trying to read non-existent file:")
        with open("does_not_exist.txt", 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("   ERROR: File not found (handled properly)")
    
    # Test 2: Permission error - cross-platform
    try:
        print("2. Trying to access restricted location:")
        if os.name == 'posix':  # Linux/Unix
            with open("/root/test.txt", 'w') as f:
                f.write("test")
        else:  # Windows
            with open("C:\\Windows\\system32\\test.txt", 'w') as f:
                f.write("test")
    except PermissionError:
        print("   ERROR: Permission denied (handled properly)")
    except Exception as e:
        print(f"   ERROR: Access denied - {e}")

def main():
    print("=" * 50)
    print("Task 1: System Calls and Process Creation")
    print("=" * 50)
    
    # Show main process info
    print(f"Main Process PID: {os.getpid()}")
    print(f"Main Process Parent PID: {os.getppid()}")
    
    # Create child process
    print(f"\n=== CREATING CHILD PROCESS ===")
    
    try:
        # Simple multiprocessing
        process = multiprocessing.Process(target=child_process_work)
        
        print("Starting child process...")
        process.start()
        
        print(f"Child process PID: {process.pid}")
        print("Waiting for child to finish...")
        
        # Wait for child
        process.join()
        
        print(f"Child process finished with exit code: {process.exitcode}")
        
    except Exception as e:
        print(f"Error with child process: {e}")
    
    # File operations
    simple_file_operations()
    
    # System interface check
    simple_interface_check()
    
    # Error handling
    simple_error_demo()
    
    print("\n" + "=" * 50)
    print("Task 1 Complete!")
    print("Demonstrated:")
    print("✓ Child process creation")
    print("✓ PID and PPID display")
    print("✓ Command execution from child")
    print("✓ File operations")
    print("✓ System interface access")
    print("✓ Error handling")
    print("=" * 50)

if __name__ == "__main__":
    main()