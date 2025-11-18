# 📊 Split by Column - Desktop Application (Enhanced v2.0)

A comprehensive Python desktop application built with Tkinter that splits datasets by column values with **real-time preview**, **multi-select column selection**, and intelligent file naming.

---

## ✨ **Key Features (v2.0 Enhanced)**

### 🆕 **New in v2.0:**
- **Multi-Select Listbox** for column selection (instead of checkboxes)
- **"Select All" option inside the list** for quick bulk selection
- **Live Preview Section** (always visible, auto-updating):
  - Sample of first 30 rows with selected columns
  - Shows unique groups count
  - Displays planned output filenames **before** execution
- **Intelligent File Naming**:
  - Single column: `<value>.csv`
  - Multiple columns: `ColumnA_ValueA__ColumnB_ValueB.csv`
  - All columns: `Group_001.csv`, `Group_002.csv` (safe naming)
- **File Logging** - All operations logged to `app.log`
- **Responsive Threading** - UI never freezes during operations

### ✅ **Core Features**
- **📁 File Loading**: Import Excel (.xlsx, .xls) or CSV files
- **🔍 Auto-Detection**: Automatically detects all columns in dataset
- **☑️ Smart Column Selection**: 
  - Select one column
  - Select multiple columns
  - Select all columns
  - Built-in "Select All" option in the list
- **📊 Dataset Splitting**:
  - Single column → Split by unique values
  - Multiple columns → Split by unique combinations
  - All columns → Each unique row gets its own file
- **💾 Export Options**:
  - CSV format (lightweight)
  - Excel (XLSX) format (with formatting)
- **📦 Auto Packaging**: Creates ZIP archive with timestamp
- **📈 Progress Tracking**: Visual progress bar with real-time status
- **📝 Comprehensive Logging**: 
  - GUI activity log (color-coded)
  - Console output
  - Persistent `.log` file
- **🛡️ Robust Error Handling**: Graceful error management with helpful messages

### 🎨 **Enhanced UI Design**
- **Two-column layout**: Controls on left, Preview + Progress on right
- **Color-coded logging**: INFO (white), WARNING (yellow), ERROR (red), SUCCESS (green)
- **Real-time preview updates**: See results instantly as you select columns
- **Sample filenames**: Know exactly what files will be created
- **Responsive design**: Works efficiently on different screen sizes

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

**Built-in packages (no installation needed):**
- `tkinter` - GUI framework
- `zipfile` - ZIP archive creation
- `threading` - Concurrent operations
- `logging` - File logging
- `os`, `datetime`, `pathlib`, `traceback` - Standard utilities

---

## 🎯 **How to Run**

### Option 1: Command Prompt/PowerShell
```powershell
cd "C:\Users\Abdussamad Ahmad\Desktop\seperatebycolumn"
python split_by_column.py
```

### Option 2: Double-Click (Windows)
1. Right-click on `split_by_column.py`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Double-click shortcut to run

### Option 3: Python IDLE
1. Open Python IDLE
2. File → Open → Select `split_by_column.py`
3. Run → Run Module (F5)

---

## 📖 **Step-by-Step Usage Guide**

### **Step 1: Load Your File**
- Click **"📁 Load Excel/CSV"** button
- Select your data file (.xlsx, .xls, or .csv)
- The app will:
  - Auto-detect all columns
  - Display column count and total rows
  - Populate the column selection list

### **Step 2: Select Columns to Split By**

You have three options in the **multi-select listbox**:

#### **Option A: Select ONE Column**
1. Click on a single column name
2. Result: One file per unique value in that column

**Example:**
- Selected: `Department`
- Output: `IT.csv`, `HR.csv`, `Sales.csv`

#### **Option B: Select MULTIPLE Columns**
1. Hold **Ctrl** and click multiple columns
2. Or hold **Shift** and click to select a range
3. Result: One file per unique combination

