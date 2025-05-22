import cv2
import numpy as np
import random
import textwrap
import time
import re

# Read sentences from a text file
def read_sentences_from_file(file_path):
    with open(file_path, 'r') as file:
        sentences = [line.strip() for line in file if line.strip()]
    return sentences

# Split sentences at punctuation marks in the middle
def split_sentence(sentence):
    # Use regular expression to split at punctuation marks not at the end
    parts = re.split(r'(?<!\.\s|\?\s|,\s)(?<=[.,?])\s', sentence)
    return parts

# Create a video with motivational sentences
def create_motivational_video(sentences, output_file_prefix, total_duration=36000, fps=1):
    # Define video parameters
    width, height = 3840, 2160
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Append epoch time to the output file name
    epoch_time = int(time.time())
    output_file = f"{output_file_prefix}_{epoch_time}.mp4"

    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Shuffle the sentences
    random.shuffle(sentences)

    # Calculate duration per sentence
    duration_per_sentence = total_duration // len(sentences)

    for sentence in sentences:
        # Split the sentence into parts
        parts = split_sentence(sentence)

        # Create a black background
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Choose a random color for the text
        color = (
            random.randint(127, 255),
            random.randint(127, 255),
            random.randint(127, 255)
        )

        # Define font settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3  # Increased font size
        thickness = 5

        # Calculate the vertical position for each line
        line_height = 100  # Adjust this value based on your font size and desired spacing
        start_y = (height - len(parts) * line_height) // 2

        for i, part in enumerate(parts):
            # Calculate text size to center it horizontally
            text_size = cv2.getTextSize(part, font, font_scale, thickness)[0]
            text_x = (width - text_size[0]) // 2
            text_y = start_y + i * line_height + text_size[1]

            # Put the text on the frame with anti-aliasing
            cv2.putText(frame, part, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

        # Write the frame to the video
        for _ in range(duration_per_sentence * fps):
            video_writer.write(frame)

    # Release the video writer
    video_writer.release()

# Main execution
if __name__ == "__main__":
    file_path = 'motivational_sentences.txt'  # Path to your text file
    output_file_prefix = 'motivational_video' # Prefix for the output video file

    sentences = read_sentences_from_file(file_path)
    for _ in range(0,10):
        create_motivational_video(sentences, output_file_prefix)
