# import the necessary packages
import time
import cv2
import os

def superrize(image, model = "models\\LapSRN_x8.pb"):
	# extract the model name and model scale from the file path
	modelName = model.split(os.path.sep)[-1].split("_")[0].lower()
	modelScale = model.split("_x")[-1]
	modelScale = int(modelScale[:modelScale.find(".")])


	# initialize OpenCV's super resolution DNN object, load the super
	# resolution model from disk, and set the model name and scale
	print("[INFO] loading super resolution model: {}".format(
		model))
	print("[INFO] model name: {}".format(modelName))
	print("[INFO] model scale: {}".format(modelScale))
	sr = cv2.dnn_superres.DnnSuperResImpl_create()
	sr.readModel(model)
	sr.setModel(modelName, modelScale)

	# source_image = "test_img1.jpg"
	# load the input image from disk and display its spatial dimensions
	# image = cv2.imread(source_image)

	print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))
	if image.shape[1] * image.shape[0] >= 220000:
		print(f"Image too large ({image.shape[1]}, {image.shape[0]}) for super resolution, unless if you want to crash your PC, scale it down.")
		return image
	# use the super resolution model to upscale the image, timing how
	# long it takes
	start = time.time()
	upscaled = sr.upsample(image)
	end = time.time()
	print("[INFO] super resolution took {:.6f} seconds".format(
		end - start))
	# show the spatial dimensions of the super resolution image
	print("[INFO] w: {}, h: {}".format(upscaled.shape[1],
		upscaled.shape[0]))


	# resize the image using standard bicubic interpolation
	start = time.time()
	bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]),
		interpolation=cv2.INTER_NEAREST)
	end = time.time()
	print("[INFO] bicubic interpolation took {:.6f} seconds".format(
		end - start))


	# show the original input image, bicubic interpolation image, and
	# super resolution deep learning output
	return upscaled
	# cv2.imshow("Original", image)
	# cv2.imshow("Bicubic", bicubic)
	# cv2.imshow("Super Resolution", cv2.resize(upscaled, (1920, 1080)))
	# cv2.imwrite("bicubic.jpg", bicubic)
	# cv2.imwrite("super.jpg", upscaled)
	# cv2.waitKey(0)