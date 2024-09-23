import os
from moviepy.editor import AudioFileClip

# path to the webm file
input_folder = "path_of_webm_file"
# name of the mp3 file to save as output
output_folder = "path_of_mp3_file"

# create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# convert for each file in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".webm"):
        webm_file = os.path.join(input_folder, filename)
        mp3_file = os.path.join(output_folder, filename.replace(".webm", ".mp3"))
        
        # save the audio file as mp3
        try:
            audio_clip = AudioFileClip(webm_file)
            audio_clip.write_audiofile(mp3_file, codec='mp3')
            print(f"Conversion successful! MP3 file: {mp3_file}")
        except Exception as e:
            print(f"Error with {filename}: {e}")
