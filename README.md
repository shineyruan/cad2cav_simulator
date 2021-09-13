# CAD2CAV: Computer-Aided Design for Cooperative Autonomous Vehicles
Welcome to the CAD2CAV simulator module. Please check out [the main repo.](https://github.com/mlab-upenn/ISP2021-cad2cav) for a much detailed project description.

## System Requirements
- Linux Ubuntu 20.04 LTS

## Software Requirements
- [NVIDIA Omniverse Isaac Sim 2021.1.1](https://developer.nvidia.com/isaac-sim)
- ROS Noetic

## Usage
**Before launching the simulator**: please edit `setenv.sh` and change `MY_DIR` to match the NVIDIA Omniverse Isaac Sim package root directory.

For launching the simulator, type
```bash
source setenv.sh
python3 run.py
```

## For Developers
This repo uses [YAPF](https://github.com/google/yapf) for coding style maintenance. **It is strong recommended for developers to pipe all contributions through YAPF before pushing onto this code base.** 
