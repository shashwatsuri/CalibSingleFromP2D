# Might have to add to path
# sys.path.append('CalibS') 
from util import *
from run_calibration_ransac import *
# from eval_human_pose import *
import json
from datetime import datetime
import csv
import matplotlib.image as mpimg
import argparse
import sys

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Description of your script.')
parser.add_argument("--pose_model", type = str, help = "currently support coco_mmpose/easy_vitpose (default)")
parser.add_argument("--frames", type = str, help = "name of subfolder of frames in frames folder to run calibration on")
parser.add_argument("--pose_results", type=str, help = "name of the json file that has the pose results in them")
args = parser.parse_args()

today = datetime.now()

FRAME_DIR = "CalibSingleFromP2D/Frames/"
PLOT_DIR = "CalibSingleFromP2D/plots/"
RESULTS_DIR = "CalibSingleFromP2D/results/"

# metrics = Metrics()


#The name of is the current date
name = str(today.strftime('%Y%m%d_%H%M%S')) + '_data'

#Gets the hyperparamter from hyperparameter.json
print("Getting hyperparameters...")
(threshold_euc, threshold_cos, angle_filter_video, 
 confidence, termination_cond, num_points, h, iter, focal_lr, point_lr) = util.hyperparameter(
     'CalibSingleFromP2D/hyperparameter.json')
hyperparam_dict = {"threshold_euc": threshold_euc, "threshold_cos": threshold_cos, 
                   "angle_filter_video": angle_filter_video, "confidence": confidence, 
                   "termination_cond": termination_cond, "num_points": num_points, "h": h, 
                   "optimizer_iteration" :iter, "focal_lr" :focal_lr, "point_lr": point_lr}

# *************************************************************************************************************

# EXTRINSIC MATRIX DETAILS
# https://ksimek.github.io/2012/08/22/extrinsic/
# for subject in ['S1', 'S5','S6','S7','S8','S9']:
# for subject in ['S5','S6','S7','S8','S9']:
# for subject in ['S1','S5','S6','S7','S8']:

# REF    SYNC   REF          SYNC         REF        SYNC
# scale, scale, shift start, shift start, shift end, shift end
# experiments_time = [experiments_time[0]]

# experiments_time = [100, 200, 400, 600, 800, 1000]

# Making the directories, eval is the accuracy wit hthe ground truth, 
# output is the calibration saved as a pickle file, plot is the plots that are created during optimization.

# *************************************************************************************************************

print("Creating files for plots...")
if os.path.isdir(PLOT_DIR) == False:
    os.mkdir(PLOT_DIR)

if os.path.isdir(PLOT_DIR+'time_' + name) == False:
    os.mkdir(PLOT_DIR+'time_' + name)

with open(PLOT_DIR+'time_' + name +  '/result_sync.csv','a') as file:
    writer1 = csv.writer(file)
    writer1.writerow(["shift gt", "shift", "subset", "camera1", "camera2"])
    file.close

with open(PLOT_DIR+'time_' + name + '/result_average_sync.csv','a') as file:
    writer1 = csv.writer(file)
    writer1.writerow(["shift gt", "cam1", "cam2", "shift avg", "shift std"])
    file.close

with open(PLOT_DIR+'time_' + name + '/result_average_all.csv','a') as file:
    writer1 = csv.writer(file)
    writer1.writerow(["shift gt", "shift avg", "shift std", "diff avg", "diff std"])
    file.close

with open(PLOT_DIR+'time_' + name + '/result_bundle_sync.csv','a') as file:
    writer1 = csv.writer(file)
    writer1.writerow(["cam1", "cam2", "offset", "offset pred", "offset diff", "exp", "focal pre bundle", "focal_tsai", "angle_diff pre bundle", "error_npjpe pre bundle", "focal_error pre bundle", "results_position_diff pre bundle", "focal bundle", "focal_tsai", "angle_diff bundle", "error_npjpe bundle", "focal_error bundle", "results_position_diff bundle"])
    file.close

with open(PLOT_DIR+'time_' + name + '/result_bundle_no_sync.csv','a') as file:
    writer1 = csv.writer(file)
    writer1.writerow(["cam1", "cam2", "offset", "offset pred", "offset diff", "exp", "focal pre bundle", "focal_tsai", "angle_diff pre bundle", "error_npjpe pre bundle", "focal_error pre bundle", "results_position_diff pre bundle", "focal bundle", "focal_tsai", "angle_diff bundle", "error_npjpe bundle", "focal_error bundle", "results_position_diff bundle"])
    file.close

#########################

# grid_step = 10
# x_2d = np.linspace(-5, 5, grid_step)
# y_2d = np.linspace(0, 10, grid_step)
# xv_2d, yv_2d = np.meshgrid(x_2d, y_2d)
# coords_xy_2d =np.array((xv_2d.ravel(), yv_2d.ravel())).T

#############

results  = os.path.join(RESULTS_DIR,args.pose_results)
if(not os.path.exists(results + ".json")):
    print("file " + results + ".json does not exist")
    sys.exit()
frames = os.path.join(FRAME_DIR,args.frames)

with open('CalibSingleFromP2D/configuration.json', 'r') as f:
    configuration = json.load(f)

num = 0
focal_array = []
calib_array = []

with open(os.path.join(results + ".json"), 'r') as f:
    points_2d = json.load(f)

if(args.pose_model == "coco_mmpose"):
    datastore_cal = data.coco_mmpose_dataloader(points_2d, bound_lower = 100, bound = 2500)  
else:
    datastore_cal = data.vitpose_easy_dataloader(points_2d)
frame = [file for file in os.listdir(frames) if file.endswith('.jpg')][0]
frame_path = os.path.join(frames,frame)
print(frame_path)
img = mpimg.imread(frame_path)

(ankles, cam_matrix, normal, ankleWorld, focal, focal_batch, ransac_focal, datastore_filtered) = run_calibration_ransac(
        datastore_cal, 'CalibSingleFromP2D/hyperparameter.json', img, 
        img.shape[1], img.shape[0], name, num, skip_frame = configuration['skip_frame'], 
        max_len = configuration['max_len'], min_size = configuration['min_size'])
focal_array.append(cam_matrix[0][0])
calib_array.append({'cam_matrix': cam_matrix, 'ground_normal': normal, 'ground_position': ankleWorld})
print("vid:" +frames)
print(cam_matrix,normal)
