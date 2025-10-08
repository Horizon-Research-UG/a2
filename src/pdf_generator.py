"""
NeuroGames PDF Generator - CS50 Style Implementation
===================================================

This module generates multiple PDF files containing randomly distributed geometric shapes.
Each PDF version contains the same number and type of objects, but with unique random
positioning, creating distinct variations suitable for testing, presentations, or educational purposes.

Supported geometric shapes:
- Circles (drawn as ellipses)
- Triangles (drawn with lines)
- Rectangles (drawn as filled rectangles)
- Pentagons (5-sided polygons)
- Hexagons (6-sided polygons)

Author: CS50-inspired implementation
Usage: python src/pdf_generator.py
"""

# Import necessary modules for PDF generation, mathematical calculations, and logging
import random       # Random number generation for object positioning and sizing
import math        # Mathematical functions for polygon calculations
from fpdf import FPDF  # PDF generation library
import os          # Operating system interface for file operations

# Import our custom logging system
from logger import log_execution


# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

# PDF page dimensions in millimeters (A4 standard)
PAGE_WIDTH = 210    # A4 width in mm
PAGE_HEIGHT = 297   # A4 height in mm

# Object placement constraints
MIN_OBJECT_SIZE = 15    # Minimum size for any geometric object
MAX_OBJECT_SIZE = 30    # Maximum size for any geometric object
PAGE_MARGIN = 15        # Margin from page edges (1.5 cm = 15mm) - professional spacing

# User input limits
MIN_PDF_COUNT = 1       # Minimum number of PDF versions to generate
MAX_PDF_COUNT = 10      # Maximum number of PDF versions to generate
MIN_OBJECT_COUNT = 1    # Minimum objects per PDF
MAX_OBJECT_COUNT = 20   # Maximum objects per PDF

# Output directory for generated PDF files
OUTPUT_DIR = "output"

# Available geometric shapes with user-friendly names
AVAILABLE_SHAPES = {
    "1": "Circle",      # Circular objects
    "2": "Triangle",    # Three-sided polygons
    "3": "Rectangle",   # Four-sided rectangles
    "4": "Pentagon",    # Five-sided polygons
    "5": "Hexagon"      # Six-sided polygons
}


# ============================================================================
# UTILITY FUNCTIONS: INPUT VALIDATION
# ============================================================================

def get_user_input_string(prompt):
    """
    Gets a string input from the user with prompt display.
    
    Args:
        prompt (str): The prompt message to display to the user
        
    Returns:
        str: The user's input string
    """
    # Display the prompt and capture user input
    user_input = input(prompt)
    
    # Return the input (strip whitespace for cleaner processing)
    return user_input.strip()


def get_user_input_integer(prompt, min_value, max_value):
    """
    Gets an integer input from the user within specified bounds.
    
    Continues prompting until a valid integer within range is provided.
    Handles invalid input gracefully with error messages.
    
    Args:
        prompt (str): The prompt message to display
        min_value (int): Minimum acceptable value (inclusive)
        max_value (int): Maximum acceptable value (inclusive)
        
    Returns:
        int: Valid integer within the specified range
    """
    # Continue asking until valid input is received
    while True:
        try:
            # Get user input and attempt to convert to integer
            user_input = input(prompt)
            value = int(user_input)
            
            # Check if the value is within acceptable range
            if min_value <= value <= max_value:
                return value  # Valid input - return the value
            else:
                # Value out of range - show error and continue loop
                print(f"Please enter a number between {min_value} and {max_value}.")
                
        except ValueError:
            # Invalid integer format - show error and continue loop
            print("Invalid input. Please enter a valid number.")


def get_shape_choice():
    """
    Displays available shapes and gets user's choice.
    
    Shows a numbered menu of available geometric shapes and validates
    the user's selection.
    
    Returns:
        str: The name of the selected shape (e.g., "Circle", "Triangle")
    """
    # Display the shape selection menu
    print("Select the geometric shape for your objects:")
    
    # Show each available shape with its selection number
    for number, shape_name in AVAILABLE_SHAPES.items():
        print(f"  {number}: {shape_name}")
    
    # Get user's choice with validation
    while True:
        # Prompt for shape selection
        choice = input(f"Enter your choice (1-{len(AVAILABLE_SHAPES)}): ")
        
        # Check if the choice is valid
        if choice in AVAILABLE_SHAPES:
            # Return the shape name corresponding to the choice
            return AVAILABLE_SHAPES[choice]
        else:
            # Invalid choice - show error and continue
            print(f"Invalid choice. Please enter a number between 1 and {len(AVAILABLE_SHAPES)}.")


