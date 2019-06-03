function radians = radians(degrees)
  % RADIANS (DEGREES)
  %
  % Conversion function from Radians to Degrees.
  %
  % Richard Medlock 12-03-2002
  %
  % Last Updated: 18-09-2009
  % - Calculation simplified to make it more efficient
  %   based on a suggestion by Joel Parker.
  %
  % Original calculation
  % radians = ((2*pi)/360)*degrees;
  %
  % Downloaded from http://www.mathworks.com/matlabcentral/fileexchange/3263-degrees-and-radians
  % BSD License
  % Copyright (c) 2009, Richard Medlock
  % All rights reserved.
  %
  % Redistribution and use in source and binary forms, with or without 
  % modification, are permitted provided that the following conditions are 
  % met:
  %
  % * Redistributions of source code must retain the above copyright 
  %   notice, this list of conditions and the following disclaimer.
  % * Redistributions in binary form must reproduce the above copyright 
  %   notice, this list of conditions and the following disclaimer in 
  %   the documentation and/or other materials provided with the distribution
  %
  % THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
  % AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
  % IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
  % ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
  % LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
  % CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
  % SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
  % INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
  % CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
  % ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
  % POSSIBILITY OF SUCH DAMAGE.
  %
  % Note: Matlab has rad2deg/deg2rad. Why does Octave not have such basic trivial functions yet?

  radians = (pi/180)*degrees;
end