**Example:**
- Selected: `Department` and `Country`
- Output: 
  - `Department_IT__Country_Nigeria.csv`
  - `Department_HR__Country_USA.csv`
  - `Department_Sales__Country_Germany.csv`

#### **Option C: Select ALL Columns**
1. Click the **">>> SELECT ALL COLUMNS <<<"** option at the top of the list
2. Or Ctrl+A to select all
3. Result: One file per unique row combination using safe naming

**Example:**
- All columns selected
- Output: `Group_001.csv`, `Group_002.csv`, ..., `Group_NNN.csv`

### **Step 3: Review the Live Preview**
- The **Preview Section** on the right updates **automatically** as you select columns
- You'll see:
  - ✅ Sample data (first 30 rows) with only selected columns
  - ✅ Total number of unique groups/files that will be created
  - ✅ **Sample output filenames** (first 10 examples)

**Preview shows:**
```
📊 Selected Columns: Department, Country
📈 Total Rows: 1500
📁 Unique Groups: 24 (one per unique combination)

Sample Output Filenames (first 10):
 1. Department_IT__Country_Nigeria.csv
 2. Department_IT__Country_USA.csv
 3. Department_IT__Country_Germany.csv
 4. Department_HR__Country_Nigeria.csv
 5. Department_HR__Country_USA.csv
... and 19 more files
```

### **Step 4: Choose Output Format**
- **📄 CSV Format** (default): Faster, smaller files, universal compatibility
- **📊 Excel Format (XLSX)**: Formatted, sortable, wider software support

### **Step 5: Choose Output Folder**
- Click **"📂 Choose Folder"** button
- Select where to save all split files and ZIP archive
- A subfolder named `split_YYYYMMDD_HHMMSS` will be created inside

### **Step 6: Start the Split**
- The **START** button is only enabled when:
  - ✅ File is loaded
  - ✅ At least one column is selected
  - ✅ Output folder is chosen

- Click **"▶ START SPLIT"** to begin
- Watch the **progress bar** fill (0% → 100%)
- The log updates in real-time with each file processed

### **Step 7: Monitor Progress**
The progress bar shows different stages:
```
5%   - Preparing split operation
10%  - Computing unique groups
15%  - Starting file export
80%  - Completed all exports
82%  - Creating ZIP archive
100% - Operation complete!
```

### **Step 8: Retrieve Your Output**
When complete, you'll see a success message showing:
- Total files created
- Output folder path
- ZIP filename and size

**Files are saved in:**
```
output_folder/
├── split_YYYYMMDD_HHMMSS/
│   ├── Group_001.csv
│   ├── Group_002.csv
│   └── ... (all split files)
└── output_split_YYYYMMDD_HHMMSS.zip  ← All files compressed
```

### **Optional: Reset**
- Click **"🔄 Reset"** to start over
- Clears all selections and resets UI to initial state

---

## 📋 **File Naming Examples**

### **Example 1: Single Column Selection**
```
Input: sales_data.csv with columns [Region, Product, Sales]
Selected: Region

Output files:
- North.csv       (all rows where Region = "North")
- South.csv       (all rows where Region = "South")
- East.csv        (all rows where Region = "East")
- West.csv        (all rows where Region = "West")
```

### **Example 2: Multiple Column Selection**
```
Input: employees.xlsx with columns [Dept, Location, Name, Salary]
Selected: Dept, Location

Output files:
- Dept_IT__Location_NYC.xlsx
- Dept_IT__Location_LA.xlsx
- Dept_HR__Location_NYC.xlsx
- Dept_HR__Location_LA.xlsx
- Dept_Sales__Location_NYC.xlsx
- Dept_Sales__Location_LA.xlsx
```

### **Example 3: All Columns Selection**
```
Input: transactions.csv with columns [Date, Amount, Category, Status]
Selected: ALL

Output files:
- Group_001.csv  (unique row #1)
- Group_002.csv  (unique row #2)
- Group_003.csv  (unique row #3)
- ... etc (one file per unique row combination)
```

---

## 📝 **Activity Log Explained**

### **Log Levels:**

