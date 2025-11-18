# 📊 Split by Column - Desktop Application

A comprehensive Python desktop application built with Tkinter that splits datasets by column values and exports them as CSV or Excel files with automatic ZIP archiving.

---

## ✨ **Features**

### ✅ Core Functionality
- **📁 File Loading**: Import Excel (.xlsx, .xls) or CSV files
- **🔍 Auto-Detection**: Automatically detects all columns in the dataset
- **☑️ Flexible Selection**: 
  - Select one column
  - Select multiple columns
  - Select all columns
- **📊 Smart Splitting**:
  - Single column → Split by unique values
  - Multiple columns → Split by unique combinations
  - All columns → Each unique row combination as separate file
- **💾 Export Options**:
  - CSV format
  - Excel (XLSX) format
- **📦 Auto Packaging**: Creates ZIP archive with all output files
- **📈 Progress Tracking**: Visual progress bar with real-time status
- **📝 Comprehensive Logging**: Detailed activity log in GUI + console output
- **🛡️ Robust Error Handling**: Graceful error management with user-friendly messages

### 🎨 User Interface
- Clean, intuitive Tkinter GUI
- Step-by-step workflow layout
- Color-coded logging (INFO, WARNING, ERROR, SUCCESS)
- Responsive design with proper validation
- Disabled START button until ready
- Real-time progress updates

### 🔐 Error Handling
- Missing or invalid files
- Invalid file extensions
- Duplicate column names
- Empty datasets
- Permission errors
- Non-ASCII characters in filenames
- pandas read/write errors
- User cancellations

---

## 🚀 **Installation**

### Step 1: Install Python
Ensure you have **Python 3.8 or higher** installed.
- Download from: https://www.python.org/downloads/
- During installation, check **"Add Python to PATH"**

### Step 2: Install Dependencies

Open Command Prompt or PowerShell and navigate to the application directory:

```powershell
cd "C:\Users\Abdussamad Ahmad\Desktop\seperatebycolumn"
```

Install required packages:

```powershell
pip install -r requirements.txt
```

**Required packages:**
- `pandas` - Data manipulation and analysis
- `openpyxl` - Excel file handling

**Built-in packages (already included in Python):**
- `tkinter` - GUI framework
- `zipfile` - ZIP archive creation
- `threading` - Concurrent operations
- `os`, `datetime`, `pathlib`, `traceback` - Standard utilities

---

## 🎯 **How to Run**

### Option 1: Using Command Prompt/PowerShell
```powershell
cd "C:\Users\Abdussamad Ahmad\Desktop\seperatebycolumn"
python split_by_column.py
```

### Option 2: Double-Click (Create a Shortcut)
1. Right-click on `split_by_column.py`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Right-click shortcut → Properties
5. In Target field, add `python` before the path if needed

### Option 3: Using Python IDLE
1. Open Python IDLE
2. File → Open → Select `split_by_column.py`
3. Run → Run Module (F5)

---

## 📖 **Usage Guide**

### Step-by-Step Workflow

#### **1. Load File**
- Click **"📁 Load Excel/CSV File"** button
- Select your data file (.xlsx, .xls, or .csv)
- The application auto-detects all columns
- You'll see "✓ filename" when loaded
- Log will show detected columns and row count

#### **2. Choose Output Folder**
- Click **"📂 Choose Output Folder"** button
- Select where to save split files
- You'll see "✓ folder_name" when selected
- All output files will be saved here

#### **3. Select Columns**
- You have three options:

  **Option A: Single Column**
  - Check ONE column checkbox
  - Result: One file per unique value in that column
  - Example: Selecting "Department" might create:
    - `Department_IT.csv`
    - `Department_HR.csv`
    - `Department_Sales.csv`

  **Option B: Multiple Columns**
  - Check 2-5 column checkboxes
  - Result: One file per unique combination
  - Example: Selecting "Department" and "Country":
    - `Department_IT__Country_Nigeria.csv`
    - `Department_HR__Country_USA.csv`

  **Option C: All Columns**
  - Click **"✓ Select All Columns"** checkbox
  - Result: Each unique row combination gets its own file

