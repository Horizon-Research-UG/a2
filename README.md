# NeuroGames Project - CS50 Implementation

![CS50](https://img.shields.io/badge/CS50-Harvard-crimson)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![PDF](https://img.shields.io/badge/PDF-Generation-green)

## 📖 Overview

The **NeuroGames Project** is a professional-grade Python application suite designed for educational and testing purposes. This CS50-inspired implementation demonstrates best practices in software engineering, including modular design, comprehensive documentation, and robust error handling.

### Key Features

- **🎲 PDF Generation**: Create multiple PDF versions with randomly distributed geometric shapes
- **📊 Execution Logging**: Comprehensive tracking of all program executions
- **🔧 Modular Design**: Clean separation of concerns with dedicated modules
- **📚 CS50-Style Documentation**: Every line documented for educational value
- **🛡️ Robust Error Handling**: Graceful handling of edge cases and user errors

## 🏗️ Project Structure

```
NeuroGames/
├── src/                          # Source code modules
│   ├── logger.py                 # Execution logging system
│   └── pdf_generator.py          # PDF generation engine
├── output/                       # Generated PDF files
├── logs/                         # Execution log files
├── docs/                         # Documentation
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── main.py                       # Program entry point
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** installed on your system
- **pip** package manager

### Installation

1. **Clone or download** the project files
2. **Navigate** to the project directory
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Method 1: Run the main program
```bash
python main.py
```

#### Method 2: Run individual modules
```bash
# Generate PDFs directly
python src/pdf_generator.py

# View execution logs
python src/logger.py
```

## 📄 PDF Generator

### What it does
Creates multiple PDF files containing randomly distributed geometric shapes. Each PDF version has the same specifications but unique random positioning.

### Supported Shapes
- **Circles** - Perfect circular objects
- **Triangles** - Equilateral triangles
- **Rectangles** - Square objects
- **Pentagons** - Five-sided regular polygons
- **Hexagons** - Six-sided regular polygons

### Example Usage
```python
from src.pdf_generator import main
main()  # Interactive mode

# Or import specific functions
from src.pdf_generator import create_multiple_pdfs
pdfs = create_multiple_pdfs("test", 3, "Circle", 10)
```

### Sample Output
- `MyProject_Version_1.pdf` - 5 triangles, random distribution A
- `MyProject_Version_2.pdf` - 5 triangles, random distribution B  
- `MyProject_Version_3.pdf` - 5 triangles, random distribution C

## 📊 Logging System

### What it does
Tracks every program execution with detailed information for analysis and debugging.

### Logged Information
- **Sequential Call Number** - Auto-incrementing execution counter
- **Timestamp** - Date and time of execution
- **Program Name** - Which program was executed
- **Full Path** - Complete file system path

### Example Usage
```python
from src.logger import log_execution, read_log, get_log_stats

# Log current program execution
log_execution()

# View all execution history
read_log()

# Display usage statistics
get_log_stats()
```

### Sample Log Output
```
=== 📋 NEUROGAMES PROGRAM EXECUTION LOG ===
#    Date         Time       Program         
==================================================
5    2025-10-08   14:30:25   pdf_generator.py    
4    2025-10-08   14:28:15   main.py             
3    2025-10-08   14:25:10   pdf_generator.py    
2    2025-10-08   14:20:05   logger.py           
1    2025-10-08   14:15:00   main.py             

📊 Total executions: 5
```

## 🔧 Technical Implementation

### Code Style
- **CS50 Standards**: Every line documented with clear, educational comments
- **Modular Design**: Separated concerns with dedicated modules
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Input Validation**: Robust checking of all user inputs

### Best Practices Demonstrated
1. **Documentation**: Docstrings for every function
2. **Constants**: Configuration values clearly defined
3. **Type Safety**: Clear parameter and return types
4. **Resource Management**: Proper file handling with context managers
5. **User Experience**: Intuitive prompts and helpful error messages

### Performance Considerations
- **Memory Efficient**: Proper cleanup of resources
- **File System Safe**: Atomic operations where possible
- **Error Recovery**: Graceful degradation on failures

## 📚 Educational Value

This project demonstrates key CS50 concepts:

### Programming Fundamentals
- **Functions**: Modular code organization
- **Loops**: Iteration for multiple operations
- **Conditionals**: Decision-making logic
- **Data Structures**: Lists, dictionaries, tuples

### Advanced Concepts
- **File I/O**: Reading and writing files safely
- **Exception Handling**: Robust error management
- **Module System**: Code organization and reusability
- **Documentation**: Professional-grade code documentation

### Software Engineering
- **Project Structure**: Logical file organization
- **Separation of Concerns**: Each module has a clear purpose
- **User Interface Design**: Intuitive command-line interface
- **Testing Mindset**: Code designed for reliability

## 🐛 Troubleshooting

### Common Issues

**"Module not found" error**
```bash
# Solution: Run from project root directory
cd /path/to/NeuroGames
python src/pdf_generator.py
```

**"Permission denied" when creating files**
```bash
# Solution: Check directory permissions
chmod 755 output/
chmod 755 logs/
```

**PDF files not visible**
```bash
# Check the output directory
ls output/
```

### Error Messages
- **Input validation errors**: Follow the prompts for valid ranges
- **File system errors**: Check permissions and disk space
- **Import errors**: Ensure all dependencies are installed

## 🤝 Contributing

This educational project welcomes improvements:

1. **Code Quality**: Enhance documentation or add type hints
2. **Features**: Add new geometric shapes or export formats
3. **Testing**: Add unit tests for reliability
4. **Documentation**: Improve examples or explanations

## 📝 License

This project is created for educational purposes in the spirit of CS50. Feel free to use, modify, and learn from the code.

## 🎓 Acknowledgments

- **CS50 Harvard**: For inspiring educational programming practices
- **David J. Malan**: For demonstrating that code can be both functional and beautiful
- **Python Community**: For excellent libraries and documentation

---

*"The best way to learn programming is to write programs."* - CS50 Philosophy

## 📞 Support

For questions about the code or implementation:
1. **Read the comments**: Every line is documented
2. **Check the logs**: The logging system tracks all operations
3. **Review error messages**: They're designed to be helpful

---

**Happy Coding! 🚀**