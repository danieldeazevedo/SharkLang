#!/usr/bin/env python3
"""
Shark Language CLI
Usage: shark <command> [args]
"""

import sys
import os

# Import the interpreter
from main import run_shark_file, run_shark

def print_help():
    """Print help message"""
    help_text = """
🦈 Shark Language - CLI Tool

Usage:
    shark init <filename>     Run a Shark file
    shark run <filename>      Run a Shark file (alias for init)
    shark repl                Start interactive REPL (coming soon)
    shark help                Show this help message
    shark version             Show version information

Examples:
    shark init index.shark    # Run index.shark
    shark run program.shark   # Run program.shark

If no command is provided and index.shark exists, it will be executed automatically.
"""
    print(help_text)

def print_version():
    """Print version information"""
    version_text = """
🦈 Shark Language v1.0.0
A modern interpreted language for mathematics and statistics

Created with ❤️ for data analysis and scientific computing
"""
    print(version_text)

def start_repl():
    """Start interactive REPL"""
    print("🦈 Shark REPL v1.0.0")
    print("Type 'exit' to quit\n")

    code_buffer = ""

    while True:
        try:
            if code_buffer:
                line = input("... ")
            else:
                line = input(">>> ")

            if line.strip() == "exit":
                print("Goodbye! 🦈")
                break

            code_buffer += line + "\n"

            # Check if we have a complete statement
            if line.strip().endswith(";") or line.strip().endswith("}") or line.strip() == "":
                if code_buffer.strip():
                    try:
                        run_shark(code_buffer)
                    except Exception as e:
                        print(f"Error: {e}")
                    code_buffer = ""
                else:
                    code_buffer = ""
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            code_buffer = ""
        except EOFError:
            print("\nGoodbye! 🦈")
            break

def main():
    """Main CLI entry point"""
    if len(sys.argv) == 1:
        # No arguments - try to run index.shark
        if os.path.exists('index.shark'):
            run_shark_file('index.shark')
        else:
            print("No index.shark file found in current directory.")
            print("Use 'shark help' for usage information.")
            sys.exit(1)

    command = sys.argv[1].lower()

    if command in ['init', 'run']:
        if len(sys.argv) < 3:
            print("Error: Filename required")
            print("Usage: shark init <filename>")
            sys.exit(1)

        filename = sys.argv[2]
        run_shark_file(filename)

    elif command == 'repl':
        start_repl()

    elif command in ['help', '--help', '-h']:
        print_help()

    elif command in ['version', '--version', '-v']:
        print_version()

    else:
        print(f"Unknown command: {command}")
        print("Use 'shark help' for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    main()