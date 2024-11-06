import os
import time
import argparse
import random
import sys
import tkinter as tk
from tkinter import ttk

def replace_random(text):
    while '&random&' in text:
        random_num = str(random.randint(0, 32768))
        text = text.replace('&random&', random_num, 1)
    return text
  
def cli(name, contents, instances, nolog):
    if not name.endswith(".txt"):
        name += ".txt"
    name = replace_random(name)
    contents = replace_random(contents)

    if not os.path.exists('Output'):
        os.mkdir('Output')

    if nolog:
        log = None
    else:
        log_file = f"Output/{name}_log.txt"
        log = open(log_file, "w")

    num = 0
    total_lines = 0

    start_time = time.time()

    with open(f"Output/{name}", "w") as file:
        if log:
            log.write("Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        for _ in range(instances):
            line = contents.replace('&linecount&', str(num + 1)) + '\n'
            file.write(line)
            if log:
                log.write(f"Generated Line {num + 1}: {line}")
            num += 1
            total_lines += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    lines_per_second = total_lines / elapsed_time if elapsed_time > 0 else 0

    if log:
        log.write(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")
        log.write(f"Average Lines Per Second: {lines_per_second:.2f} lines/s\n")
        log.close()

    print(f"Completed in {elapsed_time:.2f} seconds, with an average of {lines_per_second:.2f} lines per second.")
    if log:
        print(f"Log file '{log_file}' has been created.")

def gui():
    def enable_generate_button(event=None):
        try:
            instances = int(instances_entry.get())
            valid_instances = True
        except ValueError:
            valid_instances = False

        name = name_entry.get()
        contents = contents_entry.get()

        if name and contents and valid_instances:
            generate_button.config(state='normal')
        else:
            generate_button.config(state='disabled')

    def generate_text():
        name = name_entry.get()
        contents = contents_entry.get()
        instances = int(instances_entry.get())
        nolog = nolog_var.get()

        if not name.endswith(".txt"):
            name += ".txt"
        name = replace_random(name)
        contents = replace_random(contents)

        if not os.path.exists('Output'):
            os.mkdir('Output')

        if not nolog:
            log_file = f"Output/{name}_log.txt"
            log = open(log_file, "w")
        else:
            log = None

        num = 0
        total_lines = 0
        start_time = time.time()

        with open(f"Output/{name}", "w") as file:
            if log:
                log.write("Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            for _ in range(instances):
                line = contents.replace('&linecount&', str(num + 1)) + '\n'
                file.write(line)
                if log:
                    log.write(f"Generated Line {num + 1}: {line}")
                num += 1
                total_lines += 1

        end_time = time.time()
        elapsed_time = end_time - start_time
        lines_per_second = total_lines / elapsed_time if elapsed_time > 0 else 0

        if log:
            log.write(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")
            log.write(f"Average Lines Per Second: {lines_per_second:.2f} lines/s\n")
            log.close()

        result_label.config(text=f"Completed in {elapsed_time:.2f} seconds, with an average of {lines_per_second:.2f} lines per second.")
        if log:
            log_file_label.config(text=f"Log file '{log_file}' has been created.")
          
    root = tk.Tk()
    root.title("EntryWave - Text Content Generator")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#2E2E2E")
    style.configure("TLabel", background="#2E2E2E", foreground="white")
    style.configure("TEntry", fieldbackground="#3E3E3E", foreground="white")
    style.configure("TButton", background="#5E5E5E", foreground="white")
    style.configure("TCheckbutton", background="#2E2E2E", foreground="white")

    frame = ttk.Frame(root, padding=10)
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.columnconfigure(1, weight=1)

    ttk.Label(frame, text="File Name:").grid(column=0, row=0, sticky=tk.W)
    name_entry = ttk.Entry(frame)
    name_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))
    
    ttk.Label(frame, text="Text Content:").grid(column=0, row=1, sticky=tk.W)
    contents_entry = ttk.Entry(frame)
    contents_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))
    
    ttk.Label(frame, text="Number of Instances:").grid(column=0, row=2, sticky=tk.W)
    instances_entry = ttk.Entry(frame)
    instances_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))
    
    nolog_var = tk.BooleanVar()
    ttk.Checkbutton(frame, text="Disable Logging", variable=nolog_var).grid(column=1, row=3, sticky=tk.W)

    generate_button = ttk.Button(frame, text="Generate", command=generate_text, state='disabled')
    generate_button.grid(column=1, row=4, sticky=tk.E)

    result_label = ttk.Label(frame, text="")
    result_label.grid(column=0, row=6, columnspan=2, sticky=(tk.W, tk.E))

    log_file_label = ttk.Label(frame, text="")
    log_file_label.grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E))

    name_entry.bind("<KeyRelease>", enable_generate_button)
    contents_entry.bind("<KeyRelease>", enable_generate_button)
    instances_entry.bind("<KeyRelease>", enable_generate_button)

    root.configure(bg="#2E2E2E")
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Generate text content with CLI or GUI.")
    parser.add_argument("name", nargs="?", help="File name")
    parser.add_argument("contents", nargs="?", help="Text content to generate")
    parser.add_argument("instances", nargs="?", type=int, help="Number of times to generate the content")
    parser.add_argument("--nolog", action="store_true", help="Disable logging")
    parser.add_argument("--use-gui", action="store_true", help="Launch GUI mode")
    args = parser.parse_args()

    if args.use_gui:
        gui()
    else:
        if not (args.name and args.contents and args.instances):
            print("No arguments provided. Please enter values:")
            args.name = input("File name (without extension): ")
            args.contents = input("Text content to generate: ")
            while True:
                try:
                    args.instances = int(input("Number of instances: "))
                    break
                except ValueError:
                    print("Please enter a valid number.")
            confirm = input("Proceed with the entered values? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Exiting.")
                sys.exit(0)
        
        cli(args.name, args.contents, args.instances, args.nolog)

if __name__ == "__main__":
    main()
