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

def convert_video_process(input_path, output_path, progress_callback=None, cancel_callback=None):
    try:
        ffmpeg_exe = get_ffmpeg_path()
        
        command = [
            ffmpeg_exe,
            "-y",
            "-i", input_path,
            output_path
        ]
        
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace",
            creationflags=creationflags
        )
        
        total_duration = 0
        
        for line in process.stdout:
            if cancel_callback and cancel_callback():
                process.terminate()
                process.wait()
                raise Exception("USER_CANCEL")
                
            if "Duration" in line and total_duration == 0:
                match = re.search(r"Duration:\s*(\d{2}:\d{2}:\d{2}\.\d+)", line)
                if match:
                    total_duration = get_seconds(match.group(1))
                    
            if "time=" in line and total_duration > 0 and progress_callback:
                match = re.search(r"time=(\d{2}:\d{2}:\d{2}\.\d+)", line)
                if match:
                    current_time = get_seconds(match.group(1))
                    percent_float = min(current_time / total_duration, 1.0)
                    percent_str = f"{percent_float * 100:.1f}%"
                    progress_callback(percent_float, percent_str)

        process.wait()
        
        if process.returncode == 0:
            target_ext = os.path.splitext(output_path)[1].upper()
            return True, f"Video successfully converted to {target_ext}!"
        else:
            return False, "Conversion failed or format unsupported."
            
    except Exception as e:
        if "USER_CANCEL" in str(e):
            if os.path.exists(output_path):
                os.remove(output_path)
            return False, "Conversion cancelled by user."
        return False, f"System error: {str(e)}"