#!/usr/bin/env python3
"""
Telegram Bot for Advanced Ban Fix Offset Finder
Created by: @LEGEND_BL (PREMIUM USER)

Features:
- Upload .so files via Telegram
- Automatic analysis
- Receive results via Telegram
- Support for large files (1GB+)
"""

import os
import sys
import json
import asyncio
import tempfile
from datetime import datetime

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
except ImportError:
    print("Error: python-telegram-bot not installed")
    print("Install with: pip install python-telegram-bot")
    sys.exit(1)

# Import our advanced finder
from advanced_ban_fix_finder import AdvancedOffsetFinder

__author__ = "@LEGEND_BL"
__version__ = "1.0.0"

class TelegramBotHandler:
    """Telegram bot handler for offset analysis"""
    
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.active_analyses = {}
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_text = f"""
🤖 *Advanced Ban Fix Offset Finder Bot*

Created by {__author__}
Version {__version__}

*Features:*
✅ Multi-threaded analysis
✅ Support for large files (1GB+)
✅ Advanced pattern recognition (200+ offsets)
✅ Support for libanogs, UE4, and other .so files

*How to use:*
1. Send me a .so file or .c decompiled file
2. Wait for analysis to complete
3. Receive detailed results

*Commands:*
/start - Show this message
/help - Get help
/status - Check analysis status
/about - About this bot

Send a file to begin! 📤
        """
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = """
*Help - Advanced Ban Fix Offset Finder*

*Supported Files:*
• .so (Shared Library)
• .c (Decompiled C files)
• Any text file with function definitions

*File Size Limits:*
• Up to 1GB supported
• Larger files may take longer to process

*Analysis Time:*
• Small files (< 10MB): ~30 seconds
• Medium files (10-100MB): 1-5 minutes
• Large files (100MB-1GB): 5-30 minutes

*Output Format:*
• JSON file with all offsets
• Text report with categorized functions
• Statistics and confidence scores

*Tips:*
• Use descriptive filenames
• Compress large files if possible
• Be patient with large files

For support: Contact {__author__}
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """About command handler"""
        about_text = f"""
*About Advanced Ban Fix Offset Finder*

*Version:* {__version__}
*Created by:* {__author__}
*Status:* PREMIUM USER

*Features:*
• Advanced multi-threaded analysis
• Intelligent pattern recognition
• Support for multiple file formats
• Comprehensive categorization
• High-confidence scoring

*Categories Detected:*
• Critical Anti-Cheat Functions
• Ban Detection Mechanisms
• Signature Verification
• Encryption & Crypto
• Memory Protection
• License & Authentication
• Network Communication
• Data Collection
• File Integrity
• Process Detection
• Root Detection
• Emulator Detection
• Speed Hack Detection
• Overlay Detection
• Input Validation

*Technology:*
• Python 3.8+
• Multi-threading optimization
• Advanced regex patterns
• Machine learning-ready

© 2024 {__author__} - All Rights Reserved
        """
        
        await update.message.reply_text(about_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Status command handler"""
        user_id = update.effective_user.id
        
        if user_id in self.active_analyses:
            status_text = f"⏳ *Analysis in progress...*\n\n"
            status_text += f"File: {self.active_analyses[user_id]['filename']}\n"
            status_text += f"Started: {self.active_analyses[user_id]['start_time']}\n"
        else:
            status_text = "✅ *No active analysis*\n\nSend a file to start!"
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle uploaded documents"""
        user_id = update.effective_user.id
        document = update.message.document
        
        # Check file type
        if not (document.file_name.endswith('.so') or 
                document.file_name.endswith('.c') or
                document.mime_type == 'text/plain'):
            await update.message.reply_text(
                "❌ *Unsupported file type!*\n\n"
                "Please send:\n"
                "• .so (Shared Library)\n"
                "• .c (Decompiled C file)\n"
                "• .txt (Text file)",
                parse_mode='Markdown'
            )
            return
        
        # Check if analysis is already running
        if user_id in self.active_analyses:
            await update.message.reply_text(
                "⚠️ *Analysis already in progress!*\n\n"
                "Please wait for current analysis to complete.",
                parse_mode='Markdown'
            )
            return
        
        # Start analysis
        await update.message.reply_text(
            f"📥 *Downloading file...*\n\n"
            f"File: `{document.file_name}`\n"
            f"Size: {document.file_size / (1024*1024):.2f} MB",
            parse_mode='Markdown'
        )
        
        # Download file
        try:
            file = await context.bot.get_file(document.file_id)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(document.file_name)[1]) as tmp_file:
                await file.download_to_drive(tmp_file.name)
                temp_path = tmp_file.name
            
            # Register analysis
            self.active_analyses[user_id] = {
                'filename': document.file_name,
                'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'temp_path': temp_path
            }
            
            # Start analysis
            await self.analyze_file(update, context, temp_path, document.file_name)
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ *Error downloading file!*\n\n"
                f"Error: `{str(e)}`",
                parse_mode='Markdown'
            )
        finally:
            if user_id in self.active_analyses:
                del self.active_analyses[user_id]
    
    async def analyze_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                          filepath, filename):
        """Analyze the uploaded file"""
        user_id = update.effective_user.id
        
        # Send progress message
        progress_msg = await update.message.reply_text(
            "🔍 *Starting analysis...*\n\n"
            "This may take a few minutes...",
            parse_mode='Markdown'
        )
        
        try:
            # Progress callback
            last_update = [0]
            async def progress_callback(message, percent):
                # Update every 10%
                if percent - last_update[0] >= 10:
                    last_update[0] = percent
                    await progress_msg.edit_text(
                        f"🔍 *Analysis in progress...*\n\n"
                        f"Progress: {percent}%\n"
                        f"Status: {message}",
                        parse_mode='Markdown'
                    )
            
            # Run analysis
            finder = AdvancedOffsetFinder(filepath, 
                                         lambda msg, pct: asyncio.create_task(progress_callback(msg, pct)))
            report = await asyncio.to_thread(finder.analyze)
            
            # Save results
            json_path = filepath + '_result.json'
            txt_path = filepath + '_result.txt'
            
            with open(json_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            with open(txt_path, 'w') as f:
                f.write(self.format_text_report(report))
            
            # Send results
            await progress_msg.edit_text(
                "✅ *Analysis Complete!*\n\n"
                f"Total Functions: {report['metadata']['total_functions']:,}\n"
                f"Categories: {report['metadata']['categories_found']}\n\n"
                "Sending results...",
                parse_mode='Markdown'
            )
            
            # Send JSON
            await update.message.reply_document(
                document=open(json_path, 'rb'),
                filename=f"analysis_{filename}.json",
                caption="📊 *JSON Report*\nDetailed offset data in JSON format",
                parse_mode='Markdown'
            )
            
            # Send TXT
            await update.message.reply_document(
                document=open(txt_path, 'rb'),
                filename=f"analysis_{filename}.txt",
                caption="📄 *Text Report*\nHuman-readable analysis report",
                parse_mode='Markdown'
            )
            
            # Send summary
            summary = self.format_summary(report)
            await update.message.reply_text(summary, parse_mode='Markdown')
            
            # Cleanup
            os.unlink(filepath)
            os.unlink(json_path)
            os.unlink(txt_path)
            
        except Exception as e:
            await progress_msg.edit_text(
                f"❌ *Analysis Failed!*\n\n"
                f"Error: `{str(e)}`\n\n"
                f"Please try again or contact support.",
                parse_mode='Markdown'
            )
            
            # Cleanup
            if os.path.exists(filepath):
                os.unlink(filepath)
    
    def format_text_report(self, report):
        """Format report as text"""
        text = f"""
