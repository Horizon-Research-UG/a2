"""
NeuroGames Project - Main Entry Point
====================================

This is the primary entry point for the NeuroGames educational software suite.
It provides a user-friendly menu system to access all project functionality.

The program demonstrates CS50-style programming principles:
- Clear user interface design
- Modular code organization  
- Comprehensive error handling
- Educational documentation

Author: CS50-inspired implementation
Usage: python main.py
"""

# Import system modules for basic functionality
import sys      # System-specific parameters and functions
import os       # Operating system interface

# Add the src directory to Python's module search path
# This allows us to import our custom modules from the src/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our custom modules from the src directory
try:
    # Import the logging system for execution tracking
    from logger import log_execution, read_log, get_log_stats
    
    # Import the PDF generation system
    from pdf_generator import main as pdf_generator_main
    
except ImportError as e:
    # Handle missing module errors gracefully
    print(f"❌ Error importing modules: {e}")
    print("Please ensure all files are in the correct directories.")
    print("Expected structure:")
    print("  src/logger.py")
    print("  src/pdf_generator.py")
    sys.exit(1)


# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

# Program metadata
PROGRAM_NAME = "NeuroGames Educational Suite"
VERSION = "1.0.0"
AUTHOR = "CS50-Inspired Implementation"

# Menu options with descriptions
MENU_OPTIONS = {
    "1": {
        "title": "Generate PDF Files",
        "description": "Create multiple PDF versions with geometric shapes",
        "function": "run_pdf_generator"
    },
    "2": {
        "title": "View Execution Log", 
        "description": "Display all recorded program executions",
        "function": "run_log_viewer"
    },
    "3": {
        "title": "Show Usage Statistics",
        "description": "Display program usage analytics and trends", 
        "function": "run_statistics"
    },
    "4": {
        "title": "About This Program",
        "description": "Information about the NeuroGames project",
        "function": "show_about"
    },
    "0": {
        "title": "Exit Program",
        "description": "Quit the NeuroGames suite",
        "function": "exit_program"
    }
}


# ============================================================================
# USER INTERFACE FUNCTIONS
# ============================================================================

def display_header():
    """
    Displays the program header with title and version information.
    
    Creates a professional-looking header that identifies the program
    and provides context about its educational purpose.
    """
    # Clear visual separator
    print("=" * 70)
    
    # Program title and version
    print(f"🎓 {PROGRAM_NAME} v{VERSION}")
    print(f"📚 {AUTHOR}")
    
    # Visual separator
    print("=" * 70)
    
    # Brief description
    print("Educational software demonstrating CS50 programming principles")
    print("🔧 Modular design • 📖 Comprehensive docs • 🛡️ Error handling")
    print()


def display_menu():
    """
    Displays the main menu with all available options.
    
    Shows each menu option with:
    - Selection number
    - Option title  
    - Brief description of functionality
    """
    print("📋 Main Menu - Select an option:")
    print("-" * 40)
    
    # Display each menu option
    for option_key, option_data in MENU_OPTIONS.items():
        title = option_data["title"]
        description = option_data["description"]
        
        # Format: "1. Generate PDF Files - Create multiple PDF versions..."
        print(f"  {option_key}. {title}")
        print(f"     {description}")
        print()


def get_user_choice():
    """
    Gets and validates the user's menu selection.
    
    Continues prompting until a valid menu option is selected.
    Provides clear feedback for invalid selections.
    
    Returns:
        str: Valid menu option key (e.g., "1", "2", "0")
    """
    # List of valid menu options for validation
    valid_options = list(MENU_OPTIONS.keys())
    
    # Continue asking until valid choice is made
    while True:
        # Get user input
        choice = input(f"Enter your choice ({'/'.join(valid_options)}): ").strip()
        
        # Check if choice is valid
        if choice in valid_options:
            return choice
        
        # Invalid choice - provide helpful feedback
        print(f"❌ Invalid choice '{choice}'. Please select from: {', '.join(valid_options)}")
        print()


# ============================================================================
# MENU ACTION FUNCTIONS
# ============================================================================

def run_pdf_generator():
    """
    Launches the PDF generation module.
    
    Calls the main function from the pdf_generator module,
    which handles all PDF creation functionality.
    """
    print("\n🚀 Launching PDF Generator...")
    print("-" * 40)
    
    try:
        # Call the PDF generator's main function
        pdf_generator_main()
        
    except Exception as e:
        # Handle any errors in the PDF generator
        print(f"❌ Error in PDF generator: {e}")
        print("Please check your input and try again.")
    
    # Pause before returning to menu
    input("\nPress Enter to return to main menu...")


