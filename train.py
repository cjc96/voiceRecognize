#coding=utf-8
from cut import *
import scipy.io.wavfile as wav
from kmeans import *
import numpy as np

# 1 = dat, 2 = wav
student_num = ["12307130145","14307130003","14307130033","14307130120","14307130132","14307130159","14307130176","14307130246","14307130198","14307130223","14307130246","14307130259","14307130262","14307130264","14307130270","14307130318","14307130356","14307130360"]
audio_type = [2,1,1,1,2,1,1,1,1,2,1,1,2,2,2,2,2]
type_name = [".",".dat",".wav"]
nums = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
words = ["数字","语音","话音","信号","分析","识别","数据","中国","北京","背景","上海","商行","复旦","网络","电脑","Speech","Voice","Sound","Happy","Lucky","Data","Recognition","File","Open","Close","Start","Stop","Network","Computer","China"]

(rate,tmp) = wav.read("dat/14307130003-Happy-16.dat")
sig = []
for t in tmp:
	sig.append(t[0])
sig = np.array(sig)
mfcc_feat = calcMFCC_delta_delta(sig,rate) 
print(build_center(mfcc_feat))

# for word in words:
# 	ltype = -1
# 	mfcc_feat = np.zeros((1,39))
# 	for stu_id in student_num:
# 		ltype += 1
# 		for num in nums:
# 			file_name = "dat/" + stu_id + "-" + words + "-" + num + type_name[audio_type[ltype]]
# 			(rate,tmp) = wav.read(file_name)
# 			tmp = calcMFCC_delta_delta(sig,rate) 
# 			mfcc_feat = np.concatenate(mfcc_feat, tmp, axis = 1)
# 	kmeans_model = build_center(mfcc_feat)
# 	file = open("kmeans_dat/" + word + '.in','w')
# 	file.write(kmeans_model)
