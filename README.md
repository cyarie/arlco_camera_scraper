# ARLCo Camera Scraper
## How-to Use
### Installation
_Note: tested against Python 3.6.0 only, on OS X_

1. Setup a virtualenv with Python 3.6 as your base Python
2. Use pip to install the requirements: `pip install -r requirements.txt`
3. Make a copy of the `keys.example.env` file, and name it `keys.env`
4. Replace the example key with a copy of a real API key from the County's [developer's page](https://data.arlingtonva.us/developers/)
5. Setup [ffmpeg](https://www.ffmpeg.org/)
6. Replace FFMPEG_LOCATION in keys.env with the location of your ffmpeg binary

### Args
* `-c` or `--camera`: An integer representing the camera number you want to grab screenshots from
  * Example: `python main.py -c 1`
* `-s` or `--show_camera_list`: Enter `True` if you want to return a list of cameras from the County's open data API
  * Example: `python main.py --show_camera_list=True`
* `-l` or `--limit`: An integer representing the maximum number of cameras to return from `--show_camera_list`
  * Example: `python main.py --show_camera_list=True -l 15`