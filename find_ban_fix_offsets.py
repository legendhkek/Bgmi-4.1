#!/usr/bin/env python3
"""
BGMI 4.1 Ban Fix Offset Finder
This script identifies offsets related to anti-cheat, detection, and ban mechanisms
that are commonly targeted for patching or analysis.
"""

import re
import json
from collections import defaultdict

class BanFixOffsetFinder:
    def __init__(self, filename):
        self.filename = filename
        self.functions = []
        self.ban_fix_offsets = {
            'critical_anti_cheat': [],
            'detection_functions': [],
            'signature_verification': [],
            'license_checks': [],
            'report_functions': [],
            'memory_checks': [],
            'integrity_checks': []
        }
        
    def extract_all_functions(self):
        """Extract all function definitions with their offsets"""
        offset_pattern = r'//-+\s+\(([0-9A-Fa-f]+)\)\s+-+'
        function_pattern = r'((?:__int64|void|_QWORD\*|_WORD\*|__int128|int8x8_t|unsigned __int64\*)\s+(?:__fastcall\s+)?(\w+)\()'
        
        with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
            current_offset = None
            for line in f:
                offset_match = re.search(offset_pattern, line)
                if offset_match:
                    current_offset = offset_match.group(1)
                    continue
                
                if current_offset:
                    func_match = re.search(function_pattern, line)
                    if func_match:
                        func_name = func_match.group(2)
                        self.functions.append({
                            'offset': current_offset,
                            'name': func_name,
                            'decimal': int(current_offset, 16)
                        })
                        current_offset = None
        
        return self.functions
    
    def categorize_ban_fix_functions(self):
        """Categorize functions that are commonly used for ban fixes"""
        
        # Critical anti-cheat SDK functions
        sdk_patterns = ['AnoSDK']
        
        # Detection and check patterns
        detection_patterns = [
            'check', 'verify', 'valid', 'detect', 'scan', 
            'inspect', 'monitor', 'watch', 'guard'
        ]
        
        # Signature and crypto patterns
        signature_patterns = [
            'sign', 'signature', 'hash', 'crypto', 'encrypt',
            'decrypt', 'verify', 'cert', 'key'
        ]
        
        # License and auth patterns
        license_patterns = [
            'license', 'auth', 'token', 'credential', 
            'permission', 'access'
        ]
        
        # Report and data sending patterns
        report_patterns = [
            'report', 'send', 'upload', 'transmit', 
            'recv', 'receive', 'data'
        ]
        
        # Memory and integrity patterns
        memory_patterns = [
            'memory', 'mmap', 'protect', 'integrity',
            'crc', 'sum', 'compare'
        ]
        
        for func in self.functions:
            name_lower = func['name'].lower()
            
            # Check SDK functions (highest priority)
            if any(pattern in func['name'] for pattern in sdk_patterns):
                self.ban_fix_offsets['critical_anti_cheat'].append(func)
                continue
            
            # Check detection functions
            if any(pattern in name_lower for pattern in detection_patterns):
                self.ban_fix_offsets['detection_functions'].append(func)
                continue
            
            # Check signature functions
            if any(pattern in name_lower for pattern in signature_patterns):
                self.ban_fix_offsets['signature_verification'].append(func)
                continue
            
            # Check license functions
            if any(pattern in name_lower for pattern in license_patterns):
                self.ban_fix_offsets['license_checks'].append(func)
                continue
            
            # Check report functions
            if any(pattern in name_lower for pattern in report_patterns):
                self.ban_fix_offsets['report_functions'].append(func)
                continue
            
            # Check memory functions
            if any(pattern in name_lower for pattern in memory_patterns):
                self.ban_fix_offsets['memory_checks'].append(func)
    
    def find_hook_points(self):
        """Find common hook/patch points in the code"""
        hook_points = []
        
        # Look for common return statements that could be patched
        with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
            in_sdk_function = False
            current_function = None
            line_num = 0
            
            for line in f:
                line_num += 1
                
                # Track SDK functions
                if 'AnoSDK' in line and '(' in line:
                    match = re.search(r'(AnoSDK\w+)', line)
                    if match:
                        current_function = match.group(1)
                        in_sdk_function = True
                
                # Look for return statements in SDK functions
                if in_sdk_function and current_function:
                    if 'return' in line:
                        # Check for common return patterns
                        if re.search(r'return\s+0[xX][0-9A-Fa-f]+', line):
                            hook_points.append({
                                'function': current_function,
                                'line': line_num,
                                'pattern': line.strip(),
                                'type': 'return_value'
                            })
                        elif re.search(r'return\s+\-?\d+', line):
                            hook_points.append({
                                'function': current_function,
                                'line': line_num,
                                'pattern': line.strip(),
                                'type': 'return_code'
                            })
                
                # End of function
                if in_sdk_function and line.strip() == '}' and current_function:
                    in_sdk_function = False
                    current_function = None
        
        return hook_points
    
    def generate_report(self, output_file='ban_fix_offsets.json'):
        """Generate comprehensive ban fix offset report"""
        
        print("=" * 80)
        print("BGMI 4.1 - Ban Fix Offset Finder")
        print("=" * 80)
        print()
        
        # Extract functions
        print("[*] Extracting function offsets...")
        self.extract_all_functions()
        print(f"[+] Found {len(self.functions)} total functions")
        print()
        
        # Categorize ban fix functions
        print("[*] Categorizing ban fix related functions...")
        self.categorize_ban_fix_functions()
        print()
        
        # Display results by category
        for category, funcs in self.ban_fix_offsets.items():
            if funcs:
                print("=" * 80)
                print(f"{category.upper().replace('_', ' ')}")
                print("=" * 80)
                for func in sorted(funcs, key=lambda x: x['decimal'])[:20]:  # Show top 20
                    print(f"Offset: 0x{func['offset']} ({func['decimal']:>10}) - {func['name']}")
                print(f"[Total: {len(funcs)} functions]")
                print()
        
        # Find hook points
        print("[*] Finding potential hook/patch points...")
        hook_points = self.find_hook_points()
        print(f"[+] Found {len(hook_points)} potential hook points")
        print()
        
        if hook_points:
            print("=" * 80)
            print("POTENTIAL HOOK/PATCH POINTS")
            print("=" * 80)
            for hook in hook_points[:15]:  # Show top 15
                print(f"Function: {hook['function']}")
                print(f"  Line: {hook['line']}")
                print(f"  Type: {hook['type']}")
                print(f"  Pattern: {hook['pattern'][:70]}")
                print()
        
        # Generate JSON output
        output_data = {
            'library': 'libanogs.so',
            'version': 'BGMI 4.1',
            'analysis_type': 'ban_fix_offsets',
            'total_functions': len(self.functions),
            'categories': {}
        }
        
        for category, funcs in self.ban_fix_offsets.items():
            output_data['categories'][category] = {
                'count': len(funcs),
                'offsets': [
                    {
                        'name': f['name'],
                        'offset': f'0x{f["offset"]}',
                        'decimal': f['decimal']
                    }
                    for f in funcs
                ]
            }
        
        output_data['hook_points'] = hook_points
        
        # Save JSON
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        for category, funcs in self.ban_fix_offsets.items():
            if funcs:
                print(f"{category.replace('_', ' ').title()}: {len(funcs)} functions")
        print(f"Hook Points: {len(hook_points)}")
        print()
        print(f"[+] Detailed report saved to: {output_file}")
        print()
        
        # Generate detailed text report
        self.generate_text_report(hook_points)
    
    def generate_text_report(self, hook_points):
        """Generate detailed text report"""
        report_file = 'ban_fix_report.txt'
        
        with open(report_file, 'w') as f:
            f.write("BGMI 4.1 - Ban Fix Offset Analysis Report\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("CRITICAL ANTI-CHEAT FUNCTIONS (Primary Targets)\n")
            f.write("=" * 80 + "\n")
            for func in self.ban_fix_offsets['critical_anti_cheat']:
                f.write(f"0x{func['offset']} - {func['name']}\n")
            f.write("\n")
            
            for category, funcs in self.ban_fix_offsets.items():
                if category != 'critical_anti_cheat' and funcs:
                    f.write(f"\n{category.upper().replace('_', ' ')}\n")
                    f.write("=" * 80 + "\n")
                    for func in funcs:
                        f.write(f"0x{func['offset']} - {func['name']}\n")
                    f.write("\n")
            
            if hook_points:
                f.write("\nPOTENTIAL HOOK/PATCH POINTS\n")
                f.write("=" * 80 + "\n")
                for hook in hook_points:
                    f.write(f"\nFunction: {hook['function']}\n")
                    f.write(f"Line: {hook['line']}\n")
                    f.write(f"Type: {hook['type']}\n")
                    f.write(f"Pattern: {hook['pattern']}\n")
        
        print(f"[+] Text report saved to: {report_file}")
        print()

def main():
    filename = '/home/runner/work/Bgmi-4.1/Bgmi-4.1/libanogs.so.c'
    
    finder = BanFixOffsetFinder(filename)
    finder.generate_report('ban_fix_offsets.json')
    
    print("\n" + "=" * 80)
    print("BAN FIX OFFSET ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nFiles generated:")
    print("1. ban_fix_offsets.json - Machine-readable offset data")
    print("2. ban_fix_report.txt   - Human-readable detailed report")
    print("\nThese offsets can be used for:")
    print("- Analyzing anti-cheat behavior")
    print("- Identifying detection mechanisms")
    print("- Understanding ban logic")
    print("- Researching security implementations")
    print("\nWARNING: Use for educational and research purposes only!")
    print("=" * 80)

if __name__ == "__main__":
    main()
