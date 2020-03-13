import cv2

from utils.tracker import Tracker


class NCCTracker(Tracker):

    def name(self):
        return 'ncc'

    def initialize(self, image, region):
        self.window = max(region[2], region[3]) * 2

        left = max(region[0], 0)
        top = max(region[1], 0)

        right = min(region[0] + region[2], image.shape[1] - 1)
        bottom = min(region[1] + region[3], image.shape[0] - 1)

        self.template = image[int(top):int(bottom), int(left):int(right)]
        self.position = (region[0] + region[2] / 2, region[1] + region[3] / 2)
        self.size = (region[2], region[3])

    def track(self, image):

        left = max(round(self.position[0] - float(self.window) / 2), 0)
        top = max(round(self.position[1] - float(self.window) / 2), 0)

        right = min(round(self.position[0] + float(self.window) / 2), image.shape[1] - 1)
        bottom = min(round(self.position[1] + float(self.window) / 2), image.shape[0] - 1)

        if right - left < self.template.shape[1] or bottom - top < self.template.shape[0]:
            return [self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2, self.size[0], self.size[1]]

        cut = image[int(top):int(bottom), int(left):int(right)]

        matches = cv2.matchTemplate(cut, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matches)

        self.position = (left + max_loc[0] + float(self.size[0]) / 2, top + max_loc[1] + float(self.size[1]) / 2)

        return [left + max_loc[0], top + max_loc[1], self.size[0], self.size[1]]
