import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
import cv2
import os
from PIL import Image, ImageTk

def generate_qr():
    data = data_entry.get().strip()
    filename = filename_entry.get().strip()
    
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
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    
    messagebox.showinfo("Success", f"QR Code saved as {filename}")
    display_qr_image(filename)
  
    data_entry.delete(0, tk.END)
    filename_entry.delete(0, tk.END)

def decode_qr():
    filename = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
    if not filename:
        return
    
    if not os.path.exists(filename):
        messagebox.showerror("File Error", "File not found. Please select a valid file.")
        return
    
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    
    if data:
        messagebox.showinfo("Decoded Data", f"QR Code contains:\n{data}")
        root.clipboard_clear()
        root.clipboard_append(data)
        root.update()
    else:
        messagebox.showinfo("Result", "No QR code found in the image.")

def display_qr_image(filename):
    img = Image.open(filename)
    img = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    qr_image_label.config(image=img_tk)
    qr_image_label.image = img_tk

root = tk.Tk()
root.title("QR Code Generator & Decoder")
root.geometry("450x500")
root.resizable(False, False)

tk.Label(root, text="Enter Text/URL:", font=("Helvetica", 12)).pack(pady=10)
data_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
data_entry.pack()

tk.Label(root, text="Enter Filename (optional):", font=("Helvetica", 12)).pack(pady=10)
filename_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
filename_entry.pack()

tk.Button(root, text="Generate QR Code", font=("Helvetica", 12), bg="green", fg="white", command=generate_qr).pack(pady=15)
tk.Button(root, text="Decode QR Code", font=("Helvetica", 12), bg="blue", fg="white", command=decode_qr).pack(pady=10)

qr_image_label = tk.Label(root)
qr_image_label.pack(pady=20)

root.mainloop()