#### **4. Choose Export Format**
- Select **"CSV Format"** (default) or **"Excel Format (XLSX)"**
- Both support all splitting modes

#### **5. Monitor Progress**
- Watch the **Progress Bar** fill during processing
- Real-time status messages appear
- Progress bar shows:
  - 0-10%: Computing combinations
  - 10-80%: Exporting files
  - 80-90%: Creating ZIP archive
  - 90-100%: Completing operation

#### **6. Click START**
- **START button is only enabled when:**
  - ✓ A file is loaded
  - ✓ An output folder is selected
  - ✓ At least one column is selected
- Click **"▶ START SPLIT"** to begin
- The button becomes disabled during processing

#### **7. Review Results**
- Check the Activity Log for detailed information
- A success popup shows:
  - Total files created
  - Output folder location
  - ZIP filename
- All split files are in `split_YYYYMMDD_HHMMSS` folder
- ZIP archive: `output_split_YYYYMMDD_HHMMSS.zip`

#### **8. Optional: Reset**
- Click **"🔄 Reset"** to start over
- This clears all selections and resets the interface

---

## 📋 **Activity Log Explained**

### Log Levels:

| Level | Color | Meaning |
|-------|-------|---------|
| INFO | White | General information and progress |
| WARNING | Yellow | Non-critical issues or warnings |
| ERROR | Red | Errors that prevent operation |
| SUCCESS | Green | Operation completed successfully |

### Example Log Output:

```
[2025-01-15 14:32:10] [INFO] Application started successfully.
[2025-01-15 14:32:15] [INFO] User selected file: C:\Data\sales.csv
[2025-01-15 14:32:16] [INFO] File loaded as CSV format
[2025-01-15 14:32:16] [INFO] Columns detected: Department, Country, Region, Sales
[2025-01-15 14:32:16] [INFO] Total rows: 1500
[2025-01-15 14:32:18] [INFO] Output folder selected: C:\Output
[2025-01-15 14:32:25] [INFO] Split operation starting...
[2025-01-15 14:32:25] [INFO] Selected columns: Department, Country
[2025-01-15 14:32:25] [INFO] Output format: csv
[2025-01-15 14:32:26] [INFO] Multi-column split: 24 unique combinations found
[2025-01-15 14:32:30] [INFO] Exported: Department_IT__Country_Nigeria.csv (125 rows)
[2025-01-15 14:32:35] [SUCCESS] ZIP archive created: output_split_20250115_143235.zip
[2025-01-15 14:32:35] [SUCCESS] Split operation completed successfully!
```

---

## 💡 **Examples**

### Example 1: Split Sales Data by Region

**Input:** `sales.csv` with columns: Region, Product, Sales, Date

**Actions:**
1. Load `sales.csv`
2. Choose output folder
3. Select only "Region" column
4. Choose CSV format
5. Click START

**Output:**
```
split_20250115_143235/
├── Region_North.csv
├── Region_South.csv
├── Region_East.csv
└── Region_West.csv
output_split_20250115_143235.zip
```

### Example 2: Split Employee Data by Department & Location

**Input:** `employees.xlsx` with columns: Department, Location, Name, Salary, Hire_Date

**Actions:**
1. Load `employees.xlsx`
2. Choose output folder
3. Select "Department" and "Location" checkboxes
4. Choose Excel format
5. Click START

**Output:**
```
split_20250115_143235/
├── Department_IT__Location_NYC.xlsx
├── Department_IT__Location_LA.xlsx
├── Department_HR__Location_NYC.xlsx
├── Department_HR__Location_LA.xlsx
├── Department_Sales__Location_NYC.xlsx
└── Department_Sales__Location_LA.xlsx
output_split_20250115_143235.zip
```

### Example 3: Split All Unique Rows

**Input:** `transactions.csv` with columns: Date, Amount, Category, Status

