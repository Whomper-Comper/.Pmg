import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import struct

def open_pmg(file_path):
    with open(file_path, 'rb') as f:
        # Read the first 3 bytes to check the magic header
        magic = f.read(3)
        if magic != b'PMG':
            raise ValueError("Not a valid PMG file!")
        # Read the width and height (each 4 bytes, big-endian)
        width, height = struct.unpack('>II', f.read(8))
        # Read the remaining pixel data
        pixel_data = f.read()
    
    # Reconstruct the image from the raw RGBA pixel data
    img = Image.frombytes("RGBA", (width, height), pixel_data)
    return img

def select_and_open():
    # Open a file dialog to select a PMG file
    file_path = filedialog.askopenfilename(
        title="Select PMG file",
        filetypes=[("PMG Files", "*.pmg")])
    if not file_path:
        return  # Exit if no file is selected
    
    try:
        img = open_pmg(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open PMG file: {e}")
        return

    # Create a new window to display the image
    display_window = tk.Toplevel()
    display_window.title("Opened PMG Image")
    
    # Convert the PIL image to a format Tkinter can use
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(display_window, image=tk_img)
    label.image = tk_img  # Keep a reference to avoid garbage collection
    label.pack()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("PMG Viewer")
    root.geometry("300x100")
    
    # Button to select and open a PMG file
    open_button = tk.Button(root, text="Open PMG File", command=select_and_open)
    open_button.pack(pady=20)
    
    root.mainloop()
