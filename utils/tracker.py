import os
from abc import abstractmethod, ABC

from utils.dataset import Dataset
from utils.utils import calculate_overlap, save_regions


class Tracker(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def initialize(self, img, region: list):
        pass

    @abstractmethod
    def track(self, img):
        pass

    @abstractmethod
    def name(self):
        pass

    def evaluate(self, dataset: Dataset, results_dir: str):

        for sequence in dataset.sequences:

            print('Evaluating on sequence:', sequence.name)

            sequence_results_dir = os.path.join(results_dir, sequence.name)
            if not os.path.exists(sequence_results_dir):
                os.mkdir(sequence_results_dir)

            results_path = os.path.join(sequence_results_dir, '%s_%03d.txt' % (sequence.name, 1))

            if os.path.exists(results_path):
                continue

            init_frame = 0
            frame_index = 0

            results = sequence.length * [[0]]

            while frame_index < sequence.length:

                img = sequence.read_frame(frame_index)
                
                if frame_index == init_frame:
                    
                    self.initialize(img, sequence.gt_region(frame_index))
                    results[frame_index] = [1]
                    frame_index += 1

                else:

                    prediction = self.track(img)

                    if len(prediction) != 4:
                        print('Predicted region must be a list representing a bounding box in the format [x0, y0, width, height].')
                        exit(-1)

                    if calculate_overlap(prediction, sequence.gt_region(frame_index)) > 0:
                        results[frame_index] = prediction
                        frame_index += 1
                    else:
                        results[frame_index] = [2]
                        frame_index += 5
                        init_frame = frame_index

            save_regions(results, results_path)