**Actions:**
1. Load `transactions.csv`
2. Choose output folder
3. Click "✓ Select All Columns"
4. Choose CSV format
5. Click START

**Output:**
```
split_20250115_143235/
├── Date_2025-01-15__Amount_100.50__Category_Food__Status_Completed.csv
├── Date_2025-01-16__Amount_50.25__Category_Transport__Status_Completed.csv
├── Date_2025-01-15__Amount_200.00__Category_Electronics__Status_Pending.csv
└── ... (one file per unique row)
output_split_20250115_143235.zip
```

---

## 🛠️ **Troubleshooting**

### "ModuleNotFoundError: No module named 'pandas'"
- **Solution**: Run `pip install -r requirements.txt` again
- Ensure you're in the correct directory

### "File not found" error
- **Solution**: Verify the file exists and the path is correct
- Check file permissions
- Use absolute paths

### "Permission denied" when saving
- **Solution**: Choose a different output folder with write permissions
- Check if files are already open elsewhere
- Close any antivirus real-time scanning of that folder temporarily

### GUI appears frozen
- **Solution**: The app is still processing (check progress bar)
- Do not close the window during processing
- Wait for completion or click Reset after completion

### ZIP file not created
- **Solution**: Check available disk space
- Verify output folder has write permissions
- Review error log for details

### Non-ASCII characters in filename showing incorrectly
- **Solution**: The app automatically sanitizes filenames
- Characters are converted to underscores
- Check the Activity Log for the actual filename used

---

## 📊 **Supported File Formats**

### Input Files
- ✅ `.xlsx` - Excel 2007+ (recommended)
- ✅ `.xls` - Excel 97-2003
- ✅ `.csv` - Comma-separated values

### Output Files
- ✅ `.csv` - Comma-separated values (smaller files)
- ✅ `.xlsx` - Excel format (with formatting support)

### Archive
- ✅ `.zip` - ZIP compression (automatic)

---

## ⚙️ **Advanced Features**

### Threading
- The application uses threading to prevent UI freezing
- Long operations run in background threads
- Progress bar updates in real-time

### Memory Management
- Efficient pandas groupby operations
- Streaming writes to prevent memory overflow
- Automatic cleanup after operations

### Filename Sanitization
- Removes invalid filename characters
- Handles non-ASCII characters
- Prevents filename length issues
- Maintains readability

### Logging
- Color-coded severity levels
- Timestamped entries
- Available in both GUI and console
- Helps with debugging and auditing

---

## 📝 **Notes**

- **Large Files**: The app works efficiently with files up to millions of rows
- **Column Names**: Column names should not contain special characters (the app handles this)
- **Memory Usage**: Depends on file size; typically uses 2-3x the file size in RAM
- **ZIP Performance**: Compression depends on data redundancy; typically 20-80% reduction

---

## 🐛 **Known Limitations**

- Column names with special characters are sanitized for filenames
- Very large datasets (>1GB) may require 8GB+ RAM
- File paths longer than 260 characters may cause issues on some systems
- Application requires tkinter (included with Python)

---

## 📞 **Support**

If you encounter issues:

1. **Check the Activity Log** for error messages
2. **Review Troubleshooting section** above
3. **Verify file format** is supported
4. **Test with sample data** to isolate issues
5. **Check Python version**: `python --version` (should be 3.8+)
6. **Verify dependencies**: `pip list` (should show pandas, openpyxl)

---

## 📄 **File Structure**

```
seperatebycolumn/
├── split_by_column.py          # Main application (single file)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## ✅ **Checklist Before Running**

- ✅ Python 3.8+ installed
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Input CSV/Excel file ready
- ✅ Output folder exists and is writable
- ✅ Sufficient disk space for output files
- ✅ No antivirus blocking file operations

---

## 🎉 **You're Ready!**

Run the application:
```powershell
python split_by_column.py
```

Enjoy splitting your datasets! 🚀

---

**Version:** 1.0.0  
**Last Updated:** January 2025  
**License:** Free to use and modify  
