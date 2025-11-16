#!/usr/bin/env python3
"""
BGMI 4.1 Offset Finder
This script analyzes the decompiled libanogs.so.c file to find major function offsets
"""

import re
import sys
from collections import defaultdict

def extract_function_offsets(filename):
    """Extract all function definitions with their offsets"""
    functions = []
    
    # Pattern to match function definitions with offsets
    # Example: //----- (000000000051F88C) ----------------------------------------------------
    offset_pattern = r'//-+\s+\(([0-9A-Fa-f]+)\)\s+-+'
    function_pattern = r'((?:__int64|void|_QWORD\*|_WORD\*|__int128|int8x8_t|unsigned __int64\*)\s+(?:__fastcall\s+)?(\w+)\()'
    
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        current_offset = None
        for line in f:
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
    
    return functions

def find_sdk_functions(functions):
    """Find SDK-related functions (major functions)"""
    sdk_functions = []
    
    for func in functions:
        if func['name'].startswith('AnoSDK'):
            sdk_functions.append(func)
    
    return sdk_functions

def find_important_patterns(filename):
    """Find important hex patterns that might be offsets"""
    patterns = defaultdict(list)
    
    # Look for common game-related patterns
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            # Find hex values that look like addresses
            hex_matches = re.finditer(r'0x([0-9A-Fa-f]{6,8})u?L?L?', line)
            for match in hex_matches:
                hex_val = match.group(1)
                decimal_val = int(hex_val, 16)
                # Filter for significant values (likely addresses or important offsets)
                if decimal_val > 0x100000:  # Filter out small values
                    patterns[hex_val].append(line_num)
    
    return patterns

def main():
    filename = '/home/runner/work/Bgmi-4.1/Bgmi-4.1/libanogs.so.c'
    
    print("=" * 80)
    print("BGMI 4.1 - Offset Finder Analysis")
    print("=" * 80)
    print()
    
    # Extract all functions
    print("[*] Extracting function offsets...")
    functions = extract_function_offsets(filename)
    print(f"[+] Found {len(functions)} functions")
    print()
    
    # Find SDK functions (major functions)
    print("[*] Finding SDK functions (major offsets)...")
    sdk_functions = find_sdk_functions(functions)
    print(f"[+] Found {len(sdk_functions)} SDK functions")
    print()
    
    # Display major SDK functions
    if sdk_functions:
        print("=" * 80)
        print("MAJOR OFFSETS - SDK Functions")
        print("=" * 80)
        for func in sorted(sdk_functions, key=lambda x: x['decimal']):
            print(f"Offset: 0x{func['offset']} ({func['decimal']:>10}) - {func['name']}")
        print()
    
    # Find first 20 functions (usually important initialization functions)
    print("=" * 80)
    print("BEST OFFSETS - First 20 Functions (Early Init)")
    print("=" * 80)
    for func in functions[:20]:
        print(f"Offset: 0x{func['offset']} ({func['decimal']:>10}) - {func['name']}")
    print()
    
    # Find important patterns
    print("[*] Analyzing important hex patterns...")
    patterns = find_important_patterns(filename)
    
    # Show most frequently used patterns (likely important)
    print("=" * 80)
    print("BEST OFFSETS - Most Referenced Hex Values")
    print("=" * 80)
    sorted_patterns = sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True)[:20]
    for hex_val, line_nums in sorted_patterns:
        print(f"Value: 0x{hex_val} ({int(hex_val, 16):>10}) - Referenced {len(line_nums)} times")
    print()
    
    # Generate summary report
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Functions: {len(functions)}")
    print(f"SDK Functions (Major): {len(sdk_functions)}")
    print(f"Unique Hex Patterns: {len(patterns)}")
    print()
    
    # Save detailed report
    report_file = '/home/runner/work/Bgmi-4.1/Bgmi-4.1/offset_report.txt'
    with open(report_file, 'w') as f:
        f.write("BGMI 4.1 - Detailed Offset Report\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("MAJOR OFFSETS - SDK Functions\n")
        f.write("=" * 80 + "\n")
        for func in sorted(sdk_functions, key=lambda x: x['decimal']):
            f.write(f"0x{func['offset']} - {func['name']}\n")
        f.write("\n")
        
        f.write("ALL FUNCTIONS (First 100)\n")
        f.write("=" * 80 + "\n")
        for func in functions[:100]:
            f.write(f"0x{func['offset']} - {func['name']}\n")
        f.write("\n")
    
    print(f"[+] Detailed report saved to: {report_file}")
    print()

if __name__ == "__main__":
    main()
