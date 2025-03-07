from tkinter import Tk, Button, Label, filedialog, messagebox, Canvas
from PIL import Image, ImageTk
import os

# Initialize global variables
selected_image_path = None
image_label = None
canvas = None

def update_displayed_image(image_path):
    global canvas, image_label
    
    # Open and resize image for display
    img = Image.open(image_path)
    img.thumbnail((250, 250))  # Resize for display
    
    # Convert image to Tkinter format
    img_tk = ImageTk.PhotoImage(img)

    # Clear previous image
    if image_label:
        image_label.destroy()

    # Display new image
    image_label = Label(root, image=img_tk)
    image_label.image = img_tk  # Keep reference to prevent garbage collection
    image_label.pack(pady=10)

def encrypt_image(file_path):
    img = Image.open(file_path).convert("RGB")  # Convert to RGB
    pixels = img.load()

    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = (r ^ 42, g ^ 42, b ^ 42)  # XOR with a key

    base, ext = os.path.splitext(file_path)
    encrypted_path = f"{base}_encrypted{ext}"

    img.save(encrypted_path)
    messagebox.showinfo("Success", f"Image Encrypted! Saved as {encrypted_path}")

    update_displayed_image(encrypted_path)  # Show encrypted image

def decrypt_image(file_path):
    img = Image.open(file_path).convert("RGB")  # Convert to RGB
    pixels = img.load()

    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = (r ^ 42, g ^ 42, b ^ 42)  # XOR with same key

    base, ext = os.path.splitext(file_path)
    decrypted_path = f"{base}_decrypted{ext}"

    img.save(decrypted_path)
    messagebox.showinfo("Success", f"Image Decrypted! Saved as {decrypted_path}")

    update_displayed_image(decrypted_path)  # Show decrypted image

def select_image(action):
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    if not file_path:
        return

    selected_image_path = file_path
    update_displayed_image(file_path)  # Show original image before processing

    if action == "encrypt":
        encrypt_image(file_path)
    elif action == "decrypt":
        decrypt_image(file_path)

# Create GUI
root = Tk()
root.title("Image Encryption Tool")
root.geometry("400x450")

Label(root, text="Select an image for encryption or decryption").pack(pady=10)
Button(root, text="🔒 Encrypt Image", command=lambda: select_image("encrypt"), bg="lightblue").pack(pady=5)
Button(root, text="🔓 Decrypt Image", command=lambda: select_image("decrypt"), bg="lightcoral").pack(pady=5)

# Image Display Canvas
canvas = Canvas(root, width=250, height=250)
canvas.pack(pady=10)

root.mainloop()