def get_pdf_format_choice(pdf_count):
    """
    Gets user's preference for PDF output format when creating multiple versions.
    
    For single PDF creation, this function is not called.
    For multiple PDFs, offers two options:
    1. Separate files - Each version as its own PDF file
    2. Combined file - All versions as pages in one PDF file
    
    Args:
        pdf_count (int): Number of PDF versions to be created
        
    Returns:
        str: "separate" for individual files, "combined" for single multi-page PDF
    """
    # Only ask for format choice when creating multiple PDFs
    if pdf_count == 1:
        return "separate"  # Single PDF is always "separate" by definition
    
    # Display format options
    print()
    print("📋 PDF Output Format Options:")
    print("  1. Separate Files - Each version as individual PDF file")
    print(f"     (Creates {pdf_count} separate PDF files)")
    print("  2. Combined File - All versions as pages in one PDF file")
    print(f"     (Creates 1 PDF file with {pdf_count} pages)")
    
    # Get user's format preference
    while True:
        choice = input("Select output format (1 for separate, 2 for combined): ").strip()
        
        if choice == "1":
            return "separate"
        elif choice == "2":
            return "combined"
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


# ============================================================================
# UTILITY FUNCTIONS: FILE SYSTEM OPERATIONS
# ============================================================================

def ensure_output_directory():
    """
    Ensures the output directory exists for storing generated PDF files.
    
    Creates the directory if it doesn't exist, with error handling for
    permission issues or other filesystem problems.
    """
    # Check if the output directory already exists
    if not os.path.exists(OUTPUT_DIR):
        try:
            # Create the directory with all necessary parent directories
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            print(f"📁 Created output directory: {OUTPUT_DIR}")
        except OSError as e:
            # Handle directory creation errors
            print(f"⚠️  Warning: Could not create output directory {OUTPUT_DIR}: {e}")
            print("PDFs will be saved in the current directory instead.")


def generate_pdf_filename(base_name, version_number, total_versions):
    """
    Generates an appropriate filename for a PDF based on version information.
    
    Naming convention:
    - Single PDF: "basename.pdf"
    - Multiple PDFs: "basename_Version_X.pdf"
    
    Args:
        base_name (str): Base name provided by user
        version_number (int): Current version number (1-based)
        total_versions (int): Total number of versions being created
        
    Returns:
        str: Complete filename with .pdf extension
    """
    # For single PDF, use simple name without version number
    if total_versions == 1:
        return f"{base_name}.pdf"
    
    # For multiple PDFs, include version number for clarity
    return f"{base_name}_Version_{version_number}.pdf"


def get_pdf_filepath(filename):
    """
    Generates the complete file path for a PDF file.
    
    Combines the output directory with the filename to create
    the full path where the PDF will be saved.
    
    Args:
        filename (str): Name of the PDF file
        
    Returns:
        str: Complete file path for saving the PDF
    """
    # Combine output directory with filename
    return os.path.join(OUTPUT_DIR, filename)


# ============================================================================
# GEOMETRIC SHAPE DRAWING FUNCTIONS
# ============================================================================

def draw_circle(pdf, x, y, size):
    """
    Draws a circle at the specified position on the PDF.
    
    Uses FPDF's ellipse function with equal width and height to create
    a perfect circle with black outline and white fill.
    
    Args:
        pdf (FPDF): The PDF object to draw on
        x (float): X coordinate of the circle (top-left of bounding box)
        y (float): Y coordinate of the circle (top-left of bounding box)
        size (float): Diameter of the circle
    """
    # Draw ellipse with equal width and height (creates a circle)
    # Style 'DF' = Draw outline and Fill interior
    pdf.ellipse(x, y, size, size, style='DF')


def draw_triangle(pdf, x, y, size):
    """
    Draws a triangle at the specified position on the PDF.
    
    Creates an equilateral triangle by calculating three points
    and connecting them with lines.
    
    Triangle points:
    - Top point: centered horizontally, at top of bounding area
    - Bottom left: left edge of bounding area
    - Bottom right: right edge of bounding area
    
    Args:
        pdf (FPDF): The PDF object to draw on
        x (float): X coordinate of the triangle's bounding box
        y (float): Y coordinate of the triangle's bounding box
        size (float): Size of the triangle's bounding box
    """
    # Calculate the three points of the triangle
    top_point = (x + size/2, y)           # Top vertex (centered)
    bottom_left = (x, y + size)           # Bottom left vertex
    bottom_right = (x + size, y + size)   # Bottom right vertex
    
    # Draw the triangle by connecting the three points with lines
    pdf.line(top_point[0], top_point[1], bottom_left[0], bottom_left[1])      # Top to bottom-left
    pdf.line(bottom_left[0], bottom_left[1], bottom_right[0], bottom_right[1]) # Bottom edge
    pdf.line(bottom_right[0], bottom_right[1], top_point[0], top_point[1])     # Bottom-right to top


