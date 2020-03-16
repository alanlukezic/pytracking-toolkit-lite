import time

from utils.tracker import Tracker


class StaticTracker(Tracker):

    def name(self):
        return 'static'

    def initialize(self, image, region):
        self.bb = region

    def track(self, image):
        time.sleep(0.001)
        return self.bb