| Level | Color | Meaning |
|-------|-------|---------|
| INFO | White | General information and progress |
| WARNING | Yellow | Non-critical issues or warnings |
| ERROR | Red | Errors that prevent operation |
| SUCCESS | Green | Operation completed successfully |

### **Example Log Output:**

```
[2025-01-15 14:32:10] [INFO] Application started successfully.
[2025-01-15 14:32:15] [INFO] User selected file: C:\Data\sales.csv
[2025-01-15 14:32:16] [INFO] File loaded as CSV format
[2025-01-15 14:32:16] [INFO] Columns detected: Department, Country, Region, Sales
[2025-01-15 14:32:16] [INFO] Total rows: 1500
[2025-01-15 14:32:18] [INFO] Output folder selected: C:\Output
[2025-01-15 14:32:25] [INFO] Starting split with columns: Department, Country
[2025-01-15 14:32:26] [INFO] Multi-column split: 24 unique combinations found
[2025-01-15 14:32:28] [INFO] ✓ Exported: Department_IT__Country_Nigeria.csv (125 rows)
[2025-01-15 14:32:30] [INFO] ✓ Exported: Department_IT__Country_USA.csv (189 rows)
[2025-01-15 14:32:50] [SUCCESS] ✓ ZIP archive created: output_split_20250115_143250.zip (2.45 MB)
[2025-01-15 14:32:50] [SUCCESS] ✓ Total files exported: 24
[2025-01-15 14:32:50] [SUCCESS] ================================================================================
[2025-01-15 14:32:50] [SUCCESS] SPLIT OPERATION COMPLETED SUCCESSFULLY!
[2025-01-15 14:32:50] [SUCCESS] ================================================================================
```

### **Log File Location:**
```
C:\Users\[YourUsername]\Desktop\seperatebycolumn\app.log
```

The log file persists and appends to, so you have a complete history of all operations.

---

## 🛠️ **Troubleshooting**

### **"ModuleNotFoundError: No module named 'pandas'"**
- **Solution**: Run `pip install -r requirements.txt` again
- Make sure you're in the correct directory
- Try: `pip install --upgrade pandas openpyxl`

### **"File not found" error**
- **Solution**: Verify the file exists and is not corrupted
- Check file permissions
- Try moving file to a different location
- Ensure filename doesn't contain special characters

### **"Permission denied" when saving**
- **Solution**: 
  - Choose a different output folder with write permissions
  - Close any files currently open in that folder
  - Disable antivirus real-time scanning temporarily
  - Run the app as Administrator

### **GUI appears frozen**
- **Solution**: 
  - The app is likely still processing (check progress bar)
  - Don't close the window during processing
  - Wait for completion

### **Preview not updating**
- **Solution**:
  - Make sure columns are selected (click on them)
  - Try clicking a different column first, then your desired column
  - Reset the app and try again

### **Filenames with non-ASCII characters**
- **Solution**: The app automatically sanitizes them
- Special characters are converted to underscores
- Check the activity log for actual filename used

### **ZIP file not created**
- **Solution**:
  - Check available disk space
  - Verify output folder has write permissions
  - Check Activity Log for error details
  - Try saving to a different location

---

## 📊 **Supported Formats**

### **Input Files:**
- ✅ `.xlsx` - Excel 2007+ (recommended)
- ✅ `.xls` - Excel 97-2003
- ✅ `.csv` - Comma-separated values

### **Output Files:**
- ✅ `.csv` - Comma-separated values
- ✅ `.xlsx` - Excel format

### **Archive:**
- ✅ `.zip` - Compressed archive (automatic)

---

## ⚙️ **Technical Features**

### **Threading & Responsiveness**
- Background thread for split operations
- UI updates in real-time with `.after()`
- No UI freezing during processing

### **Memory Optimization**
- Efficient pandas `groupby` operations
- Streaming file writes
- Automatic cleanup after operations

### **Smart Filename Handling**
- Automatic sanitization of invalid characters
- Handles non-ASCII characters gracefully
- Prevents filename length issues
- Safe for all operating systems

