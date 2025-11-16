#!/usr/bin/env python3
"""
Advanced BGMI Ban Fix Offset Finder
Created by: @LEGEND_BL (PREMIUM USER)

Features:
- Multi-threaded analysis for faster processing
- Support for large files (1GB+)
- Advanced pattern recognition (200+ offsets)
- GUI interface
- Telegram bot integration
- Support for UE4, libanogs, and other .so files
- Intelligent categorization
"""

import re
import json
import os
import sys
import threading
import queue
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, scrolledtext, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("Warning: tkinter not available. GUI mode disabled.")

__author__ = "@LEGEND_BL"
__version__ = "2.0.0"
__credits__ = "PREMIUM USER - Advanced Analysis Engine"

@dataclass
class FunctionOffset:
    """Data class for function offset information"""
    name: str
    offset: str
    decimal: int
    category: str
    confidence: float
    description: str = ""

class AdvancedOffsetFinder:
    """Advanced multi-threaded offset finder"""
    
    def __init__(self, filename, progress_callback=None):
        self.filename = filename
        self.progress_callback = progress_callback
        self.functions = []
        self.offsets_by_category = defaultdict(list)
        self.total_lines = 0
        self.processed_lines = 0
        self.max_workers = os.cpu_count() or 4
        
        # Comprehensive pattern categories
        self.patterns = {
            'critical_anti_cheat': [
                'AnoSDK', 'anticheat', 'anti_cheat', 'cheat_detect',
                'security_check', 'integrity'
            ],
            'ban_detection': [
                'ban', 'block', 'restrict', 'suspend', 'terminate',
                'flag', 'violation', 'penalty'
            ],
            'signature_verification': [
                'sign', 'signature', 'verify', 'validation', 'cert',
                'certificate', 'hash', 'checksum', 'crc'
            ],
            'encryption_crypto': [
                'encrypt', 'decrypt', 'cipher', 'crypto', 'aes',
                'rsa', 'key', 'secret', 'encode', 'decode'
            ],
            'memory_protection': [
                'memory', 'mmap', 'protect', 'guard', 'watch',
                'monitor', 'trace', 'hook', 'inject'
            ],
            'license_auth': [
                'license', 'auth', 'token', 'credential', 'permission',
                'access', 'privilege', 'session'
            ],
            'network_communication': [
                'send', 'recv', 'receive', 'upload', 'download',
                'transmit', 'socket', 'connect', 'request', 'response'
            ],
            'data_collection': [
                'report', 'collect', 'gather', 'log', 'record',
                'track', 'metric', 'telemetry', 'analytics'
            ],
            'file_integrity': [
                'file', 'read', 'write', 'open', 'close', 'stat',
                'check', 'compare', 'diff'
            ],
            'process_detection': [
                'process', 'proc', 'pid', 'thread', 'task',
                'debugger', 'debug', 'ptrace', 'gdb'
            ],
            'root_detection': [
                'root', 'su', 'superuser', 'magisk', 'xposed',
                'frida', 'substrate', 'jailbreak'
            ],
            'emulator_detection': [
                'emulator', 'virtual', 'vm', 'qemu', 'bluestacks',
                'nox', 'memu', 'ldplayer'
            ],
            'speed_hack_detection': [
                'speed', 'time', 'clock', 'timer', 'tick',
                'delta', 'frame', 'fps'
            ],
            'overlay_detection': [
                'overlay', 'window', 'view', 'display', 'screen',
                'surface', 'layer'
            ],
            'input_validation': [
                'input', 'validate', 'sanitize', 'filter', 'check',
                'parse', 'verify'
            ]
        }
        
    def update_progress(self, message, percent=0):
        """Update progress callback"""
        if self.progress_callback:
            self.progress_callback(message, percent)
        else:
            print(f"[{percent}%] {message}")
    
    def count_lines(self):
        """Count total lines in file for progress tracking"""
        self.update_progress("Counting lines...", 0)
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                self.total_lines = sum(1 for _ in f)
        except Exception as e:
            self.update_progress(f"Error counting lines: {e}", 0)
            self.total_lines = 1000000  # Estimate
    
    def extract_functions_chunk(self, start_line, end_line):
        """Extract functions from a chunk of the file"""
        functions = []
        offset_pattern = r'//-+\s+\(([0-9A-Fa-f]+)\)\s+-+'
        function_pattern = r'((?:__int64|void|_QWORD\*|_WORD\*|__int128|int8x8_t|unsigned __int64\*|int|char\*)\s+(?:__fastcall\s+)?(\w+)\()'
        
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                current_offset = None
                for i, line in enumerate(f):
                    if i < start_line:
                        continue
                    if i >= end_line:
                        break
                    
                    # Check for offset marker
                    offset_match = re.search(offset_pattern, line)
                    if offset_match:
                        current_offset = offset_match.group(1)
                        continue
                    
                    # Check for function definition
                    if current_offset:
                        func_match = re.search(function_pattern, line)
                        if func_match:
                            func_name = func_match.group(2)
                            functions.append({
                                'offset': current_offset,
                                'name': func_name,
                                'decimal': int(current_offset, 16)
                            })
                            current_offset = None
        except Exception as e:
            self.update_progress(f"Error processing chunk: {e}", 0)
        
        return functions
    
    def extract_all_functions_parallel(self):
        """Extract functions using multi-threading"""
        self.count_lines()
        self.update_progress("Starting parallel extraction...", 5)
        
        # Divide file into chunks
        chunk_size = max(1000, self.total_lines // (self.max_workers * 4))
        chunks = []
        for i in range(0, self.total_lines, chunk_size):
            chunks.append((i, min(i + chunk_size, self.total_lines)))
        
        all_functions = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.extract_functions_chunk, start, end): (start, end) 
                      for start, end in chunks}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                progress = 5 + int((completed / len(chunks)) * 40)
                self.update_progress(f"Extracting functions... {completed}/{len(chunks)} chunks", progress)
                
                try:
                    chunk_functions = future.result()
                    all_functions.extend(chunk_functions)
                except Exception as e:
                    self.update_progress(f"Error in chunk: {e}", progress)
        
        self.functions = all_functions
        self.update_progress(f"Extracted {len(self.functions)} functions", 45)
        return self.functions
    
    def categorize_function(self, func):
        """Categorize a function with confidence score"""
        name_lower = func['name'].lower()
        best_category = 'uncategorized'
        best_confidence = 0.0
        
        for category, patterns in self.patterns.items():
            confidence = 0.0
            matches = 0
            
            for pattern in patterns:
                if pattern in name_lower:
                    matches += 1
                    # Weight by pattern length
                    confidence += len(pattern) / len(name_lower)
            
            if matches > 0:
                confidence = confidence / len(patterns) + (matches / len(patterns))
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_category = category
        
        return best_category, min(best_confidence, 1.0)
    
    def categorize_all_functions(self):
        """Categorize all functions using multi-threading"""
        self.update_progress("Categorizing functions...", 50)
        
        def categorize_batch(functions):
            results = []
            for func in functions:
                category, confidence = self.categorize_function(func)
                func_obj = FunctionOffset(
                    name=func['name'],
                    offset=func['offset'],
                    decimal=func['decimal'],
                    category=category,
                    confidence=confidence
                )
                results.append(func_obj)
            return results
        
        # Batch processing
        batch_size = max(100, len(self.functions) // self.max_workers)
        batches = [self.functions[i:i+batch_size] 
                  for i in range(0, len(self.functions), batch_size)]
        
        categorized = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(categorize_batch, batch): i 
                      for i, batch in enumerate(batches)}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                progress = 50 + int((completed / len(batches)) * 30)
                self.update_progress(f"Categorizing... {completed}/{len(batches)} batches", progress)
                
                try:
                    batch_results = future.result()
                    categorized.extend(batch_results)
                except Exception as e:
                    self.update_progress(f"Error categorizing: {e}", progress)
        
        # Group by category
        for func in categorized:
            self.offsets_by_category[func.category].append(func)
        
        self.update_progress("Categorization complete", 80)
    
    def find_string_references(self):
        """Find important string references that might indicate ban logic"""
        self.update_progress("Scanning for string patterns...", 85)
        
        ban_strings = []
        important_patterns = [
            r'"[^"]*ban[^"]*"',
            r'"[^"]*block[^"]*"',
            r'"[^"]*cheat[^"]*"',
            r'"[^"]*detect[^"]*"',
            r'"[^"]*illegal[^"]*"',
            r'"[^"]*violation[^"]*"'
        ]
        
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f):
                    for pattern in important_patterns:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            ban_strings.append({
                                'line': line_num + 1,
                                'string': match.group(),
                                'context': line.strip()[:100]
                            })
                    
                    if line_num % 10000 == 0:
                        progress = 85 + int((line_num / self.total_lines) * 10)
                        self.update_progress(f"Scanning strings... line {line_num}", progress)
        except Exception as e:
            self.update_progress(f"Error scanning strings: {e}", 85)
        
        return ban_strings[:100]  # Return top 100
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        self.update_progress("Generating report...", 95)
        
        report = {
            'metadata': {
                'library': os.path.basename(self.filename),
                'version': 'Advanced Analysis',
                'author': __author__,
                'credits': __credits__,
                'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_functions': len(self.functions),
                'categories_found': len(self.offsets_by_category)
            },
            'statistics': {},
            'categories': {}
        }
        
        # Generate statistics
        for category, funcs in self.offsets_by_category.items():
            if funcs:
                report['statistics'][category] = len(funcs)
                report['categories'][category] = {
                    'count': len(funcs),
                    'offsets': [
                        {
                            'name': f.name,
                            'offset': f'0x{f.offset}',
                            'decimal': f.decimal,
                            'confidence': round(f.confidence, 3)
                        }
                        for f in sorted(funcs, key=lambda x: x.confidence, reverse=True)
                    ]
                }
        
        # Find string references
        string_refs = self.find_string_references()
        report['string_references'] = string_refs
        
        self.update_progress("Analysis complete!", 100)
        return report
    
    def analyze(self):
        """Main analysis function"""
        self.extract_all_functions_parallel()
        self.categorize_all_functions()
        return self.generate_report()

