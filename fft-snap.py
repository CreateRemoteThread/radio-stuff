#!/usr/bin/env python3

# UHD DEFAULTS TO ANTENNA 2

import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import matplotlib
# import psd
# matplotlib.use("Agg")
import matplotlib.pyplot as plt
from numpy import *

#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results: print(result)

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="uhd")
sdr = SoapySDR.Device(args)

CONFIG_SR = 10 * 1024 ** 2

#query device info
print(sdr.listAntennas(SOAPY_SDR_RX, 0))
print(sdr.listGains(SOAPY_SDR_RX, 0))
freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
for freqRange in freqs: print(freqRange)

# _psd = psd.PSD(bins,CONFIG_SR,fft_window=8192,fft_overlap=0.5,crop_factor=False,

def doFrequencyFFT(sdr,center):
  sdr.setSampleRate(SOAPY_SDR_RX, 0, CONFIG_SR)
  sdr.setFrequency(SOAPY_SDR_RX, 0, center)
  rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
  sdr.activateStream(rxStream) #start streaming
  buff = numpy.array([0]*10 * 1024 ** 2, numpy.complex64)
  fig, ax = plt.subplots()
  sr = sdr.readStream(rxStream, [buff], len(buff))
  sdr.deactivateStream(rxStream) #stop streaming
  sdr.closeStream(rxStream)
  ax.specgram(buff[0:sr.ret],NFFT=256,Fs=CONFIG_SR,Fc=center,noverlap=128)
  plt.show()

doFrequencyFFT(sdr,95 * 1024 ** 2)
