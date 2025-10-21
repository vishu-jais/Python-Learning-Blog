import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import qrcode
import cv2
import os
from PIL import Image, ImageTk

def choose_fill_color():
    color_code = colorchooser.askcolor(title="Choose Fill Color")[1]
    if color_code:
        fill_color_entry.delete(0, tk.END)
        fill_color_entry.insert(0, color_code)

def choose_bg_color():
    color_code = colorchooser.askcolor(title="Choose Background Color")[1]
    if color_code:
        bg_color_entry.delete(0, tk.END)
        bg_color_entry.insert(0, color_code)

def generate_qr():
    data = data_entry.get().strip()
    filename = filename_entry.get().strip()
    fill_color = fill_color_entry.get().strip() or "black"
    back_color = bg_color_entry.get().strip() or "white"
    
    if not data:
        messagebox.showwarning("Input Error", "Please enter text or URL to generate QR code.")
        return
    
    if not filename:
        filename = "default_qr.png"
    if not filename.endswith(".png"):
        filename += ".png"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(filename)
    
    messagebox.showinfo("Success", f"QR Code saved as {filename}")
    display_qr_image(filename)
    
    data_entry.delete(0, tk.END)
    filename_entry.delete(0, tk.END)
    fill_color_entry.delete(0, tk.END)
    bg_color_entry.delete(0, tk.END)

def decode_qr():
    filename = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
    if not filename:
        return
    
    if not os.path.exists(filename):
        messagebox.showerror("File Error", "File not found. Please select a valid file.")
        return
    
    try:
        img = cv2.imread(filename)
        if img is None:
            raise ValueError("Could not read image. Please select a valid PNG file.")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(gray)
        
        if data:
            messagebox.showinfo("Decoded Data", f"QR Code contains:\n{data}")
            root.clipboard_clear()
            root.clipboard_append(data)
            root.update_idletasks()
            messagebox.showinfo("Clipboard", "Decoded data copied to clipboard!")
        else:
            messagebox.showinfo("Result", "No QR code found in the image.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode QR code:\n{str(e)}")

def display_qr_image(filename):
    img = Image.open(filename)
    img = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    qr_image_label.config(image=img_tk)
    qr_image_label.image = img_tk

root = tk.Tk()
root.title("QR Code Generator & Decoder")
root.geometry("500x600")
root.resizable(False, False)

tk.Label(root, text="Enter Text/URL:", font=("Helvetica", 12)).pack(pady=5)
data_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
data_entry.pack()

tk.Label(root, text="Enter Filename (optional):", font=("Helvetica", 12)).pack(pady=5)
filename_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
filename_entry.pack()

tk.Label(root, text="Fill Color (default black):", font=("Helvetica", 12)).pack(pady=5)
fill_color_frame = tk.Frame(root)
fill_color_frame.pack()
fill_color_entry = tk.Entry(fill_color_frame, font=("Helvetica", 12), width=30)
fill_color_entry.pack(side=tk.LEFT)
tk.Button(fill_color_frame, text="Choose Color", command=choose_fill_color).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Background Color (default white):", font=("Helvetica", 12)).pack(pady=5)
bg_color_frame = tk.Frame(root)
bg_color_frame.pack()
bg_color_entry = tk.Entry(bg_color_frame, font=("Helvetica", 12), width=30)
bg_color_entry.pack(side=tk.LEFT)
tk.Button(bg_color_frame, text="Choose Color", command=choose_bg_color).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Generate QR Code", font=("Helvetica", 12), bg="green", fg="white", command=generate_qr).pack(pady=15)
tk.Button(root, text="Decode QR Code", font=("Helvetica", 12), bg="blue", fg="white", command=decode_qr).pack(pady=10)

qr_image_label = tk.Label(root)
qr_image_label.pack(pady=20)

root.mainloop()
