import time

from source2023.huffmanAlgorithm import *
from source2023.imageFunction import *
from source2023.videoFunction import *

videoPath = "../auxiliary2023/OriginalVideos/thema_1.avi"


def videoEncoder():
    """
    Encode the original uncompressed video using Huffman encoding.
    """
    # Read the video
    frames, fps = openVideo(videoPath)
    print(
        f'The video has {len(frames)} frames, a height of {frames[0].shape[0]} pixels, a width of {frames[0].shape[1]}'
        f'pixels and a framerate of {fps} frames per second.')

    # Convert the video to grayscale
    frames = createGrayscaleVideo(frames)

    # # The grayscale original video
    # createVideoOutput(frames, fps, 'thema_1_1_originalGrayScaleVideo.avi')

    originalFrames = []
    seqErrorImages = []

    # Add all the frames to the original frames list
    originalFrames.append(frames)

    H = entropy_score(frames)

    print("Entropy of the original grayscale video is: ", H)

    # Add the first frame to the error frames list (I frame)
    seqErrorImages.append(frames[0])

    # Add the rest of the frames to the error frames list (P(n+1) - P(n) -> frame)
    for P in range(1, len(frames)):
        # Calculate the error image of the current frame
        errorImage = calculateErrorImage(frames[P], frames[P - 1])

        # Add the error image to the error frames list
        seqErrorImages.append(convertToUint8(errorImage))

    # Convert the error frames list to a numpy array
    seqErrorImages = np.array(seqErrorImages, dtype='uint8')

    # Save the video properties to a binary file
    videoSpecs = np.array([len(frames), frames[0].shape[0], frames[0].shape[1], fps], dtype='float64')

    print(f'The video has {len(seqErrorImages)} error frames.')
    start = time.time()
    count = 1
    encodedErrorImages = []
    for frame in seqErrorImages:
        print(f'Encoding error frame {count}...')
        count += 1
        encodedErrorImages.append(huffmanCompression(frame, frame.size))
    end = time.time()
    print(f'Encoding took {end - start} seconds.')

    # Save the encoded error frames to a binary file
    saveVideoInfo(encodedErrorImages, 'thema_1_1_encodedErrorFrames.pkl', videoSpecs, 'thema_1_1_videoSpecs.pkl')


def videoDecoder():
    """
    Decode the encoded video using the dictionary of the Huffman.
    """
    framesNumber, videoSpecs = readVideoInfo('thema_1_1_seqErrorFrames.pkl', 'thema_1_1_videoSpecs.pkl')

    num_frames = int(videoSpecs[0])
    height = int(videoSpecs[1])
    width = int(videoSpecs[2])
    loaded_fps = float(videoSpecs[3])

    print(
        f'The video has {num_frames} frames, a height of {height} pixels, a width of {width} pixels and a framerate of {loaded_fps} frames per second.')

    frames = np.reshape(framesNumber, (num_frames, height, width))

    # Create the output video
    createVideoOutput(frames, loaded_fps, 'thema_1_1_decodedVideo.avi')

    first_frame_flag = True

    decodedFrames = []

    prev_frame = None
    i = 0
    for frame in frames:
        if first_frame_flag:
            decodedFrames.append(frame)
            saveImage(frame, str(i) + '.jpg')
            prev_frame = frame
            first_frame_flag = False
        else:
            decodedFrame = prev_frame + frame  # Add frame to prev_frame
            saveImage(decodedFrame, str(i) + '.jpg')
            decodedFrames.append(decodedFrame)
            prev_frame = decodedFrame
        i += 1

    decodedFrames = np.array(decodedFrames, dtype='uint8')

    createVideoOutput(decodedFrames, videoSpecs[3], 'thema_1_1_decodedVideo.avi')


if __name__ == '__main__':
    videoEncoder()
    videoDecoder()