def draw_rectangle(pdf, x, y, size):
    """
    Draws a rectangle (square) at the specified position on the PDF.
    
    Uses FPDF's rectangle function with equal width and height to create
    a square with black outline and white fill.
    
    Args:
        pdf (FPDF): The PDF object to draw on
        x (float): X coordinate of the rectangle (top-left corner)
        y (float): Y coordinate of the rectangle (top-left corner)
        size (float): Width and height of the square
    """
    # Draw rectangle with equal width and height (creates a square)
    # Style 'DF' = Draw outline and Fill interior
    pdf.rect(x, y, size, size, style='DF')


def draw_pentagon(pdf, x, y, size):
    """
    Draws a pentagon at the specified position on the PDF.
    
    Creates a regular pentagon by calculating five points evenly distributed
    around a circle, then connecting them with lines.
    
    Mathematical approach:
    - Center the pentagon in the given bounding box
    - Calculate 5 points at angles: 0°, 72°, 144°, 216°, 288°
    - Start at top (subtract π/2 to rotate starting point upward)
    
    Args:
        pdf (FPDF): The PDF object to draw on
        x (float): X coordinate of the pentagon's bounding box
        y (float): Y coordinate of the pentagon's bounding box
        size (float): Size of the pentagon's bounding box
    """
    # Calculate the center point of the pentagon
    center_x = x + size/2
    center_y = y + size/2
    
    # Calculate the radius (distance from center to vertices)
    radius = size/2
    
    # Calculate the five vertices of the pentagon
    points = []
    for i in range(5):  # Five vertices for pentagon
        # Calculate angle for this vertex (72° apart, starting at top)
        angle = i * 2 * math.pi / 5 - math.pi/2
        
        # Calculate x,y coordinates using trigonometry
        point_x = center_x + radius * math.cos(angle)
        point_y = center_y + radius * math.sin(angle)
        
        # Store the calculated point
        points.append((point_x, point_y))
    
    # Draw the pentagon by connecting all adjacent vertices
    for i in range(5):  # Connect each point to the next
        current_point = points[i]
        next_point = points[(i + 1) % 5]  # Wrap around to first point after last
        
        # Draw line between current and next point
        pdf.line(current_point[0], current_point[1], next_point[0], next_point[1])


def draw_hexagon(pdf, x, y, size):
    """
    Draws a hexagon at the specified position on the PDF.
    
    Creates a regular hexagon by calculating six points evenly distributed
    around a circle, then connecting them with lines.
    
    Mathematical approach:
    - Center the hexagon in the given bounding box
    - Calculate 6 points at angles: 0°, 60°, 120°, 180°, 240°, 300°
    - Start at top (subtract π/2 to rotate starting point upward)
    
    Args:
        pdf (FPDF): The PDF object to draw on
        x (float): X coordinate of the hexagon's bounding box
        y (float): Y coordinate of the hexagon's bounding box
        size (float): Size of the hexagon's bounding box
    """
    # Calculate the center point of the hexagon
    center_x = x + size/2
    center_y = y + size/2
    
    # Calculate the radius (distance from center to vertices)
    radius = size/2
    
    # Calculate the six vertices of the hexagon
    points = []
    for i in range(6):  # Six vertices for hexagon
        # Calculate angle for this vertex (60° apart, starting at top)
        angle = i * 2 * math.pi / 6 - math.pi/2
        
        # Calculate x,y coordinates using trigonometry
        point_x = center_x + radius * math.cos(angle)
        point_y = center_y + radius * math.sin(angle)
        
        # Store the calculated point
        points.append((point_x, point_y))
    
    # Draw the hexagon by connecting all adjacent vertices
    for i in range(6):  # Connect each point to the next
        current_point = points[i]
        next_point = points[(i + 1) % 6]  # Wrap around to first point after last
        
        # Draw line between current and next point
        pdf.line(current_point[0], current_point[1], next_point[0], next_point[1])


