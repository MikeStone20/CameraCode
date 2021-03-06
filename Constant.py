# File: Constant.py
# Creator: Yihan Zhang, yz2567@columbia.edu
#
# This file handles all the constants used in the camera time-lapse system

# The ID of the web-cam used.
# If used in a labtop with a built-in web-cam, this number is likely to be 1 instead of 0
# But how the system assign these numbers remain a mistery to me
CAMERA_ID = 2

CAMERA_ID2 = 0

# This is the default interval of taking pictures
DEFAULT_SAVE_INTERVAL = 15*60
DEFAULT_LED_ON_TIME = DEFAULT_SAVE_INTERVAL - 8
DEFAULT_LED_OFF_TIME = DEFAULT_SAVE_INTERVAL + 1

# The default position of saving the images as well as the file name prefix
FILE_PREFIX = "C:\\Users\Michael\Desktop\pics"
FILE_PREFIX_2 = "C:\\Users\Michael\Desktop\pics"

# The output picture compression level. 0 means no compression, 9 means maximum compression
PNG_COMPRESSION_LEVEL = 5

# Display resolution
SCREEN_DISPLAY_RES = (720, 405)

# Picture saving resolution
PIC_SAVE_RES = (1920, 1080)

# Raw capture resolution
RAW_CAPTURE_RES = (1920, 1080)

# The baud rate of the serial commnication between arduino
ARD_BAUDRATE = 9600

# The port used by arduino
ARD_PORT = 'COM3'

# Time out for initial communication with arduino
ARD_TIMEOUT = 0.1
