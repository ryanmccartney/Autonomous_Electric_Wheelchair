#import the necessary modules
import freenect
import time
import os
import cv2
import numpy as np
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array


os.system ("sudo killall mjpg_streamer")

#Set stream framerate
fps = 2
delay = 1/fps

loading = cv2.imread('/var/www/html/media/loading.jpg',1)
cv2.imwrite('/var/www/html/stream/image.jpg',loading)

os.system ("sudo mount -t tmpfs tmpfs /var/www/html/stream")
os.system ("export LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer-experimental")
os.system ("mjpg_streamer -o 'output_http.so -w ./www/html' -i 'input_file.so -f /var/www/html/stream/ -r'")

print("STATUS: Starting Stream...")

if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        image = get_video()
        #get a frame from depth sensor
        depth = get_depth()
        #write RGB image to file
        cv2.imwrite('/var/www/html/stream/image.jpg',image)
        #write depth image to file
        #cv2.imwrite('/var/www//html/stream/depthImage.jpg',depth)

        #frame delay
        time.sleep(delay)
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    os.system ("sudo killall mjpg_streamer")