═══════════════════════════════════════════════════════════════
        Advanced Ban Fix Offset Analysis Report
                Created by {__author__}
═══════════════════════════════════════════════════════════════

Library: {report['metadata']['library']}
Analysis Date: {report['metadata']['analysis_date']}
Total Functions: {report['metadata']['total_functions']:,}
Categories Found: {report['metadata']['categories_found']}

═══════════════════════════════════════════════════════════════
STATISTICS BY CATEGORY
═══════════════════════════════════════════════════════════════

"""
        
        for category, count in sorted(report['statistics'].items(), 
                                     key=lambda x: x[1], reverse=True):
            text += f"{category.replace('_', ' ').title()}: {count} functions\n"
        
        text += "\n"
        text += "═" * 70 + "\n"
        text += "DETAILED OFFSETS BY CATEGORY\n"
        text += "═" * 70 + "\n\n"
        
        for category, data in sorted(report['categories'].items()):
            if data['offsets']:
                text += f"\n{category.upper().replace('_', ' ')}\n"
                text += "-" * 70 + "\n"
                
                for offset in data['offsets'][:30]:  # Top 30 per category
                    confidence = f"[{offset['confidence']:.1%}]"
                    text += f"{offset['offset']:>18} {confidence:>8} {offset['name']}\n"
                
                if len(data['offsets']) > 30:
                    text += f"... and {len(data['offsets']) - 30} more\n"
                text += "\n"
        
        return text
    
    def format_summary(self, report):
        """Format summary message"""
        summary = f"""
🎉 *Analysis Summary*

*File:* `{report['metadata']['library']}`
*Total Functions:* {report['metadata']['total_functions']:,}
*Categories:* {report['metadata']['categories_found']}

*Top Categories:*
"""
        
        for category, count in sorted(report['statistics'].items(), 
                                     key=lambda x: x[1], reverse=True)[:5]:
            summary += f"• {category.replace('_', ' ').title()}: {count}\n"
        
        summary += f"\n*Created by:* {__author__}\n"
        summary += "*Status:* PREMIUM USER ⭐"
        
        return summary
    
    def run(self):
        """Run the bot"""
        application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("about", self.about_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        
        print(f"🤖 Bot started! Created by {__author__}")
        print("Waiting for files...")
        
        application.run_polling()

def main():
    """Main entry point"""
    print("=" * 70)
    print("Telegram Bot for Advanced Ban Fix Offset Finder")
    print(f"Created by {__author__}")
    print("=" * 70)
    print()
    
    # Get bot token from environment or argument
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not bot_token and len(sys.argv) > 1:
        bot_token = sys.argv[1]
    
    if not bot_token:
        print("Error: Bot token not provided!")
        print()
        print("Usage:")
        print("  python3 telegram_bot.py <bot_token>")
        print("  or set TELEGRAM_BOT_TOKEN environment variable")
        print()
        print("Get your bot token from @BotFather on Telegram")
        sys.exit(1)
    
    bot = TelegramBotHandler(bot_token)
    bot.run()

if __name__ == "__main__":
    main()
