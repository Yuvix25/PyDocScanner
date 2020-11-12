import cv2
import imutils
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local
from super_reso import superrize
from ocr import ocr
import numpy as np


def remove_small(img):
    img = 255 - img
    #find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
    #connectedComponentswithStats yields every seperated component with information on each of them, such as size
    #the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
    sizes = stats[1:, -1]; nb_components = nb_components - 1

    # minimum size of particles we want to keep (number of pixels)
    #here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
    min_size = 15

    #your answer image
    img2 = np.zeros((output.shape))
    #for every component in the image, you keep it only if it's above min_size
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255
    return 255 - img2

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it

def Scan(image, apply_color_filter=True, do_super_reso=True, do_ocr=True):
    """Scan a document from image and extract text from it.  
    image - image to scan doc from.  
    apply_color_filter - convert to strong black and white color output.  
    do_super_reso - increase output resolution (also improves OCR).  
    do_ocr - return also text detected in the document.  """
    orig = image.copy()
    ratio = orig.shape[0] / 500.0
    image = imutils.resize(image, height=500)
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    # show the original image and the edge detected image
    print("STEP 1: Edge Detection")
    cv2.imshow("Image", image)
    cv2.imshow("Edged", edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    screenCnt = -1
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    if type(screenCnt) == int:
        print("No contours found.")
        return None
    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], 0, (0, 255, 0), 2)
    cv2.imshow("Outline", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    if do_super_reso:
        warped = superrize(warped)
    
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    if apply_color_filter:
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset = 13, method = "gaussian")
        warped = (warped > T).astype("uint8") * 255

        kernel = np.ones((2, 2), np.uint8)
        warped = cv2.erode(warped, kernel)

        warped = remove_small(warped)

        cv2.imshow("Scanned", imutils.resize(warped, height = 900))
        cv2.waitKey(0)

        cv2.imwrite("temp.jpg", warped)
        warped = cv2.blur(cv2.imread("temp.jpg"), (2, 2))

        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        

        # show the original and scanned images
        print("STEP 3: Apply perspective transform")
        cv2.imshow("Scanned", imutils.resize(warped, height = 900))
        # cv2.imshow("Scanned", imutils.resize(warped, height = 650))
        cv2.waitKey(0)
    else:
        cv2.imshow("Scanned", imutils.resize(warped, height = 900))
        cv2.waitKey(0)
    if do_ocr:
        return warped, ocr(warped)
    else:
        return warped


if __name__ == "__main__":
    image = cv2.imread("./test_image1.png")
    print(Scan(image, True, False, True)[1])