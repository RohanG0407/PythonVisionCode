from picamera import PiCamera
import time
import sys
sys.path.append('/home/pi/opnecv-3.0.0/include')
import SocketServer
import cv2 
import picamera.array
import numpy as np
import io
import main


#camera = PiCamera()
#camera.start_preview()
time.sleep(2)
vision = main.VisionTargeting(0.1)


def getTarget():        
        return  vision.Loop()

def shutdownPI():
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        return 'we did it';

def captureImgInMemory():
        
       # with picamera.array.PiRGBArray(camera) as stream:
                #camera.resolution = (640, 480)
                # At this point the image is available as stream.array
                #image = stream.array
                #availableimage2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                # cv2.imshow('image2',image2)
        my_stream = io.BytesIO()

        # Camera warm-up time
        camera.capture(my_stream, 'jpeg')
        print my_stream.__sizeof__()
        data = np.fromstring(my_stream.getvalue(), dtype=np.uint8)
        dataIMG = cv2.imdecode(data, 1)
        cv2.imwrite('gggg2.jpg', dataIMG)
        #img = cv2.imread(my_stream,'jpg')
        #img = imread_from_blob(my_stream, 'jpg')
        #cv2.imshow('Image', img)
        return my_stream
                 
def makeGray():
        img = cv2.imread('my_image.jpg')
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('gray_image.jpg', gray_image)        
        return "Image is gray"  

def launchCameraFile():
        my_file =  open('my_image.jpg', 'wb')
        #camera.start_preview()
        #time.sleep(1)
        camera.capture(my_file)
        my_file.close()


def t():
        print "ttt test"

def cameraStuff():
        launchCameraFile()
        return "camera"

def ultraSonic():
        return "ultraSound"

def switch_case(argument):
        switcher = {    
                0: cameraStuff,
                1: ultraSonic,
                2: lambda: "two",
                3: makeGray,
                4: captureImgInMemory,
                5: shutdownPI,
                8: getTarget
        }
        # get function from swither
        func = switcher.get(argument, lambda: "nothing")
        return func()

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
        
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        x = data[0:3]
        print x
        
        if int(x) == 1:
                print "We have the number 1"
        if int(x) == 0:
                print "We have the number 0"
                print switch_case(0)
                print switch_case(3)
        if int(x) == 4:
                capImage = switch_case(4)
                print "Image captured in memory"        
        if int(x) == 5:
                print switch_case(5)

#targeting 
        if int(x) == 8:
                print("get target data")
                socket.sendto(switch_case(8), self.client_address)

                
       # print data[0]
       #        print switch_case(1)
       # if data[0] == 'k':
        #       print "We did it \n"

       # socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    #captureImgInMemory()
    HOST, PORT = "10.0.20.9", 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