def run_log_viewer():
    """
    Displays the execution log using the logging module.
    
    Shows all recorded program executions in a formatted table.
    """
    print("\n📋 Program Execution Log")
    print("-" * 40)
    
    try:
        # Call the log reading function
        read_log()
        
    except Exception as e:
        # Handle any errors in log reading
        print(f"❌ Error reading log: {e}")
        print("The log file may be missing or corrupted.")
    
    # Pause before returning to menu
    input("\nPress Enter to return to main menu...")


def run_statistics():
    """
    Displays program usage statistics using the logging module.
    
    Shows analytics about program usage patterns and trends.
    """
    print("\n📊 Usage Statistics")
    print("-" * 40)
    
    try:
        # Call the statistics function
        get_log_stats()
        
    except Exception as e:
        # Handle any errors in statistics generation
        print(f"❌ Error generating statistics: {e}")
        print("The log file may be missing or corrupted.")
    
    # Pause before returning to menu  
    input("\nPress Enter to return to main menu...")


def show_about():
    """
    Displays information about the NeuroGames project.
    
    Provides educational context and technical details about
    the project's purpose and implementation.
    """
    print("\n📖 About NeuroGames Educational Suite")
    print("-" * 50)
    print()
    
    # Project description
    print("🎯 Purpose:")
    print("   Educational software demonstrating professional programming practices")
    print("   inspired by Harvard's CS50 course methodology.")
    print()
    
    # Technical details
    print("🔧 Technical Features:")
    print("   • Modular architecture with separated concerns")
    print("   • Comprehensive documentation on every function")
    print("   • Robust error handling and user input validation")
    print("   • Professional project structure and organization")
    print()
    
    # Educational value
    print("📚 Educational Value:")
    print("   • Demonstrates CS50 programming principles")
    print("   • Shows best practices in Python development")
    print("   • Includes real-world software engineering patterns")
    print("   • Provides examples of user interface design")
    print()
    
    # Module descriptions
    print("🧩 Modules:")
    print("   • PDF Generator: Creates geometric shape PDFs with random distributions")
    print("   • Logger: Tracks all program executions for analysis")
    print("   • Main: Provides unified interface to all functionality")
    print()
    
    # Credits
    print("🎓 Inspiration:")
    print("   Harvard CS50 - Introduction to Computer Science")
    print("   Prof. David J. Malan's teaching philosophy")
    print("   'Make code readable, maintainable, and educational'")
    
    # Pause before returning to menu
    input("\nPress Enter to return to main menu...")


def exit_program():
    """
    Handles program exit with a friendly goodbye message.
    
    Provides clear confirmation that the program is ending
    and thanks the user for using the software.
    """
    print("\n👋 Thank you for using NeuroGames Educational Suite!")
    print("🎓 Keep coding and learning!")
    print()
    
    # Exit the program
    sys.exit(0)


# ============================================================================
# MAIN PROGRAM LOOP
# ============================================================================

def main():
    """
    Main program execution function.
    
    Orchestrates the entire program flow:
    1. Log the program execution
    2. Display header and welcome
    3. Run the main menu loop
    4. Handle user selections
    5. Process menu actions
    """
    # Log this program execution for tracking
    log_execution()
    
    # Display program header
    display_header()
    
    # Main program loop - continues until user exits
    while True:
        try:
            # Display the menu options
            display_menu()
            
            # Get user's menu choice
            choice = get_user_choice()
            
            # Get the function name for the selected option
            function_name = MENU_OPTIONS[choice]["function"]
            
            # Execute the appropriate function based on user choice
            if function_name == "run_pdf_generator":
                run_pdf_generator()
            elif function_name == "run_log_viewer":
                run_log_viewer()
            elif function_name == "run_statistics":
                run_statistics()
            elif function_name == "show_about":
                show_about()
            elif function_name == "exit_program":
                exit_program()
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\n❌ Program interrupted by user.")
            print("👋 Goodbye!")
            sys.exit(0)
            
        except Exception as e:
            # Handle any unexpected errors
            print(f"\n❌ An unexpected error occurred: {e}")
            print("The program will continue running.")
            input("Press Enter to return to main menu...")


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Program entry point - executes when script is run directly.
    
    This condition ensures the main() function only runs when the script
    is executed directly (python main.py), not when imported as a module.
    
    This is a Python best practice that allows modules to be both
    executable scripts and importable libraries.
    """
    main()
# === Modul 1: PDF ERSTELLEN ===
import pdf
pdf.create_pdf()