import ffmpeg

def h264_to_custom_format(input_file, output_file, num_threads):
    try:
        # Input video stream
        input_stream = ffmpeg.input(input_file)
        print("input file open")
        # Convert to the desired format - using libx264 codec with a faster preset
        output_stream = ffmpeg.output(input_stream, output_file, codec='libx264', preset='superfast', threads=num_threads)
        print("output stream open")
        
        # Execute the conversion
        ffmpeg.run(output_stream, overwrite_output=True)
        print("Conversion complete.")
    except ffmpeg.Error as e:
        print("An error occurred:", e.stderr)


if __name__ == "__main__":
    input_video = '/home/lab353/dev/videos/smallAprilTags.h264'
    output_video = '/home/lab353/dev/videos/smallAprilTags.avi'
    num_processors = 8  # Set the number of available processors   
    h264_to_custom_format(input_video, output_video, num_processors)