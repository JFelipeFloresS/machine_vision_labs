import cv2
import os
import datetime

from utils.file_utils import VIDEO_DIR, IMAGE_DIR

def setup_camera():
    camera = cv2.VideoCapture(0)
    fps = camera.get(cv2.CAP_PROP_FPS)

    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # use current datetime as video filename
    curr_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    video_abspath = os.path.join(VIDEO_DIR, f'{curr_datetime}.avi')
    print(f"Saving video to: {video_abspath}")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_abspath, fourcc, fps, (width, height))
    return camera, out, fps

def capture_video():
    camera, out, fps = setup_camera()
    frame = 0
    recording = False
    while camera.isOpened():
        ret, img = camera.read()
        if not ret:
            break

        if recording:
            frame += 1
            out.write(img)
            cv2.imshow("Camera", img)

        key = cv2.waitKey(1)
        if key%256 == 32:  # SPACE pressed
            recording = not recording
            if recording:
                print("Started recording...")
            else:
                print("Stopped recording.")
        elif key%256 == 27:  # ESC pressed
            print("Exiting...")
            break

    out.release()
    camera.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close

def get_latest_video_path():
    video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.avi')]
    if not video_files:
        return None
    video_files.sort(key=lambda x: os.path.getmtime(os.path.join(VIDEO_DIR, x)), reverse=True)
    latest_video = video_files[0]
    video_path = os.path.join(VIDEO_DIR, latest_video)
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found.")
    print(f"Latest video path: {video_path}")
    return video_path

def get_video(video_path):
    # get all frames from the latest video
    camera = cv2.VideoCapture(video_path)
    fps = camera.get(cv2.CAP_PROP_FPS)
    frame_count = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"FPS: {fps}, Total Frames: {frame_count}")

    if frame_count < 10:
        raise Exception(f"Video has less than 10 frames. Cannot extract the 10th frame. Frame count: {frame_count}")

    return camera

def get_image_path_from_video(video_path):
    video_filename = os.path.basename(video_path)
    image_filename = os.path.splitext(video_filename)[0] + '.jpg'
    image_path = os.path.join(IMAGE_DIR, image_filename)
    return image_path

def generate_image():
    latest_video_path = get_latest_video_path()

    # get all frames from the latest video
    camera = get_video(latest_video_path)

    # Capture the 10th frame and save it as an image with the same name as the video file but with .jpg extension
    camera.set(cv2.CAP_PROP_POS_FRAMES, 9)  # 0-indexed frame
    ret, img = camera.read()
    if ret:
        image_path = get_image_path_from_video(os.path.basename(latest_video_path))
        cv2.imwrite(image_path, img)
        print(f"Saved 10th frame as image: {image_path}")
    else:
        print("Failed to read the 10th frame.")

    camera.release()

def get_latest_image_path():
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')]
    if not image_files:
        return None
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIR, x)), reverse=True)
    latest_image = image_files[0]
    return os.path.join(IMAGE_DIR, latest_image)

def display_image(image_file):
    if image_file:
        print(f"Latest image file: {image_file}")
        img = cv2.imread(image_file)
        cv2.imshow("Latest Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1)  # Force OpenCV to process window events and close
    else:
        print("No image files found.")

def display_latest_image():
    latest_image_path = get_latest_image_path()
    display_image(latest_image_path)