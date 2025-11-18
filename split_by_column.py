"""
Split by Column - Desktop Application (Enhanced Edition)
A comprehensive Tkinter-based GUI application for splitting datasets by column values.

Features:
- Load Excel/CSV files
- Auto-detect columns
- Multi-select column list with "Select All" option
- Dynamic preview section (always visible, auto-updating)
- Smart file naming based on row values
- Single, multiple, or all column selection
- Split by unique values or combinations
- Export as CSV or Excel
- Automatic ZIP archive creation
- Progress tracking with visual progress bar
- Comprehensive logging system with .log file
- Robust error handling

Author: Senior Python Developer
Version: 2.0.0 - Enhanced with Preview & Multi-Select Listbox
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import os
from datetime import datetime
import zipfile
import threading
import traceback
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
import logging
import urllib.request
import shutil
import subprocess
import sys


class DataSplitterApp:
    """Main application class for the Split by Column desktop tool (Enhanced)."""

    def __init__(self, root: tk.Tk):
        """Initialize the application with main window and UI components."""
        self.root = root
        self.root.title("Split by Column - Data Splitter")
        self.root.geometry("1200x950")
        self.root.resizable(True, True)

        # Setup logging to file
        self.log_file_path = os.path.join(
            os.path.expanduser("~"), "Desktop", "seperatebycolumn", "app.log"
        )
        self._setup_file_logging()

        # Define default fonts via a runtime helper that attempts to ensure
        # the 'Outfit' family is available across platforms. If Outfit
        # cannot be installed/registered, the helper returns a sensible
        # fallback family name.
        preferred = self._ensure_outfit_font()

        self.default_font = (preferred, 10)
        self.small_font = (preferred, 8)
        self.button_font = (preferred, 9)
        self.title_font = (preferred, 11, "bold")

        # Monospace font for preview/logs; prefer Courier New, then Consolas, else fallback to preferred
        try:
            import tkinter.font as tkfont
            families = set(tkfont.families())
            mono_family = "Courier New" if "Courier New" in families else ("Consolas" if "Consolas" in families else preferred)
        except Exception:
            mono_family = "Courier New"

        self.mono_font = (mono_family, 9)
        # Slightly larger listbox font to increase perceived line height
        self.listbox_font = (preferred, 9)

        # Application state
        self.input_file_path: Optional[str] = None
        self.output_folder_path: Optional[str] = None
        self.dataframe: Optional[pd.DataFrame] = None
        self.all_columns: List[str] = []
        self.selected_columns: List[str] = []
        self.is_processing = False
        self.split_groups_info: Dict = {}  # Store group info for preview

        # UI components storage
        self.column_listbox: Optional[tk.Listbox] = None
        self.output_format_var = tk.StringVar(value="csv")
        self.progress_var = tk.DoubleVar(value=0)
        self.log_text: Optional[scrolledtext.ScrolledText] = None
        self.start_button: Optional[tk.Button] = None
        self.preview_text: Optional[scrolledtext.ScrolledText] = None

        # Setup UI
        self._setup_ui()

        self.log("Application started successfully.")

    def _setup_ui(self) -> None:
        """Setup all UI components with enhanced layout."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Configure style for LabelFrame with Outfit font
        style = ttk.Style()
        style.configure('TLabelframe.Label', font=self.title_font)
        style.configure('TButton', font=self.button_font)
        style.configure('TRadiobutton', font=self.default_font)
        style.configure('TCheckbutton', font=self.default_font)
        style.configure('TLabel', font=self.default_font)

        # ===== LEFT COLUMN: CONTROLS =====
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(3, weight=1)

        # File Selection
        file_frame = ttk.LabelFrame(left_frame, text="1. Load File", padding="10")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)

        self.input_file_label = tk.Label(
            file_frame, text="No file selected", fg="gray", wraplength=250, justify=tk.LEFT,
            font=self.default_font
        )
        self.input_file_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        ttk.Button(
            file_frame, text="📁 Load Excel/CSV", command=self._load_file, width=25
        ).grid(row=1, column=0, sticky=tk.W)

        # Output Folder Selection
        output_frame = ttk.LabelFrame(left_frame, text="2. Output Folder", padding="10")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)

        self.output_folder_label = tk.Label(
            output_frame, text="No folder selected", fg="gray", wraplength=250, justify=tk.LEFT,
            font=self.default_font
        )
        self.output_folder_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        ttk.Button(
            output_frame, text="📂 Choose Folder", command=self._choose_output_folder, width=25
        ).grid(row=1, column=0, sticky=tk.W)

        # Column Selection with Listbox
        column_frame = ttk.LabelFrame(left_frame, text="3. Select Columns", padding="10")
        column_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        column_frame.columnconfigure(0, weight=1)
        column_frame.rowconfigure(1, weight=1)

        info_label = tk.Label(
            column_frame, 
            text="Hold Ctrl+Click to select multiple\nOr use Shift+Click for ranges",
            fg="blue", font=self.small_font
        )
        info_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5), padx=(10, 0))

        # Scrollable listbox
        scrollbar = ttk.Scrollbar(column_frame)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), padx=(0, 10))

        self.column_listbox = tk.Listbox(
            column_frame,
            selectmode=tk.EXTENDED,
            yscrollcommand=scrollbar.set,
            height=12,
            width=30,
            font=self.listbox_font
        )
        self.column_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        self.column_listbox.bind("<<ListboxSelect>>", self._on_columns_selected)
        scrollbar.config(command=self.column_listbox.yview)

        # Format Selection
        format_frame = ttk.LabelFrame(left_frame, text="4. Export Format", padding="10")
        format_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Radiobutton(
            format_frame,
            text="📄 CSV Format",
            variable=self.output_format_var,
            value="csv",
        ).pack(anchor=tk.W)

        ttk.Radiobutton(
            format_frame,
            text="📊 Excel Format (XLSX)",
            variable=self.output_format_var,
            value="excel",
        ).pack(anchor=tk.W)

        # ===== RIGHT COLUMN: PREVIEW & PROGRESS =====
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(3, weight=1)

        # Preview Section
        preview_frame = ttk.LabelFrame(right_frame, text="📋 Live Preview", padding="10")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        # Preview info labels
        self.preview_info_label = tk.Label(
            preview_frame, text="No file loaded", fg="gray", wraplength=400, justify=tk.LEFT,
            font=self.default_font
        )
        self.preview_info_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5), padx=(10, 0))

        # (font status label was removed per user request)

        # Preview data display
        preview_scroll = ttk.Scrollbar(preview_frame)
        # preview_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S), padx=(0, 10))

        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            height=15,
            width=55,
            wrap=tk.WORD,
            bg="white",
            fg="black",
            font=self.mono_font,
            yscrollcommand=preview_scroll.set
        )
        self.preview_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

        # Configure line spacing tag for better line height (spacing1 = above, spacing3 = below)
        # spacing values are pixels; tweak as needed. Also configure header/info/error tags for spacing.
        try:
            # More airy spacing for preview lines and headers
            self.preview_text.tag_configure("line_spacing", spacing1=8, spacing3=8)
            self.preview_text.tag_configure("header", spacing1=10, spacing3=10)
            self.preview_text.tag_configure("info", spacing1=6, spacing3=6, foreground="gray")
            self.preview_text.tag_configure("error", spacing1=6, spacing3=6, foreground="red")
        except Exception:
            # Some tkinter versions/platforms may not support spacing; ignore if not available
            pass

        self.preview_text.config(state=tk.DISABLED)
        preview_scroll.config(command=self.preview_text.yview)

        # Progress Section
        progress_frame = ttk.LabelFrame(right_frame, text="⏳ Progress", padding="10")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 10))
        progress_frame.columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        self.progress_label = tk.Label(progress_frame, text="Ready", fg="blue", font=self.default_font)
        self.progress_label.grid(row=1, column=0, sticky=tk.W)

        # Action Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        button_frame.columnconfigure(0, weight=1)

        buttons_subframe = ttk.Frame(button_frame)
        buttons_subframe.pack()

        self.start_button = ttk.Button(
            buttons_subframe, text="▶ START SPLIT", command=self._start_split, width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        self.start_button.config(state=tk.DISABLED)

        ttk.Button(buttons_subframe, text="🔄 Reset", command=self._reset_app, width=15).pack(
            side=tk.LEFT, padx=(0, 5)
        )

        ttk.Button(buttons_subframe, text="❌ Exit", command=self.root.quit, width=15).pack(
            side=tk.LEFT
        )

        # ===== BOTTOM: LOGGING =====
        log_frame = ttk.LabelFrame(main_frame, text="📝 Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=8, width=150, wrap=tk.WORD, bg="black", fg="white", font=("Courier New", 8)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure line spacing for log display as well
        try:
            self.log_text.tag_configure("line_spacing", spacing1=3, spacing3=3)
            # Default tag for unstyled log lines
            self.log_text.tag_configure("default", foreground="white")
            self.log_text.tag_configure("error", foreground="red")
            self.log_text.tag_configure("warning", foreground="yellow")
            self.log_text.tag_configure("success", foreground="lightgreen")
        except Exception:
            pass

        self.log_text.config(state=tk.DISABLED)

        # Configure grid weights
        main_frame.rowconfigure(4, weight=0)

    def _setup_file_logging(self) -> None:
        """Setup logging to file."""
        try:
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            logging.basicConfig(
                filename=self.log_file_path,
                level=logging.INFO,
                format="[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                filemode="a",
            )
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")

    def _ensure_outfit_font(self) -> str:
        """
        Ensure the 'Outfit' font family is available at runtime.

        Strategy:
        - If 'Outfit' already present in the system's font families, return it.
        - Otherwise, attempt to download Outfit-Regular.ttf from the
          Google Fonts repository and register it for the current session.
          Registration is platform-specific:
            - Windows: use AddFontResourceExW (private) via ctypes.
            - macOS: copy into ~/Library/Fonts.
            - Linux: copy into ~/.local/share/fonts and run fc-cache.
        - If registration succeeds and the family becomes visible to Tk, return 'Outfit'.
        - On any failure, return the system default family as a safe fallback.

        Note: Download/registration is best-effort and behaves gracefully when
        offline or when the current user lacks permission to install fonts.
        """
        try:
            import tkinter.font as tkfont
            families = set(tkfont.families())
            if "Outfit" in families:
                # Already installed system-wide
                try:
                    self._font_loaded_source = "system"
                except Exception:
                    pass
                return "Outfit"
        except Exception:
            families = set()

        # Prefer a bundled font inside the project: ./fonts/Outfit-Regular.ttf
        try:
            script_dir = Path(__file__).parent
        except Exception:
            script_dir = Path(os.path.expanduser("~"))

        bundled_font_path = script_dir / "fonts" / "Outfit-Regular.ttf"

        local_path = None
        if bundled_font_path.exists():
            local_path = str(bundled_font_path)
            try:
                self._font_loaded_source = "bundled"
            except Exception:
                pass
        else:
            # Prepare local fonts directory inside the user's Desktop as fallback
            fonts_dir = os.path.join(os.path.expanduser("~"), "Desktop", "seperatebycolumn", "fonts")
            try:
                os.makedirs(fonts_dir, exist_ok=True)
            except Exception:
                fonts_dir = os.path.join(os.path.expanduser("~"), ".local_separatebycolumn_fonts")
                os.makedirs(fonts_dir, exist_ok=True)

            ttf_url = "https://raw.githubusercontent.com/google/fonts/main/ofl/outfit/Outfit-Regular.ttf"
            local_path = os.path.join(fonts_dir, "Outfit-Regular.ttf")

            try:
                # Download if not present
                if not os.path.exists(local_path):
                    try:
                        urllib.request.urlretrieve(ttf_url, local_path)
                        try:
                            self._font_loaded_source = "downloaded"
                        except Exception:
                            pass
                    except Exception:
                        # If download fails, give up gracefully
                        local_path = None

            except Exception:
                local_path = None

        if local_path and os.path.exists(local_path):
                # Platform specific registration
                if sys.platform.startswith("win"):
                    try:
                        from ctypes import windll
                        FR_PRIVATE = 0x10
                        # Registers font for this session
                        windll.gdi32.AddFontResourceExW(local_path, FR_PRIVATE, 0)
                        # Broadcast WM_FONTCHANGE so applications notice the new font
                        HWND_BROADCAST = 0xFFFF
                        WM_FONTCHANGE = 0x001D
                        windll.user32.SendMessageW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)
                    except Exception:
                        pass

                elif sys.platform == "darwin":
                    # macOS: attempt to register font for the current process using CoreText
                    try:
                        from ctypes import cdll, c_void_p, c_int, c_bool, c_char_p
                        coretext = cdll.LoadLibrary('/System/Library/Frameworks/CoreText.framework/CoreText')
                        cf = cdll.LoadLibrary('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
                        CFURLCreateFromFileSystemRepresentation = cf.CFURLCreateFromFileSystemRepresentation
                        CFURLCreateFromFileSystemRepresentation.restype = c_void_p
                        CFURLCreateFromFileSystemRepresentation.argtypes = [c_void_p, c_char_p, c_int, c_bool]
                        url = CFURLCreateFromFileSystemRepresentation(None, local_path.encode('utf-8'), len(local_path), True)
                        CTFontManagerRegisterFontsForURL = coretext.CTFontManagerRegisterFontsForURL
                        CTFontManagerRegisterFontsForURL.argtypes = [c_void_p, c_int, c_void_p]
                        CTFontManagerRegisterFontsForURL.restype = c_bool
                        kCTFontManagerScopeProcess = 1
                        try:
                            CTFontManagerRegisterFontsForURL(url, kCTFontManagerScopeProcess, None)
                        except Exception:
                            pass
                    except Exception:
                        # If CoreText registration is unavailable, do not copy or install
                        pass

                else:
                    # Linux-ish: attempt to add font to the application's fontconfig
                    try:
                        from ctypes import cdll, c_char_p
                        # Try common lib names
                        for libname in ("libfontconfig.so.1", "libfontconfig.so"):
                            try:
                                libfc = cdll.LoadLibrary(libname)
                                break
                            except Exception:
                                libfc = None
                        if libfc is not None:
                            try:
                                FcInitLoadConfigAndFonts = libfc.FcInitLoadConfigAndFonts
                                FcInitLoadConfigAndFonts.restype = c_void_p
                                config = FcInitLoadConfigAndFonts()
                                FcConfigAppFontAddFile = libfc.FcConfigAppFontAddFile
                                FcConfigAppFontAddFile.argtypes = [c_void_p, c_char_p]
                                FcConfigAppFontAddFile.config = None
                                FcConfigAppFontAddFile(config, local_path.encode('utf-8'))
                            except Exception:
                                pass
                    except Exception:
                        pass

                # After registration attempt, refresh families and check
                try:
                    import tkinter.font as tkfont2
                    families = set(tkfont2.families())
                    if "Outfit" in families:
                        return "Outfit"
                except Exception:
                    pass

        # Final fallback: system default family or sensible Windows default
        try:
            try:
                self._font_loaded_source = "system"
            except Exception:
                pass
            import tkinter.font as tkfont
            return tkfont.nametofont("TkDefaultFont").actual().get("family", "Segoe UI")
        except Exception:
            try:
                self._font_loaded_source = "fallback"
            except Exception:
                pass
            return "Segoe UI"

    def log(self, message: str, level: str = "INFO") -> None:
        """
        Log a message to GUI, console, and file.

        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR, SUCCESS)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"

        # Console output
        print(log_message)

        # File logging
        try:
            if level == "ERROR":
                logging.error(message)
            elif level == "WARNING":
                logging.warning(message)
            elif level == "SUCCESS":
                logging.info(message)
            else:
                logging.info(message)
        except Exception as e:
            print(f"Error writing to log file: {e}")

        # GUI output
        if self.log_text:
            self.log_text.config(state=tk.NORMAL)

            # Color coding
            color_tag = "default"
            if level == "ERROR":
                color_tag = "error"
            elif level == "WARNING":
                color_tag = "warning"
            elif level == "SUCCESS":
                color_tag = "success"

            # Configure tags if not exist
            if not self.log_text.tag_ranges(color_tag):
                if level == "ERROR":
                    self.log_text.tag_configure(color_tag, foreground="red")
                elif level == "WARNING":
                    self.log_text.tag_configure(color_tag, foreground="yellow")
                elif level == "SUCCESS":
                    self.log_text.tag_configure(color_tag, foreground="lightgreen")

            self.log_text.insert(tk.END, log_message + "\n", color_tag)
            self.log_text.see(tk.END)
            # Ensure consistent line spacing across the whole log
            try:
                self.log_text.tag_add("line_spacing", "1.0", tk.END)
            except Exception:
                pass
            self.log_text.config(state=tk.DISABLED)


    def _load_file(self) -> None:
        """Load Excel or CSV file and auto-detect columns."""
        file_path = filedialog.askopenfilename(
            title="Select Excel or CSV file",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            return

        self.log(f"User selected file: {file_path}")

        try:
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Detect file type and read
            if file_path.lower().endswith((".xlsx", ".xls")):
                self.dataframe = pd.read_excel(file_path)
                self.log("File loaded as Excel format")
            elif file_path.lower().endswith(".csv"):
                self.dataframe = pd.read_csv(file_path)
                self.log("File loaded as CSV format")
            else:
                raise ValueError(
                    "Invalid file format. Please use .xlsx, .xls, or .csv"
                )

            # Validate data
            if self.dataframe is None or self.dataframe.empty:
                raise ValueError("Dataset is empty")

            if len(self.dataframe.columns) == 0:
                raise ValueError("No columns detected in dataset")

            self.input_file_path = file_path
            self._update_input_label()

            # Auto-detect columns
            self.all_columns = list(self.dataframe.columns)
            self.log(f"Columns detected: {', '.join(self.all_columns)}")
            self.log(f"Total rows: {len(self.dataframe)}")

            # Update UI - populate listbox
            self._populate_column_listbox()
            self._update_preview()
            self._update_start_button_state()

        except FileNotFoundError as e:
            self.log(f"File not found: {str(e)}", "ERROR")
            messagebox.showerror("File Error", f"File not found:\n{str(e)}")
        except ValueError as e:
            self.log(f"Data validation error: {str(e)}", "ERROR")
            messagebox.showerror("Data Error", f"Invalid data:\n{str(e)}")
        except Exception as e:
            self.log(f"Error loading file: {str(e)}", "ERROR")
            self.log(traceback.format_exc(), "ERROR")
            messagebox.showerror("Error", f"Error loading file:\n{str(e)}")

    def _update_input_label(self) -> None:
        """Update the input file label with the loaded file path."""
        if self.input_file_path:
            filename = os.path.basename(self.input_file_path)
            self.input_file_label.config(text=f"✓ {filename}", fg="green")
        else:
            self.input_file_label.config(text="No file selected", fg="gray")

    def _choose_output_folder(self) -> None:
        """Let user choose the output folder."""
        folder_path = filedialog.askdirectory(title="Select Output Folder")

        if not folder_path:
            return

        # Verify folder exists and is writable
        try:
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"Folder does not exist: {folder_path}")

            if not os.access(folder_path, os.W_OK):
                raise PermissionError(f"No write permission for: {folder_path}")

            self.output_folder_path = folder_path
            self.log(f"Output folder selected: {folder_path}")

            # Update label
            folder_name = os.path.basename(folder_path)
            self.output_folder_label.config(text=f"✓ {folder_name}", fg="green")

            self._update_start_button_state()

        except (FileNotFoundError, PermissionError) as e:
            self.log(f"Folder selection error: {str(e)}", "ERROR")
            messagebox.showerror("Folder Error", str(e))

    def _populate_column_listbox(self) -> None:
        """Populate the multi-select listbox with all columns and 'Select All' option."""
        self.column_listbox.delete(0, tk.END)

        # Add "Select All Columns" at the top
        self.column_listbox.insert(0, ">>> SELECT ALL COLUMNS <<<")

        # Add all columns
        for idx, column in enumerate(self.all_columns, start=1):
            self.column_listbox.insert(idx, column)

        self.log(f"Column listbox populated with {len(self.all_columns)} columns")

    def _on_columns_selected(self, event=None) -> None:
        """Handle column selection changes - update preview immediately."""
        self._update_preview()
        self._update_start_button_state()

    def _get_selected_columns(self) -> List[str]:
        """
        Get the list of selected columns from listbox.
        Handles "Select All" option specially.
        """
        selected_indices = self.column_listbox.curselection()

        if not selected_indices:
            return []

        # Check if "Select All" is selected
        if 0 in selected_indices:
            # Select all columns
            return self.all_columns

        # Otherwise, get selected columns (skip index 0 which is "Select All")
        selected_columns = []
        for idx in selected_indices:
            if idx > 0:  # Skip "Select All" item
                column_name = self.column_listbox.get(idx)
                selected_columns.append(column_name)

        return selected_columns

    def _update_preview(self) -> None:
        """Update preview section with sample data, groups, and planned filenames."""
        if self.preview_text is None or self.dataframe is None:
            return

        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)

        try:
            selected_columns = self._get_selected_columns()

            if not selected_columns:
                self.preview_text.insert(
                    tk.END, "Select columns from the list to see preview...", "info"
                )
                self.preview_info_label.config(
                    text="No columns selected", fg="gray"
                )
                # Apply spacing tag for consistent line height
                try:
                    self.preview_text.tag_add("line_spacing", "1.0", tk.END)
                except Exception:
                    pass
                self.preview_text.config(state=tk.DISABLED)
                return

            # Display selected columns info
            info_text = f"📊 Selected Columns: {', '.join(selected_columns)}\n"
            info_text += f"📈 Total Rows: {len(self.dataframe)}\n"

            # Get unique groups
            if len(selected_columns) == 1:
                unique_groups = self.dataframe[selected_columns[0]].nunique()
                info_text += f"📁 Unique Groups: {unique_groups} (one per value)\n\n"
                group_type = "Value-based"
            elif len(selected_columns) == len(self.all_columns):
                grouped = self.dataframe.groupby(selected_columns, dropna=False)
                unique_groups = len(grouped)
                info_text += f"📁 Unique Groups: {unique_groups} (one per unique row combination)\n\n"
                group_type = "Combination-based (All)"
            else:
                grouped = self.dataframe.groupby(selected_columns, dropna=False)
                unique_groups = len(grouped)
                info_text += f"📁 Unique Groups: {unique_groups} (one per unique combination)\n\n"
                group_type = "Combination-based"

            self.preview_info_label.config(text=info_text, fg="black")

            # Display sample data with selected columns only
            sample_df = self.dataframe[selected_columns].head(30)
            
            self.preview_text.insert(tk.END, "═" * 100 + "\n", "header")
            self.preview_text.insert(
                tk.END, f"Sample Data (First 30 rows, {group_type}):\n", "header"
            )
            self.preview_text.insert(tk.END, "═" * 100 + "\n", "header")

            # Display as formatted table
            preview_str = sample_df.to_string(index=True)
            self.preview_text.insert(tk.END, preview_str)

            # Display planned filenames sample
            self.preview_text.insert(tk.END, "\n\n" + "═" * 100 + "\n", "header")
            self.preview_text.insert(
                tk.END, "Sample Output Filenames (first 10):\n", "header"
            )
            self.preview_text.insert(tk.END, "═" * 100 + "\n", "header")

            # Generate sample filenames
            grouped = self.dataframe.groupby(selected_columns, dropna=False)
            sample_filenames = self._generate_sample_filenames(
                selected_columns, grouped, sample_count=10
            )

            for i, filename in enumerate(sample_filenames, 1):
                ext = ".csv" if self.output_format_var.get() == "csv" else ".xlsx"
                self.preview_text.insert(tk.END, f"{i:2d}. {filename}{ext}\n")

            if unique_groups > 10:
                self.preview_text.insert(
                    tk.END,
                    f"\n... and {unique_groups - 10} more files\n",
                    "info",
                )

            # Apply spacing tag for consistent line height
            try:
                self.preview_text.tag_add("line_spacing", "1.0", tk.END)
            except Exception:
                pass
            self.preview_text.config(state=tk.DISABLED)

        except Exception as e:
            self.preview_text.insert(tk.END, f"Error generating preview: {str(e)}", "error")
            try:
                self.preview_text.tag_add("line_spacing", "1.0", tk.END)
            except Exception:
                pass
            self.preview_text.config(state=tk.DISABLED)
            self.log(f"Preview error: {str(e)}", "WARNING")

    def _generate_sample_filenames(
        self, selected_columns: List[str], grouped, sample_count: int = 10
    ) -> List[str]:
        """Generate sample filenames from first N groups."""
        filenames = []

        for idx, (group_key, _) in enumerate(grouped):
            if idx >= sample_count:
                break

            filename = self._create_filename(selected_columns, group_key, "preview")
            filenames.append(filename)

        return filenames

    def _update_start_button_state(self) -> None:
        """Enable/disable START button based on validation."""
        can_start = (
            self.input_file_path is not None
            and self.output_folder_path is not None
            and len(self._get_selected_columns()) > 0
        )

        if can_start:
            self.start_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.DISABLED)

    def _start_split(self) -> None:
        """Start the split operation in a separate thread."""
        if self.is_processing:
            messagebox.showwarning("Processing", "A split operation is already in progress.")
            return

        # Get user selections
        selected_columns = self._get_selected_columns()
        output_format = self.output_format_var.get()

        if not selected_columns:
            messagebox.showwarning("Column Selection", "Please select at least one column.")
            return

        self.log(f"Split operation starting...")
        self.log(f"Selected columns: {', '.join(selected_columns)}")
        self.log(f"Output format: {output_format}")

        # Start split in separate thread to avoid UI freeze
        self.is_processing = True
        self.start_button.config(state=tk.DISABLED)

        thread = threading.Thread(
            target=self._perform_split,
            args=(selected_columns, output_format),
            daemon=True,
        )
        thread.start()

    def _perform_split(self, selected_columns: List[str], output_format: str) -> None:
        """
        Perform the actual split operation.

        Args:
            selected_columns: List of columns to split by
            output_format: Output format ('csv' or 'excel')
        """
        try:
            self._update_progress(5, "Preparing split operation...")
            self.log(f"Starting split with columns: {', '.join(selected_columns)}")

            # Get unique combinations
            self._update_progress(10, "Computing unique groups...")

            # Create a safe copy of the dataframe for grouping to avoid Pandas
            # errors when columns are categorical and contain null-like values.
            # We only sanitize the selected columns on the copy so original data
            # remains unchanged for other operations.
            safe_df = self.dataframe.copy()
            for col in selected_columns:
                try:
                    # Convert to string and normalize common null representations to 'Unknown'
                    safe_df[col] = (
                        safe_df[col]
                        .astype(str)
                        .replace(["nan", "None", "<NA>", "NoneType", "NA", "NaN", ""], "Unknown")
                        .fillna("Unknown")
                    )
                except Exception:
                    # Fallback: ensure no nulls, then cast to string
                    try:
                        safe_df[col] = safe_df[col].fillna("Unknown").astype(str)
                    except Exception:
                        # If all else fails, create a column of 'Unknown'
                        safe_df[col] = "Unknown"

            if len(selected_columns) == 1:
                # Single column: split by unique values (use sanitized copy)
                split_groups = safe_df.groupby(selected_columns[0], dropna=False)
                total_groups = len(split_groups)
                self.log(f"Single column split: {total_groups} unique values found", "INFO")

            elif len(selected_columns) == len(self.all_columns):
                # All columns: each unique row combination (use sanitized copy)
                split_groups = safe_df.groupby(selected_columns, dropna=False)
                total_groups = len(split_groups)
                self.log(
                    f"All columns split: {total_groups} unique row combinations found",
                    "INFO",
                )

            else:
                # Multiple columns: split by unique combinations (use sanitized copy)
                split_groups = safe_df.groupby(selected_columns, dropna=False)
                total_groups = len(split_groups)
                self.log(
                    f"Multi-column split: {total_groups} unique combinations found",
                    "INFO",
                )

            # Guard against zero groups to avoid division by zero
            if total_groups == 0:
                self.log("No groups found to export.", "WARNING")
                self._update_progress(100, "No groups to export")
                self.is_processing = False
                self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
                return

            self._update_progress(15, f"Exporting {total_groups} groups...")

            # Create output directory for split files
            # Prefer a descriptive folder name based on selected column(s)
            try:
                if len(selected_columns) == 1:
                    base_folder = self._sanitize_string(selected_columns[0])
                elif len(selected_columns) == len(self.all_columns):
                    base_folder = "all_columns"
                else:
                    parts = [self._sanitize_string(c) for c in selected_columns]
                    base_folder = "__".join(parts)
            except Exception:
                base_folder = "split_output"

            # Keep folder name reasonably short
            if len(base_folder) > 80:
                base_folder = base_folder[:80]

            split_output_dir = os.path.join(self.output_folder_path, base_folder)

            # If folder exists, append a counter to avoid collisions
            if os.path.exists(split_output_dir):
                counter = 1
                orig = split_output_dir
                while os.path.exists(split_output_dir):
                    split_output_dir = f"{orig}_{counter}"
                    counter += 1

            os.makedirs(split_output_dir, exist_ok=True)
            self.log(f"Created output directory: {split_output_dir}", "INFO")

            # Export each group
            exported_files = []
            errors = []

            for idx, (group_key, group_data) in enumerate(split_groups):
                try:
                    # Create filename from group key
                    filename = self._create_filename(
                        selected_columns, group_key, mode="export"
                    )

                    extension = ".csv" if output_format == "csv" else ".xlsx"
                    full_filename = f"{filename}{extension}"
                    file_path = os.path.join(split_output_dir, full_filename)

                    # Ensure unique filename if collision occurs
                    original_path = file_path
                    counter = 1
                    while os.path.exists(file_path):
                        name, ext = os.path.splitext(original_path)
                        file_path = f"{name}_{counter}{ext}"
                        counter += 1

                    # Export based on format
                    if output_format == "csv":
                        group_data.to_csv(file_path, index=False)
                    elif output_format == "excel":
                        group_data.to_excel(file_path, index=False, engine="openpyxl")

                    exported_files.append(file_path)
                    # Track exported group info for future features
                    try:
                        # store without extension
                        self.split_groups_info[filename] = len(group_data)
                    except Exception:
                        pass
                    self.log(
                        f"✓ Exported: {full_filename} ({len(group_data)} rows)",
                        "INFO",
                    )

                except Exception as e:
                    error_msg = f"Error exporting group {idx + 1}: {str(e)}"
                    self.log(error_msg, "ERROR")
                    errors.append(error_msg)

                # Update progress
                progress = 15 + (idx / total_groups) * 65
                self._update_progress(
                    progress,
                    f"Exporting files... ({idx + 1}/{total_groups})",
                )

            if errors:
                self.log(f"Completed with {len(errors)} errors", "WARNING")

            self._update_progress(82, "Creating ZIP archive...")

            # Create ZIP archive named after the output folder (sanitized)
            try:
                zip_base = os.path.basename(split_output_dir)
                zip_base_safe = self._sanitize_string(zip_base)
            except Exception:
                zip_base_safe = "output_split"

            zip_filename = f"{zip_base_safe}.zip"
            zip_path = os.path.join(self.output_folder_path, zip_filename)

            # Ensure unique zip filename
            if os.path.exists(zip_path):
                zcnt = 1
                orig_zip = zip_path
                while os.path.exists(zip_path):
                    name, ext = os.path.splitext(orig_zip)
                    zip_path = f"{name}_{zcnt}{ext}"
                    zcnt += 1

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in exported_files:
                    arcname = os.path.relpath(file_path, self.output_folder_path)
                    zipf.write(file_path, arcname)

            zip_size_mb = os.path.getsize(zip_path) / 1024 / 1024

            self.log(f"✓ ZIP archive created: {os.path.basename(zip_path)} ({zip_size_mb:.2f} MB)", "SUCCESS")
            self.log(
                f"✓ Total files exported: {len(exported_files)}",
                "SUCCESS",
            )

            self._update_progress(100, "✓ Split completed successfully!")
            self.log("=" * 80, "INFO")
            self.log("SPLIT OPERATION COMPLETED SUCCESSFULLY!", "SUCCESS")
            self.log("=" * 80, "INFO")

            # Show success message
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success",
                    f"Split operation completed!\n\n"
                    f"Total files: {len(exported_files)}\n"
                    f"Output folder: {split_output_dir}\n"
                    f"ZIP file: {zip_filename}\n"
                    f"ZIP size: {zip_size_mb:.2f} MB",
                ),
            )

        except Exception as e:
            self.log(f"Split operation failed: {str(e)}", "ERROR")
            self.log(traceback.format_exc(), "ERROR")
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error", f"Split operation failed:\n{str(e)}"
                ),
            )

        finally:
            # Reset UI state
            self.is_processing = False
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.root.after(0, self._update_start_button_state)

    def _create_filename(
        self,
        selected_columns: List[str],
        group_key: Tuple,
        mode: str = "export",  # 'export' or 'preview'
    ) -> str:
        """
        Create a safe, readable filename from group key.

        Naming rules:
        - One column: <value>
        - Multiple columns: ColumnA_ValueA__ColumnB_ValueB
        - All columns: Group_001, Group_002, etc.

        Args:
            selected_columns: List of columns used for splitting
            group_key: Tuple of values for this group
            mode: 'export' for actual files, 'preview' for display

        Returns:
            Safe filename string (without extension)
        """
        # Special case: if all columns selected, use Group_NNN format
        if len(selected_columns) == len(self.all_columns):
            if mode == "export":
                group_num = len(self.split_groups_info) + 1
                return f"Group_{group_num:03d}"
            else:
                # For preview, just show Group_NNN
                return f"Group_NNN"

        # Single column: just the value
        if len(selected_columns) == 1:
            val_safe = self._sanitize_string(str(group_key[0]))
            return val_safe

        # Multiple columns: ColumnA_ValueA__ColumnB_ValueB
        parts = []
        for col, value in zip(selected_columns, group_key):
            col_safe = self._sanitize_string(str(col))
            val_safe = self._sanitize_string(str(value))
            parts.append(f"{col_safe}_{val_safe}")

        return "__".join(parts)

    def _sanitize_string(self, s: str) -> str:
        """
        Sanitize a string for use in filenames.

        Args:
            s: String to sanitize

        Returns:
            Sanitized string safe for filenames
        """
        # Remove/replace invalid characters
        invalid_chars = r'<>:"/\\|?*'
        result = s

        for char in invalid_chars:
            result = result.replace(char, "_")

        # Replace spaces with underscores
        result = result.replace(" ", "_")

        # Remove leading/trailing dots and spaces
        result = result.strip(". ")

        # Replace multiple underscores with single
        while "__" in result and not result.startswith("__"):
            result = result.replace("__", "_")

        # Limit length
        if len(result) > 100:
            result = result[:100]

        return result if result else "empty"

    def _update_progress(self, value: float, message: str) -> None:
        """
        Update progress bar and label.

        Args:
            value: Progress value (0-100)
            message: Progress message
        """
        self.progress_var.set(value)
        self.progress_label.config(text=message, fg="blue")
        self.root.update_idletasks()

    def _reset_app(self) -> None:
        """Reset the application to initial state."""
        if self.is_processing:
            messagebox.showwarning(
                "Processing",
                "Cannot reset while split operation is in progress.",
            )
            return

        self.input_file_path = None
        self.output_folder_path = None
        self.dataframe = None
        self.all_columns = []
        self.selected_columns = []
        self.split_groups_info = {}

        # Reset UI
        self.input_file_label.config(text="No file selected", fg="gray")
        self.output_folder_label.config(text="No folder selected", fg="gray")

        self.column_listbox.delete(0, tk.END)

        self.progress_var.set(0)
        self.progress_label.config(text="Ready")
        self.output_format_var.set("csv")

        # Clear preview
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.config(state=tk.DISABLED)
        self.preview_info_label.config(text="No file loaded", fg="gray")

        self._update_start_button_state()
        self.log("Application reset to initial state.", "INFO")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = DataSplitterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
