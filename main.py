import tkinter as tk
from tkinter import scrolledtext

# Functions for encoding and decoding RS232
def encode_to_rs232(text):
    encoded = []
    for char in text:
        ascii_code = ord(char)
        bits = f"{ascii_code:08b}"  # Convert to 8-bit binary
        frame = f"1{bits}00"  # Add start bit and 2 stop bits
        encoded.append(frame)
    return " ".join(encoded)

def decode_from_rs232(encoded_text):
    frames = encoded_text.split(" ")
    decoded = ""
    for frame in frames:
        if len(frame) == 11 and frame.startswith("1") and frame.endswith("00"):
            bits = frame[1:-2]  # Remove start and stop bits
            decoded += chr(int(bits, 2))  # Convert binary to ASCII
    return decoded

# Function to replace profanities with asterisks
def censor_profanities(text, profanities):
    words = text.split()
    censored = []
    for word in words:
        if word.lower() in profanities:
            censored.append("*" * len(word))
        else:
            censored.append(word)
    return " ".join(censored)

# Load profanities from a file
def load_profanities():
    try:
        with open("profanities.txt", "r") as f:
            return set(line.strip().lower() for line in f)
    except FileNotFoundError:
        return set()

# GUI Functions
def send_text():
    text = sender_input.get("1.0", tk.END).strip()
    profanities = load_profanities()
    censored_text = censor_profanities(text, profanities)
    encoded_text = encode_to_rs232(censored_text)
    receiver_input.delete("1.0", tk.END)
    receiver_input.insert(tk.END, encoded_text)

def receive_text():
    encoded_text = receiver_input.get("1.0", tk.END).strip()
    decoded_text = decode_from_rs232(encoded_text)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, decoded_text)

# Main GUI application
root = tk.Tk()
root.title("RS232 Communication Simulator")

# Sender frame
sender_frame = tk.Frame(root)
sender_frame.pack(pady=10)

sender_label = tk.Label(sender_frame, text="Sender (ASCII Text):")
sender_label.pack(anchor="w")

sender_input = scrolledtext.ScrolledText(sender_frame, wrap=tk.WORD, width=50, height=10)
sender_input.pack()

send_button = tk.Button(sender_frame, text="Send", command=send_text)
send_button.pack(pady=5)

# Receiver frame
receiver_frame = tk.Frame(root)
receiver_frame.pack(pady=10)

receiver_label = tk.Label(receiver_frame, text="Receiver (Encoded RS232):")
receiver_label.pack(anchor="w")

receiver_input = scrolledtext.ScrolledText(receiver_frame, wrap=tk.WORD, width=50, height=10)
receiver_input.pack()

receive_button = tk.Button(receiver_frame, text="Receive", command=receive_text)
receive_button.pack(pady=5)

# Output frame
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_label = tk.Label(output_frame, text="Output (Decoded ASCII Text):")
output_label.pack(anchor="w")

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=50, height=10)
output_text.pack()

# Run the application
root.mainloop()
