import socket
from PIL import Image, ImageTk
import io
import struct
import tkinter as tk

print("\x1B]0;Rigol\x07", end='', flush=True)

# Function to get live BMP data using a socket connection
def get_live_bmp_stream():
    host = '192.168.222.2'
    port = 5555
    command = ':display:data?\n'  # Command with newline

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(20)
        s.connect((host, port))
        s.sendall(command.encode())
        
        initial_data = s.recv(64)
        bmp_offset = initial_data.find(b'BM')
        if bmp_offset == -1:
            raise ValueError("BMP header not found in initial data")
        
        bmp_data = initial_data[bmp_offset:]
        if len(bmp_data) < 14:
            bmp_data += s.recv(14 - len(bmp_data))
        
        file_size = struct.unpack('<I', bmp_data[2:6])[0]
        remaining_size = file_size - len(bmp_data)
        
        while remaining_size > 0:
            part = s.recv(min(4096, remaining_size))
            if not part:
                break
            bmp_data += part
            remaining_size -= len(part)

        if remaining_size != 0:
            raise ValueError("Incomplete BMP file received")

    return bmp_data

# Function to update the image in the Tkinter window
def update_image():
    try:
        bmp_data = get_live_bmp_stream()
        image = Image.open(io.BytesIO(bmp_data))
        photo = ImageTk.PhotoImage(image)

        # Update the image in the label
        label.config(image=photo)
        label.image = photo
    except Exception as e:
        print(f"Error: {e}")

    # Schedule the update function to be called again after 200msecs 
    # this keeps the scope responsive
    root.after(200, update_image)

# Create the Tkinter window
root = tk.Tk()
root.title("Live BMP Display")

# Create a label to display the image
label = tk.Label(root)
label.pack()

# Start the updating loop
update_image()

# Run the Tkinter main loop
root.mainloop()

