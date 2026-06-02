#!/usr/bin/env python3
# YouTube Downloader Pro - with Playlist Support

import os
import sys
import subprocess
import re

# --- Auto install missing dependencies ---
def auto_install_dependencies():
    required = {
        "yt_dlp": "yt-dlp",
        "rich": "rich"
    }
    missing = []
    for mod, pip in required.items():
        try:
            __import__(mod)
        except ImportError:
            missing.append(pip)
    if missing:
        print("\n[!] Missing dependencies found. Installing automatically...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("[+] Dependencies installed successfully.\n")
        except Exception as e:
            print(f"[X] Installation failed: {e}")
            sys.exit(1)

auto_install_dependencies()

from yt_dlp import YoutubeDL
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, TextColumn
from rich import print as rprint

console = Console()

# --- Logo & Credits ---
def show_logo():
    logo = r"""
    ██╗   ██╗████████╗    ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      
    ╚██╗ ██╔╝╚══██╔══╝    ██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║      
     ╚████╔╝    ██║       ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║      
      ╚██╔╝     ██║       ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║      
       ██║      ██║       ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗ 
       ╚═╝      ╚═╝       ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ 
    """
    console.print(Panel(logo, title="[bold cyan]YouTube Downloader Pro[/bold cyan]", border_style="magenta", expand=False))
    credit = Panel(
        "[bold white]👨‍💻 Developer :[/bold white] [yellow]Murphy >_[/yellow]\n"
        "[bold white]🌐 GitHub    :[/bold white] [green]github.com/sadikmahedi88[/green]\n"
        "[bold white]📢 Telegram  :[/bold white] [green]t.me/Murphython[/green]",
        title="[bold red]👑 Credits[/bold red]",
        border_style="cyan",
        expand=False
    )
    console.print(credit)
    console.print("[bold yellow]⚡ Professional & Smart Downloader Tool ⚡[/bold yellow]\n")

# --- Get download path (Android or local) ---
def get_base_download_folder():
    android_path = '/storage/emulated/0/Download'
    if os.path.exists(android_path):
        return android_path
    return os.getcwd()

# --- Check if URL is a playlist ---
def is_playlist(url):
    """Return True if URL points to a playlist."""
    ydl_opts = {'quiet': True, 'extract_flat': True}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return 'entries' in info and info.get('playlist_count', 0) > 0
        except:
            return False

# --- Get playlist info (title, entries) ---
def get_playlist_info(url, max_display=30):
    """Return (playlist_title, list of (index, title)) for first max_display videos."""
    ydl_opts = {'quiet': True, 'extract_flat': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        playlist_title = info.get('playlist_title', 'Playlist')
        entries = info.get('entries', [])
        total = len(entries)
        display_entries = []
        for i, entry in enumerate(entries[:max_display], start=1):
            title = entry.get('title', f'Video {i}')
            display_entries.append((i, title))
        return playlist_title, display_entries, total

# --- Parse user selection (e.g., "1,3,5" or "1-5" or "99") ---
def parse_selection(selection_str, total_videos):
    """Return a string like '1,3,5-7' for yt-dlp playlist_items."""
    selection_str = selection_str.strip()
    if selection_str == '99':
        return None  # None means all videos
    items = []
    parts = selection_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            try:
                s = int(start)
                e = int(end)
                if s < 1 or e > total_videos or s > e:
                    console.print(f"[red]Invalid range: {part}[/red]")
                    return None
                items.append(f"{s}-{e}")
            except:
                console.print(f"[red]Invalid range format: {part}[/red]")
                return None
        else:
            try:
                num = int(part)
                if num < 1 or num > total_videos:
                    console.print(f"[red]Number {num} out of range (1-{total_videos})[/red]")
                    return None
                items.append(str(num))
            except:
                console.print(f"[red]Invalid number: {part}[/red]")
                return None
    return ','.join(items) if items else None

# --- Display playlist menu with colored table ---
def show_playlist_menu(entries, total):
    """Display a rich table of videos."""
    table = Table(title=f"Playlist Videos (showing first {len(entries)} of {total})",
                  title_style="bold blue",
                  border_style="blue")
    table.add_column("#", style="bold green", justify="right")
    table.add_column("Video Title", style="cyan")
    for idx, title in entries:
        # Shorten long titles
        if len(title) > 60:
            title = title[:57] + "..."
        table.add_row(str(idx), title)
    if total > len(entries):
        table.add_row("...", f"... and {total - len(entries)} more videos")
    console.print(table)

# --- Ask for quality settings (video or audio) ---
def get_quality_settings():
    """Return ydl_opts dictionary for video or audio."""
    console.print("\n[bold blue]Select Download Type:[/bold blue]")
    console.print(" [1] 🎥 Video")
    console.print(" [2] 🎵 Audio Only")
    choice = console.input("[bold yellow]Choose (1 or 2): [/bold yellow]").strip()

    if choice == '1':
        console.print("\n[bold blue]Select Video Quality:[/bold blue]")
        console.print(" [1] 🔥 Best Available")
        console.print(" [2] 📺 Full HD (1080p)")
        console.print(" [3] ⚡ HD (720p)")
        console.print(" [4] 📱 Eco (480p/360p)")
        q = console.input("[bold yellow]Enter quality number: [/bold yellow]").strip()
        if q == '2':
            fmt = 'bestvideo[height<=1080]+bestaudio/best'
        elif q == '3':
            fmt = 'bestvideo[height<=720]+bestaudio/best'
        elif q == '4':
            fmt = 'bestvideo[height<=480]+bestaudio/best'
        else:
            fmt = 'bestvideo+bestaudio/best'
        
        console.print("\n[bold blue]Select Output Format:[/bold blue]")
        console.print(" [1] MP4 (Compatible)")
        console.print(" [2] MKV (Lossless)")
        ext = console.input("[bold yellow]Enter format number: [/bold yellow]").strip()
        merge = 'mp4' if ext == '1' else 'mkv'
        
        return {
            'format': fmt,
            'merge_output_format': merge
        }
    elif choice == '2':
        console.print("\n[bold blue]Select Audio Quality:[/bold blue]")
        console.print(" [1] 💎 320 kbps (High)")
        console.print(" [2] 📻 192 kbps (Standard)")
        console.print(" [3] 📉 128 kbps (Eco)")
        aq = console.input("[bold yellow]Enter quality number: [/bold yellow]").strip()
        quality_map = {'1': '320', '3': '128'}
        chosen = quality_map.get(aq, '192')
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': chosen,
            }]
        }
    else:
        console.print("[red]Invalid choice. Exiting.[/red]")
        sys.exit(1)

