# 🚗 Self-Driving Car Lane Detection with Steering Angle Estimation

This project demonstrates a basic **lane detection system** for self-driving cars using Python and OpenCV. It detects lane lines from a road video, classifies left and right lanes using slopes, and estimates the **steering angle** required for vehicle navigation.

---

## 📌 Features

- **Edge detection** using Canny algorithm
- **Region of Interest (ROI)** masking to focus on road lanes
- **Hough Line Transform** to detect lane lines
- **Slope-based classification** of left vs. right lanes
- **Steering angle estimation** using the average slope of lanes
- **Real-time visualization** with overlaid lines and angle display





---

## 🛠 Tech Stack

- Python 3.x
- OpenCV (`cv2`)
- NumPy

---

## 🚀 Getting Started

### 📦 Requirements

Install dependencies:

```bash
pip install opencv-python numpy
