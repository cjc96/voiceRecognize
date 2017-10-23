#coding:utf-8
import os
import time

num = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
word = ['Recognition','File']

for n in num:
	t = raw_input('No. ' + n + ' Enter')
	time.sleep(1)
	for w in word:
		print '朗读： ' + w
		name = '14307130003-' + w + '-' + n + '.dat'
		print 'Now : ' + name
		os.system('python rec.py ' + name)
		os.system('clear')