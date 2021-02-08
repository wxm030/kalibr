# Toolbox of sensor calibration


# Build 
mkdir catkin_ws/src
cd catkin_ws/src
git clone git@github.com:wxm030/kalibr.git
cd ..
catkin init
catkin build -DCMAKE_BUILD_TYPE=Release -j4
source  devel/setup.bash

# Run example(python2 default)
kalibr_calibrate_cameras   --target    '/home/wxm/Documents/code/imu_preintegrate/catkin_kalibr_ws/data/april_6x6.yaml'     --bag   '/home/wxm/Documents/code/imu_preintegrate/catkin_kalibr_ws/data/out.bag'      --models pinhole-radtan --topics /cam0/image_raw  --dont-show-report

kalibr_calibrate_imu_camera --target april_6x6.yaml --cam camchain.yaml --imu imu_adis16448.yaml --bag dynamic.bag --bag-from-to 5 45

# make target board
kalibr_create_target_pdf --type apriltag --nx 6 --ny 6 --tsize 0.03 --tspace 0.3

# bag extract or create script
source devel/setup.bash
kalibr_bagcreater --folder dataset-dir  --output-bag  out.bag

source devel/setup.bash
kalibr_bagextractor --image-topics /cam0/image_raw  /cam1/image_raw  --imu-topics  /imu0  --output-folder dataset_dir  --bag input.bag

# Todo
- 修改bag包读取方法，解决陀螺仪和加速度计不同步的问题！
- 在kalibr中支持随机圆的标定板(棋盘格，circle grid, AprilTag标定板)
- 增加多目相机标定（有重叠视场．无重叠视场）
- 相机单目内参或者多目内参标定，采用静态拍摄图像标定．
- kalibr_calibrate_cameras now support omni, eucm and ds
- 放宽kalibr_calibrate_rs_cameras和kalibr_calibrate_imu_rs_camera中对于aprilgrid 解码标志数的限制
- 添加Brown-RollingShutter模型
- imu-cam标定，加速度和角速度曲线绘制顺序和颜色修改

##commit kalibration
- 修改bag包读取方法，解决陀螺仪和加速度计不同步的问题！
- 解决






#Todo
- 相机标定调整为单张图像静态标定
- 增加lidar与imu的标定
- 增加立体箱支持


# mono camera

# multiply camera

# rs camera

# imu-cam calibration

# lidar_imu calibration
