"""
NeuroGames Logging System - CS50 Style Implementation
====================================================

This module provides comprehensive logging functionality for the NeuroGames project.
It tracks every program execution with detailed information including:
- Sequential call numbers (auto-incrementing across all log files)
- Execution timestamp (date and time)
- Source file information (name and full path)
- Newest entries appear first for easy monitoring

Author: CS50-inspired implementation
Usage: from src.logger import log_execution; log_execution()
"""

# Import necessary modules for file operations, time handling, and stack inspection
import os           # Operating system interface for file operations
import datetime     # Date and time manipulation utilities
import inspect      # Runtime introspection of live objects (call stack analysis)


# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

# Primary log file location - stored in dedicated logs directory
LOG_FILE = "logs/program_log.txt"

# Legacy log files to maintain compatibility with older versions
LEGACY_LOG_FILES = [
    "program_log.txt",                    # Root directory log file
    "sub/program_log.txt",               # Subdirectory log file
    os.path.join("logs", "program_log.txt")  # New structured location
]


# ============================================================================
# CORE FUNCTIONALITY: CALLER IDENTIFICATION
# ============================================================================

def get_caller_info():
    """
    Identifies the program that called the logging function.
    
    Uses Python's call stack inspection to determine:
    - The filename of the calling program
    - The full path to the calling program
    
    Call stack navigation: This function -> log_execution() -> calling program
    We need to go back 2 frames to reach the actual calling program.
    
    Returns:
        tuple: (filename, full_path) of the calling program
        Returns ("Unknown", "Unknown") if caller cannot be determined
    """
    # Get the current execution frame for stack inspection
    frame = inspect.currentframe()
    
    try:
        # Navigate back through the call stack:
        # frame.f_back = log_execution() function
        # frame.f_back.f_back = actual calling program
        caller_frame = frame.f_back.f_back
        
        # Check if we successfully found the calling frame
        if caller_frame is None:
            return "Unknown", "Unknown"
        
        # Extract the full file path from the code object
        file_path = caller_frame.f_code.co_filename
        
        # Extract just the filename (without directory path) for cleaner display
        file_name = os.path.basename(file_path)
        
        # Return both the clean filename and full path
        return file_name, file_path
        
    finally:
        # Critical: Delete frame reference to prevent memory leaks
        # Python's garbage collector has issues with frame references
        del frame


# ============================================================================
# CORE FUNCTIONALITY: SEQUENTIAL NUMBERING
# ============================================================================

def get_next_call_number():
    """
    Determines the next sequential call number for logging.
    
    Searches through ALL existing log files (current and legacy) to find
    the highest existing call number, then returns the next number in sequence.
    This ensures continuity even when log files are moved or renamed.
    
    Algorithm:
    1. Initialize maximum number to 0
    2. Check each possible log file location
    3. Parse each data line to extract call numbers
    4. Track the highest number found
    5. Return highest + 1 for the next entry
    
    Returns:
        int: Next sequential call number (starts at 1 for new installations)
    """
    # Initialize the highest call number found so far
    max_number = 0
    
    # Check all possible log file locations for existing entries
    for log_file in LEGACY_LOG_FILES:
        # Skip files that don't exist
        if not os.path.exists(log_file):
            continue
            
        try:
            # Open the log file and read all lines
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Process each line in the file
            for line in lines:
                # Skip empty lines and comment lines (starting with #)
                if not line.strip() or line.startswith('#'):
                    continue
                    
                # Split the line by tabs to extract fields
                parts = line.split('\t')
                
                # Ensure the line has at least the call number field
                if len(parts) >= 1:
                    try:
                        # Extract the call number (first field)
                        number = int(parts[0])
                        
                        # Update maximum if this number is higher
                        max_number = max(max_number, number)
                        
                    except ValueError:
                        # Skip lines where the first field isn't a valid number
                        continue
                        
        except Exception:
            # If any error occurs reading this file, skip it and continue
            # This handles file permission issues, encoding problems, etc.
            continue
    
    # Return the next number in sequence
    return max_number + 1


# ============================================================================
# CORE FUNCTIONALITY: LOG FILE MANAGEMENT
# ============================================================================

