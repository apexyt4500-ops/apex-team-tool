#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
APEX TEAM - Professional Binary URL Patcher
Reverse Engineering & Game Modding Tool
"""

import os
import sys
import time

# =============================================================================
# COLOR PALETTE (Dark Hacker Theme - max 4 colors)
# =============================================================================
C_RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Primary: Electric Blue
BLUE = "\033[38;5;39m"      # Neon Blue
# Secondary: White / Light Gray
WHITE = "\033[97m"
GRAY = "\033[38;5;250m"     # Light Gray
# Success: Green
GREEN = "\033[38;5;46m"
# Error: Red
RED = "\033[38;5;196m"

# =============================================================================
# ASCII ART BANNER (APEX TEAM full name - stacked: APEX above TEAM)
# =============================================================================
BANNER_ART = f"""
{BLUE}╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  {WHITE}   █████╗  ██████╗ ███████╗██╗  ██╗                        {BLUE}   ║
║  {WHITE}   ██╔══██╗██╔════╝ ██╔════╝╚██╗██╔╝                        {BLUE}   ║
║  {WHITE}   ███████║██║  ███╗█████╗   ╚███╔╝                         {BLUE}   ║
║  {WHITE}   ██╔══██║██║   ██║██╔══╝   ██╔██╗                         {BLUE}   ║
║  {WHITE}   ██║  ██║╚██████╔╝███████╗██╔╝ ██╗                        {BLUE}   ║
║  {WHITE}   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                        {BLUE}   ║
║                                                                ║
║  {GRAY}   ████████╗███████╗ █████╗ ███╗   ███╗                    {BLUE}   ║
║  {GRAY}   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║                    {BLUE}   ║
║  {GRAY}      ██║   █████╗  ███████║██╔████╔██║                    {BLUE}   ║
║  {GRAY}      ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║                    {BLUE}   ║
║  {GRAY}      ██║   ███████╗██║  ██║██║ ╚═╝ ██║                    {BLUE}   ║
║  {GRAY}      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝                    {BLUE}   ║
║                                                                ║
║                  {WHITE}APEX TEAM{BLUE} - {GRAY}FUTURISTIC BINARY PATCHER{BLUE}              ║
╚════════════════════════════════════════════════════════════════╝{C_RESET}
"""

# =============================================================================
# UI HELPER FUNCTIONS
# =============================================================================

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display professional ASCII banner with APEX TEAM name."""
    clear_screen()
    print(BANNER_ART)
    time.sleep(0.5)

def boot_screen():
    """Hacker-style initialization sequence with full APEX TEAM name."""
    print(f"\n{BLUE}Initializing {WHITE}APEX TEAM{BLUE} Core...{C_RESET}")
    time.sleep(0.3)

    modules = [
        ("Binary Scanner", "OK"),
        ("Patch Engine", "OK"),
        ("XOR Analyzer", "OK"),
        ("URL Scanner", "OK")
    ]

    for name, status in modules:
        print(f"  {GRAY}Loading {name} {BLUE}..........{GREEN} {status}{C_RESET}")
        time.sleep(0.2)

    print(f"\n{WHITE}{BOLD}APEX TEAM Engine Ready.{C_RESET}\n")
    time.sleep(0.5)

def print_step(step_num, title):
    """Print a formatted step header."""
    print(f"\n{BLUE}{'─' * 60}{C_RESET}")
    print(f"{BLUE}[ STEP {step_num} ]{C_RESET} {WHITE}{title}{C_RESET}")
    print(f"{BLUE}{'─' * 60}{C_RESET}")

def print_info(message):
    """Print informational message."""
    print(f"  {BLUE}[*]{C_RESET} {GRAY}{message}{C_RESET}")

def print_success(message):
    """Print success message."""
    print(f"  {GREEN}[+]{C_RESET} {WHITE}{message}{C_RESET}")

def print_error(message):
    """Print error message."""
    print(f"  {RED}[-]{C_RESET} {WHITE}{message}{C_RESET}")

def print_input_prompt(message):
    """Print input prompt."""
    print(f"  {BLUE}[?]{C_RESET} {WHITE}{message}{C_RESET} ", end='', flush=True)

def safe_input(prompt):
    """
    Safely get input from user, handling EOFError and KeyboardInterrupt.
    Returns the stripped input string, or exits on error.
    """
    print_input_prompt(prompt)
    try:
        return input().strip()
    except EOFError:
        print_error("Input stream closed. Exiting.")
        sys.exit(1)
    except KeyboardInterrupt:
        print_error("\nInterrupted by user.")
        sys.exit(1)

def print_url_item(index, offset, raw_bytes, url):
    """Display a single URL entry with details."""
    print(f"\n  {BLUE}[#{index}]{C_RESET}")
    print(f"    {GRAY}Offset :{C_RESET} {WHITE}0x{offset:08x}{C_RESET}")
    print(f"    {GRAY}Length :{C_RESET} {WHITE}{len(raw_bytes)} bytes{C_RESET}")
    print(f"    {GRAY}URL    :{C_RESET} {WHITE}{url}{C_RESET}")

def progress_bar(duration, message="Processing"):
    """Simple progress bar (no gradients)."""
    width = 40
    print(f"  {GRAY}{message}...{C_RESET}")
    for i in range(width + 1):
        percent = i * 100 // width
        bar = "█" * i + "░" * (width - i)
        print(f"\r  {BLUE}[{bar}]{C_RESET} {WHITE}{percent:3d}%{C_RESET}", end='', flush=True)
        time.sleep(duration / width)
    print()

# =============================================================================
# CORE LOGIC FUNCTIONS
# =============================================================================

def xor_data(data, key):
    """Apply XOR to data using the given key (0 = no change)."""
    if key == 0:
        return data
    return bytes([b ^ key for b in data])

