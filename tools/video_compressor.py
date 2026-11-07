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

def compress_video_process(input_path, output_path, level="Balanced (720p)", progress_callback=None, cancel_callback=None):
    try:
        ffmpeg_exe = get_ffmpeg_path()

        if level == "Smallest (360p)":
            res_clean = "640:360"
            crf_value = "32"
            preset_val = "veryfast"
        elif level == "Small (480p)":
            res_clean = "854:480"
            crf_value = "28"
            preset_val = "fast"
        else: # Balanced (720p)
            res_clean = "1280:720"
            crf_value = "23"
            preset_val = "medium"
            
        command = [
            ffmpeg_exe,
            "-y",                                  
            "-i", input_path,                      
            "-vf", f"scale={res_clean}",           
            "-c:v", "libx264",
            "-crf", crf_value,
            "-preset", preset_val,
            "-c:a", "aac",               
            "-b:a", "128k",
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
                raise Exception("DIBATALKAN_USER")
                
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
            original_size = os.path.getsize(input_path) / (1024 * 1024)
            new_size = os.path.getsize(output_path) / (1024 * 1024)
            return True, (f"Video berhasil dikompresi!\n"
                          f"Level: {level}\n"
                          f"Ukuran Awal: {original_size:.2f} MB\n"
                          f"Ukuran Baru: {new_size:.2f} MB")
        else:
            return False, "Proses gagal atau format tidak didukung."
            
    except Exception as e:
        if "DIBATALKAN_USER" in str(e):
            if os.path.exists(output_path):
                os.remove(output_path)
            return False, "Proses dibatalkan oleh pengguna."
        return False, f"Terjadi kesalahan sistem: {str(e)}"