import os
import sys
import shutil
import re
import json

import pandas as pd
import numpy as np
import pyquaternion


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Usage: {0} data_path".format(sys.argv[0]))
        exit(-1)
    for root, folders, files in os.walk(sys.argv[1]):
        for file in files:
            if ".bag" in file and not "out" in file:
                bag_dir = os.path.join(os.path.join(root, os.path.splitext(file)[0]+"_result"))
                if not os.path.exists(bag_dir):
                    os.mkdir(bag_dir)
                os.chdir(bag_dir)
                out_bag = os.path.splitext(file)[0]+"_out.bag"
                #os.system("kalibr_extract_msg --image-topics /cam0/image_raw --output-bag %s --bag %s " % (os.path.join(bag_dir,out_bag), os.path.join(root,file)))

                feature_variance = (str)(1/0.26)
                #os.system("kalibr_calibrate_rs_cameras  --target %s --bag %s --model  pinhole-radtan-rs --topic /cam0/image_raw --feature-variance %s --frame-rate 30 |tee camera_rs_intrinsic_calib.log" % (os.path.join(sys.argv[1], "april_6x6.yaml"), os.path.join(bag_dir,out_bag), feature_variance))


                for cur_f in os.listdir("."):
                    if ".yaml" in cur_f and "imucam" not in cur_f:
                        os.system("kalibr_calibrate_imu_rs_camera --target %s --cam %s --imu %s --bag %s --imu-models scale-misalignment  --dont-show-report |tee rs_imu_camera_calib.log" % (os.path.join(sys.argv[1], "april_6x6.yaml"), cur_f, os.path.join(sys.argv[1], "imu_r17.yaml"), os.path.join(bag_dir,out_bag)))

                for cur_file in os.listdir("."):
                    if "results-imucam-" in cur_file:
                        print cur_file
                        fin = open(cur_file, "r")
                        lines = fin.readlines()
                        #extrinsic  imu-cam
                        line23 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[23])))])
                        line24 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[24])))])
                        line25 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[25])))])
                        tranform = np.vstack([np.vstack([line23, line24]), line25])
                        q = pyquaternion.Quaternion(matrix=tranform[:, 0:3])
                        t1 = tranform[0, 3]
                        t2 = tranform[1, 3]
                        t3 = tranform[2, 3]
                        #cam intrinsic
                        line42 = np.array([float(i) for i in list(filter(None, re.split("[\[\,\Focal length:\]\n ]", lines[42])))])
                        fx = (line42[0])/640*480
                        fy = (line42[1])/640*480
                        line43 = np.array([float(i) for i in list(filter(None, re.split("[\[\,\Principal point:\]\n ]", lines[43])))])
                        cx = line43[0]
                        cy = line43[1]
                        #imu noise
                        line63 = np.array([float(i) for i in list(filter(None, re.split("[\[\,\Noise density:\]\n]", lines[63])))])
                        line65 = np.array([float(i) for i in list(filter(None, re.split("[\[\,\Random walk:\]\n]", lines[65])))])
                        line67 = np.array([float(i) for i in list(filter(None, re.split("[\[\,\Noise density:\]\n]", lines[67])))])
                        line69 = np.array([float(i) for i in list(filter(None, re.split("[\[\,\Random walk:\]\n]", lines[69])))])
                        Accelerometer_noise = line63[0]
                        Accelerometer_random_walk = line65[0]
                        Gyroscope_noise = line67[0]
                        Gyroscope_random_walk = line69[0]
                        #imu intrinsics
                        #gyro scale  mis-alignment
                        line78 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[78])))])
                        line79 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[79])))])
                        line80 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[80])))])
                        scale_gyro=list()
                        scale_gyro.append(line78[0])
                        scale_gyro.append(line79[1])
                        scale_gyro.append(line80[2])
                        mis_alignment_gyro = list()
                        mis_alignment_gyro.append(line79[0]/line79[1])
                        mis_alignment_gyro.append(line80[0]/line80[1])
                        mis_alignment_gyro.append(line80[1]/line80[2])


                        #rotation  gyro_acc
                        line86 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[86])))])
                        line87 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[87])))])
                        line88 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[88])))])
                        C_gyro_acc = np.vstack([np.vstack([line86, line87]), line88])
                        q_gyro_acc = pyquaternion.Quaternion(matrix=C_gyro_acc)


                        #acc  scale  mis-alignment
                        line91 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[91])))])
                        line92 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[92])))])
                        line93 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[93])))])
                        scale_acc=list()
                        scale_acc.append(line91[0])
                        scale_acc.append(line92[1])
                        scale_acc.append(line93[2])
                        mis_alignment_acc = list()
                        mis_alignment_acc.append(line92[0]/line92[1])
                        mis_alignment_acc.append(line93[0]/line93[1])
                        mis_alignment_acc.append(line93[1]/line93[2])

                        input_json = os.path.join(sys.argv[1], "ARcore.json")
                        with open(input_json,'rb')as f:
                            data = json.load(f)

                            data["cameras"][0]["calibratedFocalLength"]["x"]  = fx
                            data["cameras"][0]["calibratedFocalLength"]["y"] = fy
                            data["cameras"][0]["calibratedPrincipalPoint"]["x"] = cx
                            data["cameras"][0]["calibratedPrincipalPoint"]["y"] = cy


                            data["cameraExtrinsics"][0]["frameTCamera"]["p"]["x"] = t1
                            data["cameraExtrinsics"][0]["frameTCamera"]["p"]["y"] = t2
                            data["cameraExtrinsics"][0]["frameTCamera"]["p"]["z"] = t3

                            data["cameraExtrinsics"][0]["frameTCamera"]["q"]["x"] = q.x
                            data["cameraExtrinsics"][0]["frameTCamera"]["q"]["y"] = q.y
                            data["cameraExtrinsics"][0]["frameTCamera"]["q"]["z"] = q.z
                            data["cameraExtrinsics"][0]["frameTCamera"]["q"]["w"] = q.w

                            data["generalExtrinsics"][0]["aTB"]["p"]["x"] = t1
                            data["generalExtrinsics"][0]["aTB"]["p"]["y"] = t2
                            data["generalExtrinsics"][0]["aTB"]["p"]["z"] = t3

                            data["generalExtrinsics"][0]["aTB"]["q"]["x"] = q.x
                            data["generalExtrinsics"][0]["aTB"]["q"]["y"] = q.y
                            data["generalExtrinsics"][0]["aTB"]["q"]["z"] = q.z
                            data["generalExtrinsics"][0]["aTB"]["q"]["w"] = q.w

                            data["imus"]["100"]["gyroNoiseSigma"] = Gyroscope_noise
                            data["imus"]["100"]["gyroBiasSigma"] = Gyroscope_random_walk
                            data["imus"]["100"]["accelNoiseSigma"] = Accelerometer_noise
                            data["imus"]["100"]["accelBiasSigma"] = Accelerometer_random_walk
 
                        with open('out2.json','wb')as f_out:
                            json.dump(data,f_out,sort_keys=True,indent=1)
                    
