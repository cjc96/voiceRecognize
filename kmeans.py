import numpy as np
import math

def dist(a,b):
	temp=0
	for i in range(39):
		temp += math.abs(a[i]-b[i])
	return temp

def vq(vecs, core):
	ans = np.zeros((vecs.shape[0], 1))
	for i in range(vecs.shape[0]):
		label = -1
		for j in range(core.shape[0]):
			minn = 999999
			if dist(vecs[i],core[j]) < minn:
				minn = dist(vecs[i],core[j])
				label = j
		ans[i] = label
	return ans

def build_center(vecs, means = 16):
	core = np.zeros((means, vecs.shape[1]))
	for i in range(means):
		core[i] = vecs[i]
	num = vecs.shape[0]
	change = True
	last_label = np.zeros((means, 1))
	while (change):
		change = False
		state = np.zeros((means, vecs.shape[1]))
		status = np.zeros((means, 1))
		for v in range(vecs.shape[0]):
			label = -1
			for t in range(core.shape[0]):
				minn = 999999
				if dist(vecs[v],core[t]) < minn:
					minn = dist(vecs[v],core[t])
					label = t
			assert label != -1
			if (last_label[v] != label):
				change = True
			last_label[v] = label
			state[label] += vecs[v]
			status[label] += 1
		for i in range(means):
			core[i] = state[i] / status[i]
	return vq(vecs,core)

def get_center_label(vecs, core):
	num = vecs.shape[0]
	state = np.zeros((means, vecs.shape[1]))
	status = np.zeros((means, 1))
	last_label = np.zeros((means, 1))
	for v in range(vecs.shape[0]):
		label = -1
		for t in range(core.shape[0]):
			minn = 999999
			if dist(vecs[v],core[t]) < minn:
				minn = dist(vecs[v],core[t])
				label = t
		assert label != -1
		last_label[v] = label
		state[label] += vecs[v]
		status[label] += 1	
	return last_label