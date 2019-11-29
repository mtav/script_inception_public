function Xangle = FIS_PositionToAngle(position, centro, factor, bool_trigonometric_mode)
  % NA=0.90 -> 1.88 degrees per 0.100 mm (section 4.5.2.2, p96 in Lifeng thesis)
  % NA=0.75 -> 1.31 degrees per 0.100 mm (section 4.3.1, p81 in Lifeng thesis)
  if bool_trigonometric_mode
    Xangle = rad2deg(atan(factor * (position - centro)));
  else
    Xangle = factor * (position - centro);
  end
end
