function s = get (p, f)
  if (nargin == 1)
    s.coeffs = p.coeffs;
  elseif (nargin == 2)
    if (ischar (f))
      switch (f)
        case "coeffs"
          s = p.coeffs;
        otherwise
          error ("get: invalid property %s", f);
      endswitch
    else
      error ("get: expecting the property to be a string");
    endif
  else
    print_usage ();
  endif
endfunction
