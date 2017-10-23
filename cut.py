import numpy as np
import math
from scipy.fftpack import dct 

def audio2frame(signal,frame_length,frame_step,winfunc=lambda x:np.ones((x,))):
    signal_length=len(signal)
    frame_length=int(round(frame_length))
    frame_step=int(round(frame_step))
    if signal_length<=frame_length:
        frames_num=1
    else:
        frames_num=1+int(math.ceil((1.0*signal_length-frame_length)/frame_step))
    pad_length=int((frames_num-1)*frame_step+frame_length)
    zeros=np.zeros((pad_length-signal_length,))
    pad_signal=np.concatenate((signal,zeros))
    indices=np.tile(np.arange(0,frame_length),(frames_num,1))+np.tile(np.arange(0,frames_num*frame_step,frame_step),(frame_length,1)).T
    indices=np.array(indices,dtype=np.int32)
    frames=pad_signal[indices]
    win=np.tile(winfunc(frame_length),(frames_num,1))
    return frames*win

def deframesignal(frames,signal_length,frame_length,frame_step,winfunc=lambda x:np.ones((x,))):
    signal_length=round(signal_length)
    frame_length=round(frame_length)
    frames_num=np.shape(frames)[0]
    indices=np.tile(np.arange(0,frame_length),(frames_num,1))+np.tile(np.arange(0,frames_num*frame_step,frame_step),(frame_length,1)).T
    indices=np.array(indices,dtype=np.int32)
    pad_length=(frames_num-1)*frame_step+frame_length
    if signal_length<=0:
        signal_length=pad_length
    recalc_signal=np.zeros((pad_length,))
    window_correction=np.zeros((pad_length,1))
    win=winfunc(frame_length)
    for i in range(0,frames_num):
        window_correction[indices[i,:]]=window_correction[indices[i,:]]+win+1e-15
        recalc_signal[indices[i,:]]=recalc_signal[indices[i,:]]+frames[i,:]
    recalc_signal=recalc_signal/window_correction
    return recalc_signal[0:signal_length]

def get_512_spectrun(frames):
    complex_spectrum=np.fft.rfft(frames,512)
    return np.absolute(complex_spectrum)

def spectrum_power(frames):
    return 1.0 * np.square(get_512_spectrun(frames,512))

def log_spectrum_power(frames,norm=1):
    spec_power=spectrum_power(frames,512)
    spec_power[spec_power<1e-30]=1e-30
    log_spec_power=10*np.log10(spec_power)
    if norm:
        return log_spec_power-np.max(log_spec_power)
    else:
        return log_spec_power

def pre_emphasis(signal,coefficient=0.95):
    return np.append(signal[0],signal[1:]-coefficient*signal[:-1])

def calcMFCC_delta_delta(signal,samplerate=8192,cep_num=13,low_freq=0,high_freq=None,cep_lifter=22,appendEnergy=True):
    feat=calcMFCC(signal,samplerate,0.025,0.01,cep_num,26,512,low_freq,high_freq,0.97,cep_lifter,appendEnergy)
    result1=get_delta(feat)
    result2=get_delta(result1)
    result3=np.concatenate((feat,result1),axis=1)
    result=np.concatenate((result3,result2),axis=1)
    return result


def calcMFCC_delta(signal,samplerate=8192,cep_num=13,low_freq=0,high_freq=None,cep_lifter=22,appendEnergy=True):
    feat=calcMFCC(signal,samplerate,0.025,0.01,cep_num,26,512,low_freq,high_freq,0.97,cep_lifter,appendEnergy)
    result=get_delta(feat)
    result=np.concatenate((feat,result),axis=1)
    return result

def get_delta(feat,big_theta=2,cep_num=13):
    result=np.zeros(feat.shape)
    denominator=0
    for theta in np.linspace(1,big_theta,big_theta):
        denominator=denominator+theta**2
    denominator=denominator*2
    for row in range(0, feat.shape[0]):
        tmp=np.zeros((cep_num,))
        numerator=np.zeros((cep_num,))
        for t in range(1,cep_num + 1):
            a=0
            b=0
            s=0
            for theta in range(1,big_theta + 1):
                if (t+theta)>cep_num:
                    a=0
                else:
                    a=feat[row][t+theta-1]
                if (t-theta)<1:
                    b=0
                else:
                    b=feat[row][t-theta-1]
                s+=theta*(a-b)
            numerator[t-1]=s
        tmp=numerator*1.0/denominator
        result[row]=tmp
    return result

def calcMFCC(signal,samplerate=8192,cep_num=13,low_freq=0,high_freq=None,cep_lifter=22,appendEnergy=True):
    feat,energy=fftbank(signal,samplerate,0.025,0.01,26,512,low_freq,high_freq,0.97)
    feat=np.log(feat)
    feat=dct(feat,type=2,axis=1,norm='ortho')[:,:cep_num]
    feat=lifter(feat,cep_lifter)
    if appendEnergy:
        feat[:,0]=np.log(energy)
    return feat

def fftbank(signal,samplerate=8192,low_freq=0,high_freq=None):
    high_freq=high_freq or samplerate/2
    signal=pre_emphasis(signal,0.97)
    frames=audio2frame(signal,0.025*samplerate,0.01*samplerate)
    spec_power=spectrum_power(frames,512)
    energy=np.sum(spec_power,1)
    energy=np.where(energy==0,np.finfo(float).eps,energy)
    fb=get_filter_banks(26,512,samplerate,low_freq,high_freq)
    feat=np.dot(spec_power,fb.T)
    feat=np.where(feat==0,np.finfo(float).eps,feat)
    return feat,energy

def hz2mel(hz):
    return 2595*np.log10(1+hz/700.0)

def mel2hz(mel):
    return 700*(10**(mel/2595.0)-1)

def get_filter_banks(samplerate=8192):
    low_mel=hz2mel(0)
    high_mel=hz2mel(None)
    mel_points=np.linspace(low_mel,high_mel,20+2)
    hz_points=mel2hz(mel_points)
    bin=np.floor((512+1)*hz_points/samplerate)
    fftbank=np.zeros([20,512/2+1])
    for j in range(0,20):
        for i in range(int(bin[j]),int(bin[j+1])):
            fftbank[j,i]=(i-bin[j])/(bin[j+1]-bin[j])
        for i in range(int(bin[j+1]),int(bin[j+2])):
            fftbank[j,i]=(bin[j+2]-i)/(bin[j+2]-bin[j+1])
    return fftbank

def lifter(cepstra,L=22):
    nframes,ncoeff=np.shape(cepstra)
    n=np.arange(ncoeff)
    lift=1+(L/2)*np.sin(np.pi*n/L)
    return lift*cepstra
