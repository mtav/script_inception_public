function position = FIS_AngleToPosition(Xangle, centro, factor, bool_trigonometric_mode)
  % NA=0.90 -> 1.88 degrees per 0.100 mm (section 4.5.2.2, p96 in Lifeng thesis)
  % NA=0.75 -> 1.31 degrees per 0.100 mm (section 4.3.1, p81 in Lifeng thesis)
  if bool_trigonometric_mode
    position = tan(deg2rad(Xangle))/factor + centro;
  else
    position = (Xangle/factor) + centro;
  end
end
