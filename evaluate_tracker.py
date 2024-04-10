import argparse
import os
import shutil

from utils.utils import load_tracker, load_dataset


def evaluate_tracker(workspace_path, tracker_id, reevaluate=False):

    tracker_class = load_tracker(workspace_path, tracker_id)
    tracker = tracker_class()

    dataset = load_dataset(workspace_path)

    results_dir = os.path.join(workspace_path, 'results', tracker.name())

    if reevaluate:
        shutil.rmtree(results_dir)

    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    tracker.evaluate(dataset, results_dir)
    print('Evaluation has been completed successfully.')


def main():
    parser = argparse.ArgumentParser(description='Tracker Evaluation Utility')

    parser.add_argument('--workspace_path', help='Path to the VOT workspace', required=True, action='store')
    parser.add_argument('--tracker', help='Tracker identifier', required=True, action='store')
    parser.add_argument('--reevaluate', help='Re-evaluate the tracker', action='store_true')

    args = parser.parse_args()

    evaluate_tracker(args.workspace_path, args.tracker, args.reevaluate)

if __name__ == "__main__":
    main()


