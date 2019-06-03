% Returns the Planck constant h in eV*s
function h_eVs = get_h_eVs()
  h_eVs = get_h()/get_e(); % eV*s
end
