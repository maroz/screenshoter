# screenshoter

A Python project for capturing screenshots from the videostream

## Features

- Start/stop video stream
- Capture screenshots from the video stream

## Requirements
- Python 3.13

## Installation
Install system dependencies:
```bash
$ sudo apt update
$ sudo apt install -y ffmpeg default-jre-headless libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x \
    gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

Install Python dependencies using pip:
```bash
$ pip install -r requirements.txt
```

Install Allure:
```bash
$ wget -O allure_2.34.0-1_all.deb https://github.com/allure-framework/allure2/releases/download/2.34.0/allure_2.34.0-1_all.deb
$ sudo dpkg -i allure_2.34.0-1_all.deb
```


## Usage
Run the application:
```bash
$ python app.py
```

## Testing
Run the tests:
```bash
$ python -m pytest -vv tests/
```

## Generate Allure Report
```bash
$ allure serve allure-results/
```
