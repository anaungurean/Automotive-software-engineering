import cv2
import object_socket
import numpy as np
q
def exercise_2(frame):
    height, width, _ = frame.shape
    rows = 3
    cols = 4
    new_width = width // cols
    new_height = height // rows
    resized_frame = cv2.resize(frame, (new_width, new_height))
    # cv2.imshow("Small", resized_frame)
    return resized_frame

def exercise_3(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray Frame", gray_frame)
    return gray_frame

def exercise_4(frame):
    upper_left_rel = (0.44, 0.77)
    upper_right_rel = (0.57, 0.77)
    lower_left_rel = (0.03, 1)
    lower_right_rel = (1, 1)
    new_width = frame.shape[1]
    new_height = frame.shape[0]

    upper_left = (int(new_width * upper_left_rel[0]), int(new_height * upper_left_rel[1]))
    upper_right = (int(new_width * upper_right_rel[0]), int(new_height * upper_right_rel[1]))
    lower_left = (int(new_width * lower_left_rel[0]), int(new_height * lower_left_rel[1]))
    lower_right = (int(new_width * lower_right_rel[0]), int(new_height * lower_right_rel[1]))

    points = np.array([upper_right, upper_left, lower_left, lower_right], dtype=np.int32)

    trapezoid_frame = np.zeros(frame.shape, dtype=np.uint8)
    cv2.fillConvexPoly(trapezoid_frame, points, 1)

    road_only_frame = frame * trapezoid_frame

    # cv2.imshow("Trapezoid Frame", trapezoid_frame * 255)
    # cv2.imshow("Road Only", road_only_frame)

    return [upper_left, upper_right, lower_right, lower_left]

def exercise_5(frame, trapezoid_bounds):

    screen_bounds = np.float32([[0, 0], [frame.shape[1], 0], [frame.shape[1], frame.shape[0]], [0, frame.shape[0]]])
    trapezoid_bounds = np.float32(trapezoid_bounds)
    screen_bounds = np.float32(screen_bounds)

    magic_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, screen_bounds)
    stretched_street_image = cv2.warpPerspective(frame, magic_matrix, (frame.shape[1], frame.shape[0]))

    # cv2.imshow("Top-Down", stretched_street_image)
    return stretched_street_image

def exercise_6(frame):
    blurred_frame = cv2.blur(frame, ksize=(3, 3))
    # cv2.imshow("Blur", blurred_frame)
    return blurred_frame

