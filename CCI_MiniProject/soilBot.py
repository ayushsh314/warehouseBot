import cv2
import numpy as np
img = cv2.imread('area.JPG')

# cv2.imshow("Read image",img)
# cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# Find Canny edges
edged = cv2.Canny(gray, 1200, 200)
# cv2.waitKey(0)
  

contours, hierarchy = cv2.findContours(edged, 
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 5) 

#         n = approx.ravel() 
#         i = 0
  
#         for j in n :
#             if(i % 2 == 0):
#                 x = n[i]
#                 y = n[i + 1]
  
#             # String containing the co-ordinates.
#                 string = str(x) + " " + str(y) 
  
#                 if(i == 0):
#                 # text on topmost co-ordinate.
#                     cv2.putText(img, "Arrow tip", (x, y),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0)) 
#                 else:
#                 # text on remaining co-ordinates.
#                     cv2.putText(img, string, (x, y),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0)) 
#             i = i + 1
  
cv2.imshow('Contours', img)
cv2.waitKey(0)
# cv2.destroyAllWindows()

#harris corner
import cv2
import numpy as np
img = cv2.imread('area.JPG')
operatedImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
# modify the data type
# setting to 32-bit floating point
operatedImage = np.float32(operatedImage)
 
# apply the cv2.cornerHarris method
# to detect the corners with appropriate
# values as input parameters
dest = cv2.cornerHarris(operatedImage, 2, 5, 0.07)
 
# Results are marked through the dilated corners
dest = cv2.dilate(dest, None)
 
# Reverting back to the original image,
# with optimal threshold value
img[dest > 0.01 * dest.max()]=[0, 0, 255]
 
# the window showing output image with corners
cv2.imshow('Image with Borders', img)

cv2.waitKey(0)


#hough

import cv2
import numpy as np
  
# Read image.
img = cv2.imread('area.jpg', cv2.IMREAD_COLOR)
  
# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))

edged = cv2.Canny(gray_blurred,1200,100)
# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred, 
                   cv2.HOUGH_GRADIENT, 1, 50, param1 = 50,
               param2 = 30, minRadius = 1, maxRadius = 40)
  
# Draw circles that are detected.
# if detected_circles is not None:
  
    # Convert the circle parameters a, b and r to integers.
detected_circles = np.uint16(np.around(detected_circles))
print(detected_circles[0])

def dis(x1,y1,x2,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

# for i in detected_circles:
#     if()

for pt in detected_circles[0, :]:
    a, b, r = pt[0], pt[1], pt[2]

    # Draw the circumference of the circle.
    cv2.circle(img, (a, b), r, (0, 255, 0), 2)

    # Draw a small circle (of radius 1) to show the center.
    #cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
    cv2.imshow("Detected Circle", img)
    cv2.waitKey(0)