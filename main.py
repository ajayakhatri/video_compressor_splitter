import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from tkinter import Tk, Button, filedialog, Listbox, Label, Frame, Entry
import subprocess
import platform
from tkinter import ttk

output_folder = os.getcwd()



def split_video(filename, video_file, max_size):
    const = 1
    clip = VideoFileClip(video_file)
    duration = clip.duration
    # parts, remainder = divmod(duration, max_size)
    parts = duration // max_size
    remainder = duration % max_size
    global output_folder
    total: int = int(parts)
    if remainder > 0:
        total += 1
    for i in range(int(parts)):
        start_time = i * max_size
        end_time = (i + 1) * max_size
        ffmpeg_extract_subclip(
            video_file,
            start_time,
            end_time,
            targetname=os.path.join(
                output_folder, f"{const}-of-{total}-{filename}.mkv"
            ),
        )
        const += 1
    if remainder > 0:
        start_time = parts * max_size
        end_time = start_time + remainder
        ffmpeg_extract_subclip(
            video_file,
            start_time,
            end_time,
            targetname=os.path.join(
                output_folder, f"{const}-of-{total}-{filename}.mkv"
            ),
        )
    return f"-of-{total}-{filename}.mkv"


def split(file_path):
    global output_folder

    max_size: int = 900  # replace with your desired value
    max_size_input = max_size_entry.get()
    if len(max_size_input) == 0:
        max_size = 150
    elif int(max_size_input) < 150:
        max_size = 150
    else:
        max_size = int(max_size_input)
    # Split all videos in the directory
    endname: str = split_video(
        os.path.basename(file_path).split(".")[0], file_path, max_size
    )
  

    delete_button.config(
        command=lambda: delete_files_in_directory(output_folder, endname)
    )
    splitted_videos = [f for f in os.listdir(output_folder) if f.endswith(endname)]
    return splitted_videos, output_folder


def delete_files_in_directory(directory, endname):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) and filename.endswith(endname):
                os.unlink(file_path)
        except Exception as exception:
            print("Failed to delete %s. Reason: %s" % (file_path, exception))
    listbox.delete(0, "end")
    listbox.pack_forget()
    play_label.pack_forget()
    delete_button.pack_forget()




def play_video(output_folder):
    selected_video = listbox.get(listbox.curselection())

    video_path = os.path.join(output_folder, selected_video)
    if platform.system() == "Windows":
        subprocess.Popen(["start", "", video_path], shell=True)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", video_path])
    elif platform.system() == "Linux":
        subprocess.Popen(["xdg-open", video_path])
    else:
        print("Unsupported operating system")


def display_splitted_videos(splitted_videos):
    listbox.delete(0, "end")
    for video in splitted_videos:
        listbox.insert("end", video)


def upload_videos(file_path):
    splitted_videos, output_folder = split(file_path)
    play_label.pack(pady=5)
    listbox.pack(pady=(5, 10))
    listbox.bind("<Double-Button-1>", lambda event: play_video(output_folder))
    display_splitted_videos(splitted_videos)
    sort_listbox()
    delete_button.pack(pady=10)


def askfile():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.*")])
    if len(os.path.basename(file_path)) != 0:
        output_label.pack()
        output_button.pack(pady=(5, 10))
        max_size_label.pack(pady=(5, 0))
        max_size_entry.pack(pady=(5, 10))
        trim_label.pack(pady=(5, 0))
        trim_button.pack(pady=(5, 10))

        trim_button.config(
            command=lambda: upload_videos(file_path)
        )  # Update the command for upload button
        status_label.config(text=f"Video choosed: {os.path.basename(file_path)}")


def askoutputfolder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if os.path.isdir(output_folder):
        output_label.config(text=output_folder)
        output_folder = output_folder
    else:
        output_label.config(text=f"Invalid folder path, Path set to: {os.getcwd()}")
        output_folder = os.getcwd()


def set_max_size():
    max_size = max_size_entry.get()
    print(f"Maximum Size: {max_size}")


def sort_listbox():
    items = list(listbox.get(0, "end"))
    items.sort(key=lambda x: int(x.split("-")[0]))
    listbox.delete(0, "end")
    for item in items:
        listbox.insert("end", item)


if __name__ == "__main__":
    root = Tk()
    # root.geometry("400x300")  # Set initial window size
    root.iconbitmap("icon.ico")
    root.title("Video Splitter- By AJ")

    style = ttk.Style()
    style.theme_use("clam")

    # Apply a modern theme
    style = ttk.Style()
    style.theme_use("clam")

    # Create a frame for the content and make it occupy the entire root window
    content_frame = ttk.Frame(root)
    content_frame.pack(fill="both", expand=True, padx=10)

    choose_frame = Frame(
        content_frame, highlightbackground="black", highlightthickness=1
    )

    choose_frame.pack(pady=(10, 0))

    status_label = Label(choose_frame, width=50, text="Welcome to the Video Splitter!")
    choose_button = Button(choose_frame, text="Choose Video", command=askfile)
    status_label.pack(pady=(10, 0))
    choose_button.pack(pady=10)

    output_frame = Frame(
        content_frame, highlightbackground="black", highlightthickness=1
    )
    output_frame.pack(pady=(10, 0))

    output_button = Button(
        output_frame, text="Select Output Folder", command=askoutputfolder
    )
    output_label = Label(
        output_frame, width=50, wraplength=300, text=f"Output to: {os.getcwd()}"
    )
    output_button.pack(pady=(10, 4))
    output_label.pack()
    output_button.pack_forget()
    output_label.pack_forget()

    max_size_frame = Frame(
        content_frame, highlightbackground="black", highlightthickness=1
    )
    max_size_frame.pack(pady=(10, 0))

    max_size_label = Label(
        max_size_frame,
        width=50,
        wraplength=300,
        text="Maximum Size of a splitted video in seconds:",
    )

    # Create a validation function to allow only numbers
    def validate_max_size_input(new_value):
        return new_value.isdigit() or new_value == ""

    validate_max_size_input_command = (root.register(validate_max_size_input), "%P")
    max_size_entry = Entry(
        max_size_frame, validate="key", validatecommand=validate_max_size_input_command
    )
    max_size_entry.insert(0, "150")
    max_size_entry.pack(pady=5)
    max_size_label.pack(pady=5)
    max_size_entry.pack_forget()
    max_size_label.pack_forget()

    trim_frame = Frame(content_frame, highlightbackground="black", highlightthickness=1)
    trim_frame.pack(pady=(10, 10))

    trim_label = Label(trim_frame, width=50, wraplength=300, text="Click Button Below to Split the Video:")
    trim_button = Button(trim_frame, text="Split the Video")
    trim_label.pack()
    trim_label.pack_forget()
    trim_button.pack(pady=10)
    trim_button.pack_forget()

    #  Create a listbox to display the trimmed videos
    play_label = Label(
        trim_frame,
        width=50,
        wraplength=300,
        text="Double Click the videos below to play:",
    )
    listbox = Listbox(trim_frame, width=50)
    listbox.pack(pady=10)
    listbox.pack_forget()

    delete_button = Button(trim_frame, text="Delete All Splitted Videos")
    delete_button.pack(pady=10)
    delete_button.pack_forget()
    root.mainloop()
