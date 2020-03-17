# Python Tracking Evaluation Toolkit

The toolkit is developed as a tool to evaluate trackers at the course Advanced Computer Vision Methods at Faculty of Computer and Information Science, University of Ljubljana. It implements the VOT reset-based experiment and two basic performance measures accuracy and robustness. The toolkit is developed for educational purposes only and should not be used in the research community.

In the following you can find the instructions for creating a workspace, integrating a tracker, running evaluaton and computing tracking performance measures.

## 1.) Create workspace
- Checkout this repository to an empty folder - called `toolkit-dir` </br>
- Create a new directory (not within `toolkit-dir` directory) - we will call it `workspace-dir` </br>
- Go to the `toolkit-dir` directory and run the command: 
```console
python create_workspace.py --workspace_path workspace-dir --dataset dataset-version
```
Note that `dataset-version` represents the version of the VOT dataset and can be choosen among the following options: `vot2013`, `vot2014`, `vot2015`, `vot2016`. The script will automatically download the dataset (which can take some time), create several folders and the file `trackers.yaml` in the `toolkit-dir`. 

## 2.) Tracker integration and running
- After the workspace has been successfully created, edit the file `trackers.yaml` in the `toolkit-dir`. See the commented example for the NCC tracker in the `trackers.yaml`.
- You can run your tracker on the dataset by running the following command:
```console
python evaluate_tracker.py --workspace_path workspace-dir --tracker tracker_id
```
Note that the `tracker-id` is a tracker identifier (see example in `trackers.yaml`, denoted as <i>tracker identifier</i>). The command will create a new directory with the name of your tracker in the `results` folder, which contains regions predicted by the tracker on all video sequences from the dataset.

## 3.) Results visualization and tracking performance evaluation
- After the `evaluate_tracker` command has successfully finished, you can visualize tracking results on a specific sequence (`sequence-name`) by running the following command:
```console
python visualize_result.py --workspace_path workspace-dir --tracker tracker-id --sequence sequence-name
```
The command will open a window and show a video with a predicted bounding box on a selected video sequence.
- To compare results of multiple trackers (which have previously been run on the dataset) you can run the following command:
```console
python compare_trackers.py --workspace_path workspace-dir --trackers tracker-id1 tracker-id2 tracker-id3 ... --sensitivity 100
```
Note that `...` denotes arbitrary number of trackers which can be compared. This command calculates two tracking performance measures: accuracy and robustness and stores the per-sequence results in the directory: `workspace-dir/analysis/tracker-id/results.json`. Additionally, you can find the AR plot in the `workspace-dir/analysis/ar.png` comparing all trackers you specified when running the comparison command.

## 4.) Performance measures
- <b>Accuracy</b>: is the average overlap, averaged over all sequences in the dataset. Average overlap on one sequence is calculated as the average of overlaps on frames where overlap is greater than zero. The overlap on a frame is defined as an intersection over union between the predicted and ground-truth bounding boxes.
- <b>Robustness</b>: represents how often a tracker fails. Evaluation protocol is defined as following: a tracker is initialized at the beginning of the sequence and let to track until the overlap between the predicted region and ground-truth annotation is greater than zero. When the overlap drops to zero - this is considered as a failure of a tracker - the tracker is re-initialized after five frames. Number of failures is count on all sequences in the dataset and is denoted as F, while number of all frames in a dataset is denoted as M. The robustness (R) is defined as following:
```math
R = exp(- S * (F / M))
```
where S represents sensitivity parameter and robutness can be interpreted as a probability that the tracker does not fail after S frames.
