import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube, Playlist
import re


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.output_path = None
        self.selected_resolution = tk.StringVar(value="Melhor Resolução")

        bg_color = "#121212"
        fg_color = "white"
        button_color = "#2e2e2e"

        self.root.configure(bg=bg_color)
        self.root.option_add("*TButton*highlightBackground", bg_color)
        self.root.option_add("*TButton*highlightColor", bg_color)
        self.root.option_add("*TButton*background", button_color)
        self.root.option_add("*TButton*foreground", fg_color)
        self.root.option_add("*TButton*bd", 0)
        self.root.option_add("*TEntry*background", "#333333")
        self.root.option_add("*TEntry*foreground", fg_color)
        self.root.option_add("*TEntry*bd", 0)

        self.root.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.root.eval("tk::PlaceWindow . center")

        header_frame = tk.Frame(self.root, bg="#121212")
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(
            header_frame,
            text="YouTube Downloader",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#121212",
        )
        header_label.pack(pady=10)

        body_frame = tk.Frame(self.root, bg="#121212")
        body_frame.pack(fill=tk.BOTH, expand=True)

        url_label = tk.Label(
            body_frame,
            text="Cole a URL do vídeo ou da playlist abaixo:",
            font=("Arial", 12),
            bg="#121212",
            fg="white",
        )
        url_label.grid(row=0, column=0, pady=(20, 5), padx=20, sticky=tk.W)

        self.url_entry = tk.Entry(
            body_frame,
            width=60,
            font=("Arial", 12),
            bg="#333333",
            fg="white",
        )
        self.url_entry.grid(row=1, column=0, pady=5, padx=20)

        browse_button = tk.Button(
            body_frame,
            text="Escolher Local de Salvamento",
            bg="#2e2e2e",
            fg="white",
            padx=10,
            pady=5,
            command=self.browse_directory,
        )
        browse_button.grid(row=2, column=0, pady=10, padx=20)

        download_button = tk.Button(
            body_frame,
            text="Baixar",
            bg="#2e2e2e",
            fg="white",
            padx=10,
            pady=5,
            command=self.download,
        )
        download_button.grid(row=3, column=0, pady=10, padx=20)

        progress_label = tk.Label(
            body_frame,
            text="",
            font=("Arial", 12),
            bg="#121212",
            fg="white",
        )
        progress_label.grid(row=4, column=0, pady=5, padx=20, sticky=tk.W)

        progress_bar_frame = tk.Frame(body_frame, bg="#121212")
        progress_bar_frame.grid(row=5, column=0, pady=10, padx=20)

        self.progress_bar = tk.Canvas(
            progress_bar_frame,
            width=400,
            height=20,
            bg="#333333",
        )
        self.progress_bar.pack()

    def browse_directory(self):
        self.output_path = filedialog.askdirectory()

    def download(self):
        video_url = self.url_entry.get()

        if not self.output_path:
            messagebox.showinfo(
                "Alerta", "Escolha um diretório de salvamento antes de baixar."
            )
            return

        if "list=" in video_url:
            self.download_playlist(video_url)
        else:
            self.download_single_video(video_url)

    def download_playlist(self, video_url):
        playlist = Playlist(video_url)
        total_videos = len(playlist.video_urls)

        for idx, video_url in enumerate(playlist.video_urls, 1):
            self.update_progress(idx, total_videos)
            self.download_video(video_url, idx)

        messagebox.showinfo("Concluído", "Download da playlist concluído.")

    def download_single_video(self, video_url):
        self.update_progress(0, 1)
        self.download_video(video_url)
        messagebox.showinfo("Concluído", "Download do vídeo único concluído.")

    def download_video(self, video_url, idx=None):
        try:
            video = YouTube(video_url)
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao obter informações do vídeo: {e}",
            )
            return

        if idx is not None:
            sanitized_title = re.sub(r"[^\w\s.-]", "", video.title)
            filename = f"{idx:02d} - {sanitized_title}"
        else:
            sanitized_title = re.sub(r"[^\w\s.-]", "", video.title)
            filename = sanitized_title

        stream = video.streams.get_highest_resolution()
        if stream:
            stream.download(output_path=self.output_path, filename=filename)

    def update_progress(self, current, total):
        if total == 1:
            percentage = 100
        else:
            percentage = int((current / total) * 100)

        progress = current / total * 400

        if hasattr(self, "progress_label"):
            self.progress_label.config(text=f"{percentage}% concluído")

        if hasattr(self, "progress_bar"):
            self.progress_bar.delete("all")
            self.progress_bar.create_rectangle(
                0,
                0,
                progress,
                20,
                fill="#191970",
            )

        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
