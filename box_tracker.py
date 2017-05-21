import math
from random import randint
import time
from operator import attrgetter


class box_tracker():
    def __init__(self, resolution=100, depth_resolution=120, ttl=100, movement=10):
        self.boxes = []
        self.resolution = resolution
        self.depth_resolution = depth_resolution
        self.ttl = ttl
        self.movement = movement

    def distance(self, a, b):
        return math.floor(math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2)))

    def get_center(self, rect):
        try:
            point = (rect[0] + rect[2] //
                     2, rect[1] + rect[3] // 2)
            return point
        except:
            return (0, 0)

    def get_random_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def init_frame(self):
        for index, box in enumerate(self.boxes):
            box['age'] = box['age'] - 1
            if box['age'] < self.ttl // 2:
                box['enable'] = False
            else:
                box['enable'] = True

            if box['age'] == 0:
                del self.boxes[index]
                continue

    def update_box(self, input_box, input_depth):
        point = self.get_center(input_box)

        detected = False
        for index, box in enumerate(self.boxes):
            box_point = self.get_center(box['rect'])
            if (self.distance(box_point, point) < self.resolution) and (input_depth > box['depth'] - self.depth_resolution and input_depth < box['depth'] + self.depth_resolution):
                if self.distance(box_point, point) > self.movement:
                    box['rect'] = input_box
                box['depth'] = input_depth
                box['age'] = self.ttl
                detected = True

        if not detected:
            box = {'rect': input_box, 'depth': input_depth,
                   'color': self.get_random_color(), 'age': self.ttl, 'enable': True}
            self.boxes.append(box)

    def get_boxes(self):
        self.boxes.sort(key=lambda tup: tup['depth'])         
        for box in self.boxes:
            if box['enable']:
                yield box
