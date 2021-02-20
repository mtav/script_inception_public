#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division

import numpy
import warnings
import configparser
from numpy import array

import photonics.utilities as utilities
from photonics.utilities.common import *
from photonics.constants.physcon import get_c0, get_e, get_eV, get_epsilon0, get_mu0, get_h, get_h_eVs, get_hb, get_me

from .meshobject import *
from .excitationTemplate import *

'''
Various type of Excitation objects, used for writing the excitations into the .inp file.
.. todo:: Check that MIN_TIME_OFFSET_TIME_CONSTANT_RATIO=3 is a sufficient condition.
'''

MIN_TIME_OFFSET_TIME_CONSTANT_RATIO = 5

class Excitation(object):
  '''
  The base class for BFDTD excitations.
  
  When using a gaussian sinewave, undesired effects (part of the signal cut off) might happen, if the time offset is too small compared to the time constant.
  
  To prevent this, the writing procedure automatically checks if::
  
      MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant > self.time_offset.
  
  If this is the case, there are 3 possible outcomes, depending on the value of **self.TimeOffsetSafetyBehaviour**:

  * self.TimeOffsetSafetyBehaviour=0 (the default): adapt the time offset by setting ``self.time_offset = MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant``
  * self.TimeOffsetSafetyBehaviour=1: raise an Exception
  * self.TimeOffsetSafetyBehaviour=2: ignore and continue writing
  
  .. note:: You can change MIN_TIME_OFFSET_TIME_CONSTANT_RATIO in interactive mode as follows: ``bfdtd.excitation.MIN_TIME_OFFSET_TIME_CONSTANT_RATIO=42``
  
  From MEEP documentation. Not fully implemented yet, but the plan is to clearly and accurately document the sources and make it easier to get exactly what we want.
  It is possible that BFDTD gaussian sources behave differently than MEEP sources.
  BFDTD sources do not seem to have a proper cutoff for instance, or at least not properly return to zero and stay there.
  
  .. note:: Units: Usually DISTANCE=1μm, so that frequencies are in MHz and times in μs.
  
  Gaussian source:
  
    A Gaussian-pulse source roughly proportional to exp( − iωt − (t − t0)^2 / (2*w^2)). cf MEEP documentation.
  
  Attributes:
  
  * frequency [number]:
  
      The center frequency f in units of (m/s)/DISTANCE (or ω in units of 2π*(m/s)/DISTANCE).
      
      No default value.
      
      You can instead specify:
      
        * wavelength = c0/f in units of DISTANCE
        * period = 1/f in units of DISTANCE/(m/s)
      
  * width [number]:
  
      The width w used in the Gaussian.
      No default value.
      You can instead specify:
      
      * fwidth x, which is a synonym for (width (/ 1 x)) (i.e. the frequency width is proportional to the inverse of the temporal width)      
      * FWHM_time
      * FWHM_frequency
      * FWHM_angular_frequency
      
  * start-time [number]:
  
      The starting time for the source; default is 0 (turn on at t = 0). (Not the time of the peak! See below.)
      You can instead specify:
      
      * end-time
      * peak-time
      
  * cutoff [number]:
  
      How many widths the current decays for before we cut it off and set it to zero—this applies for both turn-on and turn-off of the pulse.
      The default is 5.0.
      A larger value of cutoff will reduce the amount of high-frequency components that are introduced by the start/stop of the source,
      but will of course lead to longer simulation times.
      The peak of the gaussian is reached at the time t0= start-time + cutoff*width. 
  
  .. todo:: check coherence between excitation_direction (templates) and E,H (excitation) attributes. Are both necessary? Leads to confusion.
  .. todo:: add centre/size/orientation options/attributes/methods to excitation, to make it easier to switch between orientations
  .. todo:: Improve documentation.
  '''
  def __init__(self,
                name = None,
                current_source = None,
                P1 = None,
                P2 = None,
                E = None,
                H = None,
                Type = None,
                time_constant = None,
                amplitude = None,
                time_offset = None,
                frequency = None,
                param1 = None,
                param2 = None,
                template_filename = None,
                template_source_plane = None,
                template_target_plane = None,
                template_direction = None,
                template_rotation = None,
                layer = None,
                group = None):

    if name is None: name = 'excitation'
    if current_source is None: current_source = 7
    if P1 is None: P1 = [0,0,0]
    if P2 is None: P2 = [0,0,0]
    if E is None: E = [1,0,0]
    if H is None: H = [0,0,0]
    if Type is None: Type = 10
    if time_constant is None: time_constant = 4.000000E-09 #mus
    if amplitude is None: amplitude = 1.000000E+01 #V/mum???
    if time_offset is None: time_offset = 2.700000E-08 #mus
    if frequency is None: frequency = get_c0() # in MHz, this corresponds to a wavelength of 1mum
    if param1 is None: param1 = 0
    if param2 is None: param2 = 0
    if template_source_plane is None: template_source_plane = 'x'
    if template_target_plane is None: template_target_plane = 'x'
    if template_direction is None: template_direction = 0
    if template_rotation is None: template_rotation = 0
    if layer is None: layer = 'excitation'
    if group is None: group = 'excitation'

    # read configuration options from a config file
    # if it does not exist, use defaults and create the config file
    config = configparser.ConfigParser({
                                          'SafetyChecks': 'True',
                                          'AutoFix': 'True',
                                        })
    
    configdir = os.path.join(utilities.getuserdir.getuserdir(), '.config', 'script_inception_public')
    os.makedirs(configdir, exist_ok=True)
    configfile_name = os.path.join(configdir, 'Excitation.ini')
    #print('configfile_name = ', configfile_name)
    configfiles_read = config.read(configfile_name)
    #print('configfiles_read = ', configfiles_read)
    self.SafetyChecks = config['DEFAULT'].getboolean('SafetyChecks')
    self.AutoFix = config['DEFAULT'].getboolean('AutoFix')
    
    if not configfiles_read:
      print('No config file found. Creating {}'.format(configfile_name))
      with open(configfile_name, 'w') as configfile:
        config.write(configfile)

    self.name = name
    self.layer = layer
    self.group = group
    self.current_source = current_source
    self.P1 = P1
    self.P2 = P2
    self.E = E
    self.H = H
    self.Type = Type
    self.time_constant = time_constant
    self.amplitude = amplitude
    self.time_offset = time_offset
    self.frequency = frequency
    self.param1 = param1
    self.param2 = param2
    self.template_filename = template_filename
    self.template_source_plane = template_source_plane
    self.template_target_plane = template_target_plane
    self.template_direction = template_direction
    self.template_rotation = template_rotation

    self.meshing_parameters = MeshingParameters()
    
    self.fixLowerUpperAtWrite = True
    self.useForMeshing = True # set to False to disable use of this object during automeshing
    
    # .. todo:: deprecated, to be removed once a better safety/autofix system with adjustable reactions is put in place
    self.TimeOffsetSafetyBehaviour = 0

  def getName(self):
    return(self.name)

  def setEx(self):
    self.E = [1,0,0]
    return

  def setEy(self):
    self.E = [0,1,0]
    return

  def setEz(self):
    self.E = [0,0,1]
    return

  def getExcitedComponentNames(self):
    L = []
    if self.E[0] != 0:
      L.append('Ex')
    if self.E[1] != 0:
      L.append('Ey')
    if self.E[2] != 0:
      L.append('Ez')
    if self.H[0] != 0:
      L.append('Hx')
    if self.H[1] != 0:
      L.append('Hy')
    if self.H[2] != 0:
      L.append('Hz')

    return ', '.join(L)

  def setName(self, name):
    self.name = name
    return

  def setWavelength(self, lambda_mum):
    self.frequency = get_c0()/lambda_mum
  def setLambda(self, lambda_mum):
    warnings.warn('setLambda() is deprecated. Please use setWavelength() instead.', DeprecationWarning)
    self.setWavelength(lambda_mum)
    
  def setFrequency(self, freq_MHz):
    self.frequency = freq_MHz

  def setPeriod(self, period):
    self.setFrequency(1/period)
    return(period)

  def printInfo(self):
    print('StartTime = {}'.format(self.getStartTime()))
    print('PeakTime = {}'.format(self.getPeakTime()))
    print('EndTime = {}'.format(self.getEndTime()))
    print('Period = {}'.format(self.getPeriod()))
    print('WavelengthRange = {}'.format(self.getWavelengthRange()))
    print('WavelengthCentral = {}'.format(self.getWavelength()))

  #######
  # start, peak, end time settings, i.e. time offsets
  def setTimeOffset(self, time_offset=None):
    '''
    Set the time offset.
    If *time_offset* is *None*, it adapts the time offset by setting ``self.time_offset = MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant``
    
    The time offset can be get/set using the following three alternatives:
    
    * StartTime = self.time_offset - MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant :
    
      * :py:func:`setStartTime`
      * :py:func:`getStartTime`
      
    * PeakTime = self.time_offset :
    
      * :py:func:`getPeakTime`
      * :py:func:`setPeakTime`
      
    * EndTime = self.time_offset + MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant :
    
      * :py:func:`getEndTime`
      * :py:func:`setEndTime`

    .. image:: /images/excitation_doc_annotated.png
       :align: center

    '''
    if time_offset is None:
      self.time_offset = self.getAdaptedTimeOffset()
    else:
      self.time_offset = time_offset
    return(self.time_offset)
  
  def getTimeOffset(self):
    ''' cf :py:func:`setTimeOffset` '''
    return self.time_offset
  
  def getAdaptedTimeOffset(self):
    '''
    Returns ``MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant``
    
    .. todo:: Round up to 6 decimals to make sure it is bigger than the required min value after writing out files with "{:E}".format(time_offset).
    
    cf :py:func:`setTimeOffset`
    '''
    new_time_offset = MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant
    #exponent = np.floor(np.log10(np.abs(x)))
    #mantissa = 
    return(new_time_offset)
  
  def getStartTime(self):
    ''' cf :py:func:`setTimeOffset` '''
    return(self.getPeakTime() - MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.getTimeConstant())
  
  def getPeakTime(self):
    ''' cf :py:func:`setTimeOffset` '''
    return self.getTimeOffset()
  
  def getEndTime(self):
    ''' cf :py:func:`setTimeOffset` '''
    return(self.getPeakTime() + MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.getTimeConstant())
    
  def setStartTime(self, start_time):
    ''' cf :py:func:`setTimeOffset` '''
    return self.setPeakTime(start_time + MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.getTimeConstant())

  def setPeakTime(self, peak_time):
    ''' cf :py:func:`setTimeOffset` '''
    return self.setTimeOffset(peak_time)
  
  def setEndTime(self, end_time):
    ''' cf :py:func:`setTimeOffset` '''
    return self.setPeakTime(end_time - MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.getTimeConstant())
    
  #######
  
  def setTimeConstant(self, time_constant):
    self.time_constant = time_constant
    return(self.time_constant)
    
  def setFrequencyRange(self, fmin, fmax, autofix=False):
    '''
    Sets central frequency and frequency width so that the FFT of the pulse covers from fmin to fmax.
    
    Formulas used:
    
      * frequency = 0.5*(fmin+fmax)
      * time_constant = 1/(4*(fmax-fmin))
    
    .. todo:: Explain what exactly it means for the FFT (FWHM or other?).
    .. todo:: Make it equivalent to fwidth setting in MEEP.
    .. todo:: Add a warning if the user is trying to make the frequency range too wide (which leads to not really oscillating source since time width will be smaller than sine period).
    .. todo:: Add warning if the time offset is to short OR set the time offset as well...
    '''
    
    f0 = 0.5*(fmin + fmax)
    deltaFreq = numpy.abs(fmax - fmin)
    
    #if f0 < 4*deltaFreq:
      #print('ERROR: f0={} < 4*deltaFreq={}'.format(f0, 4*deltaFreq))
    if f0 < 4*deltaFreq:
      if not math.isclose(f0, 4*deltaFreq):
        D = f0/4
        fa = f0 - D/2
        fb = f0 + D/2
        if autofix:
          return self.setFrequencyRange(fa, fb, autofix=False)
        else:
          raise Exception('''Specified frequency range is too large.
            f0={} < 4*|fmax-fmin|={}
            Make sure that 4*|fmax-fmin| < f0=(fmax+fmin)/2.
            fmin = {}
            fmax = {}
            f0 = {}
            |fmax-fmin| = {}
            Try:
              fmin = {}
              fmax = {}
            '''.format(f0, 4*deltaFreq, fmin, fmax, f0, deltaFreq, fa, fb))
      else:
        print('Specified frequency range is slighty too big, but close enough: f0={} < 4*deltaFreq={}'.format(f0, 4*deltaFreq))
      
    self.setFrequency( f0 )
    self.setTimeConstant( 1/(4*deltaFreq) )
    
    self.checkPeriodvsTimeConstant(raise_exception=True)
    
    return (self.frequency, self.time_constant)
  
  def setWavelengthRange(self, lambda_min, lambda_max):
    fmax = get_c0()/lambda_min
    fmin = get_c0()/lambda_max
    return self.setFrequencyRange(fmin, fmax)
  
  def getFrequencyRange(self):
    df = 1/(4*self.time_constant)
    return (self.getFrequency()-0.5*df, self.getFrequency()+0.5*df)
  
  def getFrequencyMin(self):
    (fmin, fmax) = self.getFrequencyRange()
    return fmin
  
  def getFrequencyMax(self):
    (fmin, fmax) = self.getFrequencyRange()
    return fmax

  def getWavelengthRange(self):
    (fmin, fmax) = self.getFrequencyRange()
    return (get_c0()/fmax, get_c0()/fmin)

  def getWavelengthMin(self):
    (fmin, fmax) = self.getFrequencyRange()
    return get_c0()/fmax

  def getWavelengthMax(self):
    (fmin, fmax) = self.getFrequencyRange()
    return get_c0()/fmin

  def setAmplitude(self, amplitude):
    self.amplitude = amplitude
    return

  def getWavelength(self):
    return get_c0()/self.frequency

  def getLambda(self):
    warnings.warn('getLambda() is deprecated. Please use getWavelength() instead.', DeprecationWarning)
    return self.getWavelength()
    
  def getFrequency(self):
    return self.frequency

  def getPeriod(self):
    return(1/self.getFrequency())

  def getAmplitude(self):
    return self.amplitude

  def getTimeConstant(self):
    return self.time_constant
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'current_source = ' + str(self.current_source) + '\n' +\
    'P1 = ' + str(self.P1) + '\n' +\
    'P2 = ' + str(self.P2) + '\n' +\
    'E = ' + str(self.E) + '\n' +\
    'H = ' + str(self.H) + '\n' +\
    'Type = ' + str(self.Type) + '\n' +\
    'time_constant = ' + str(self.time_constant) + '\n' +\
    'amplitude = ' + str(self.amplitude) + '\n' +\
    'time_offset = ' + str(self.time_offset) + '\n' +\
    'frequency = ' + str(self.frequency) + '\n' +\
    'param1 = ' + str(self.param1) + '\n' +\
    'param2 = ' + str(self.param2) + '\n' +\
    'template_filename = ' + str(self.template_filename) + '\n' +\
    'template_source_plane = ' + str(self.template_source_plane) + '\n' +\
    'template_target_plane = ' + str(self.template_target_plane) + '\n' +\
    'template_direction = ' + str(self.template_direction) + '\n' +\
    'template_rotation = ' + str(self.template_rotation)
    return ret
    
  def getExtension(self):
    return (array(self.P1), array(self.P2))
    
  def setExtension(self,P1,P2):
    self.P1, self.P2 = fixLowerUpper(P1, P2)
    
  def getLocation(self):
    return self.getCentro()

  def setLocation(self, loc):
    return self.setCentro(loc)
    
  def getCentro(self):
    self.P1 = array(self.P1)
    self.P2 = array(self.P2)
    return 0.5*(self.P1+self.P2)
    
  def getSize(self):
    return numpy.absolute(array(self.P2) - array(self.P1))
    
  def setSize(self, size_vec3):
    C = self.getCentro()
    size_vec3 = array(size_vec3)
    self.P1 = C - 0.5*size_vec3
    self.P2 = C + 0.5*size_vec3
    return size_vec3
    
  def setCentro(self, nova_centro):
    nova_centro = array(nova_centro)    
    nuna_centro = self.getCentro()
    self.translate(nova_centro - nuna_centro)
    return nova_centro
    
  def translate(self, vec3):
    self.P1 = array(self.P1) + array(vec3)
    self.P2 = array(self.P2) + array(vec3)
    return vec3
    
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    idx = 0
    self.current_source = int(entry.data[idx]); idx = idx+1
    self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.E = int_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.H = int_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.Type = int(entry.data[idx]); idx = idx+1
    self.time_constant = float(entry.data[idx]); idx = idx+1
    self.amplitude = float(entry.data[idx]); idx = idx+1
    self.time_offset = float(entry.data[idx]); idx = idx+1
    if idx<len(entry.data):
      self.frequency = float(entry.data[idx]); idx = idx+1
    if idx<len(entry.data):
      self.param1 = float(entry.data[idx]); idx = idx+1
    if idx<len(entry.data):
      self.param2 = float(entry.data[idx]); idx = idx+1
    if idx<len(entry.data):
      self.template_filename = entry.data[idx]; idx = idx+1
    if idx<len(entry.data):
      self.template_source_plane = entry.data[idx]; idx = idx+1
    if idx<len(entry.data):
      self.template_target_plane = entry.data[idx]; idx = idx+1
    if idx<len(entry.data):
      self.template_direction = int(entry.data[idx]); idx = idx+1
    if idx<len(entry.data):
      self.template_rotation = int(entry.data[idx]); idx = idx+1
    return(0)
  
  def check(self):
    '''
    Checks the excitation for common mistakes.
    '''
    
    self.checkPeriodvsTimeConstant(raise_exception=True)
      
    # check that start time is positive
    if self.getStartTime() < 0:
      raise Exception('self.getStartTime()={} < 0'.format(self.getStartTime()))
    return
  
  def checkPeriodvsTimeConstant(self, raise_exception=False):
    # check that Period <= TimeConstant
    #
    # The 1e-6 part is a hack to deal with the limited number of digits in the ASCII input files.
    # Do this properly using the decimal module and/or math.isclose. cf: https://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
    # .. todo:: finish testing by writing, then reading.
    
    #if self.getPeriod() > self.getTimeConstant():
      #if not math.isclose(self.getPeriod(), self.getTimeConstant()):
        #raise Exception('NEW: self.getPeriod()={} > self.getTimeConstant()={}'.format(self.getPeriod(), self.getTimeConstant()))
        
    #if self.getPeriod()/self.getTimeConstant() - 1 > 1e-6:
    
    if self.getPeriod() > self.getTimeConstant():
      msg = 'self.getPeriod()={} > self.getTimeConstant()={}'.format(self.getPeriod(), self.getTimeConstant())
      if not math.isclose(self.getPeriod(), self.getTimeConstant()):
        print(msg)
        #print('self.getPeriod()/self.getTimeConstant() - 1 = {:e}'.format(self.getPeriod()/self.getTimeConstant() - 1))
        if raise_exception:
          raise Exception(msg)
        return False
      else:
        print('The period is slightly bigger than the time constant, but close enough: {}'.format(msg))

    else:
      return True
  
  def fix(self):
    '''
    Automatically fix common mistakes.
    '''
    
    # fix time constant
    if not self.checkPeriodvsTimeConstant(raise_exception=False):
      sys.stderr.write('WARNING: Setting time_constant = period = {}.\n'.format(self.getPeriod()))
      self.setTimeConstant(self.getPeriod())
    
    # fix time offset
    # round min_time_offset before checking to avoid unnecessary warnings
    min_time_offset = float('{:E}'.format(MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*self.time_constant))
    if min_time_offset > self.getTimeOffset():
      default_message = 'WARNING: ( {}*time_constant = {} ) > ( time_offset = {} ). cf documentation on self.TimeOffsetSafetyBehaviour.'.format(MIN_TIME_OFFSET_TIME_CONSTANT_RATIO, min_time_offset, self.getTimeOffset())
      if self.TimeOffsetSafetyBehaviour == 0:
        self.setTimeOffset(self.getAdaptedTimeOffset())
        sys.stderr.write(default_message + '\n')
        sys.stderr.write('WARNING: Setting time_offset = {}*time_constant = {}.\n'.format(MIN_TIME_OFFSET_TIME_CONSTANT_RATIO, self.getTimeOffset()))
      elif self.TimeOffsetSafetyBehaviour == 1:
        raise Exception(default_message)
      else:
        sys.stderr.write(default_message + '\n')
    return
  
  def disableSafetyChecks(self):
    self.SafetyChecks = False
  
  def enableSafetyChecks(self):
    self.SafetyChecks = True
  
  def disableAutoFix(self):
    self.AutoFix = False
  
  def enableAutoFix(self):
    self.AutoFix = True
  
  def write_entry(self, FILE=sys.stdout, AutoFix=True, SafetyChecks=True):
    '''
    write entry into FILE
    .. todo:: reduce code duplication here
    .. todo:: Should fix+check functions be called from BFDTDobject? Or should fix+check args be passed to write_entry? or should object's AutoFix/SafetyChecks be modified from BFDTDobject?
    
    Every function should do one thing and do it well -> no fix+check in here
    Having fix+check in here reduces risk of accidental bad output writing -> fix+check should be in here
    
    Writing bad output should be made difficult, but not too difficult for testing purposes.
    '''
    
    # autofix
    if AutoFix:
      self.fix()
    
    # safety checks
    if SafetyChecks:
      self.check()
    
    if self.current_source != 11:
      if self.fixLowerUpperAtWrite:
        self.P1, self.P2 = fixLowerUpper(self.P1, self.P2)
      FILE.write('EXCITATION **name={}\n'.format(self.getName()))
      FILE.write('{\n')
      FILE.write("{:d} ** CURRENT SOURCE\n".format(self.current_source))
      FILE.write("{:E} **X1\n".format(self.P1[0]))
      FILE.write("{:E} **Y1\n".format(self.P1[1]))
      FILE.write("{:E} **Z1\n".format(self.P1[2]))
      FILE.write("{:E} **X2\n".format(self.P2[0]))
      FILE.write("{:E} **Y2\n".format(self.P2[1]))
      FILE.write("{:E} **Z2\n".format(self.P2[2]))
      FILE.write("{:d} **EX\n".format(self.E[0]))
      FILE.write("{:d} **EY\n".format(self.E[1]))
      FILE.write("{:d} **EZ\n".format(self.E[2]))
      FILE.write("{:d} **HX\n".format(self.H[0]))
      FILE.write("{:d} **HY\n".format(self.H[1]))
      FILE.write("{:d} **HZ\n".format(self.H[2]))
      FILE.write("{:d} **GAUSSIAN MODULATED SINUSOID\n".format(self.Type))
      FILE.write("{:E} **TIME CONSTANT (mus if dimensions in mum)\n".format(self.getTimeConstant()))
      FILE.write("{:E} **AMPLITUDE\n".format(self.getAmplitude()))
      FILE.write("{:E} **TIME OFFSET (mus if dimensions in mum)\n".format(self.getTimeOffset()))
      FILE.write("{:E} **FREQUENCY (MHz if dimensions in mum) (c0/f = {:E})\n".format(self.getFrequency(), get_c0()/self.getFrequency()))
      FILE.write("{:E} **UNUSED PARAMETER\n".format(self.param1))
      FILE.write("{:E} **UNUSED PARAMETER\n".format(self.param2))
      if self.template_filename:
        # template specific
        # NOTE: Adding these template parameters seems to have no effect with current_source!=11, but it makes sense to not write them if no template_filename has been defined.
        FILE.write(addDoubleQuotesIfMissing(self.template_filename) + ' ** TEMPLATE FILENAME\n')
        FILE.write(addDoubleQuotesIfMissing(self.template_source_plane) + ' ** TEMPLATE SOURCE PLANE\n')
      FILE.write('}\n')
      FILE.write('\n')
    else:
      self.E = [1,1,1]
      self.H = [1,1,1]
      self.P1, self.P2 = fixLowerUpper(self.P1, self.P2)
      FILE.write('EXCITATION **name='+self.name+'\n')
      FILE.write('{\n')
      FILE.write("%d ** CURRENT SOURCE\n" % self.current_source)
      FILE.write("%E **X1\n" % self.P1[0])
      FILE.write("%E **Y1\n" % self.P1[1])
      FILE.write("%E **Z1\n" % self.P1[2])
      FILE.write("%E **X2\n" % self.P2[0])
      FILE.write("%E **Y2\n" % self.P2[1])
      FILE.write("%E **Z2\n" % self.P2[2])
      FILE.write("%d **EX\n" % self.E[0])
      FILE.write("%d **EY\n" % self.E[1])
      FILE.write("%d **EZ\n" % self.E[2])
      FILE.write("%d **HX\n" % self.H[0])
      FILE.write("%d **HY\n" % self.H[1])
      FILE.write("%d **HZ\n" % self.H[2])
      FILE.write("%d **GAUSSIAN MODULATED SINUSOID\n" % self.Type)
      FILE.write("%E **TIME CONSTANT\n" % self.time_constant)
      FILE.write("%E **AMPLITUDE\n" % self.amplitude)
      FILE.write("{:E} **TIME OFFSET\n".format(self.getTimeOffset()))
      FILE.write("%E **FREQUENCY (MHz if dimensions in mum) (c0/f = %E)\n" % (self.frequency, get_c0()/self.frequency))
      FILE.write("%d **UNUSED PARAMETER\n" % self.param1)
      FILE.write("%d **UNUSED PARAMETER\n" % self.param2)
      if self.template_filename:
        # template specific
        FILE.write(addDoubleQuotesIfMissing(self.template_filename) + ' ** TEMPLATE FILENAME\n')
        FILE.write(addDoubleQuotesIfMissing(self.template_source_plane) + ' ** TEMPLATE SOURCE PLANE\n')
        FILE.write(addDoubleQuotesIfMissing(self.template_target_plane) + ' ** TEMPLATE TARGET PLANE\n')
        FILE.write("%d ** DIRECTION 0=-ve 1=+ve\n" % self.template_direction)
        FILE.write("%d ** ROTATE 0=no, 1=yes\n" % self.template_rotation)
      FILE.write('}\n')
      FILE.write('\n')

  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.P1[0],self.P2[0]])
    objy = numpy.sort([self.P1[1],self.P2[1]])
    objz = numpy.sort([self.P1[2],self.P2[2]])
    eps = 1
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz

class ExcitationWithGaussianTemplate(Excitation):
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    centre = None, 
    sigma_x = None,
    sigma_y = None,
    amplitude = None,
    plane_direction = None,
    excitation_direction = None,
    frequency = None,
    template_filename = None,
    mesh = None):

    if name is None: name = 'excitation_with_gaussian_template'
    if layer is None: layer = 'excitation_with_gaussian_template'
    if group is None: group = 'excitation_with_gaussian_template'
    if centre is None: centre = [0,0,0]
    if sigma_x is None: sigma_x = 1
    if sigma_y is None: sigma_y = 1
    if amplitude is None: amplitude = 1
    if plane_direction is None: plane_direction = [0,0,1]
    if excitation_direction is None: excitation_direction = ['Exre']
    if frequency is None: frequency = 1
    if template_filename is None: template_filename = 'template.dat'
    if mesh is None: mesh = MeshObject()

    Excitation.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    
    self.centre = centre
    self.sigma_x = sigma_x
    self.sigma_y = sigma_y
    self.amplitude = amplitude
    
    # the mesh is essential for template excitations
    self.mesh = mesh
    
    self.plane_direction = plane_direction
    self.excitation_direction = excitation_direction # for the template generation
    self.frequency = frequency
    self.template_filename = template_filename

    self.current_source = 11
    self.E = [1,1,1] # for the .inp file

    # set extension
    plane_direction_vector, plane_direction_alpha = getVecAlphaDirectionFromVar(self.plane_direction)
    diagonal = (numpy.array(plane_direction_vector)^numpy.array([1,1,1]))
    sigma = max(sigma_x, sigma_y)
    self.setExtension(centre - sigma*diagonal, centre + sigma*diagonal)

    self.updateTemplate()
  
  def getTemplate(self):
    updateTemplate()
    return self.template
  
  def updateTemplate(self):
    # set up template
    plane_direction_vector, plane_direction_alpha = getVecAlphaDirectionFromVar(self.plane_direction)

    self.template_source_plane = plane_direction_alpha
    self.template_target_plane = plane_direction_alpha
    self.template_direction = 1
    self.template_rotation = 1

    out_col_name = self.excitation_direction
  
    if plane_direction_alpha=='x':
      column_titles = ['y','z']
      x = self.centre[1]
      y = self.centre[2]
      x_list = self.mesh.getYmesh()
      y_list = self.mesh.getZmesh()
      P1 = [self.centre[0],min(x_list),min(y_list)]
      P2 = [self.centre[0],max(x_list),max(y_list)]
    if plane_direction_alpha=='y':
      column_titles = ['x','z']
      x = self.centre[0]
      y = self.centre[2]
      x_list = self.mesh.getXmesh()
      y_list = self.mesh.getZmesh()
      P1 = [min(x_list),self.centre[1],min(y_list)]
      P2 = [max(x_list),self.centre[1],max(y_list)]
    if plane_direction_alpha=='z':
      column_titles = ['x','y']
      x = self.centre[0]
      y = self.centre[1]
      x_list = self.mesh.getXmesh()
      y_list = self.mesh.getYmesh()
      P1 = [min(x_list),min(y_list),self.centre[2]]
      P2 = [max(x_list),max(y_list),self.centre[2]]
      
    column_titles.extend(['Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim'])

    # set extension
    self.setExtension(P1, P2)
    
    self.template = ExcitationGaussian1(amplitude = self.amplitude, beam_centre_x = x, beam_centre_y = y, sigma_x = self.sigma_x, sigma_y = self.sigma_y, fileName = self.template_filename)
    #template = ExcitationGaussian2(amplitude = amplitude, beam_centre_x = x, beam_centre_y = y, c = 0, sigma = size, fileName='template.dat')
    self.template.x_list = x_list
    self.template.y_list = y_list
    self.template.out_col_name = out_col_name
    self.template.column_titles = column_titles
    
  def write_entry(self, FILE):

    self.updateTemplate()
    
    # write the INP entry using the parent class
    Excitation.write_entry(self, FILE)
    
    # write the template
    #print self.mesh
    self.template.writeDatFile( os.path.join(os.path.dirname(FILE.name), self.template_filename) )