def find_all_urls(data):
    """
    Scan binary data for http:// or https:// URLs.
    Returns list of tuples: (offset, raw_bytes, url_string)
    """
    urls = []
    patterns = [b'http://', b'https://']
    for pattern in patterns:
        start = 0
        while True:
            pos = data.find(pattern, start)
            if pos == -1:
                break
            # Extend until non-printable character (ASCII 32-126)
            end = pos
            while end < len(data) and 32 <= data[end] <= 126:
                end += 1
            raw = data[pos:end]
            try:
                url_str = raw.decode('utf-8')
            except UnicodeDecodeError:
                url_str = str(raw)  # fallback
            urls.append((pos, raw, url_str))
            start = end
    return urls

def patch_file(original_data, offset, old_raw, new_url, xor_key):
    """
    Create patched binary with the new URL (padded with nulls).
    Returns patched bytes.
    """
    new_bytes = new_url.encode('utf-8')
    old_len = len(old_raw)
    new_len = len(new_bytes)

    if new_len > old_len:
        raise ValueError(f"New URL longer than old ({new_len} > {old_len})")

    # Pad with null bytes
    padded_new = new_bytes + b'\x00' * (old_len - new_len)

    # Apply XOR if needed
    if xor_key != 0:
        padded_new = xor_data(padded_new, xor_key)

    # Patch
    modified = bytearray(original_data)
    modified[offset:offset+old_len] = padded_new
    return bytes(modified)

# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print_banner()
    boot_screen()

    step = 1

    # -------------------------------------------------------------------------
    # STEP 1: Target File
    # -------------------------------------------------------------------------
    print_step(step, "Target File")
    step += 1

    while True:
        file_path = safe_input("Enter file path (e.g., /sdcard/lib.so):")
        if os.path.isfile(file_path):
            break
        print_error("File not found. Please check the path.")

    print_success(f"File loaded: {file_path}")

    # -------------------------------------------------------------------------
    # STEP 2: XOR Analysis
    # -------------------------------------------------------------------------
    print_step(step, "XOR Analysis")
    step += 1

    xor_input = safe_input("Enter XOR key (decimal, 0 for none):")
    try:
        xor_key = int(xor_input, 0)
    except ValueError:
        xor_key = 0
    print_info(f"XOR key set to {xor_key}")

    # Read file
    try:
        with open(file_path, 'rb') as f:
            original_data = f.read()
        print_success("Binary data read successfully.")
    except Exception as e:
        print_error(f"Failed to read file: {e}")
        sys.exit(1)

    # Decrypt if needed
    if xor_key != 0:
        print_info("Applying XOR decryption for scanning...")
        search_data = xor_data(original_data, xor_key)
    else:
        search_data = original_data

    # -------------------------------------------------------------------------
    # STEP 3: URL Scan
    # -------------------------------------------------------------------------
    print_step(step, "URL Scan")
    step += 1

    print_info("Scanning for http:// and https:// URLs...")
    urls = find_all_urls(search_data)

    if not urls:
        print_error("No URLs found in the file.")
        sys.exit(1)

    print_success(f"Found {len(urls)} URL(s):")
    for i, (offset, raw, url_str) in enumerate(urls):
        print_url_item(i + 1, offset, raw, url_str)

    # -------------------------------------------------------------------------
    # STEP 4: Replace URL
    # -------------------------------------------------------------------------
    print_step(step, "Replace URL")
    step += 1

    # Choose URL
    while True:
        choice = safe_input("Enter URL number to replace (or 0 to quit):")
        if choice == '0':
            print_info("Operation cancelled.")
            sys.exit(0)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(urls):
                break
            else:
                print_error("Invalid number. Try again.")
        except ValueError:
            print_error("Please enter a valid number.")

    offset, old_raw, old_url = urls[idx]
    print_info(f"Selected URL: {old_url}")

    # New URL
    new_url = safe_input("Enter new URL:")
    if not new_url:
        print_error("No URL provided.")
        sys.exit(1)

    # Validate length
    if len(new_url.encode('utf-8')) > len(old_raw):
        print_error("New URL is too long for the allocated space.")
        sys.exit(1)

    # Create backup
    backup_path = file_path + ".bak"
    try:
        with open(backup_path, 'wb') as bf:
            bf.write(original_data)
        print_success(f"Backup created: {backup_path}")
    except Exception as e:
        print_error(f"Backup failed: {e}")
        sys.exit(1)

    # Patch
    try:
        patched_data = patch_file(original_data, offset, old_raw, new_url, xor_key)
    except ValueError as e:
        print_error(str(e))
        sys.exit(1)

    # Write with progress bar
    progress_bar(1.2, "Writing patch")

    try:
        with open(file_path, 'wb') as f:
            f.write(patched_data)
        print_success("Patch applied successfully.")
    except Exception as e:
        print_error(f"Write failed: {e}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # STEP 5: Verification
    # -------------------------------------------------------------------------
    print_step(step, "Verification")
    step += 1

    # Re-scan modified file
    if xor_key != 0:
        verify_data = xor_data(patched_data, xor_key)
    else:
        verify_data = patched_data

    new_urls = find_all_urls(verify_data)
    print_info("URLs after patching:")
    for i, (_, _, url_str) in enumerate(new_urls):
        if url_str == new_url:
            print(f"  {GREEN}[#{i+1}] {url_str} ✓{C_RESET}")
        else:
            print(f"  {WHITE}[#{i+1}] {url_str}{C_RESET}")

    # Final success message
    print(f"\n{BLUE}{'─' * 60}{C_RESET}")
    print_success("Operation completed. Thank you for using APEX TEAM.")
    print(f"{BLUE}{'─' * 60}{C_RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
        