def ensure_log_directory():
    """
    Ensures the logs directory exists for storing log files.
    
    Creates the directory if it doesn't exist, with error handling
    for permission issues or other filesystem problems.
    """
    # Extract the directory path from the log file location
    log_dir = os.path.dirname(LOG_FILE)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(log_dir):
        try:
            # Create directory with all necessary parent directories
            os.makedirs(log_dir, exist_ok=True)
        except OSError as e:
            # Handle permission errors or other filesystem issues
            print(f"Warning: Could not create log directory {log_dir}: {e}")


def create_log_file_header():
    """
    Creates a new log file with professional header information.
    
    The header includes:
    - Project identification
    - Column descriptions
    - Visual separator for readability
    """
    # Ensure the directory exists before creating the file
    ensure_log_directory()
    
    # Create the log file with header information
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        # Project header with clear identification
        f.write("# NeuroGames Project - Program Execution Log\n")
        
        # Column header explaining the data format
        f.write("# CallNumber\tDate\tTime\tFileName\tFullPath\n")
        
        # Visual separator for improved readability
        f.write("#" + "=" * 80 + "\n")


def insert_entry_at_top(new_entry):
    """
    Inserts a new log entry at the top of the file (newest first).
    
    Algorithm:
    1. Read all existing content
    2. Separate header lines from data lines
    3. Write header + new entry + existing data
    
    Args:
        new_entry (str): Formatted log entry to insert
    """
    # Ensure log file exists before trying to modify it
    if not os.path.exists(LOG_FILE):
        create_log_file_header()
    
    # Read all existing content from the log file
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        existing_lines = f.readlines()
    
    # Separate header lines (comments) from data lines
    header_lines = []  # Lines starting with # (comments/headers)
    data_lines = []    # Actual log data lines
    
    # Classify each line as header or data
    for line in existing_lines:
        if line.startswith('#'):
            header_lines.append(line)
        else:
            data_lines.append(line)
    
    # Rewrite the file with new entry at the top
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        # Write header section first
        f.writelines(header_lines)
        
        # Insert the new entry at the top of data section
        f.write(new_entry)
        
        # Append all existing data entries below
        f.writelines(data_lines)


# ============================================================================
# PRIMARY PUBLIC INTERFACE
# ============================================================================

def log_execution():
    """
    Main logging function - Records the execution of the calling program.
    
    This function should be called at the beginning of any program that
    wants to be tracked in the execution log.
    
    Process:
    1. Determine sequential call number
    2. Get current timestamp
    3. Identify the calling program
    4. Format and store the log entry
    5. Provide user feedback
    
    Usage:
        from src.logger import log_execution
        log_execution()  # Call at program start
    """
    # Step 1: Get the next sequential call number
    call_number = get_next_call_number()
    
    # Step 2: Capture current date and time
    current_time = datetime.datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")  # Format: 2025-10-08
    time_str = current_time.strftime("%H:%M:%S")  # Format: 14:30:25
    
    # Step 3: Identify the program that called this function
    file_name, file_path = get_caller_info()
    
    # Step 4: Format the log entry with tab-separated values
    log_entry = f"{call_number}\t{date_str}\t{time_str}\t{file_name}\t{file_path}\n"
    
    # Step 5: Store the entry in the log file
    try:
        # Insert the new entry at the top (newest first)
        insert_entry_at_top(log_entry)
        
        # Provide success feedback to the user
        print(f"✓ Log entry #{call_number} recorded for: {file_name}")
        
    except Exception as e:
        # Handle any file system errors gracefully
        print(f"✗ Error writing to log file: {e}")


# ============================================================================
# UTILITY FUNCTIONS: LOG READING AND ANALYSIS
# ============================================================================