# Shape drawing function dispatcher
SHAPE_DRAWING_FUNCTIONS = {
    "Circle": draw_circle,
    "Triangle": draw_triangle,
    "Rectangle": draw_rectangle,
    "Pentagon": draw_pentagon,
    "Hexagon": draw_hexagon
}


# ============================================================================
# CORE PDF GENERATION FUNCTIONS
# ============================================================================

def create_single_pdf(filename, shape_name, object_count):
    """
    Creates a single PDF file with randomly distributed geometric objects.
    
    Process:
    1. Create new PDF document
    2. Configure page settings and drawing styles
    3. Generate random positions and sizes for each object
    4. Draw each object using the appropriate shape function
    5. Save the PDF file
    
    Args:
        filename (str): Name of the PDF file to create
        shape_name (str): Type of geometric shape to draw
        object_count (int): Number of objects to place on the page
        
    Returns:
        bool: True if PDF was created successfully, False otherwise
    """
    try:
        # Create a new PDF document
        pdf = FPDF()
        
        # Add a page to the document
        pdf.add_page()
        
        # Configure page settings
        pdf.set_auto_page_break(auto=False, margin=0)  # Disable automatic page breaks
        
        # Set drawing colors
        pdf.set_draw_color(0, 0, 0)      # Black outline (RGB: 0,0,0)
        pdf.set_fill_color(255, 255, 255) # White fill (RGB: 255,255,255)
        
        # Get the drawing function for the selected shape
        draw_function = SHAPE_DRAWING_FUNCTIONS[shape_name]
        
        # Generate and draw each object
        for object_index in range(object_count):
            # Generate random size for this object first
            size = random.randint(MIN_OBJECT_SIZE, MAX_OBJECT_SIZE)
            
            # Calculate available positioning space with proper margin handling
            # Professional PDF layout: 1.5cm (15mm) margins on all sides
            # 
            # Logic: Object positioned at (x,y) extends to (x+size, y+size)
            # Therefore: x+size must be <= PAGE_WIDTH-PAGE_MARGIN
            # Which means: x must be <= PAGE_WIDTH-size-PAGE_MARGIN
            
            max_x = PAGE_WIDTH - size - PAGE_MARGIN   # Rightmost valid X position
            max_y = PAGE_HEIGHT - size - PAGE_MARGIN  # Bottommost valid Y position
            
            # Ensure we have valid positioning space (object isn't too large for page)
            if max_x < PAGE_MARGIN or max_y < PAGE_MARGIN:
                # Object too large for current page margins - skip this object
                continue
            
            # Generate random position ensuring complete object fits within margins
            x = random.randint(PAGE_MARGIN, max_x)  # Left edge at least PAGE_MARGIN from left
            y = random.randint(PAGE_MARGIN, max_y)  # Top edge at least PAGE_MARGIN from top
            
            # Draw the object using the appropriate shape function
            draw_function(pdf, x, y, size)
        
        # Generate the complete file path
        file_path = get_pdf_filepath(filename)
        
        # Save the PDF to the file system
        pdf.output(file_path)
        
        # Return success
        return True
        
    except Exception as e:
        # Handle any errors during PDF creation
        print(f"   ❌ Error creating {filename}: {e}")
        return False


