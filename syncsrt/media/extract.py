import subprocess
import os

class extract:
    def convert_video_to_audio_ffmpeg(self, video_file, start, end, output_ext="wav"):
        filename, ext = os.path.splitext(video_file)
        subprocess.call(["ffmpeg", "-i", video_file, "-ss", start, "-t", end, f"{filename}.{output_ext}"], 
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
