
import cv2
import numpy as np

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def draw_lines(img, lines, color=[255, 0, 0], thickness=5):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def calculate_steering_angle(lines, image_width):
    left_slope_sum = 0
    left_count = 0
    right_slope_sum = 0
    right_count = 0
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            if slope < 0:
                left_slope_sum += slope
                left_count += 1
            else:
                right_slope_sum += slope
                right_count += 1
    
    if left_count > 0:
        avg_left_slope = left_slope_sum / left_count
    else:
        avg_left_slope = 0
    
    if right_count > 0:
        avg_right_slope = right_slope_sum / right_count
    else:
        avg_right_slope = 0
    
    steering_angle = np.arctan((avg_left_slope + avg_right_slope) / 2)
    return np.degrees(steering_angle)

def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny edge detection
    edges = cv2.Canny(blur, 50, 150)
    
    # region of interest 
    height = image.shape[0]
    width = image.shape[1]
    
    # vertices for region of interest
    roi_bottom_left = (0, height)
    roi_top_left = (width * 0.45, height * 0.6)
    roi_top_right = (width * 0.55, height * 0.6)
    roi_bottom_right = (width, height)
    vertices = np.array([[roi_bottom_left, roi_top_left, roi_top_right, roi_bottom_right]], dtype=np.int32)
    
    # Apply region of interest mask
    masked_edges = region_of_interest(edges, vertices)
    
    # Apply Hough transform
    lines = cv2.HoughLinesP(masked_edges, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    
    # Draw lines
    line_image = np.zeros_like(image)
    if lines is not None:
        left_lines = []
        right_lines = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1)
                if slope < 0:
                    left_lines.append(line)
                else:
                    right_lines.append(line)
        
        if left_lines:
            draw_lines(line_image, left_lines, color=[0, 0, 255])  # blue color for the left lanes
        if right_lines:
            draw_lines(line_image, right_lines, color=[0, 255, 0])  #green color for the right lanes
        
        steering_angle = calculate_steering_angle(lines, width)
        cv2.putText(line_image, f'Steering Angle: {steering_angle:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Combine line image with original image
    result = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    
    return result

# Read video
cap = cv2.VideoCapture('test1.mp4')  

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # frame
        processed_frame_default = process_image(frame)
        
        
        cv2.imshow('Lane Detection', processed_frame_default)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()




