Methods for camera instrinsics and extrinsics (relative to ground plane) based on 2D pose.

## Dependencies

Requires to run 2D detection, e.g., using the Pose2DSingle module

## Install
The following script sets up a conda environment CalibSingleFrom2DP and installs required packages.

https://github.com/JunkyByte/easy_ViTPose

```sh ./install.sh --easy_ViTPose```

## Run
The following script extracts frames and runs pose detection
```sh ./run.sh input_poses.json input_config.json output_folder```

## Input format
input_poses.json stores the 2D pose in the following json format: ```TODO:```

input_config.json stores the index of head and ankle joints, TODO what else?


## Output format

Output is the camera intrinsics, ground plane normal, ground plane position in the TODO .json format.

```TODO: describe format in detail, we may have to code conversion functions to end up with a common format```

## Conventions and assumptions

People are up-right, if multiple people are present, their height is assumed to be the same.

The output calibration assumes a camera in right-handed coordinate system, i.e.,
x-axis points TODO right?
y-axis points TODO up?
z-axis points TODO forward/backwards?