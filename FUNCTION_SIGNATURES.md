# AnoSDK Function Signatures - BGMI 4.1

Complete list of AnoSDK function signatures extracted from libanogs.so.

## Core SDK Functions

### Initialization Functions

#### AnoSDKInit
```c
__int64 __fastcall AnoSDKInit(__int64 result);
```
- **Offset**: 0x1D3814 (1914900)
- **Description**: Basic SDK initialization
- **Parameters**: 
  - `result`: Initialization parameter
- **Returns**: __int64 status code

#### AnoSDKInitEx
```c
__int64 __fastcall AnoSDKInitEx(__int64 a1, const char *a2);
```
- **Offset**: 0x1D3B40 (1915712)
- **Description**: Extended SDK initialization with configuration
- **Parameters**:
  - `a1`: Configuration parameter
  - `a2`: Configuration string
- **Returns**: __int64 status code

### User Information Functions

#### AnoSDKSetUserInfo
```c
_QWORD *__fastcall AnoSDKSetUserInfo(unsigned int a1, unsigned __int8 *a2);
```
- **Offset**: 0x1D4050 (estimated)
- **Description**: Set user information
- **Parameters**:
  - `a1`: User ID
  - `a2`: User data buffer
- **Returns**: Pointer to result

#### AnoSDKSetUserInfoWithLicense
```c
_QWORD *__fastcall AnoSDKSetUserInfoWithLicense(unsigned int a1, unsigned __int8 *a2, _BYTE *a3);
```
- **Offset**: 0x1D4680 (estimated)
- **Description**: Set user information with license data
- **Parameters**:
  - `a1`: User ID
  - `a2`: User data buffer
  - `a3`: License data
- **Returns**: Pointer to result

### Lifecycle Functions

#### AnoSDKOnPause
```c
void AnoSDKOnPause();
```
- **Offset**: 0x1D4C0C (1920012)
- **Description**: Called when application is paused
- **Parameters**: None
- **Returns**: void

#### AnoSDKOnResume
```c
void AnoSDKOnResume();
```
- **Offset**: 0x1D5030 (1921072)
- **Description**: Called when application is resumed
- **Parameters**: None
- **Returns**: void

### Data Reporting Functions

#### AnoSDKGetReportData
```c
__int64 AnoSDKGetReportData();
```
- **Offset**: 0x1D551C (1922332)
- **Description**: Get report data (version 1)
- **Parameters**: None
- **Returns**: __int64 pointer to report data

#### AnoSDKDelReportData
```c
_QWORD *__fastcall AnoSDKDelReportData(__int64 a1);
```
- **Offset**: 0x1D5CD0 (estimated)
- **Description**: Delete/free report data
- **Parameters**:
  - `a1`: Report data pointer
- **Returns**: Pointer result

#### AnoSDKGetReportData2
```c
__int64 AnoSDKGetReportData2();
```
- **Offset**: 0x1D78CC (1931468)
- **Description**: Get report data (version 2)
- **Parameters**: None
- **Returns**: __int64 pointer to report data

#### AnoSDKGetReportData3
```c
__int64 __fastcall AnoSDKGetReportData3(
    __int64 a1, __int64 a2, __int64 a3, __int64 a4,
    __int64 a5, __int64 a6, __int64 a7, __int64 a8, __int64 a9);
```
- **Offset**: 0x1D7938 (1931576)
- **Description**: Get report data (version 3) with extended parameters
- **Parameters**: 9 __int64 parameters
- **Returns**: __int64 pointer to report data

#### AnoSDKDelReportData3
```c
void __fastcall AnoSDKDelReportData3(__int64 a1);
```
- **Offset**: 0x1D79A4 (1931684)
- **Description**: Delete/free report data v3
- **Parameters**:
  - `a1`: Report data pointer
- **Returns**: void

