import yt_dlp
import os
import sys

def get_ffmpeg_path():
    """get ffmpeg.exe in bin, to use for the yt downloader"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'bin', 'ffmpeg.exe')
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bin', 'ffmpeg.exe')

def download_yt_process(url, output_dir, file_type, quality, progress_callback=None, cancel_callback=None):
    try:
        ffmpeg_location = get_ffmpeg_path()
        
        # PROGESS BAR
        def my_hook(d):
            
                    if cancel_callback and cancel_callback():
                        raise Exception("DIBATALKAN_USER")
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                        downloaded = d.get('downloaded_bytes', 0)
                        
                        if total > 0 and progress_callback:
                            percent_float = downloaded / total
                            percent_str = d.get('_percent_str', '').strip()
                            speed_str = d.get('_speed_str', '').strip()
                            
                            downloaded_mb = downloaded / (1024 * 1024)
                            total_mb = total / (1024 * 1024)
                            progress_callback(percent_float, percent_str, speed_str, downloaded_mb, total_mb)
        
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, f'%(title)s [{quality}].%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'color': 'no_color',
            'no_warnings': True,
            'ffmpeg_location': ffmpeg_location,
            'progress_hooks': [my_hook]
        }
        
        if file_type == "MP4 (Video)":
            res = quality.replace("p", "")
            ydl_opts['format'] = f'bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/best[height<={res}][ext=mp4]/best'
            ydl_opts['merge_output_format'] = 'mp4'
        else:
            bitrate = quality.replace("kbps", "")
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return True, "Download berhasil diselesaikan!"
            
    except Exception as e:
            if "DIBATALKAN_USER" in str(e):
                return False, "Download dibatalkan oleh pengguna."
            return False, f"Gagal mengunduh: {str(e)}"