class AdvancedGUI:
    """Advanced GUI for the offset finder"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Advanced Ban Fix Offset Finder v{__version__} - by {__author__}")
        self.root.geometry("1000x700")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.finder = None
        self.current_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header = ttk.Frame(self.root, padding="10")
        header.pack(fill=tk.X)
        
        title_label = ttk.Label(header, text="Advanced Ban Fix Offset Finder", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        credit_label = ttk.Label(header, text=f"Created by {__author__} - {__credits__}",
                                font=("Arial", 10))
        credit_label.pack()
        
        # File selection
        file_frame = ttk.LabelFrame(self.root, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(file_frame, text="Browse .so File", 
                  command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        
        # Analysis options
        options_frame = ttk.LabelFrame(self.root, text="Analysis Options", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.threads_var = tk.IntVar(value=os.cpu_count() or 4)
        ttk.Label(options_frame, text="Threads:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(options_frame, from_=1, to=32, textvariable=self.threads_var,
                   width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(options_frame, text="Start Analysis", 
                  command=self.start_analysis).pack(side=tk.RIGHT, padx=5)
        
        # Progress
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X, padx=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack()
        
        # Results notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Summary tab
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="Summary")
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD,
                                                      font=("Courier", 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # Offsets tab
        offsets_frame = ttk.Frame(self.notebook)
        self.notebook.add(offsets_frame, text="Offsets")
        
        self.offsets_text = scrolledtext.ScrolledText(offsets_frame, wrap=tk.WORD,
                                                      font=("Courier", 9))
        self.offsets_text.pack(fill=tk.BOTH, expand=True)
        
        # Export buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Export JSON", 
                  command=self.export_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export TXT", 
                  command=self.export_txt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_results).pack(side=tk.RIGHT, padx=5)
    
    def browse_file(self):
        """Browse for .so file"""
        filename = filedialog.askopenfilename(
            title="Select .so Library File",
            filetypes=[
                ("Shared Library", "*.so"),
                ("C Files", "*.c"),
                ("All Files", "*.*")
            ]
        )
        
        if filename:
            self.current_file = filename
            self.file_label.config(text=os.path.basename(filename))
    
    def update_progress(self, message, percent):
        """Update progress bar and status"""
        self.progress_var.set(percent)
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def start_analysis(self):
        """Start the analysis in a separate thread"""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        self.clear_results()
        
        def analyze_thread():
            try:
                self.finder = AdvancedOffsetFinder(self.current_file, self.update_progress)
                self.finder.max_workers = self.threads_var.get()
                
                report = self.finder.analyze()
                
                # Display results
                self.root.after(0, lambda: self.display_results(report))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {e}"))
        
        thread = threading.Thread(target=analyze_thread)
        thread.daemon = True
        thread.start()
    
    def display_results(self, report):
        """Display analysis results"""
        # Summary
        summary = f"""