### **Robust Error Handling**
- Graceful error messages
- Detailed logging of all errors
- Application continues running even on errors
- User-friendly popup messages

### **File Logging**
- Timestamp on every log entry
- Organized by severity level
- Persists across sessions
- Easy to debug issues

---

## 📋 **Checklist Before Running**

- ✅ Python 3.8+ installed
- ✅ Dependencies installed: `pip install -r requirements.txt`
- ✅ Input CSV/Excel file ready
- ✅ Output folder accessible
- ✅ Sufficient disk space for output files
- ✅ Read/write permissions on output folder

---

## 🎉 **Quick Start Summary**

```powershell
# 1. Navigate to folder
cd "C:\Users\Abdussamad Ahmad\Desktop\seperatebycolumn"

# 2. Install dependencies (one-time)
pip install -r requirements.txt

# 3. Run the application
python split_by_column.py

# 4. Follow the 8-step guide above
```

---

## 📈 **Performance**

- **Small files** (<10MB): < 5 seconds
- **Medium files** (10-100MB): 5-30 seconds
- **Large files** (>100MB): 30-120 seconds
- ZIP compression typically achieves 40-80% size reduction

---

## 🔧 **Advanced Usage**

### **Keyboard Shortcuts in Column List:**
- **Ctrl + A**: Select all items
- **Shift + Click**: Select range
- **Ctrl + Click**: Toggle individual items
- **Arrow Keys**: Navigate list

### **Filename Collision Prevention:**
- If a filename already exists, app appends `_1`, `_2`, etc.
- Example: `Department_IT_1.csv` if `Department_IT.csv` exists

### **Large Column Names:**
- Long column names are truncated in filenames (max 100 chars)
- Full names shown in preview section

---

## 📄 **File Structure**

```
seperatebycolumn/
├── split_by_column.py    # Main application (complete, single file)
├── requirements.txt       # Python dependencies
├── README.md             # Original README
├── README_v2.md          # This file (enhanced documentation)
└── app.log              # Created on first run, logs all operations
```

---

## ✅ **Known Limitations**

- Very large datasets (>1GB) may require 8GB+ RAM
- File paths longer than 260 characters may have issues on older Windows
- Tkinter (included with Python) required for GUI
- Column names with many special chars are heavily sanitized

---

## 🌟 **Version History**

### **v2.0.0 (Current) - Enhanced Edition**
- ✨ Multi-select listbox instead of checkboxes
- ✨ "Select All" option inside the list
- ✨ Live preview section (always visible, auto-updating)
- ✨ Smart file naming rules (single/multiple/all columns)
- ✨ Sample output filenames in preview
- ✨ File logging to `app.log`
- ✨ Improved UI layout (2-column design)
- ✨ Better progress tracking

### **v1.0.0 - Initial Release**
- Basic file loading and splitting
- Simple checkbox column selection
- CSV/Excel export
- Progress bar and logging

---

## 📞 **Support & Debugging**

### **How to Debug Issues:**

1. **Check the Activity Log** for error messages
2. **Review `app.log`** file for complete operation history
3. **Verify your data** using Excel/CSV viewer first
4. **Test with sample data** to isolate issues
5. **Check Python version**: `python --version` (should be 3.8+)
6. **Verify packages**: `pip list` (check pandas, openpyxl)

### **Common Issue Checklist:**
- [ ] File exists and is readable
- [ ] Output folder exists and is writable
- [ ] At least one column is selected
- [ ] Sufficient disk space available
- [ ] Python 3.8+ is installed
- [ ] pandas and openpyxl are installed

---

## 🎯 **You're Ready!**

Run the application and enjoy splitting your datasets:

```powershell
python split_by_column.py
```

**Happy splitting!** 🚀

---

**Version:** 2.0.0 (Enhanced)  
**Last Updated:** January 2025  
**License:** Free to use and modify  
**Author:** Senior Python Developer  