# --- Progress hook for rich progress bar ---
def make_progress_hook(progress, task):
    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percent = (downloaded / total) * 100
                progress.update(task, completed=percent, visible=True)
        elif d['status'] == 'finished':
            progress.update(task, completed=100)
    return hook

# --- Download single video or playlist ---
def download_media():
    show_logo()
    url = console.input("[bold green]🔗 Enter YouTube URL (video or playlist): [/bold green]").strip()
    if not url:
        console.print("[red]URL cannot be empty![/red]")
        return

    # Check if playlist
    console.print("[yellow]Analyzing link...[/yellow]")
    playlist_flag = is_playlist(url)
    
    # Get quality settings first (same for all videos in playlist)
    quality_opts = get_quality_settings()
    
    # Prepare base output path
    base_folder = get_base_download_folder()
    
    if not playlist_flag:
        # Single video
        console.print("[green]Single video detected.[/green]")
        out_template = os.path.join(base_folder, '%(title)s.%(ext)s')
        ydl_opts = quality_opts.copy()
        ydl_opts['outtmpl'] = out_template
        ydl_opts['quiet'] = True
        
        with Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=30, style="black on blue", complete_style="green"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task_id = progress.add_task("[magenta]Downloading...[/magenta]", total=100, visible=False)
            ydl_opts['progress_hooks'] = [make_progress_hook(progress, task_id)]
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                console.print("\n[bold green]✅ Download completed successfully![/bold green]")
                console.print(f"[green]📂 Saved to: {base_folder}[/green]")
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")
    else:
        # Playlist
        console.print("[green]Playlist detected. Fetching information...[/green]")
        playlist_title, entries, total = get_playlist_info(url)
        console.print(f"[bold cyan]Playlist: {playlist_title} (Total: {total} videos)[/bold cyan]")
        
        if total == 0:
            console.print("[red]No videos found in playlist.[/red]")
            return
        
        # Show table of first 30 videos
        show_playlist_menu(entries, total)
        
        # Ask for selection
        console.print("\n[bold yellow]Enter video numbers:[/bold yellow]")
        console.print("[dim]Examples: 1,3,5  or  1-5  or  1,3-5,7  or  99 for ALL[/dim]")
        sel = console.input("[bold green]Your choice: [/bold green]").strip()
        
        playlist_items = parse_selection(sel, total)
        if playlist_items is None and sel != '99':
            return
        
        # Create folder for playlist
        safe_title = re.sub(r'[\\/*?:"<>|]', "", playlist_title).strip()
        if not safe_title:
            safe_title = "Playlist"
        playlist_dir = os.path.join(base_folder, safe_title)
        os.makedirs(playlist_dir, exist_ok=True)
        
        out_template = os.path.join(playlist_dir, '%(playlist_index)s - %(title)s.%(ext)s')
        ydl_opts = quality_opts.copy()
        ydl_opts['outtmpl'] = out_template
        ydl_opts['quiet'] = True
        if playlist_items:
            ydl_opts['playlist_items'] = playlist_items
        
        # Download with progress for each video
        with Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=30, style="black on blue", complete_style="green"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task_id = progress.add_task("[magenta]Downloading playlist...[/magenta]", total=100, visible=False)
            ydl_opts['progress_hooks'] = [make_progress_hook(progress, task_id)]
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                console.print("\n[bold green]✅ Playlist download completed![/bold green]")
                console.print(f"[green]📂 Saved to: {playlist_dir}[/green]")
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")

if __name__ == "__main__":
    download_media()