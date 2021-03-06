from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
import sys



#
ball_cascade = cv2.CascadeClassifier('../samples/cascade_v14.xml')
class_scale = 1.01
class_neigh = 10


vs = VideoStream(src=0).start()

time.sleep(2.0)

counter = 260


def directions(direct, near):
	# Direction: -1 left, 0 centre, 1 right, 2 none
	# Near True/False
	s_near = ''
	if near:
		s_near = ' !'
	if direct == -1:
		print '<' + s_near
	elif direct == 1:
		print '>' + s_near
	elif direct == 0:
		print '|' + s_near
	else:
		print 'x'

while True:
	frame = vs.read()
	if frame is None:
		break

	# Resize if needed
	WIDTH = 600 # 600
	HEIGHT = WIDTH *480 / 600
	#frame = imutils.resize(frame, width=WIDTH)
	frame_orig = frame.copy()

	fy = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	balls = ball_cascade.detectMultiScale(fy, class_scale, class_neigh)

	nearest_x = 0
	nearest_y = HEIGHT

	for (x,y,w,h) in balls:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)

		c_x = x + w/2
		c_y = HEIGHT - y + h/2
		if c_y < nearest_y:
			nearest_y = c_y
			nearest_x = c_x
		print x, y, w, h, c_x, c_y
	if nearest_y != HEIGHT:
		near = False
		print nearest_y, HEIGHT * 260 / 480
		if nearest_y < HEIGHT * 260 / 480:
			near = True
		if nearest_x < WIDTH / 8 * 3:
			d = -1
		elif nearest_x > WIDTH / 8 * 5:
			d = 1
		else:
			d = 0
		directions(d, near)
		#print nearest_x, nearest_y
	else:
		directions(2, False)
		#print 'x'


	cv2.imshow("Frame", frame)

	#if len(balls) != 1:
	#	cv2.imwrite("sample%04d.png"%counter, frame_orig)
	#	counter += 1

	key = cv2.waitKey(1) & 0xFF
	if key == ord("c") and len(balls) < 3:
		print "captured", counter
		cv2.imwrite("sample%04d.png"%counter, frame_orig)
		counter += 1
	if key == ord("q"):
		break

vs.stop()

cv2.destroyAllWindows()
