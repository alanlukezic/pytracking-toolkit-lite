import argparse
import os

import urllib.request
import zipfile
from shutil import copyfile


def create_workspace(workspace_path, dataset_name):
    
    if not os.path.exists(workspace_path):
        print('Directory given as a workspace does not exist. Please create it meanually.')
        exit(-1)

    # download dataset
    dataset_name = dataset_name.lower()
    if dataset_name == 'vot2013':
        dataset_url = 'http://box.vicos.si/vot/vot2013.zip'
    elif dataset_name == 'vot2014':
        dataset_url = 'http://box.vicos.si/vot/vot2014.zip'
    elif dataset_name == 'vot2015':
        dataset_url = 'http://box.vicos.si/vot/vot2015.zip'
    elif dataset_name == 'vot2016':
        dataset_url = 'http://box.vicos.si/vot/vot2016.zip'
    elif dataset_name == 'test':
        dataset_url = 'http://box.vicos.si/vot/test.zip'
    else:
        print('Unknown dataset identifier. The following are supported: vot2013/vot2014/vot2015/vot2016')
        exit(-1)

    temp_dataset_path = os.path.join(workspace_path, 'dataset_tmp.zip')
    
    print('Downloading dataset. This may take a while...')
    urllib.request.urlretrieve(dataset_url, temp_dataset_path)

    dataset_dir = os.path.join(workspace_path, 'sequences')
    if not os.path.exists(dataset_dir):
        os.mkdir(dataset_dir)

    print('Extracting dataset...')
    with zipfile.ZipFile(temp_dataset_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)

    # remove dataset .zip file
    os.remove(temp_dataset_path)
    
    if not os.path.exists(os.path.join(workspace_path, 'results')):
        os.mkdir(os.path.join(workspace_path, 'results'))
    
    # copy a template trackers.yaml file from utils to workspace directory
    copyfile('utils/trackers.yaml', os.path.join(workspace_path, 'trackers.yaml'))

    print('Workspace has been created successfully.')


def main():
    parser = argparse.ArgumentParser(description='Tracking Workspace Creation Utility')

    parser.add_argument("--workspace_path", help="Path to the VOT workspace", required=True, action='store')
    parser.add_argument("--dataset", help="VOT dataset (vot2013/vot2014/vot2015/vot2016)", required=True, action='store')

    args = parser.parse_args()

    create_workspace(args.workspace_path, args.dataset)

if __name__ == "__main__":
    main()
