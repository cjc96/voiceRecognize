# -*- coding: utf-8 -*-
import io
import os
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
from google.cloud import speech
speech_client = speech.Client()
file_name = os.path.join(os.path.dirname(__file__),'dat','tempInput.dat')
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    sample = speech_client.sample(content,source_uri=None,encoding='LINEAR16',sample_rate_hertz=8192)
output = open('output.txt', 'wb')
alternatives = sample.recognize('en_US')
alternative = alternatives[0]
result = alternative.transcript
confidence = alternative.confidence
print result, confidence, 1
result = result + '|' + str(confidence)
output.write(result.encode('utf8'))
output.write('\n'.encode('utf8'))
alternatives = sample.recognize('cmn-Hans-CN')
alternative = alternatives[0]
result = alternative.transcript
confidence = alternative.confidence
print result, confidence, 2
result = result + '|' + str(confidence)
output.write(result.encode('utf8'))
output.close()
