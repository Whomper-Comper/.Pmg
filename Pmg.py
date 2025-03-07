import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import struct
import os

def convert_png_to_pmg(input_file, output_file):
    # Open the PNG image and ensure it's in RGBA mode
    with Image.open(input_file) as img:
        img = img.convert("RGBA")
        width, height = img.size
        pixel_data = img.tobytes()
    
    # Write out the custom .pmg file
    with open(output_file, "wb") as f:
        # Write a three-byte magic identifier "PMG"
        f.write(b'PMG')
        # Write width and height as 4-byte big-endian unsigned integers
        f.write(struct.pack('>II', width, height))
        # Write the raw pixel data (RGBA)
        f.write(pixel_data)

def select_file_and_convert():
    # Open a file dialog to select a PNG file
    input_file = filedialog.askopenfilename(
        title="Select PNG file",
        filetypes=[("PNG Images", "*.png")])
    if not input_file:
        return  # Exit if no file is selected

    # Open a save file dialog to choose the output .pmg file
    output_file = filedialog.asksaveasfilename(
        title="Save PMG file as",
        defaultextension=".pmg",
        filetypes=[("PMG Files", "*.pmg")])
    if not output_file:
        return  # Exit if no destination is chosen

    try:
        convert_png_to_pmg(input_file, output_file)
        messagebox.showinfo("Success", f"Converted {os.path.basename(input_file)} to {os.path.basename(output_file)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == '__main__':
    # Set up the main Tkinter window
    root = tk.Tk()
    root.title("PNG to PMG Converter")
    root.geometry("300x100")
    
    # Create and place a button to trigger the file selection and conversion
    convert_button = tk.Button(root, text="Select PNG and Convert", command=select_file_and_convert)
    convert_button.pack(pady=20)
    
    # Run the Tkinter event loop
    root.mainloop()
