import cv2

image = cv2.imread('muichiro_white_bg_crop_02.jpg')
# image = cv2.imread('nezuko_test.png')

img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
img = cv2.bitwise_and(image, image, mask=mask_inv)

def run(image, mask):
  """
  Takes in an image and a mask, then opens the webcam and takes a picture.
  The region within the mask uses the given picture, and the rest of the region is captured by the webcam.
  When the camera opens, the masked region should show in front.

  Args:
    image: The image to be used in the masked region.
    mask: The mask to be used to define the masked region.
  """

  # Open the webcam
  cap = cv2.VideoCapture(0)

  # Check if the webcam is open
  if not cap.isOpened():
    raise RuntimeError("Error opening webcam")

  # Get the width and height of the webcam frame
  frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

  # Resize the image and mask to match the webcam frame size
  image = cv2.resize(image, (int(frame_width), int(frame_height)))
  mask = cv2.resize(mask, (int(frame_width), int(frame_height)))

  # Start the webcam loop
  while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
      break

    # Apply the mask to the frame
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Add the masked image to the masked frame
    final_frame = cv2.add(masked_frame, image)

    # Display the final frame
    cv2.imshow("Webcam", final_frame)

    # Check if the user pressed the Esc key to quit
    if cv2.waitKey(1) == 27:
      cv2.imwrite('result.jpg', final_frame)
      break

  # Release the webcam
  cap.release()

  # Destroy all windows
  cv2.destroyAllWindows()

run(img, mask)
