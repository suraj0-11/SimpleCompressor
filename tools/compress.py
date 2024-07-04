import ffmpeg
import os

def compress_file(input_file_path, output_file_path):
    (
        ffmpeg
        .input(input_file_path)
        .output(output_file_path, vcodec='libx265', crf=28, preset='veryfast')
        .run()
    )

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
