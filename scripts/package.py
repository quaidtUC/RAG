#!/usr/bin/env python3
"""Helper script for packaging the application with PyInstaller."""
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Build a standalone executable using PyInstaller")
    parser.add_argument("entry", help="Path to the application's entry-point script")
    parser.add_argument("--windowed", "-w", action="store_true", help="Build without an attached console window")
    args = parser.parse_args()

    cmd = [sys.executable, "-m", "PyInstaller", "--onefile"]
    if args.windowed:
        cmd.append("--windowed")
    cmd.append(str(Path(args.entry)))

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
