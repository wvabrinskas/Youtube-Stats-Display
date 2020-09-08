# Youtube Stats Display
A youtube stats display in python for use with Tkinter and Raspberry Pi TFT35 touch display

# Hardware
- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- [Pi TFT35 Hat](https://www.amazon.com/SparkFun-LCD-Touchscreen-HAT-Raspberry/dp/B07HNNQZVS)

# Dependencies 
- Tkinter 
- PIL
- Python 3

# Setup 

## OS
- [Raspberry pi OS with Desktop](https://www.raspberrypi.org/downloads/raspberry-pi-os/)

## Hardware
- Enable the pi to use the LCD. 
    1. clone https://github.com/waveshare/LCD-show 
    1. `cd LCD-show`
    1. run `./LCD35-show`

## Code 
- In `yt.py` 
    - replace `CHANNEL_ID` with your Youtube channel id. 
    - replace `API_KEY` with your Youtube api key. 


# Usage 
`python3 yt.py` 
- This will make a full screen app appear over the desktop on the raspberry pi tft screen. You can exit by hitting `F3` on the keyboard or killing the process. 

