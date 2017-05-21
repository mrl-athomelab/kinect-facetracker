#!/usr/bin/env python
from freenect import sync_get_video as get_video
from freenect import sync_get_depth as get_depth
from box_tracker import box_tracker
import cv2
import sys

cascadePath = "haarcascade_frontalface_alt2.xml"
face_cascade = cv2.CascadeClassifier(cascadePath)
alpha = 0.5
tracker = box_tracker()
font = cv2.FONT_HERSHEY_SIMPLEX


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


while True:
    try:
        image, _ = get_video()
        depth, _ = get_depth()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        blank_image = image.copy()

        tracker.init_frame()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for face in faces:
            face_center = tracker.get_center(face)
            tracker.update_box(face, depth[face_center[1], face_center[0]])

        for box in tracker.get_boxes():
            draw_face(box['rect'], blank_image, box['color'])
            cv2.putText(blank_image, str(
                box['depth']), (box['rect'][0], box['rect'][1]), font, 1, (200, 255, 155), 2)

        cv2.addWeighted(blank_image, alpha, image, 1 - alpha, 0, image)
        cv2.imshow("camera", image)
        cv2.waitKey(5)
    except KeyboardInterrupt:
        sys.exit(1)
