# Quick Start Guide - Advanced Ban Fix Offset Finder

**Created by: @LEGEND_BL (PREMIUM USER)**

## 🚀 Quick Start

### Option 1: Command Line (Fastest)

```bash
# Run analysis on your .so file
python3 advanced_ban_fix_finder.py your_file.so

# Or on decompiled C file
python3 advanced_ban_fix_finder.py libanogs.so.c
```

**Output:**
- `advanced_ban_fix_offsets.json` - Complete analysis (2.6MB+)

### Option 2: GUI Mode

```bash
# Start GUI (if tkinter is installed)
python3 advanced_ban_fix_finder.py

# Then:
# 1. Click "Browse .so File"
# 2. Select your file
# 3. Click "Start Analysis"
# 4. Wait for results
# 5. Export as needed
```

### Option 3: Telegram Bot

```bash
# Install dependencies
pip install python-telegram-bot

# Start bot with your token
python3 telegram_bot.py YOUR_BOT_TOKEN

# Then in Telegram:
# 1. Send /start to your bot
# 2. Upload .so file
# 3. Receive results automatically
```

## 📊 What You Get

### 200+ Offsets Across 15 Categories:

1. ✅ **Critical Anti-Cheat** - AnoSDK and security functions
2. 🚫 **Ban Detection** - Ban logic and enforcement
3. 🔐 **Signature Verification** - Crypto validation
4. 🔒 **Encryption & Crypto** - Security functions
5. 🛡️ **Memory Protection** - Memory guards
6. 📜 **License & Auth** - Authentication checks
7. 🌐 **Network Communication** - Server comms
8. 📊 **Data Collection** - Telemetry functions
9. 📁 **File Integrity** - File checks
10. 🔍 **Process Detection** - Process monitoring
11. 🔓 **Root Detection** - Root/jailbreak checks
12. 💻 **Emulator Detection** - Virtual environment
13. ⚡ **Speed Hack Detection** - Time checks
14. 🎨 **Overlay Detection** - UI overlays
15. ✏️ **Input Validation** - Input checks

### Output Includes:

- **Function Name** - Original or decompiled name
- **Offset Address** - Hexadecimal and decimal
- **Category** - What the function does
- **Confidence Score** - How sure we are (0-100%)
- **Statistics** - Complete analysis metrics

## 💡 Example Output

```json
{
  "metadata": {
    "total_functions": 17532,
    "categories_found": 15,
    "author": "@LEGEND_BL"
  },
  "categories": {
    "critical_anti_cheat": {
      "count": 18,
      "offsets": [
        {
          "name": "AnoSDKInit",
          "offset": "0x1D3814",
          "decimal": 1914900,
          "confidence": 0.95
        }
      ]
    }
  }
}
```

## ⚙️ System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum, 8GB+ recommended
- **CPU:** Multi-core recommended
- **Storage:** 100MB free space

## 🔥 Key Features

- ✅ **Multi-threaded** - Uses all CPU cores
- ✅ **Large Files** - Handles 1GB+ files
- ✅ **Smart Detection** - AI-like pattern matching
- ✅ **Three Interfaces** - CLI, GUI, Telegram
- ✅ **Fast Analysis** - 10MB in 30 seconds
- ✅ **Detailed Reports** - JSON and TXT formats

## 📝 Need Help?

1. **Read the Guide:** `ADVANCED_GUIDE.md`
2. **Check Examples:** See example files
3. **Contact:** @LEGEND_BL on Telegram
4. **Issues:** Report bugs on GitHub

## 🎯 Pro Tips

1. **Use CLI for large files** - Faster and more reliable
2. **Adjust thread count** - More threads = faster (up to CPU limit)
3. **Check confidence scores** - Higher = more reliable
4. **Export to JSON** - Easier to process programmatically
5. **Use Telegram bot** - Perfect for remote analysis

## 🏆 Advanced Usage

### Batch Process Multiple Files

```bash
for file in *.so; do
    echo "Analyzing $file..."
    python3 advanced_ban_fix_finder.py "$file"
    mv advanced_ban_fix_offsets.json "${file}_analysis.json"
done
```

### Filter by Category

```python
import json

# Load results
with open('advanced_ban_fix_offsets.json') as f:
    data = json.load(f)

# Get only critical anti-cheat functions
critical = data['categories']['critical_anti_cheat']['offsets']
for func in critical:
    print(f"{func['offset']} - {func['name']}")
```

### Compare Two Libraries

```bash
# Analyze both
python3 advanced_ban_fix_finder.py lib_v1.so
mv advanced_ban_fix_offsets.json v1_analysis.json

python3 advanced_ban_fix_finder.py lib_v2.so
mv advanced_ban_fix_offsets.json v2_analysis.json

# Compare manually or write a script
```

## ⚠️ Important Notes

1. **Educational Use Only** - For learning and research
2. **No Warranty** - Use at your own risk
3. **Keep Updated** - Check for new versions
4. **Credit Author** - Always credit @LEGEND_BL
5. **Report Issues** - Help improve the tool

## 📞 Support

**Premium Support Available:**
- Custom features
- Priority bug fixes
- Commercial licensing
- Private consultation

**Contact:** @LEGEND_BL on Telegram

---

**Made with ❤️ by @LEGEND_BL - PREMIUM USER**

*For the complete guide, see `ADVANCED_GUIDE.md`*