def exercise_7(frame):
    sobel_vertical = np.float32([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    sobel_horizontal = np.transpose(sobel_vertical)
    frame_as_float = np.float32(frame)
    gradient_x = cv2.filter2D(frame_as_float, -1, sobel_horizontal)
    gradient_y = cv2.filter2D(frame_as_float, -1, sobel_vertical)
    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude, gradient_magnitude)
    # cv2.imshow("Sobel", gradient_magnitude)
    return gradient_magnitude

def exercise_8(frame):
    threshold_value =  int(255/2 - 30)
    _, thresholded_frame = cv2.threshold(frame, threshold_value, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Binarized", thresholded_frame)
    return thresholded_frame


def exercise_9(frame):
    clean_frame = frame.copy()
    height, width = frame.shape
    black_columns = int(width * 0.05)
    clean_frame[:, :black_columns] = 0
    clean_frame[:, -black_columns:] = 0

    left_half = clean_frame[:, :width // 2]
    right_half = clean_frame[:, width // 2:]

    white_pixels_left = np.argwhere(left_half > 0)
    left_xs = white_pixels_left[:, 1]
    left_ys = white_pixels_left[:, 0]

    white_pixels_right = np.argwhere(right_half > 0)
    right_xs = white_pixels_right[:, 1] + width // 2
    right_ys = white_pixels_right[:, 0]

    return left_xs, left_ys, right_xs, right_ys


def exercise_10(trapezoid_bounds, resized_frame, frame, left_xs, left_ys, right_xs, right_ys, last_valid_left_top, last_valid_left_bottom, last_valid_right_top, last_valid_right_bottom):

    left_coefficients = np.polynomial.polynomial.polyfit(left_xs, left_ys, 1)
    left_b, left_a = left_coefficients[0], left_coefficients[1]

    right_coefficients = np.polynomial.polynomial.polyfit(right_xs, right_ys, 1)
    right_b, right_a = right_coefficients[0], right_coefficients[1]

    height, width = frame.shape[:2]

    bottom_y = 0
    top_y = height

    left_bottom_x = int((bottom_y - left_b) / left_a)
    left_top_x = int((top_y - left_b) / left_a)

    right_bottom_x = int((bottom_y - right_b) / right_a)
    right_top_x = int((top_y - right_b) / right_a)

    if not left_bottom_x in range(-10**8, 10**8):
        left_bottom_x = last_valid_left_bottom[0]

    if not left_top_x in range(-10**8, 10**8):
        left_top_x = last_valid_left_top[0]

    if not right_bottom_x in range(-10**8, 10**8):
        right_bottom_x = last_valid_right_bottom[0]

    if not right_top_x in range(-10**8, 10**8):
        right_top_x = last_valid_right_top[0]

    last_valid_left_top = (left_top_x, top_y)
    last_valid_left_bottom = (left_bottom_x, bottom_y)
    last_valid_right_top = (right_top_x, top_y)
    last_valid_right_bottom = (right_bottom_x, bottom_y)

    left_top = int(left_top_x), int(top_y)
    left_bottom = int(left_bottom_x), int(bottom_y)
    right_top = int(right_top_x), int(top_y)
    right_bottom = int(right_bottom_x), int(bottom_y)

    cv2.line(frame, left_top, left_bottom, (200, 0, 0), 5)
    cv2.line(frame, right_top, right_bottom, (100, 0, 0), 5)
    # cv2.imshow("Lines", frame)

    #Exercise 11
    left_final_frame = np.zeros(resized_frame.shape, dtype=np.uint8)
    cv2.line(left_final_frame , left_top, left_bottom, (255, 0, 0), 3)
    screen_bounds = np.float32([[0, 0], [frame.shape[1], 0], [frame.shape[1], frame.shape[0]], [0, frame.shape[0]]])
    trapezoid_bounds = np.float32(trapezoid_bounds)
    transform_matrix_top_down = cv2.getPerspectiveTransform(screen_bounds,  trapezoid_bounds)
    stretched_final_frame_left = cv2.warpPerspective(left_final_frame, transform_matrix_top_down, (frame.shape[1], frame.shape[0]))

    white_pixels = np.argwhere(stretched_final_frame_left > 0)
    left_white_xs = white_pixels[:, 1]
    left_white_ys = white_pixels[:, 0]

    right_final_frame = np.zeros(resized_frame.shape, dtype=np.uint8)
    cv2.line(right_final_frame, right_top, right_bottom, (255, 0, 0), 10)
    stretched_final_frame_right = cv2.warpPerspective(right_final_frame, transform_matrix_top_down, (frame.shape[1], frame.shape[0]))

    white_pixels = np.argwhere(stretched_final_frame_right > 0)
    right_white_xs = white_pixels[:, 1]
    right_white_ys = white_pixels[:, 0]

    colored_frame = resized_frame.copy()
    colored_frame[left_white_ys, left_white_xs] = (50,50,250)
    colored_frame[right_white_ys, right_white_xs] = (50, 250, 50)
    cv2.imshow("Final", colored_frame)



def old_code(frame):
    resized_frame = exercise_2(frame)
    gray_frame = exercise_3(resized_frame)
    trapezoid_bounds = exercise_4(gray_frame)
    stretched_street_frame = exercise_5(gray_frame, trapezoid_bounds)
    blurred_frame = exercise_6(stretched_street_frame)
    gradient_magnitude = exercise_7(blurred_frame)
    thresholded_frame = exercise_8(gradient_magnitude)
    left_xs, left_ys, right_xs, right_ys = exercise_9(thresholded_frame)
    exercise_10(trapezoid_bounds, resized_frame, thresholded_frame, left_xs, left_ys, right_xs, right_ys,
    last_valid_left_top, last_valid_left_bottom, last_valid_right_top, last_valid_right_bottom)




last_valid_left_top = (0, 0)
last_valid_left_bottom = (0, 0)
last_valid_right_top = (0, 0)
last_valid_right_bottom = (0, 0)

s = object_socket.ObjectReceiverSocket('127.0.0.1', 5000, print_when_connecting_to_sender=True, print_when_receiving_object=True)

while True:
    ret, frame = s.recv_object()
    if not ret:
        break

    # cv2.imshow('Frame', frame)
    old_code(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# for i in range(5):
#     a = s.recv()
#
#     print(f'\n--- {i} ---\n')
#     print(a)


















