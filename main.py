import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor
import threading

root = tk.Tk()
root.title("Lew's WebP Converter")
root.geometry("400x200")

quality_label = tk.Label(root, text="Quality (0-100)")
quality_label.pack()

quality_input = tk.Entry(root)
quality_input.pack()


def select_files():
    files = filedialog.askopenfilenames(title = "Select Images", filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
    if not files:
        messagebox.showerror("Error", "No files selected")
        return
    return files

def select_folder():
    folder = filedialog.askdirectory(title = "Select Output Folder")
    if not folder:
        messagebox.showerror("Error", "No folder selected")
        return
    return folder

def convert_image(file, quality, output_folder):
    image = Image.open(file)
    image_name = file.split("/")[-1].replace("jpg","webp").replace("png","webp")
    new_path = output_folder + "/" + image_name
    image.save(new_path, "webp", quality=quality)

def convert_images(files, quality, output_folder, progress_bar):
    if not files or not output_folder:
        return
    if not quality or not quality.isnumeric() or int(quality) < 0 or int(quality) > 100:
        messagebox.showerror("Error", "Please enter a valid quality value between 0 and 100")
        return
    total = len(files)
    progress = 0
    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(convert_image, file, quality, output_folder): file for file in files}
        for future in future_to_file:
            file = future_to_file[future]
            try:
                future.result()
                progress += 1
                progress_bar["value"] = progress
                root.update_idletasks()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while processing {file}\n {e}")
    progress_bar.destroy()

def start_conversion():
    files = select_files()
    if not files:
        return
    quality = quality_input.get()
    folder = select_folder()
    if not folder:
        return
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack()
    progress_bar["maximum"] = len(files)
    thread = threading.Thread(target=convert_images, args=(files, quality, folder, progress_bar))
    thread.start()

select_files_button = tk.Button(root, text="Select Files", command=start_conversion)
select_files_button.pack()

root.mainloop()