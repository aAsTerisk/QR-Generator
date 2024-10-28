#!/usr/bin/env python3

import curses
import qrcode
import os
from PIL import Image
from termcolor import colored

def curses_input(stdscr):
    """Use curses to handle multiline, editable input in the terminal."""
    stdscr.clear()
    stdscr.addstr("Enter the text for the QR Code (press Ctrl+G when done):\n")
    text_lines = []
    current_line = ""
    cursor_x, cursor_y = 0, 1

    while True:
        stdscr.move(cursor_y, cursor_x)
        key = stdscr.getch()

        if key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
            if cursor_x > 0:
                current_line = current_line[:cursor_x - 1] + current_line[cursor_x:]
                cursor_x -= 1
                stdscr.addstr(cursor_y, 0, current_line + " ")
                stdscr.move(cursor_y, cursor_x)
            elif cursor_y > 1:
                cursor_y -= 1
                current_line = text_lines[cursor_y - 1]
                text_lines = text_lines[:cursor_y]
                cursor_x = len(current_line)
        elif key in (curses.KEY_ENTER, 10, 13):  # Handle Enter for new line
            text_lines.append(current_line)
            current_line = ""
            cursor_y += 1
            cursor_x = 0
        elif key == curses.KEY_LEFT and cursor_x > 0:  # Left arrow key
            cursor_x -= 1
        elif key == curses.KEY_RIGHT and cursor_x < len(current_line):  # Right arrow key
            cursor_x += 1
        elif key == 7:  # Ctrl+G to finish input
            text_lines.append(current_line)
            break
        else:  # Regular character input
            current_line = current_line[:cursor_x] + chr(key) + current_line[cursor_x:]
            cursor_x += 1
            stdscr.addstr(cursor_y, 0, current_line)
            stdscr.move(cursor_y, cursor_x)

    return "\n".join(text_lines)


def create_qr_code(text, file_path, fill_color="black", back_color="white"):
    """Generate and save a QR code with specified colors."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(file_path)
    print(colored(f"QR Code saved as '{file_path}'", 'green'))

def display_qr_in_terminal(text):
    """Display a simple QR code in terminal using ASCII characters."""
    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    
    for row in qr.get_matrix():
        print("".join(['██' if col else '  ' for col in row]))

def main():
    print(colored("Welcome to the Advanced QR Code Generator!", 'cyan', attrs=['bold']))

    # Multiline editable text input
    print(colored("Press Ctrl+G to finish your input.", 'yellow'))
    text = curses.wrapper(curses_input).strip()
    
    if not text:
        print(colored("Error: Text cannot be empty.", 'red'))
        return

    # Display QR in terminal
    display_qr = input(colored("Do you want to display the QR Code in the terminal? (y/n): ", 'yellow')).strip().lower()
    if display_qr == 'y':
        print(colored("\nQR Code Display:", 'cyan', attrs=['bold']))
        display_qr_in_terminal(text)
    
    # Save QR as image
    save_image = input(colored("\nDo you want to save the QR Code as an image file? (y/n): ", 'yellow')).strip().lower()
    if save_image == 'y':
        file_format = input(colored("Choose file format (png/jpg): ", 'yellow')).strip().lower()
        if file_format not in ["png", "jpg"]:
            print(colored("Error: Invalid file format. Choose 'png' or 'jpg'.", 'red'))
            return

        # Get colors
        fill_color = input(colored("Enter QR Code color (default: black): ", 'yellow')).strip() or "black"
        back_color = input(colored("Enter background color (default: white): ", 'yellow')).strip() or "white"
        
        # File name
        output_file = input(colored("Enter output file name (without extension): ", 'yellow')).strip()
        output_file = f"{output_file}.{file_format}"
        
        # Prevent overwriting
        if os.path.exists(output_file):
            overwrite = input(colored(f"{output_file} already exists. Overwrite? (y/n): ", 'yellow')).strip().lower()
            if overwrite != 'y':
                print(colored("Operation cancelled.", 'red'))
                return

        # Create and save QR code
        create_qr_code(text, output_file, fill_color, back_color)

if __name__ == "__main__":
    main()
