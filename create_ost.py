import os
import random
from pydub import AudioSegment


def combine_mp3_files(input_folder, output_file):
    # Get a list of all MP3 files in the input folder
    mp3_files = [file for file in os.listdir(input_folder) if file.lower().
                 endswith('.mp3')]

    if not mp3_files:
        print("No MP3 files found in the input folder.")
        return

    # Create a list to store AudioSegment objects
    audio_segments = []

    # Load each MP3 file and append it to the list
    for mp3_file in mp3_files:
        file_path = os.path.join(input_folder, mp3_file)
        audio_segments.append(AudioSegment.from_mp3(file_path))

    # Shuffle the list of AudioSegment objects
    random.shuffle(audio_segments)

    # Concatenate all AudioSegment objects into one
    combined_audio = sum(audio_segments)

    # Export the combined audio to the output file
    combined_audio.export(output_file, format="mp3")


if __name__ == "__main__":
    # Specify the input folder containing your MP3 files
    input_folder_path = "assets/enviroment/background-music"

    # Specify the output file for the combined audio
    output_file_path = "assets/enviroment/ost.mp3"

    # Combine MP3 files
    combine_mp3_files(input_folder_path, output_file_path)

    print(f"Combined MP3 files saved to: {output_file_path}")
