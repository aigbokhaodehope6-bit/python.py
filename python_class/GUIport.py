import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox


def scan_ports():
    target = entry_target.get()
    start_port = entry_start.get()
    end_port = entry_end.get()

    if not target or not start_port or not end_port:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        start_port = int(start_port)
        end_port = int(end_port)
    except ValueError:
        messagebox.showerror("Error", "Port range must be numbers")
        return

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Scanning {target}...\n\n")

    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            result = s.connect_ex((target, port))

            if result == 0:
                output_text.insert(tk.END, f"[OPEN] Port {port}\n")

            s.close()
        except:
            pass

    output_text.insert(tk.END, "\nScan Complete.")


def start_scan_thread():
    thread = threading.Thread(target=scan_ports)
    thread.start()


# GUI Setup
root = tk.Tk()
root.title("Python Port Scanner")
root.geometry("600x500")

tk.Label(root, text="Target IP:").pack()
entry_target = tk.Entry(root, width=40)
entry_target.pack()

tk.Label(root, text="Start Port:").pack()
entry_start = tk.Entry(root, width=20)
entry_start.pack()

tk.Label(root, text="End Port:").pack()
entry_end = tk.Entry(root, width=20)
entry_end.pack()

scan_button = tk.Button(root, text="Scan", command=start_scan_thread)
scan_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=70, height=20)
output_text.pack()

root.mainloop()