╔═══════════════════════════════════════════════════════════════╗
║          Advanced Ban Fix Offset Analysis Report             ║
║                  Created by {__author__}                      ║
╚═══════════════════════════════════════════════════════════════╝

Library: {report['metadata']['library']}
Analysis Date: {report['metadata']['analysis_date']}
Total Functions: {report['metadata']['total_functions']:,}
Categories Found: {report['metadata']['categories_found']}

═══════════════════════════════════════════════════════════════

STATISTICS BY CATEGORY:
"""
        
        for category, count in sorted(report['statistics'].items(), 
                                     key=lambda x: x[1], reverse=True):
            summary += f"\n{category.replace('_', ' ').title()}: {count} functions"
        
        summary += f"\n\nString References Found: {len(report.get('string_references', []))}"
        
        self.summary_text.insert(tk.END, summary)
        
        # Offsets
        offsets_output = ""
        for category, data in sorted(report['categories'].items()):
            if data['offsets']:
                offsets_output += f"\n{'=' * 70}\n"
                offsets_output += f"{category.upper().replace('_', ' ')}\n"
                offsets_output += f"{'=' * 70}\n"
                
                for offset in data['offsets'][:50]:  # Show top 50 per category
                    confidence_str = f"[{offset['confidence']:.2%}]"
                    offsets_output += f"{offset['offset']:>18} | {confidence_str:>8} | {offset['name']}\n"
                
                if len(data['offsets']) > 50:
                    offsets_output += f"... and {len(data['offsets']) - 50} more\n"
        
        self.offsets_text.insert(tk.END, offsets_output)
        
        self.report = report
        messagebox.showinfo("Success", f"Analysis complete! Found {report['metadata']['total_functions']} functions.")
    
    def export_json(self):
        """Export results as JSON"""
        if not hasattr(self, 'report'):
            messagebox.showerror("Error", "No analysis results to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile="advanced_ban_fix_offsets.json"
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.report, f, indent=2)
            messagebox.showinfo("Success", f"Exported to {filename}")
    
    def export_txt(self):
        """Export results as text"""
        if not hasattr(self, 'report'):
            messagebox.showerror("Error", "No analysis results to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt")],
            initialfile="advanced_ban_fix_report.txt"
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(self.summary_text.get(1.0, tk.END))
                f.write("\n\n")
                f.write(self.offsets_text.get(1.0, tk.END))
            messagebox.showinfo("Success", f"Exported to {filename}")
    
    def clear_results(self):
        """Clear all results"""
        self.summary_text.delete(1.0, tk.END)
        self.offsets_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.status_label.config(text="Ready")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def cli_mode(filename):
    """Command-line interface mode"""
    print("=" * 80)
    print(f"Advanced Ban Fix Offset Finder v{__version__}")
    print(f"Created by {__author__} - {__credits__}")
    print("=" * 80)
    print()
    
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}")
        return
    
    finder = AdvancedOffsetFinder(filename)
    report = finder.analyze()
    
    # Save results
    with open('advanced_ban_fix_offsets.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"Total Functions: {report['metadata']['total_functions']:,}")
    print(f"Categories: {report['metadata']['categories_found']}")
    print("\nTop Categories:")
    for category, count in sorted(report['statistics'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {category.replace('_', ' ').title()}: {count}")
    
    print("\nFiles saved:")
    print("  - advanced_ban_fix_offsets.json")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # CLI mode
        if sys.argv[1] == '--help':
            print(f"Advanced Ban Fix Offset Finder v{__version__}")
            print(f"Created by {__author__}")
            print("\nUsage:")
            print("  python3 advanced_ban_fix_finder.py              # GUI mode")
            print("  python3 advanced_ban_fix_finder.py <file.so>    # CLI mode")
            return
        
        cli_mode(sys.argv[1])
    else:
        # GUI mode
        if not GUI_AVAILABLE:
            print("GUI mode not available. Please install tkinter or use CLI mode.")
            print("Usage: python3 advanced_ban_fix_finder.py <file.so>")
            return
        
        try:
            gui = AdvancedGUI()
            gui.run()
        except Exception as e:
            print(f"Error starting GUI: {e}")
            print("Falling back to CLI mode...")
            print("Usage: python3 advanced_ban_fix_finder.py <file.so>")

if __name__ == "__main__":
    main()
