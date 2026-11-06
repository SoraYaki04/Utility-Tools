import yt_dlp
import os

def download_yt_process(url, output_dir, file_type, quality):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True
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
        return False, f"Gagal mengunduh: {str(e)}"