import cv2
import numpy as np

def exercise_2(frame):
    height, width, _ = frame.shape

    rows = 3  # Number of rows
    cols = 4  # Number of columns
    new_width = width // cols
    new_height = height // rows
    resized_frame = cv2.resize(frame, (new_width, new_height))
    cv2.imshow("Resized Frame", resized_frame)
    return resized_frame

def exercise_3(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray Frame", gray_frame)
    return gray_frame

def exercise_4(frame):
    upper_left_rel = (0.48, 0.75)
    upper_right_rel = (0.53, 0.75)
    lower_left_rel = (0, 1)
    lower_right_rel = (1, 1)
    new_width = frame.shape[1]
    new_height = frame.shape[0]

    upper_left = (int(new_width * upper_left_rel[0]), int(new_height * upper_left_rel[1]))
    upper_right = (int(new_width * upper_right_rel[0]), int(new_height * upper_right_rel[1]))
    lower_left = (int(new_width * lower_left_rel[0]), int(new_height * lower_left_rel[1]))
    lower_right = (int(new_width * lower_right_rel[0]), int(new_height * lower_right_rel[1]))

    # Create an array of points of the trapezoid
    points = np.array([upper_right, upper_left, lower_left, lower_right], dtype=np.int32)

    # Create an empty black frame
    trapezoid_frame = np.zeros(frame.shape, dtype=np.uint8)

    # Draw the trapezoid on the black frame
    cv2.fillConvexPoly(trapezoid_frame, points, 1)

    # Multiply grayscale frame with trapezoid frame
    road_only_frame = frame * trapezoid_frame

    # Display the frames
    cv2.imshow("Trapezoid Frame", trapezoid_frame * 255)  # Multiply by 255 to visualize
    cv2.imshow("Road Only", road_only_frame)
    return [upper_left, upper_right, lower_right, lower_left]

def exercise_5(frame, trapezoid_bounds):
    # Define corners of the screen (entire frame

    screen_bounds = np.float32([[0, 0], [frame.shape[1], 0], [frame.shape[1], frame.shape[0]], [0, frame.shape[0]]])


    # Convert corners to float32
    trapezoid_bounds = np.float32(trapezoid_bounds)
    screen_bounds = np.float32(screen_bounds)

    # Compute perspective transform matrix
    magic_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, screen_bounds)

    # Apply perspective transform to stretch the cropped street image
    stretched_street_image = cv2.warpPerspective(frame, magic_matrix, (frame.shape[1], frame.shape[0]))

    # Display the stretched street image
    cv2.imshow("Top-Down", stretched_street_image)
    return stretched_street_image

def exercise_6(frame):
    #Apply blur to the frame
    blurred_frame = cv2.blur(frame, ksize=(3, 3))
    #Display the blurred frame
    cv2.imshow("Blur", blurred_frame)
    return blurred_frame

def main():
    cam = cv2.VideoCapture('Lane_Detection_Test_Video_01.mp4')

    # Get the width and height of the frame
    ret, frame = cam.read()
    if not ret:
        print("Error: Cannot read video file.")
        return


    while True:
        ret, frame = cam.read()

        if not ret:
            break

        resized_frame = exercise_2(frame)
        gray_frame = exercise_3(resized_frame)
        trapezoid_bounds = exercise_4(gray_frame)
        stretched_street_frame = exercise_5(gray_frame, trapezoid_bounds)
        exercise_6(stretched_street_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
