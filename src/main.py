import cv2, queue, threading, time
import numpy as np

# video capture object
class VideoCapture:

	# constructor
	def __init__(self, name):
		
		# create new video capture
		self.cap = cv2.VideoCapture(name)
		
		# modify frame width 480p
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)

		# worker thread's queue
		self.q = queue.Queue()

		# worker thread runs the _reader method
		t = threading.Thread(target=self._reader)

		# daemon runs in the background
		t.daemon = True

		# start the thread
		t.start()

	# Worker Thread Method
	def _reader(self):

		# worker thread loop forever
		while True:
			
			# acquire image from capture object
			ret, frame = self.cap.read()
			
			# if no image was aquired, then try again
			if not ret:
				break
			
			# if the queue is not empty
			if not self.q.empty():
				# try to remove the old (unprocessed) frame
				try:
					self.q.get_nowait()
				# otherwise continue
				except queue.Empty:
					pass
			
			# add the new frame to the queue
			self.q.put(frame)

	# return the new frame to the main thread
	def read(self):
		return self.q.get()

# Transform Color Image into Black and White Image
def transformImg(img):
	
	# convert to grayscale
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# convert to black and white
	(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
	
	# mirror the image
	img = cv2.flip(img, 1)

	# crop the image
	img = img[0:480,0:480]
	
	return img

# Draw Lines on the Provided Image
def drawLines(img):

	# copy img
	dispImg = img.copy()

	# vertical lines
	cv2.line(dispImg,(120,0),(120,480),(255,255,255))
	cv2.line(dispImg,(240,0),(240,480),(255,255,255))
	cv2.line(dispImg,(360,0),(360,480),(255,255,255))

	# horizontal lines
	cv2.line(dispImg,(0,120),(480,120),(255,255,255))
	cv2.line(dispImg,(0,240),(480,240),(255,255,255))
	cv2.line(dispImg,(0,360),(480,360),(255,255,255))

	return dispImg

# Get the downsampled image
def getSubImage(img):
	
	results = np.ndarray(16)
	
	ctr = 0

	for row in range(0,480,120):
		for col in range(0,480,120):

			# sum up the white pixels
			totalNumWhite = img[row:row+120,col:col+120].sum() / 255

			# if more than half are white, the sub image is white
			results[ctr] = 255 if totalNumWhite >= 7200 else 0

			# increment counter
			ctr += 1

	return results

if __name__ == "__main__":

	# create a video capture object
	cap = VideoCapture(0)
	
	while True:
		img = transformImg(cap.read())

		# draw lines on image
		dispImg = drawLines(img)

		# show image
		cv2.imshow("image", dispImg)

		# get primary color of subimages
		results = getSubImage(img)

		# show the downsampled image
		cv2.imshow("result", results.reshape(4,4))

		# quit if q key is pressed
		if chr(cv2.waitKey(1)&255) == 'q':
			break
