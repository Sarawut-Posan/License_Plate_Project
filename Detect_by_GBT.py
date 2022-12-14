import cv2

# Read the image
image = cv2.imread('C:/Users/SP3th/OneDrive/Desktop/License Plate Projecy/lpr/bicycle/bicycle/90.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian blur to the image to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use the Canny edge detection algorithm to find the outlines of objects in the image
edges = cv2.Canny(blurred, 50, 150)

# Find contours in the edged image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop through the contours and filter out any that are not rectangular
for contour in contours:
    if len(contour) != 4:
        continue

    # Compute the bounding box for the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Check if the aspect ratio of the bounding box is approximately equal to 3:1
    # This is a reasonable assumption for a license plate
    if w / h > 3 and w / h < 5:
        # Crop the license plate from the image and save it
        license_plate = image[y:y+h, x:x+w]
        cv2.imwrite('license_plate.jpg', license_plate)