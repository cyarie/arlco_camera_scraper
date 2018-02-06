import argparse
import librtmp
import requests
import shlex
import subprocess
import sys
from datetime import datetime
from dotenv import load_dotenv
from os import environ
from os.path import join, dirname


def grab_camera_list(api_key, limit):
    # Just grabs and returns a list of traffic cameras in the county.
    api_base_url = "https://api.data.arlingtonva.us/api/v2/"
    camera_list_url = f"{api_base_url}datastreams/TRAFF-CAMER/data.pjson/?auth_key={api_key}&limit={limit}"
    r = requests.get(camera_list_url)

    cameras = r.json().get('result')
    for cam in cameras:
        if cam.get('STATUS') and cam.get('STATUS') == 'ONLINE':
            print(f"Location: {cam['Camera-Encoder']} -- "
                  f"Site: {cam['Camera-Site']} -- "
                  f"Status: {cam['STATUS'].capitalize()}")


def grab_screenshot(second: int, video_name: str):
    # This assumes ffmpeg is installed locally.
    ffmpeg_loc = environ.get('FFMPEG_LOCATION') or '/usr/local/bin/ffmpeg'
    no_ext = video_name.split(".")[0]
    command = f"{ffmpeg_loc} -i {video_name} -ss {second} -vframes 1 {no_ext}_{second}_f1.jpg"
    subprocess.call(shlex.split(command))


def grab_video(camera_num):
    # Setting "frame_length" to 112 will grab about three seconds worth of video,
    # which is plenty. No need to be rude.
    frame = bytearray()
    frame_length = 112
    url = f"rtmp://itsvideo.arlingtonva.us:8001/live/cam{camera_num}.stream"
    conn = librtmp.RTMP(url, live=True)
    conn.connect()
    stream = conn.create_stream()
    dt = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    video_name = f"cam_{camera_num}_{dt}.flv"

    # Iterate through the frame_length range, and assemble a bytearray,
    # which we can write to a file (FLV, in this case)
    for i in range(frame_length):
        data = bytes(stream.read(1024 * 100000))
        for b in data:
            frame.append(b)

    stream.close()

    with open(video_name, 'wb') as f:
        f.write(frame)

    for i in range(1, 3):
        grab_screenshot(i, video_name)


def main():
    # Setup argparse
    parser = argparse.ArgumentParser(description="Tell us which camera you want to grab a still image from.")
    parser.add_argument("-c", "--camera", dest="camera", nargs="?")
    parser.add_argument("-s", "--show_camera_list", dest="show_camera_list", nargs="?")
    parser.add_argument("-l", "--limit", dest="limit", nargs="?")
    args = parser.parse_args()
    camera = args.camera
    camera_list = args.show_camera_list
    list_limit = args.limit or 10

    # Setup the API key
    dotenv_path = join(dirname(__file__), 'keys.env')
    load_dotenv(dotenv_path, verbose=True)
    api_key = environ.get('API_KEY')
    if camera_list:
        grab_camera_list(api_key, list_limit)
        sys.exit(0)

    grab_video(camera)


if __name__ == '__main__':
    main()