def create_combined_pdf(base_name, pdf_count, shape_name, object_count):
    """
    Creates a single PDF file with multiple pages, each containing different random distributions.
    
    Each page represents what would have been a separate PDF version,
    but all pages are combined into one convenient PDF file.
    
    Args:
        base_name (str): Base name for the PDF file
        pdf_count (int): Number of pages (versions) to create
        shape_name (str): Type of geometric shape to draw
        object_count (int): Number of objects per page
        
    Returns:
        bool: True if PDF was created successfully, False otherwise
    """
    try:
        # Create a single PDF document for all versions
        pdf = FPDF()
        
        # Configure PDF settings (same for all pages)
        pdf.set_auto_page_break(auto=False, margin=0)  # Disable automatic page breaks
        pdf.set_draw_color(0, 0, 0)      # Black outline (RGB: 0,0,0)
        pdf.set_fill_color(255, 255, 255) # White fill (RGB: 255,255,255)
        
        # Get the drawing function for the selected shape
        draw_function = SHAPE_DRAWING_FUNCTIONS[shape_name]
        
        # Create each page with unique random distribution
        for version_number in range(1, pdf_count + 1):
            # Add a new page for this version
            pdf.add_page()
            
            # Display progress for current page
            print(f"📄 Creating page {version_number}/{pdf_count}")
            
            # Generate and draw objects for this page
            for object_index in range(object_count):
                # Generate random size for this object first
                size = random.randint(MIN_OBJECT_SIZE, MAX_OBJECT_SIZE)
                
                # Calculate available positioning space with proper margin handling
                max_x = PAGE_WIDTH - size - PAGE_MARGIN   # Rightmost valid X position
                max_y = PAGE_HEIGHT - size - PAGE_MARGIN  # Bottommost valid Y position
                
                # Ensure we have valid positioning space
                if max_x < PAGE_MARGIN or max_y < PAGE_MARGIN:
                    # Object too large for current page margins - skip this object
                    continue
                
                # Generate random position ensuring complete object fits within margins
                x = random.randint(PAGE_MARGIN, max_x)
                y = random.randint(PAGE_MARGIN, max_y)
                
                # Draw the object using the appropriate shape function
                draw_function(pdf, x, y, size)
        
        # Generate filename for combined PDF
        filename = f"{base_name}_Combined.pdf"
        file_path = get_pdf_filepath(filename)
        
        # Save the multi-page PDF to the file system
        pdf.output(file_path)
        
        # Success feedback
        print(f"   ✅ {filename} created successfully with {pdf_count} pages!")
        
        # Return the filename for tracking
        return filename
        
    except Exception as e:
        # Handle any errors during PDF creation
        print(f"   ❌ Error creating combined PDF: {e}")
        return None


def create_multiple_pdfs(base_name, pdf_count, shape_name, object_count, pdf_format="separate"):
    """
    Creates multiple PDF versions with the same specifications but different random distributions.
    
    Can create either separate PDF files or one combined multi-page PDF file,
    depending on the pdf_format parameter.
    
    Args:
        base_name (str): Base name for all PDF files
        pdf_count (int): Number of PDF versions to create
        shape_name (str): Type of geometric shape to draw
        object_count (int): Number of objects per PDF
        pdf_format (str): "separate" for individual files, "combined" for single multi-page PDF
        
    Returns:
        list: List of successfully created PDF filenames
    """
    # List to track successfully created PDFs
    created_pdfs = []
    
    # Handle combined PDF format
    if pdf_format == "combined":
        # Display progress header for combined format
        print(f"\n🚀 Creating combined PDF with {pdf_count} pages, each with {object_count} {shape_name} objects...")
        print("=" * 70)
        
        # Create single multi-page PDF
        combined_filename = create_combined_pdf(base_name, pdf_count, shape_name, object_count)
        
        # Track success
        if combined_filename:
            created_pdfs.append(combined_filename)
        
        return created_pdfs
    
    # Handle separate PDF format (default)
    # Display progress header for separate format
    print(f"\n🚀 Creating {pdf_count} separate PDF version(s) with {object_count} {shape_name} objects each...")
    print("=" * 70)
    
    # Create each PDF version
    for version_number in range(1, pdf_count + 1):
        # Generate filename for this version
        filename = generate_pdf_filename(base_name, version_number, pdf_count)
        
        # Display progress for current version
        print(f"📄 Creating version {version_number}/{pdf_count}: {filename}")
        
        # Create the PDF file
        success = create_single_pdf(filename, shape_name, object_count)
        
        # Track successful creations
        if success:
            created_pdfs.append(filename)
            print(f"   ✅ {filename} created successfully!")
        # Error message already handled in create_single_pdf()
    
    # Return list of created files
    return created_pdfs


# ============================================================================
# USER INTERFACE FUNCTIONS
# ============================================================================

def display_welcome_message():
    """
    Displays the welcome message and program description.
    
    Provides clear information about what the program does and its capabilities.
    """
    print("=" * 70)
    print("📄 NeuroGames PDF Generator - CS50 Implementation")
    print("=" * 70)
    print("Creates multiple PDF versions with randomly distributed geometric shapes.")
    print("🎲 Each version has unique object positioning for variety and testing.")
    print("💎 Perfect for educational materials, presentations, or visual testing.")
    print()


