%% -*- texinfo -*-
%% @deftypefn  {Function File} {} polynomial ()
%% @deftypefnx {Function File} {} polynomial (@var{a})
%% Create a polynomial object representing the polynomial
%%
%% @example
%% a0 + a1 * x + a2 * x^2 + @dots{} + an * x^n
%% @end example
%%
%% @noindent
%% from a vector of coefficients [a0 a1 a2 @dots{} an].
%% @end deftypefn

function p = polynomial (a)
  %nargin
  if (nargin == 0)
    p.coeffs = [0];
    p = class (p, "polynomial");
  elseif (nargin == 1)
    if (strcmp (class (a), "polynomial"))
      p = a;
    elseif (isvector (a) && isreal (a))
      p.coeffs = a(:).';
      p = class (p, "polynomial");
    else
      error ("polynomial: expecting real vector");
    endif
  else
    disp('usage:')
    print_usage();
  endif
endfunction
