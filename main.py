from SimpleCV import *
import time
import os
import math
import sys
import cv2
#from imageInMem import im
import numpy as np

class VisionTargeting(object):

	def __init__(self, speed = 0.1):

		global display
		global count
		global CUSTGREEN_LIST
		global ultraSonic_Dist 
		global text_FontSize
		global MINSATURATION
		global img
		global MINVALUE
		
		display = Display()
		img = cv2.imread('image1.jpg') #Image('%s' % self.image)

		#CUSTOM COLOR CONSTANTS
		
		self.ultraSonic_Dist= 0 
		self.ultraSonic_Dist2 = 0
		self.text_FontSize = 15
		self.speed = speed

	
	def Loop(self):
		global text_FontSize
		global img
		speed = self.speed
		print 'Loop Started'

		global imgorig
		imgorig = img

		while display.isNotDone(): # Breaks loop if SimpleCV gui is exited

			img = imgorig
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			lower_green = np.array([70,150,20])
			upper_green = np.array([95,255,60])
			mask = cv2.inRange(hsv, lower_green, upper_green)
			res = cv2.bitwise_and(img,img,mask=mask)

			img = Image(res)
			green_target = img
			green_target = green_target.rotate(-90)
			green_target = green_target.flipHorizontal()
			green_target = green_target.scale(500,500)
			img_center = (green_target.width/2, green_target.height/2)

			try:	# If blobs are not found... program does not crash...prints "No target found" 

				blobs = green_target.findBlobs()

				## BLOB IDENTIFICATION + ASSIGNMENT

				blob_color = blobs[-1].meanColor()

				blobs[-1].drawMinRect(color=Color.RED, width = 1, alpha = 128)
				blobs[-2].drawMinRect(color=Color.RED, width = 1, alpha = 128)


				top_LeftCorner = blobs[-1].topLeftCorner()
				top_RightCorner = blobs[-1].topRightCorner()
				bottom_LeftCorner = blobs[-1].bottomLeftCorner()
				bottom_RightCorner = blobs[-1].bottomRightCorner()

				top_LeftCorner2 = blobs[-2].topLeftCorner()
				top_RightCorner2 = blobs[-2].topRightCorner()
				bottom_LeftCorner2 = blobs[-2].bottomLeftCorner()
				bottom_RightCorner2 = blobs[-2].bottomRightCorner()


				tlc_List = list(top_LeftCorner)
				trc_List = list(top_RightCorner)
				blc_List = list(bottom_LeftCorner)
				brc_List = list(bottom_RightCorner)

				tlc_List2 = list(top_LeftCorner2)
				trc_List2 = list(top_RightCorner2)
				blc_List2 = list(bottom_LeftCorner2)
				brc_List2 = list(bottom_RightCorner2)

				blobs_bottom_length = blc_List[0] - brc_List2[0]
				blobs_bottom_length = blobs_bottom_length / 2
				blobs_middle_height = trc_List[0] - tlc_List2[0]
				blobs_middle_height = blobs_middle_height / 2

				boundingBox_length = trc_List[0] - tlc_List[0]
				boundingBox_width = brc_List[1] - trc_List[1]
				boundingBox_length2 = trc_List2[0] - tlc_List2[0]
				boundingBox_width2 = brc_List2[1] - trc_List2[1]

				bb_size = (boundingBox_length ** 2) + (boundingBox_width ** 2) # a^2 + b^2 = c^2
				bb_size = sqrt(bb_size) #hypotenuse
				bb_size2 = (boundingBox_length2 ** 2) + (boundingBox_width2 ** 2) # a^2 + b^2 = c^2
				bb_size2 = sqrt(bb_size2) #hypotenuse

				## DISTANCE FINDER

				self.ultraSonic_Dist = 293.027302482 / bb_size # PEGS DISTANCE 293 pixels for 1 foot
				self.ultraSonic_Dist = round(self.ultraSonic_Dist, 2)
				self.ultraSonic_Dist2 = 293.027302482 / bb_size2 # PEGS DISTANCE 293 pixels for 1 foot
				self.ultraSonic_Dist2 = round(self.ultraSonic_Dist2, 2)

				adjusted_y = tlc_List[1] - 17
				adjusted2_y = tlc_List2[1] - 17        # Adjusted Y axis for text to show in a better location

				x_center = (brc_List2[0] - blc_List[0]) / 2
				x_center += blc_List[0]
				y_center = (blc_List[1] - tlc_List[1]) / 2
				y_center += tlc_List[1]
				target_center = (x_center, y_center)

				print y_center

				if tlc_List[0] < trc_List2[0]:
					x_center = (brc_List[0] - blc_List2[0]) / 2
					x_center += blc_List2[0]
					y_center = (blc_List2[1] - tlc_List2[1]) / 2
					y_center += tlc_List2[1]
					target_center = (x_center, y_center)


				blob_center = (blobs[-1].minRectX(), blobs[-1].minRectY())
				blob_center2 = (blobs[-2].minRectX(), blobs[-2].minRectY())       # Identify center of bounding box

				angle_OppSide = abs(250 - x_center)
				angle_AdjSide = abs(250 - y_center)
				angle_Tangent = float(angle_OppSide)/float(angle_AdjSide)
				angle_Tangent =  math.tan(angle_Tangent)
				angle_Tangent = math.atan(angle_Tangent)
				angle_Tangent = math.degrees(angle_Tangent)
				angle_Tangent = round(angle_Tangent, 2)

				print angle_AdjSide

				if (250) > x_center:
					angle_Tangent -= (angle_Tangent * 2)


				## DRAWING LAYERS

				green_target.dl().selectFont('consolas')
				green_target.dl().circle((blob_center), 4, color = Color.BLUE)  # Bounding BOX Center Circle - BLUE
				green_target.dl().circle((blob_center2), 4, color = Color.BLUE)  # Bounding BOX Center Circle - BLUE
				green_target.dl().circle((img_center), 2, color = Color.YELLOW) # Image Center Circle - YELLOW
				#green_target.drawText(text = str(self.ultraSonic_Dist) + " ft", x = tlc_List[0], y = adjusted_y, color = Color.WHITE, fontsize = self.text_FontSize) #Draws distance text for biggest blob
				#green_target.drawText(text = str(self.ultraSonic_Dist2) + " ft", x = tlc_List2[0], y = adjusted2_y, color = Color.WHITE, fontsize = self.text_FontSize) #Draws distance text for second small blob
				green_target.dl().circle((target_center), 3, color = Color.RED) #Draws a circle at center of 2 targets, represents peg location
				green_target.dl().line((target_center), (img_center), color = Color.RED, width = 1) # Draws the hypotenuse
				#green_target.dl().line((0,250), (500,250), color = Color.WHITE, width = 1) # Draws x axis
				#green_target.dl().line((250,0), (250, 500), color = Color.WHITE, width = 1) # Draws y axis
				green_target.dl().line((target_center), (x_center, 250), color = Color.RED, width = 1) # Opposite Side
				green_target.dl().line((x_center, 250), (250,250), color = Color.RED, width = 1) # Adjacent Side
				green_target.drawText(text = str(angle_Tangent) + "", x = 255, y = 250, color = Color.WHITE, fontsize = self.text_FontSize)

				

			except Exception as e:
				print e
				print 'NoneType Error = No Blob found --- Else refer above'
				return '*008*Angle*%s*Distance*%s*' %(0,0)

			green_target.save('Output.png') # Overwriting save if loop is commented
			green_target.show()
			#print 'saved!'
			time.sleep(speed) # Decrease Values for a smoother image rendering + faster CON - Heavy load on CPU 
			print 'Loop Ran'
			
			#return '008*Angle*%s*Distance*%s*' % (angle_Tangent, self.ultraSonic_Dist2) 


if __name__ == "__main__":
	VisionTargeting1 = VisionTargeting(0.1)
	print VisionTargeting1.Loop()





		

	
