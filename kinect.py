#!/usr/bin/python
from freenect import sync_get_video as get_video
from freenect import sync_get_depth as get_depth
import box_tracker
import cv2
import sys


def draw_face(d, output, color):
    scale_x = (d[0] + d[2] - d[0]) / 4
    scale_y = (d[1] + d[3] - d[1]) / 4
    cv2.line(output, (d[0], d[1]), (d[0] + scale_x, d[1]), color)
    cv2.line(output, (d[0], d[1]), (d[0], d[1] + scale_y), color)
    cv2.line(output, (d[0] + d[2], d[1]), (d[0] + d[2] - scale_x, d[1]), color)
    cv2.line(output, (d[0] + d[2], d[1]), (d[0] + d[2], d[1] + scale_y), color)
    cv2.line(output, (d[0], d[1] + d[3]), (d[0] + scale_x, d[1] + d[3]), color)
    cv2.line(output, (d[0], d[1] + d[3]), (d[0], d[1] + d[3] - scale_y), color)
    cv2.line(output, (d[0] + d[2], d[1] + d[3]),
             (d[0] + d[2] - scale_x, d[1] + d[3]), color)
    cv2.line(output, (d[0] + d[2], d[1] + d[3]),
             (d[0] + d[2], d[1] + d[3] - scale_y), color)


def get_kinect():
    image, _ = get_video()
    depth, _ = get_depth()
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, depth


def detect_and_draw_faces(input, output, tracker):
    gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for face in faces:
        face_center = box_tracker.get_center(face)
        tracker.update_box(face, depth[face_center[1], face_center[0]])

    for box in tracker.get_boxes():
        scale = (float(box['rect'][2]) / input.shape[1]) * 3
        draw_face(box['rect'], output, box['color'])
        cv2.putText(output, str(
            box['depth']), (box['rect'][0], box['rect'][1]), font, scale, (200, 255, 155), 2)


def merge_and_show(image1, image2, alpha=0.5):
    cv2.addWeighted(image2, alpha, image1, 1 - alpha, 0, image1)
    cv2.imshow("camera", image1)
    cv2.waitKey(5)


if __name__ == '__main__':
    cascadePath = "haarcascade_frontalface_alt2.xml"
    face_cascade = cv2.CascadeClassifier(cascadePath)
    alpha = 0.5
    tracker = box_tracker.BoxTracker()
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        try:
            image, depth = get_kinect()
            blank_image = image.copy()

            tracker.init_frame()

            detect_and_draw_faces(image, blank_image, tracker)

            merge_and_show(image, blank_image)
        except KeyboardInterrupt:
            sys.exit(1)
