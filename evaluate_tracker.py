import argparse
import os

from utils.utils import load_tracker, load_dataset


def evaluate_tracker(workspace_path, tracker_dir_path, tracker_id):

    tracker_class = load_tracker(tracker_dir_path, tracker_id)
    tracker = tracker_class()

    dataset = load_dataset(workspace_path)

    results_dir = os.path.join(workspace_path, 'results', tracker.name())
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    tracker.evaluate(dataset, results_dir)

def main():
    parser = argparse.ArgumentParser(description='Tracker Evaluation Utility')

    parser.add_argument('--workspace_path', help='Path to the VOT workspace', required=True, action='store')
    parser.add_argument('--tracker_path', help='Path to the tracker directory', required=True, action='store')
    parser.add_argument('--tracker', help='Tracker class identifier', required=True, action='store')

    args = parser.parse_args()

    evaluate_tracker(args.workspace_path, args.tracker_path, args.tracker)

if __name__ == "__main__":
    main()
