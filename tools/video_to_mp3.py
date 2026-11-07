import subprocess
import os
import sys
import re

def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'bin', 'ffmpeg.exe')
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bin', 'ffmpeg.exe')

def get_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def convert_media_to_mp3(input_path, output_path, bitrate="320k", progress_callback=None, cancel_callback=None):
    ffmpeg_exe = get_ffmpeg_path()
    
    # CONVERTION VIDEO TO MP3
    command = [
        ffmpeg_exe,
        "-y",
        "-i", input_path,
        "-b:a", bitrate,
        output_path
    ]
    
    try:
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        
        # PROGESS BAR
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, 
            universal_newlines=True,
            creationflags=creationflags
        )
        
        total_duration = 0
        
        for line in process.stdout:

            if cancel_callback and cancel_callback():
                process.terminate() 
                process.wait()
                raise Exception("DIBATALKAN_USER")
                
            if "Duration" in line and total_duration == 0:
                match = re.search(r"Duration:\s*(\d{2}:\d{2}:\d{2}\.\d+)", line)
                if match:
                    total_duration = get_seconds(match.group(1))
                    
            if "time=" in line and total_duration > 0 and progress_callback:
                match = re.search(r"time=(\d{2}:\d{2}:\d{2}\.\d+)", line)
                if match:
                    current_time = get_seconds(match.group(1))
                    percent_float = current_time / total_duration
                    percent_float = min(percent_float, 1.0)
                    
                    percent_str = f"{percent_float * 100:.1f}%"
                    
                    progress_callback(percent_float, percent_str)

        process.wait()
        
        if process.returncode == 0:
            return True, "Konversi media berhasil diselesaikan!"
        else:
            return False, "Proses konversi gagal atau file rusak."
            
    except Exception as e:
        if "DIBATALKAN_USER" in str(e):
            # DELETE CANCELLED FILE
            if os.path.exists(output_path):
                os.remove(output_path)
            return False, "Konversi dibatalkan oleh pengguna."
        return False, f"Error sistem: {str(e)}"