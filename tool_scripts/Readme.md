# tool scripts for data process

# acc and gyro topic data merge to imu topic data
  python two_imu_topic_2_one_imu_topic.py   --bag  input.bag  --output-bag  out.bag

# Batch processing scripts and save result as ARcore.json
- for GS camera
  python batch_bags_process_GS_camera.py  data_path
- for RS camera
  python batch_bags_process_RS_camera.py data_path

# extract_result_from_txt_to_csv
  python extract_result_from_txt_to_csv.py data_path

# bag_deal_with
- depress rosbag
  python DeCompress_rosbag_not_vcm.py  --bag  input.bag   --output-bag   out.bag
- extract data from rosbag
  python  bagwxtractor.py   --bag   input_Bag  --image-topics  /cam0/image_raw  --imu-topics   /imu0    --output-folder  out 
- create rosbag from yuv data
  python AR_glass_bagcreater_yuv.py --images_folder_cam0 data_path_1 --images_folder_cam1 data_path_2  --imu_csv  imu_csv_file_path  --output-bag out.bag
- change rosbag message
  python ChangeBagWithVCM.py  --bag input.bag  --output-bag  out.bag

#  make target board
  source devel/setup.bash
  kalibr_create_target_pdf --type apriltag --nx 6 --ny 6 --tsize 0.03 --tspace 0.3

