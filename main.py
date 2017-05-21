#!/usr/bin/env python
from freenect import sync_get_video as get_video
from freenect import sync_get_depth as get_depth
import cv2
import sys

cascadePath = "haarcascade_frontalface_alt2.xml"
face_cascade = cv2.CascadeClassifier(cascadePath)
alpha = 0.9

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

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for index,face in enumerate(faces):
            draw_face(face, blank_image, (100, 200, 100))
            face_center = (face[0] + face[2] // 2, face[1] + face[3] // 2)
            cv2.circle(blank_image, face_center, 2, (0, 0, 200))
            t_depth = depth[face_center[1], face_center[0]]
            print index, t_depth

        cv2.addWeighted(blank_image, alpha, image, 1 - alpha, 0, image)
        cv2.imshow("camera", image)
        cv2.waitKey(5)
    except KeyboardInterrupt:
        sys.exit(1)

