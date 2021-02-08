import os
import sys
import shutil
import re
import json

import pandas as pd
import numpy as np
import pyquaternion
import csv

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Usage: {0} data_path".format(sys.argv[0]))
        exit(-1)


    data_path = sys.argv[1]
    out_file = os.path.join(data_path, "calib_result_from_txt.csv")
    fout = open(out_file, "w+")
    file_head = ["folder_name", "tx", "ty", "tz", "qx", "qy", "qz", "qw","gravity_x", "gravity_y", "gravity_z", "timeshift", "gyroscale_x", "gyroscale_y", "gyroscale_z", "gyro_misalignment_x", "gyro_misalignment_y", "gyro_misalignment_z", "acc_scale_x", "acc_scale_y", "acc_scale_z", "acc_misalignment_x", "acc_misalignment_y", "acc_misalignment_z", "gyroQAccel_qw", "gyroQAccel_qx", "gyroQAccel_qy", "gyroQAccel_qz"]
    dict_writer = csv.DictWriter(fout, file_head)
    dict_writer.writerow(dict(zip(file_head, file_head)))



    for root, folders, files in os.walk(sys.argv[1]):
        for file in files:
            if ".bag" in file and not "out" in file:
                bag_dir = os.path.join(os.path.join(root, os.path.splitext(file)[0]+"_result"))
                if not os.path.exists(bag_dir):
                    os.mkdir(bag_dir)
                os.chdir(bag_dir)


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
                        #gravity
                        line33 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[33])))])
                        gravity_x = line33[0]
                        gravity_y = line33[1]
                        gravity_z = line33[2]
                        #timeshift
                        line29 = np.array([float(i) for i in list(filter(None, re.split("[\[\]\n ]", lines[29])))])
                        timeshift = line29[0]

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


                        dict_writer.writerow({
                            "folder_name" : file,
                            "tx": t1,
                            "ty": t2,
                            "tz": t3,
                            "qx": q.x,
                            "qy": q.y,
                            "qz": q.z, 
                            "qw": q.w,
                            "gravity_x": gravity_x,
                            "gravity_y": gravity_y,
                            "gravity_z": gravity_z,
                            "timeshift": timeshift,
                            "gyroscale_x": scale_gyro[0],
                            "gyroscale_y": scale_gyro[1],
                            "gyroscale_z": scale_gyro[2],
                            "gyro_misalignment_x": mis_alignment_gyro[0],
                            "gyro_misalignment_y": mis_alignment_gyro[1],
                            "gyro_misalignment_z": mis_alignment_gyro[2],
                            "acc_scale_x": scale_gyro[0],
                            "acc_scale_y": scale_gyro[1],
                            "acc_scale_z": scale_gyro[2],
                            "acc_misalignment_x": mis_alignment_acc[0],
                            "acc_misalignment_y": mis_alignment_acc[1],
                            "acc_misalignment_z": mis_alignment_acc[2],
                            "gyroQAccel_qw": q_gyro_acc.w,
                            "gyroQAccel_qx": q_gyro_acc.x,
                            "gyroQAccel_qy": q_gyro_acc.y,
                            "gyroQAccel_qz": q_gyro_acc.z
                        })

                    
