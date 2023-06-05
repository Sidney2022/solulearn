# import subprocess
# import re, os
# from solulearn.settings import BASE_DIR, MEDIA_ROOT
# file_path = "./media/lessons\yeshua.mp4"
# print(file_path)
# # def get_file_length(file_path):
# command = ['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")]
# output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
# duration = float(output)
# print( duration)

# Example usage
# file_path = "path/to/your/video_or_audio_file.mp4"
# length = get_file_length(file_path)
# print("File length:", length, "seconds")


# # 2nd 
# from moviepy.editor import VideoFileClip

# def get_file_length(file_path):
#     clip = VideoFileClip(file_path)
#     duration = clip.duration
#     clip.close()
#     return duration

# # Example usage
# file_path = "path/to/your/video_or_audio_file.mp4"
# length = get_file_length(file_path)
# print("File length:", length, "seconds")



# # filemagic to check file type
# import magic

# def check_file_type(file_path):
#     detector = magic.Magic(mime=True)
#     file_type = detector.from_file(file_path)
#     return file_type

# # Example usage
# file_path = "path/to/your/file"
# file_type = check_file_type(file_path)
# print("File type:", file_type)

import os
# print(os.path.realpath('media'))





list_o = [1,2,3,4,5,6,8]
print(list_o.index(4))