def get_user_requirements():
    """
    Collects all user requirements through interactive prompts.
    
    Gathers:
    - Base name for PDF files
    - Number of PDF versions to create
    - Number of objects per PDF
    - Type of geometric shape to use
    - PDF output format (separate files or combined file)
    
    Returns:
        tuple: (base_name, pdf_count, object_count, shape_name, pdf_format)
    """
    print("📝 Please provide the following information:")
    print()
    
    # Get base name for PDF files
    base_name = get_user_input_string("Enter the base name for your PDF files (without .pdf): ")
    
    # Get number of PDF versions to create
    pdf_count = get_user_input_integer(
        f"How many PDF versions would you like to create? ({MIN_PDF_COUNT}-{MAX_PDF_COUNT}): ",
        MIN_PDF_COUNT,
        MAX_PDF_COUNT
    )
    
    # Get number of objects per PDF
    object_count = get_user_input_integer(
        f"How many objects per PDF? ({MIN_OBJECT_COUNT}-{MAX_OBJECT_COUNT}): ",
        MIN_OBJECT_COUNT,
        MAX_OBJECT_COUNT
    )
    
    # Get shape selection
    print()
    shape_name = get_shape_choice()
    
    # Get PDF format preference (only for multiple PDFs)
    pdf_format = get_pdf_format_choice(pdf_count)
    
    # Return all collected requirements
    return base_name, pdf_count, object_count, shape_name, pdf_format


def display_completion_summary(created_pdfs, total_requested, shape_name, object_count, pdf_format="separate"):
    """
    Displays a comprehensive summary of the PDF generation process.
    
    Shows:
    - Success/failure statistics
    - List of created files
    - Technical specifications
    - Location information
    
    Args:
        created_pdfs (list): List of successfully created PDF filenames
        total_requested (int): Total number of PDFs that were requested
        shape_name (str): Type of geometric shape used
        object_count (int): Number of objects per PDF
    """
    # Display completion header
    print("=" * 60)
    print("🎉 PDF GENERATION COMPLETED!")
    print("=" * 60)
    
    # Display success statistics based on PDF format
    success_count = len(created_pdfs)
    
    if pdf_format == "combined":
        # Combined format - one file with multiple pages
        if success_count > 0:
            print(f"📊 Successfully created: 1 combined PDF file with {total_requested} pages")
            print(f"📄 Each page contains: {object_count} {shape_name} objects")
            print(f"🎲 Each page has unique random object distribution")
        else:
            print(f"📊 Failed to create combined PDF file")
    else:
        # Separate format - multiple individual files
        print(f"📊 Successfully created: {success_count}/{total_requested} separate PDF files")
        print(f"📄 Each PDF contains: {object_count} {shape_name} objects")
        print(f"🎲 Each file has unique random object distribution")
    
    print(f"📁 All files saved in: {OUTPUT_DIR}/ directory")
    
    # Display list of created files
    if created_pdfs:
        print()
        print("📋 Created files:")
        for index, filename in enumerate(created_pdfs, 1):
            print(f"   {index}. {filename}")
    
    # Display warning if some PDFs failed (only for separate format)
    if pdf_format == "separate":
        failed_count = total_requested - success_count
        if failed_count > 0:
            print()
            print(f"⚠️  Warning: {failed_count} PDF file(s) could not be created.")
            print("   Check file permissions and available disk space.")
    elif pdf_format == "combined" and success_count == 0:
        print()
        print(f"⚠️  Warning: Combined PDF could not be created.")
        print("   Check file permissions and available disk space.")
    
    print()
    print("✨ Thank you for using NeuroGames PDF Generator!")


# ============================================================================
# MAIN PROGRAM EXECUTION
# ============================================================================

def main():
    """
    Main program execution function.
    
    Orchestrates the entire PDF generation process:
    1. Log the program execution
    2. Display welcome message
    3. Ensure output directory exists
    4. Collect user requirements
    5. Generate PDF files
    6. Display completion summary
    """
    # Log this program execution for tracking
    log_execution()
    
    # Display welcome message and program information
    display_welcome_message()
    
    # Ensure output directory exists for saving PDFs
    ensure_output_directory()
    
    try:
        # Collect user requirements interactively
        base_name, pdf_count, object_count, shape_name, pdf_format = get_user_requirements()
        
        # Generate the requested PDF files
        created_pdfs = create_multiple_pdfs(base_name, pdf_count, shape_name, object_count, pdf_format)
        
        # Display comprehensive completion summary
        display_completion_summary(created_pdfs, pdf_count, shape_name, object_count, pdf_format)
        
    except KeyboardInterrupt:
        # Handle user interruption gracefully
        print("\n\n❌ Program interrupted by user.")
        print("No PDF files were created.")
        
    except Exception as e:
        # Handle unexpected errors
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please check your input and try again.")


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Program entry point - executes when script is run directly.
    
    This condition ensures the main() function only runs when the script
    is executed directly, not when it's imported as a module.
    """
    main()