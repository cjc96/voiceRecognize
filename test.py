# coding=utf-8
import os
import sys
import subprocess
import numpy as np

def levenshtein(a,b):
	lena = len(a)
	lenb = len(b)
	d = np.zeros((30,30))
	for i in range(lena + 1):
		d[i][0] = i
	for j in range(lenb + 1):
		d[0][j] = j
	for i in range(1, lena + 1):
		for j  in range(1, lenb + 1):
			if a[i - 1] == b[j - 1]:
				d[i][j] = d[i - 1][j - 1]
			else:
				d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + 1)
	return int(d[lena][lenb])

def compare(sp):
	if sp[0][0] == possibility[len(possibility) - 1] or sp[1][0] == possibility[len(possibility) - 1]:
		print possibility[2]
		return False
	if sp[0][0] == possibility[len(possibility) - 2] or sp[1][0] == possibility[len(possibility) - 2]:
		print possibility[6]
		return False
	if sp[0][0] in possibility and sp[0][0] != possibility[len(possibility) - 1] :
		print sp[0][0]
		return False
	if sp[1][0] in possibility and sp[1][0] != possibility[len(possibility) - 1] :
		print sp[1][0]
		return False
	return True

def get_HMM_value(name_label, sig):
	test_MFCC = calcMFCC_delta_delta(sig)
	file = open("kmeans_dat/model.in",'r').read()
	core = np.array(file[name_label])
	get_KMEANS = get_center_label(feat, core)
	#print get_KMEANS
	return upload_HMM(name_label,get_KMEANS)

def compare_HMM():
	HMM_possible = np.zeros((30,1))
	minn = 2.0
	ans = -1
	for i in len(possibility):
		HMM_possible[i] = get_HMM_value(i,sig)
		if HMM_possible[i] < minn:
			minn = HMM_possible[i]
			ans = i
	assert ans != -1
	return possibility[ans]

os.system('python rec.py tempInput.dat')
# file_name = os.path.join(os.path.dirname(__file__),'test.dat')
possibility = ["数字","语音","话音","信号","分析","识别","数据","中国","北京","背景","上海","商行","复旦","网络","电脑","Speech","Voice","Sound","Happy","Lucky","Data","Recognition","File","Open","Close","Start","Stop","Network","Computer","China","复制","华阴"]
try:
	os.popen('python start.py')
	tmp = possibility[-1]
	dislist = [(levenshtein(tmp, t),t) for t in possibility[:-2]]
	print dislist
	print possibility[:-2]
except Exception,e:
	print e
	sys.exit()
present = open('output.txt','r').read()
sp = [t.split('|') for t in present.split('\n')]
tmp = ''
if compare(sp):
	if sp[0][1] > sp[1][1]:
		tmp = sp[0][0]
	else:
		tmp = sp[1][0]
	dislist = [(levenshtein(tmp, t),t) for t in possibility[:-2]]
	print dislist
	minn = 10000000
	ans = ''
	for i in dislist:
		if i[0] < minn:
			minn = i[0]
			ans = i[1]
	print ans