class ExcitationWithUniformTemplate(Excitation):
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    centre = None, 
    amplitude = None,
    plane_direction = None,
    excitation_direction = None,
    frequency = None,
    template_filename = None,
    mesh = None):

    if name is None: name = 'excitation_with_uniform_template'
    if layer is None: layer = 'excitation_with_uniform_template'
    if group is None: group = 'excitation_with_uniform_template'
    if centre is None: centre = [0,0,0]
    if amplitude is None: amplitude = 1
    if plane_direction is None: plane_direction = [0,0,1]
    if excitation_direction is None: excitation_direction = ['Exre']
    if frequency is None: frequency = 1
    if template_filename is None: template_filename = 'template.dat'
    if mesh is None: mesh = MeshObject()

    Excitation.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    
    self.centre = centre
    self.amplitude = amplitude
    
    # the mesh is essential for template excitations
    self.mesh = mesh
    
    self.plane_direction = plane_direction
    self.excitation_direction = excitation_direction # for the template generation
    self.frequency = frequency
    self.template_filename = template_filename

    self.current_source = 11
    self.E = [1,1,1] # for the .inp file

    # set extension
    plane_direction_vector, plane_direction_alpha = getVecAlphaDirectionFromVar(self.plane_direction)
    diagonal = (numpy.array(plane_direction_vector)^numpy.array([1,1,1]))
    self.setExtension(centre - diagonal, centre + diagonal)

    self.updateTemplate()
  
  def getTemplate(self):
    updateTemplate()
    return self.template
  
  def updateTemplate(self):
    # set up template
    plane_direction_vector, plane_direction_alpha = getVecAlphaDirectionFromVar(self.plane_direction)

    self.template_source_plane = plane_direction_alpha
    self.template_target_plane = plane_direction_alpha
    self.template_direction = 1
    self.template_rotation = 1

    out_col_name = self.excitation_direction
  
    if plane_direction_alpha=='x':
      column_titles = ['y','z']
      x = self.centre[1]
      y = self.centre[2]
      x_list = self.mesh.getYmesh()
      y_list = self.mesh.getZmesh()
      P1 = [self.centre[0],min(x_list),min(y_list)]
      P2 = [self.centre[0],max(x_list),max(y_list)]
    if plane_direction_alpha=='y':
      column_titles = ['x','z']
      x = self.centre[0]
      y = self.centre[2]
      x_list = self.mesh.getXmesh()
      y_list = self.mesh.getZmesh()
      P1 = [min(x_list),self.centre[1],min(y_list)]
      P2 = [max(x_list),self.centre[1],max(y_list)]
    if plane_direction_alpha=='z':
      column_titles = ['x','y']
      x = self.centre[0]
      y = self.centre[1]
      x_list = self.mesh.getXmesh()
      y_list = self.mesh.getYmesh()
      P1 = [min(x_list),min(y_list),self.centre[2]]
      P2 = [max(x_list),max(y_list),self.centre[2]]
      
    column_titles.extend(['Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim'])

    # set extension
    self.setExtension(P1, P2)
    
    self.template = ExcitationUniform( amplitude = self.amplitude, fileName = self.template_filename )
    #template = ExcitationGaussian2(amplitude = amplitude, beam_centre_x = x, beam_centre_y = y, c = 0, sigma = size, fileName='template.dat')
    self.template.x_list = x_list
    self.template.y_list = y_list
    self.template.out_col_name = out_col_name
    self.template.column_titles = column_titles
    
  def write_entry(self, FILE):

    self.updateTemplate()
    
    # write the INP entry using the parent class
    Excitation.write_entry(self, FILE)
    
    # write the template
    #print self.mesh
    self.template.writeDatFile( os.path.dirname(FILE.name) + os.path.sep + self.template_filename)

if __name__ == '__main__':
  pass
