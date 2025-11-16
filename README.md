# BGMI 4.1 - Offset Analysis

This repository contains the decompiled `libanogs.so` library from BGMI (Battlegrounds Mobile India) version 4.1 and tools to find major offsets.

## Overview

The `libanogs.so` library is an anti-cheat/security SDK used in BGMI. This analysis identifies the most important function offsets for research and analysis purposes.

## Files

- `libanogs.so.c` - Decompiled C code from the shared library (21MB)
- `find_offsets.py` - Python script to analyze and extract function offsets
- `offsets.json` - JSON file containing all major offsets
- `offset_report.txt` - Detailed text report of all findings

## Usage

Run the offset finder:

```bash
python3 find_offsets.py
```

## Major Offsets Found

### SDK Functions (Major Offsets)

These are the primary functions exposed by the AnoSDK (Anti-cheat SDK):

| Function Name | Offset | Decimal | Description |
|---------------|--------|---------|-------------|
| AnoSDKInit | 0x1D3814 | 1914900 | Initialize SDK |
| AnoSDKInitEx | 0x1D3B40 | 1915712 | Extended initialization |
| AnoSDKOnPause | 0x1D4C0C | 1920012 | Handle app pause |
| AnoSDKOnResume | 0x1D5030 | 1921072 | Handle app resume |
| AnoSDKGetReportData | 0x1D551C | 1922332 | Get report data |
| AnoSDKOnRecvData | 0x1D624C | 1925708 | Receive data handler |
| AnoSDKIoctl | 0x1D6730 | 1926960 | I/O control |
| AnoSDKFree | 0x1D7398 | 1930136 | Free resources |
| AnoSDKGetReportData2 | 0x1D78CC | 1931468 | Get report data v2 |
| AnoSDKGetReportData3 | 0x1D7938 | 1931576 | Get report data v3 |
| AnoSDKGetReportData4 | 0x1D7FC4 | 1933252 | Get report data v4 |
| AnoSDKOnRecvSignature | 0x1D88EC | 1935596 | Receive signature |
| AnoSDKRegistInfoListener | 0x1D8C74 | 1936500 | Register info listener |

### Best Offsets (Early Initialization)

These are the first functions in the library, typically critical for initialization:

| Function Name | Offset | Decimal |
|---------------|--------|---------|
| sub_1C1350 | 0x1C1350 | 1839952 |
| sub_1C1360 | 0x1C1360 | 1839968 |
| sub_1C1368 | 0x1C1368 | 1839976 |
| sub_1C1384 | 0x1C1384 | 1840004 |
| sub_1C13A0 | 0x1C13A0 | 1840032 |

### Critical Memory Values

Most frequently referenced hex values (potential memory addresses or masks):

- `0xFFFFFFFF` (4294967295) - Referenced 1430 times - All bits set mask
- `0x80000000` (2147483648) - Referenced 389 times - Sign bit
- `0x10000000` (268435456) - Referenced 98 times - Memory base address
- `0x7FFFFFFF` (2147483647) - Referenced 58 times - Max positive integer
- `0x40000000` (1073741824) - Referenced 43 times - Memory base address

## Statistics

- **Total Functions**: 17,531
- **SDK Functions**: 18
- **Unique Hex Patterns**: 1,132

## Analysis Details

The library was analyzed using pattern matching to identify:

1. **Function offsets** - All 17,531 function definitions with their memory offsets
2. **SDK functions** - The 18 major AnoSDK API functions
3. **Hex patterns** - Frequently used memory addresses and constants

## Notes

- This is a decompiled binary, so function names starting with `sub_` are automatically generated
- AnoSDK functions retain their original names from the symbol table
- Offsets are base addresses and need to be adjusted based on where the library is loaded in memory
- This analysis is for educational and research purposes only

## License

This repository contains decompiled code for analysis purposes. All rights belong to the original authors.
