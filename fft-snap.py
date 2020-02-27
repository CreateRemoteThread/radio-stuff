#!/usr/bin/env python3

# UHD defaults to antenna 2.

import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from numpy import *
import getopt
import sys
import os

CONFIG_SR = 10 * 1024 ** 2
CONFIG_FREQS = []
CONFIG_FREQS.append(88 * 1024 ** 2) # FM Band
CONFIG_FREQS.append(98 * 1024 ** 2)
CONFIG_FREQS.append(108 * 1024 ** 2)
CONFIG_FREQS.append(423 * 1024 ** 2) # 433Mhz Band
CONFIG_FREQS.append(433 * 1024 ** 2)
CONFIG_FREQS.append(443 * 1024 ** 2)
CONFIG_PREFIX = "output/fft"
CONFIG_DRIVER = "uhd"

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
  plt.savefig("%s-%d.png" % (CONFIG_PREFIX,center))

def usage():
  print("-h: display this message")
  print("-d: select driver (default: uhd, antenna 2)")
  print("-f: add a frequency (default: 88,433 + 20 either way)")
  print("-w: specify the write prefix (default: fft)")
  sys.exit(0)

CONFIG_GAIN = None

def saneUnits(str_freq):
  if str_freq[-1] in ('m','M'):
    return int(str_freq[0:-1]) * 1024 ** 2
  else:
    return int(str_freq)

if __name__ == "__main__":
  args,opts  = getopt.getopt(sys.argv[1:],"hd:f:w:g:",["help","driver=","freq=","writefile=","gain="])
  for opt,arg in args:
    if opt in ("-h","--help"):
      usage()
    elif opt in ("-d","--driver"):
      CONFIG_DRIVER = arg
    elif opt in ("-w","--writefile"):
      CONFIG_PREFIX = arg
    elif opt in ("-f","--freq"):
      CONFIG_FREQS.append(saneUnits(arg))
    elif opt in ("-g","--gain"):
      CONFIG_GAIN = float(arg)
  if CONFIG_PREFIX == "output/fft":
    os.system("mkdir output")
  args = dict(driver=CONFIG_DRIVER)
  sdr = SoapySDR.Device(args)
  if CONFIG_GAIN is not None:
    sdr.setGain(SOAPY_SDR_RX, 0, CONFIG_GAIN)
  for freq in CONFIG_FREQS:
    doFrequencyFFT(sdr,freq)
