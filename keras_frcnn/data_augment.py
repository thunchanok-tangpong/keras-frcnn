import cv2
import numpy as np
import copy
from osgeo import gdal

def augment(img_data, config, augment=True):
	assert 'filepath' in img_data
	assert 'bboxes' in img_data
	assert 'width' in img_data
	assert 'height' in img_data

	img_data_aug = copy.deepcopy(img_data)
	# for 1 band img
	# img = cv2.imread(img_data_aug['filepath'], -1)
	# _, img = cv2.threshold(img, 0, 1, cv2.THRESH_TOZERO)
	# img = img * 255
	# img=img.astype(np.uint8)
	# img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

	# for rgb
	# img = cv2.imread(img_data_aug['filepath'])

	# for 5 band
	
	# print(img_data_aug['filepath'])
	inRas1 = gdal.Open(img_data_aug['filepath'])
	myarray1 = inRas1.ReadAsArray()
	myarray1=myarray1*255
	myarray1=myarray1.astype(np.uint8)
	
	img=myarray1
	if augment:
		# rows, cols = img.shape[:2]
		rows, cols = img.shape[1:3]

		if config.use_horizontal_flips and np.random.randint(0, 2) == 0:
			img = cv2.flip(img, 1)
			for bbox in img_data_aug['bboxes']:
				x1 = bbox['x1']
				x2 = bbox['x2']
				bbox['x2'] = cols - x1
				bbox['x1'] = cols - x2

		if config.use_vertical_flips and np.random.randint(0, 2) == 0:
			img = cv2.flip(img, 0)
			for bbox in img_data_aug['bboxes']:
				y1 = bbox['y1']
				y2 = bbox['y2']
				bbox['y2'] = rows - y1
				bbox['y1'] = rows - y2

		if config.rot_90:
			angle = np.random.choice([0,90,180,270],1)[0]
			if angle == 270:
				img = np.transpose(img, (1,0,2))
				img = cv2.flip(img, 0)
			elif angle == 180:
				img = cv2.flip(img, -1)
			elif angle == 90:
				img = np.transpose(img, (1,0,2))
				img = cv2.flip(img, 1)
			elif angle == 0:
				pass

			for bbox in img_data_aug['bboxes']:
				x1 = bbox['x1']
				x2 = bbox['x2']
				y1 = bbox['y1']
				y2 = bbox['y2']
				if angle == 270:
					bbox['x1'] = y1
					bbox['x2'] = y2
					bbox['y1'] = cols - x2
					bbox['y2'] = cols - x1
				elif angle == 180:
					bbox['x2'] = cols - x1
					bbox['x1'] = cols - x2
					bbox['y2'] = rows - y1
					bbox['y1'] = rows - y2
				elif angle == 90:
					bbox['x1'] = rows - y2
					bbox['x2'] = rows - y1
					bbox['y1'] = x1
					bbox['y2'] = x2        
				elif angle == 0:
					pass

	# img_data_aug['width'] = img.shape[1]
	# img_data_aug['height'] = img.shape[0]
	img_data_aug['width'] = img.shape[2]
	img_data_aug['height'] = img.shape[1]
	print(myarray1.shape)
	return img_data_aug, img
