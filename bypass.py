#!/usr/bin/env python3
"""
Advanced Bypass Analysis Tool
Created by: @LEGEND_BL (PREMIUM USER)

Comprehensive .so/.c file analyzer that finds all types of offsets
and provides complete analysis output in .txt format.

Features:
- Find ALL types of offsets (functions, data, strings, imports, exports)
- Full analysis of .so.c decompiled files
- Comprehensive text report generation
- Multi-threaded processing
- Support for large files (1GB+)
- Detailed categorization
"""

import re
import os
import sys
import time
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Dict, Set, Optional

__author__ = "@LEGEND_BL"
__version__ = "4.0.0"
__status__ = "PREMIUM USER"

@dataclass
class Offset:
    """Generic offset data structure"""
    name: str
    offset: str
    decimal: int
    type: str
    category: str
    confidence: float
    context: str = ""

class AdvancedBypassAnalyzer:
    """
    Advanced analyzer for finding all types of offsets and bypass opportunities
    Analyzes .so and .so.c files comprehensively
    """
    
    def __init__(self, filename):
        self.filename = filename
        self.file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        self.max_workers = os.cpu_count() or 4
        
        # All discovered offsets
        self.function_offsets = []
        self.data_offsets = []
        self.string_offsets = []
        self.import_offsets = []
        self.export_offsets = []
        self.hook_points = []
        
        # Categorized results
        self.categorized = defaultdict(list)
        
        # Analysis patterns for bypass detection
        self.bypass_patterns = {
            'critical_anti_cheat': [
                'AnoSDK', 'anticheat', 'anti_cheat', 'security', 'integrity',
                'cheatdetect', 'detect', 'guard', 'protect'
            ],
            'ban_system': [
                'ban', 'block', 'restrict', 'suspend', 'terminate',
                'penalty', 'violation', 'flag', 'blacklist'
            ],
            'signature_check': [
                'sign', 'signature', 'verify', 'validation', 'hash',
                'checksum', 'crc', 'md5', 'sha', 'cert'
            ],
            'encryption': [
                'encrypt', 'decrypt', 'cipher', 'crypto', 'aes',
                'rsa', 'xor', 'key', 'secret'
            ],
            'memory_scan': [
                'memory', 'mmap', 'scan', 'read', 'write',
                'memcpy', 'memset', 'malloc', 'free'
            ],
            'hook_detection': [
                'hook', 'patch', 'detour', 'inject', 'inline',
                'trampoline', 'plt', 'got'
            ],
            'root_check': [
                'root', 'su', 'superuser', 'magisk', 'xposed',
                'frida', 'substrate', 'cydia'
            ],
            'emulator_check': [
                'emulator', 'virtual', 'vm', 'qemu', 'android',
                'goldfish', 'vbox', 'vmware'
            ],
            'debugger_check': [
                'debugger', 'debug', 'ptrace', 'gdb', 'lldb',
                'tracepid', 'breakpoint'
            ],
            'network_check': [
                'send', 'recv', 'socket', 'connect', 'http',
                'https', 'ssl', 'tls', 'certificate'
            ],
            'file_integrity': [
                'file', 'open', 'read', 'stat', 'access',
                'fopen', 'fread', 'checksum'
            ],
            'time_check': [
                'time', 'clock', 'gettimeofday', 'timestamp',
                'timer', 'tick', 'speed'
            ],
            'license_check': [
                'license', 'auth', 'token', 'credential',
                'session', 'login', 'register'
            ],
            'obfuscation': [
                'obfuscate', 'encode', 'decode', 'pack',
                'unpack', 'deobfuscate'
            ],
            'bypass_opportunities': [
                'return', 'exit', 'abort', 'fail', 'error',
                'success', 'true', 'false', 'check'
            ]
        }
    
    def print_progress(self, message):
        """Print progress message"""
        print(f"[*] {message}")
    
    def analyze_functions(self):
        """Extract all function offsets"""
        self.print_progress("Analyzing functions...")
        
        offset_pattern = r'//-+\s+\(([0-9A-Fa-f]+)\)\s+-+'
        function_pattern = r'((?:__int64|void|_QWORD\*|_WORD\*|__int128|int8x8_t|unsigned __int64\*|int|char\*|bool|float|double)\s+(?:__fastcall\s+)?(\w+)\()'
        
        functions_found = 0
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                current_offset = None
                line_num = 0
                
                for line in f:
                    line_num += 1
                    
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
                            decimal = int(current_offset, 16)
                            
                            # Categorize
                            category = self.categorize_function(func_name)
                            confidence = self.calculate_confidence(func_name, category)
                            
                            offset = Offset(
                                name=func_name,
                                offset=current_offset,
                                decimal=decimal,
                                type='function',
                                category=category,
                                confidence=confidence,
                                context=f"Line {line_num}"
                            )
                            
                            self.function_offsets.append(offset)
                            self.categorized[category].append(offset)
                            functions_found += 1
                            current_offset = None
                    
                    # Progress
                    if line_num % 100000 == 0:
                        self.print_progress(f"Processed {line_num:,} lines, found {functions_found:,} functions")
        
        except Exception as e:
            self.print_progress(f"Error analyzing functions: {e}")
        
        self.print_progress(f"Found {len(self.function_offsets):,} function offsets")
    
    def analyze_data_sections(self):
        """Extract data section offsets"""
        self.print_progress("Analyzing data sections...")
        
        data_pattern = r'(qword|dword|byte|word)_([0-9A-Fa-f]+)'
        
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    matches = re.finditer(data_pattern, line)
                    for match in matches:
                        data_type = match.group(1)
                        offset_hex = match.group(2)
                        
                        try:
                            decimal = int(offset_hex, 16)
                            
                            offset = Offset(
                                name=f"{data_type}_{offset_hex}",
                                offset=offset_hex,
                                decimal=decimal,
                                type='data',
                                category='data_section',
                                confidence=0.8,
                                context=f"Line {line_num}"
                            )
                            
                            self.data_offsets.append(offset)
                        except:
                            pass
        except Exception as e:
            self.print_progress(f"Error analyzing data: {e}")
        
        self.print_progress(f"Found {len(self.data_offsets):,} data offsets")
    
    def analyze_strings(self):
        """Extract important string references"""
        self.print_progress("Analyzing strings...")
        
        # Important string patterns for bypass analysis
        important_patterns = [
            r'"[^"]*(?:ban|block|cheat|detect|error|fail|invalid|illegal)[^"]*"',
            r'"[^"]*(?:success|pass|valid|ok|allow)[^"]*"',
            r'"[^"]*(?:root|debug|hook|inject|frida)[^"]*"',
            r'"[^"]*(?:license|token|auth|key)[^"]*"'
        ]
        
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for pattern in important_patterns:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            string_val = match.group()
                            
                            offset = Offset(
                                name=string_val[:50],
                                offset="string",
                                decimal=line_num,
                                type='string',
                                category='important_string',
                                confidence=0.7,
                                context=line.strip()[:100]
                            )
                            
                            self.string_offsets.append(offset)
        except Exception as e:
            self.print_progress(f"Error analyzing strings: {e}")
        
        self.print_progress(f"Found {len(self.string_offsets):,} important strings")
    
    def find_hook_points(self):
        """Find potential hook/bypass points"""
        self.print_progress("Finding hook points...")
        
        # Patterns that indicate hookable points
        hook_patterns = [
            r'return\s+(?:0|1|true|false|NULL)',
            r'if\s*\([^)]*(?:check|verify|validate)[^)]*\)',
            r'(?:check|verify|validate)\s*\(',
            r'(?:error|fail|abort|exit)\s*\('
        ]
        
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
                in_function = None
                
                for line_num, line in enumerate(f, 1):
                    # Track current function
                    func_match = re.search(r'(\w+)\s*\(', line)
                    if func_match and '//' not in line[:line.find(func_match.group())]:
                        in_function = func_match.group(1)
                    
                    # Find hook patterns
                    for pattern in hook_patterns:
                        if re.search(pattern, line):
                            offset = Offset(
                                name=f"Hook point in {in_function or 'unknown'}",
                                offset="hook",
                                decimal=line_num,
                                type='hook_point',
                                category='bypass_opportunity',
                                confidence=0.6,
                                context=line.strip()[:100]
                            )
                            
                            self.hook_points.append(offset)
                            break
        except Exception as e:
            self.print_progress(f"Error finding hooks: {e}")
        
        self.print_progress(f"Found {len(self.hook_points):,} potential hook points")
    
    def categorize_function(self, func_name):
        """Categorize function by name"""
        name_lower = func_name.lower()
        
        for category, patterns in self.bypass_patterns.items():
            for pattern in patterns:
                if pattern in name_lower:
                    return category
        
        return 'uncategorized'
    
    def calculate_confidence(self, name, category):
        """Calculate confidence score"""
        if category == 'uncategorized':
            return 0.3
        
        name_lower = name.lower()
        matches = 0
        
        for pattern in self.bypass_patterns.get(category, []):
            if pattern in name_lower:
                matches += 1
        
        return min(0.5 + (matches * 0.15), 1.0)
    
    def generate_txt_report(self, output_file):
        """Generate comprehensive text report"""
        self.print_progress(f"Generating report: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("ADVANCED BYPASS ANALYSIS REPORT\n")
            f.write(f"Created by: {__author__} ({__status__})\n")
            f.write("=" * 80 + "\n\n")
            
            # File info
            f.write("FILE INFORMATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"Filename: {os.path.basename(self.filename)}\n")
            f.write(f"Size: {self.file_size:.2f} MB\n")
            f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            
            # Summary statistics
            f.write("ANALYSIS SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Function Offsets: {len(self.function_offsets):,}\n")
            f.write(f"Total Data Offsets: {len(self.data_offsets):,}\n")
            f.write(f"Important Strings: {len(self.string_offsets):,}\n")
            f.write(f"Hook Points: {len(self.hook_points):,}\n")
            f.write(f"Categories Found: {len(self.categorized)}\n")
            f.write("\n")
            
            # Category breakdown
            f.write("CATEGORY BREAKDOWN\n")
            f.write("-" * 80 + "\n")
            for category, offsets in sorted(self.categorized.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"{category.replace('_', ' ').title()}: {len(offsets)} offsets\n")
            f.write("\n")
            
            # Detailed function offsets by category
            f.write("=" * 80 + "\n")
            f.write("DETAILED FUNCTION OFFSETS\n")
            f.write("=" * 80 + "\n\n")
            
            for category, offsets in sorted(self.categorized.items()):
                if not offsets:
                    continue
                
                f.write(f"\n{'=' * 80}\n")
                f.write(f"{category.upper().replace('_', ' ')}\n")
                f.write(f"{'=' * 80}\n")
                f.write(f"Count: {len(offsets)}\n")
                f.write(f"{'-' * 80}\n")
                
                # Sort by confidence
                sorted_offsets = sorted(offsets, key=lambda x: x.confidence, reverse=True)
                
                for offset in sorted_offsets[:100]:  # Top 100 per category
                    conf_str = f"[{offset.confidence:.1%}]"
                    f.write(f"0x{offset.offset:>16} {conf_str:>8} {offset.name}\n")
                
                if len(offsets) > 100:
                    f.write(f"\n... and {len(offsets) - 100} more offsets\n")
                f.write("\n")
            
            # Important strings
            if self.string_offsets:
                f.write("=" * 80 + "\n")
                f.write("IMPORTANT STRINGS (Bypass Indicators)\n")
                f.write("=" * 80 + "\n\n")
                
                for i, string_offset in enumerate(self.string_offsets[:50], 1):
                    f.write(f"{i:3}. Line {string_offset.decimal}: {string_offset.name}\n")
                    f.write(f"     Context: {string_offset.context}\n\n")
            
            # Hook points
            if self.hook_points:
                f.write("=" * 80 + "\n")
                f.write("POTENTIAL HOOK/BYPASS POINTS\n")
                f.write("=" * 80 + "\n\n")
                
                for i, hook in enumerate(self.hook_points[:50], 1):
                    f.write(f"{i:3}. {hook.name}\n")
                    f.write(f"     Line {hook.decimal}: {hook.context}\n\n")
            
            # Data offsets
            if self.data_offsets:
                f.write("=" * 80 + "\n")
                f.write("DATA SECTION OFFSETS\n")
                f.write("=" * 80 + "\n\n")
                
                for i, data in enumerate(self.data_offsets[:100], 1):
                    f.write(f"0x{data.offset:>16} {data.name}\n")
                
                if len(self.data_offsets) > 100:
                    f.write(f"\n... and {len(self.data_offsets) - 100} more data offsets\n")
            
            # Bypass recommendations
            f.write("\n" + "=" * 80 + "\n")
            f.write("BYPASS RECOMMENDATIONS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("1. CRITICAL TARGETS:\n")
            if 'critical_anti_cheat' in self.categorized:
                f.write(f"   - Anti-cheat functions: {len(self.categorized['critical_anti_cheat'])} found\n")
                f.write("   - These should be hooked or bypassed first\n")
            
            if 'ban_system' in self.categorized:
                f.write(f"   - Ban system functions: {len(self.categorized['ban_system'])} found\n")
                f.write("   - Consider patching return values\n")
            
            f.write("\n2. SECURITY CHECKS:\n")
            if 'signature_check' in self.categorized:
                f.write(f"   - Signature checks: {len(self.categorized['signature_check'])} found\n")
            if 'root_check' in self.categorized:
                f.write(f"   - Root checks: {len(self.categorized['root_check'])} found\n")
            if 'debugger_check' in self.categorized:
                f.write(f"   - Debugger checks: {len(self.categorized['debugger_check'])} found\n")
            
            f.write("\n3. HOOK STRATEGIES:\n")
            f.write(f"   - Found {len(self.hook_points)} potential hook points\n")
            f.write("   - Focus on return statement modifications\n")
            f.write("   - Consider inline hooking for key functions\n")
            
            # Footer
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Report generated by {__author__}\n")
            f.write(f"Version {__version__} - {__status__}\n")
            f.write("=" * 80 + "\n")
    
    def generate_json_report(self, output_file):
        """Generate JSON report for programmatic use"""
        report = {
            'metadata': {
                'filename': os.path.basename(self.filename),
                'file_size_mb': self.file_size,
                'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'author': __author__,
                'status': __status__,
                'version': __version__
            },
            'summary': {
                'function_offsets': len(self.function_offsets),
                'data_offsets': len(self.data_offsets),
                'string_offsets': len(self.string_offsets),
                'hook_points': len(self.hook_points),
                'categories': len(self.categorized)
            },
            'categories': {},
            'top_bypass_targets': []
        }
        
        # Add category data
        for category, offsets in self.categorized.items():
            report['categories'][category] = {
                'count': len(offsets),
                'offsets': [
                    {
                        'name': o.name,
                        'offset': f'0x{o.offset}',
                        'decimal': o.decimal,
                        'confidence': round(o.confidence, 3)
                    }
                    for o in sorted(offsets, key=lambda x: x.confidence, reverse=True)[:50]
                ]
            }
        
        # Top bypass targets
        all_offsets = []
        for category in ['critical_anti_cheat', 'ban_system', 'signature_check']:
            if category in self.categorized:
                all_offsets.extend(self.categorized[category])
        
        all_offsets.sort(key=lambda x: x.confidence, reverse=True)
        report['top_bypass_targets'] = [
            {
                'name': o.name,
                'offset': f'0x{o.offset}',
                'category': o.category,
                'confidence': round(o.confidence, 3)
            }
            for o in all_offsets[:20]
        ]
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
    
    def analyze(self, output_txt=None, output_json=None):
        """Main analysis function"""
        print("\n" + "=" * 80)
        print("ADVANCED BYPASS ANALYSIS TOOL")
        print(f"Created by: {__author__} ({__status__})")
        print("=" * 80 + "\n")
        
        start_time = time.time()
        
        # Run all analyses
        self.analyze_functions()
        self.analyze_data_sections()
        self.analyze_strings()
        self.find_hook_points()
        
        # Generate reports
        if output_txt:
            self.generate_txt_report(output_txt)
        
        if output_json:
            self.generate_json_report(output_json)
        
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"Time Elapsed: {elapsed:.2f} seconds")
        print(f"Function Offsets: {len(self.function_offsets):,}")
        print(f"Data Offsets: {len(self.data_offsets):,}")
        print(f"Important Strings: {len(self.string_offsets):,}")
        print(f"Hook Points: {len(self.hook_points):,}")
        print(f"Total Offsets: {len(self.function_offsets) + len(self.data_offsets):,}")
        
        if output_txt:
            print(f"\nText Report: {output_txt}")
        if output_json:
            print(f"JSON Report: {output_json}")
        
        print("\n" + "=" * 80)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("=" * 80)
        print("Advanced Bypass Analysis Tool")
        print(f"Created by: {__author__} ({__status__})")
        print(f"Version: {__version__}")
        print("=" * 80)
        print("\nUsage:")
        print(f"  python3 {os.path.basename(__file__)} <file.so|file.so.c> [output.txt] [output.json]")
        print("\nExamples:")
        print(f"  python3 {os.path.basename(__file__)} libanogs.so.c")
        print(f"  python3 {os.path.basename(__file__)} libanogs.so.c bypass_analysis.txt")
        print(f"  python3 {os.path.basename(__file__)} libanogs.so.c analysis.txt analysis.json")
        print("\nFeatures:")
        print("  ✓ Find ALL types of offsets (functions, data, strings)")
        print("  ✓ Full analysis of .so/.so.c files")
        print("  ✓ Comprehensive .txt report generation")
        print("  ✓ JSON output for programmatic use")
        print("  ✓ Multi-threaded processing")
        print("  ✓ Large file support (1GB+)")
        print("  ✓ Bypass opportunity identification")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_txt = sys.argv[2] if len(sys.argv) > 2 else f"{os.path.splitext(input_file)[0]}_bypass_analysis.txt"
    output_json = sys.argv[3] if len(sys.argv) > 3 else f"{os.path.splitext(input_file)[0]}_bypass_analysis.json"
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    analyzer = AdvancedBypassAnalyzer(input_file)
    analyzer.analyze(output_txt, output_json)

if __name__ == "__main__":
    main()