#### AnoSDKGetReportData4
```c
__int64 __fastcall AnoSDKGetReportData4(
    unsigned int a1, __int64 a2, __int64 a3, __int64 a4,
    __int64 a5, __int64 a6, __int64 a7, __int64 a8);
```
- **Offset**: 0x1D7FC4 (1933252)
- **Description**: Get report data (version 4)
- **Parameters**: 1 unsigned int + 7 __int64 parameters
- **Returns**: __int64 pointer to report data

#### AnoSDKDelReportData4
```c
__int64 __fastcall AnoSDKDelReportData4(__int64 result);
```
- **Offset**: 0x1D82CC (1934028)
- **Description**: Delete/free report data v4
- **Parameters**:
  - `result`: Report data pointer
- **Returns**: __int64 status

### Communication Functions

#### AnoSDKOnRecvData
```c
void __fastcall AnoSDKOnRecvData(__int64 a1, int a2);
```
- **Offset**: 0x1D624C (1925708)
- **Description**: Handle received data
- **Parameters**:
  - `a1`: Data pointer
  - `a2`: Data size/type
- **Returns**: void

#### AnoSDKOnRecvSignature
```c
__int64 __fastcall AnoSDKOnRecvSignature(_BYTE *a1, __int64 a2, unsigned int a3, int a4);
```
- **Offset**: 0x1D88EC (1935596)
- **Description**: Handle received signature data
- **Parameters**:
  - `a1`: Signature data buffer
  - `a2`: Buffer pointer/size
  - `a3`: Signature length
  - `a4`: Signature type/flags
- **Returns**: __int64 status code

### Control Functions

#### AnoSDKIoctlOld
```c
__int64 AnoSDKIoctlOld();
```
- **Offset**: 0x1D6598 (1926552)
- **Description**: Old I/O control interface (deprecated)
- **Parameters**: None
- **Returns**: __int64 result

#### AnoSDKIoctl
```c
_WORD *__fastcall AnoSDKIoctl(int a1, __int64 a2);
```
- **Offset**: 0x1D6730 (1926960)
- **Description**: I/O control interface for SDK operations
- **Parameters**:
  - `a1`: Control command code
  - `a2`: Control data/parameter
- **Returns**: Pointer to result

### Resource Management Functions

#### AnoSDKFree
```c
void __fastcall AnoSDKFree(__int64 a1);
```
- **Offset**: 0x1D7398 (1930136)
- **Description**: Free SDK allocated resources
- **Parameters**:
  - `a1`: Resource pointer to free
- **Returns**: void

### Listener Functions

#### AnoSDKRegistInfoListener
```c
__int64 __fastcall AnoSDKRegistInfoListener(__int64 a1);
```
- **Offset**: 0x1D8C74 (1936500)
- **Description**: Register information listener callback
- **Parameters**:
  - `a1`: Listener callback pointer
- **Returns**: __int64 registration status

### Export Functions

#### AnoSDKForExport
```c
void AnoSDKForExport();
```
- **Offset**: 0x1D9024 (1937444)
- **Description**: Export function for external use
- **Parameters**: None
- **Returns**: void

## Usage Notes

1. All offsets are base addresses relative to the library load address
2. Functions marked `__fastcall` use ARM64 calling convention
3. `__int64` is typically a 64-bit integer on ARM64
4. `_QWORD` is a pointer/quad-word type
5. `_WORD` is a 16-bit word type
6. `_BYTE` is a byte/8-bit type

## Calling Convention

ARM64 (AArch64) calling convention:
- First 8 integer arguments in X0-X7
- First 8 floating-point arguments in V0-V7
- Additional arguments on stack
- Return value in X0 (or V0 for floating-point)

## Integration Example

```c
// Load library
void *handle = dlopen("libanogs.so", RTLD_NOW);

// Get function pointer
typedef __int64 (*AnoSDKInit_t)(__int64);
AnoSDKInit_t AnoSDKInit = (AnoSDKInit_t)dlsym(handle, "AnoSDKInit");

// Call function
__int64 result = AnoSDKInit(0);

// Cleanup
dlclose(handle);
```