def read_log():
    """
    Displays all log entries from all log files in a formatted table.
    
    Features:
    - Combines entries from all log file locations
    - Removes duplicates based on entry content
    - Sorts by call number (newest first)
    - Displays in readable table format
    """
    print("=== 📋 NEUROGAMES PROGRAM EXECUTION LOG ===")
    
    # Collection to store all unique log entries
    all_entries = []
    
    # Set to track entries and prevent duplicates
    seen_entries = set()
    
    # Process all possible log file locations
    for log_file in LEGACY_LOG_FILES:
        # Skip non-existent files
        if not os.path.exists(log_file):
            continue
            
        try:
            # Read all lines from this log file
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Process each line in the file
            for line in lines:
                # Skip empty lines and comments
                if not line.strip() or line.startswith('#'):
                    continue
                    
                # Parse the tab-separated fields
                parts = line.strip().split('\t')
                
                # Ensure line has all required fields
                if len(parts) >= 4:
                    try:
                        # Extract individual fields
                        number = int(parts[0])      # Call number
                        date = parts[1]             # Date
                        time = parts[2]             # Time
                        filename = parts[3]         # Filename
                        filepath = parts[4] if len(parts) > 4 else ''  # Full path (optional)
                        
                        # Create unique identifier for duplicate detection
                        entry_key = (number, date, time, filename)
                        
                        # Only add if we haven't seen this exact entry before
                        if entry_key not in seen_entries:
                            seen_entries.add(entry_key)
                            all_entries.append({
                                'number': number,
                                'date': date,
                                'time': time,
                                'filename': filename,
                                'filepath': filepath
                            })
                            
                    except ValueError:
                        # Skip lines with invalid number format
                        continue
                        
        except Exception:
            # Skip files that can't be read
            continue
    
    # Check if any entries were found
    if not all_entries:
        print("❌ No log entries found.")
        return
    
    # Sort entries by call number (highest first = newest first)
    all_entries.sort(key=lambda x: x['number'], reverse=True)
    
    # Display formatted table header
    print(f"{'#':<4} {'Date':<12} {'Time':<10} {'Program':<20}")
    print("=" * 50)
    
    # Display each entry in the table
    for entry in all_entries:
        print(f"{entry['number']:<4} {entry['date']:<12} {entry['time']:<10} {entry['filename']:<20}")
    
    # Display summary statistics
    print(f"\n📊 Total executions: {len(all_entries)}")


def get_log_stats():
    """
    Displays comprehensive statistics about program usage.
    
    Statistics include:
    - Total number of executions
    - Date range of executions
    - Most frequently executed programs
    - Usage patterns
    """
    print("=== 📊 EXECUTION STATISTICS ===")
    
    # Collection for all log entries
    all_entries = []
    
    # Read entries from all log files (same logic as read_log)
    seen_entries = set()
    
    for log_file in LEGACY_LOG_FILES:
        if not os.path.exists(log_file):
            continue
            
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                if not line.strip() or line.startswith('#'):
                    continue
                    
                parts = line.strip().split('\t')
                if len(parts) >= 4:
                    try:
                        number = int(parts[0])
                        date = parts[1]
                        time = parts[2]
                        filename = parts[3]
                        
                        entry_key = (number, date, time, filename)
                        if entry_key not in seen_entries:
                            seen_entries.add(entry_key)
                            all_entries.append({
                                'number': number,
                                'date': date,
                                'time': time,
                                'filename': filename
                            })
                    except ValueError:
                        continue
        except Exception:
            continue
    
    # Check if any data exists
    if not all_entries:
        print("❌ No execution data found.")
        return
    
    # Sort by call number for analysis
    all_entries.sort(key=lambda x: x['number'], reverse=True)
    
    # Basic statistics
    print(f"Total Executions: {len(all_entries)}")
    
    # Date range analysis
    if all_entries:
        newest = all_entries[0]  # First item after reverse sort
        oldest = all_entries[-1]  # Last item after reverse sort
        
        print(f"Most Recent: {newest['date']} {newest['time']}")
        print(f"Oldest Entry: {oldest['date']} {oldest['time']}")
    
    # Program frequency analysis
    program_counts = {}
    for entry in all_entries:
        program = entry['filename']
        program_counts[program] = program_counts.get(program, 0) + 1
    
    # Display top programs
    if program_counts:
        print("\n🏆 Most Executed Programs:")
        # Sort by frequency (descending) and show top 5
        sorted_programs = sorted(program_counts.items(), key=lambda x: x[1], reverse=True)
        for program, count in sorted_programs[:5]:
            print(f"   {program}: {count} executions")


# ============================================================================
# MODULE USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    """
    Demonstration of the logging system functionality.
    
    This code runs when the module is executed directly (not imported).
    It shows how to use all the logging functions.
    """
    print("=== NeuroGames Logging System Demo ===")
    
    # Test the main logging function
    print("\n1. Recording execution...")
    log_execution()
    
    # Display the current log
    print("\n2. Current log contents:")
    read_log()
    
    # Show statistics
    print("\n3. Usage statistics:")
    get_log_stats()