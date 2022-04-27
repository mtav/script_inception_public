Here are some examples to test it with:

MEEP:
  meep fcen=3.14 df=0.1 sampling_time=0.01 time_signal.ctl && h5ls time_signal-ez-source.h5
MATLAB:
  close all; clear all; fcen=3.14; df=0.1; sampling_time=0.01; resolution=10; plot_time_signal(fcen, df, sampling_time, resolution);

MEEP:
  meep fcen=0.14 df=0.1 sampling_time=0.01 time_signal.ctl && h5ls time_signal-ez-source.h5
MATLAB:
  close all; clear all; fcen=0.14; df=0.1; sampling_time=0.01; resolution=10; plot_time_signal(fcen, df, sampling_time, resolution);

MEEP:
  meep fcen=5 df=0.1 sampling_time=0.01 time_signal.ctl && h5ls time_signal-ez-source.h5
MATLAB:
  close all; clear all; fcen=5; df=0.1; sampling_time=0.01; resolution=10; plot_time_signal(fcen, df, sampling_time, resolution);

Watch out for undersampling!

Note: This simulation does not have any PML layers, which might lead to reflections from the boundaries, which is why you might see a small resonance effect.
