import cv2
import numpy as np
import random
import time
import re
from PIL import Image, ImageDraw, ImageFont

# Read sentences from a text file with UTF-8 encoding
def read_sentences_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = [line.strip() for line in file if line.strip()]
    return sentences

# Split sentences at specified characters for line breaks within the same slide
def split_sentence(sentence):
    # Define characters that provoke a line break
    line_break_chars = [',', ';', '.']
    # Use regular expression to split at any of the specified characters followed by a space
    pattern = '|'.join(map(re.escape, line_break_chars))
    parts = re.split(rf'(?<=[{pattern}])\s', sentence)
    return parts

# Create a video with motivational sentences
def create_motivational_video(sentences, output_file_prefix, total_duration=36000, fps=10):
    # Define video parameters
    width, height = 1920, 1080
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Append epoch time to the output file name
    epoch_time = int(time.time())
    output_file = f"{output_file_prefix}_{epoch_time}.mp4"

    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Shuffle the sentences
    random.shuffle(sentences)

    # Calculate total frames needed
    total_frames = total_duration * fps
    frames_written = 0

    for sentence in sentences:
        if frames_written >= total_frames:
            break

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
        font_path = "arial.ttf"  # Specify the path to your font file
        font_size = 40  # Increased font size
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the vertical position for each line
        line_height = 60  # Adjust this value based on your font size and desired spacing
        start_y = (height - len(parts) * line_height) // 2

        # Write-on effect
        for i, part in enumerate(parts):
            if frames_written >= total_frames:
                break

            for j in range(len(part) + 1):
                if frames_written >= total_frames:
                    break

                # Create a new frame for each letter
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                pil_image = Image.fromarray(frame)
                draw = ImageDraw.Draw(pil_image)

                # Display all parts up to the current part
                for k in range(i + 1):
                    current_text = part[:j] if k == i else parts[k]

                    # Calculate text size to center it horizontally
                    text_bbox = draw.textbbox((0, 0), current_text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    text_x = (width - text_width) // 2
                    text_y = start_y + k * line_height

                    # Draw the text on the PIL image
                    draw.text((text_x, text_y), current_text, font=font, fill=color)

                # Convert the PIL image back to an OpenCV image
                frame = np.array(pil_image)

                # Write the frame to the video
                video_writer.write(frame)
                frames_written += 1

                # Display the frame buffer
                cv2.imshow('Frame Buffer', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Hold the final frame for 10 seconds
        hold_frames = 10 * fps
        while frames_written < total_frames and hold_frames > 0:
            video_writer.write(frame)
            frames_written += 1
            hold_frames -= 1

    # Release the video writer
    video_writer.release()
    cv2.destroyAllWindows()

# Main execution
if __name__ == "__main__":
    file_path = 'motivational_sentences.txt'  # Path to your text file
    output_file_prefix = 'motivational_video' # Prefix for the output video file

    sentences = read_sentences_from_file(file_path)
    for _ in range(0, 1):
        create_motivational_video(sentences, output_file_prefix)
