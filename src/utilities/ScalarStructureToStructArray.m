function struct_array = ScalarStructureToStructArray(scalar_structure)
  % struct_array = ScalarStructureToStructArray(scalar_structure)
  %
  % Converts "scalar structure containing array fields" into "structure array containing scalar fields".
  % i.e.: A.field(index) ->  A(index).field
  
  field_name_list = fieldnames(scalar_structure);

  % If the fields within scalar_structure are not arrays, there is no need for conversion. (Happens when there is only one object in an input file.)
  if ~iscell(getfield(scalar_structure, char(field_name_list(1))))
    struct_array = scalar_structure;
    return;
  end

  Nfields = length(field_name_list);

  % do the conversion
  field_name = cell(1,Nfields);
  field_array = cell(1,Nfields);
  N = cell(1,Nfields);

  for field_idx= 1:Nfields
    current_field_name = char(field_name_list(field_idx));
    current_field_array = getfield(scalar_structure, current_field_name);
    field_name{field_idx} = current_field_name;
    field_array{field_idx} = current_field_array;
    N{field_idx} = length(current_field_array);
  end

  struct_array = struct();

  for idx = 1:N{1}
    for field_idx = 1:Nfields
      struct_array(idx).(field_name{field_idx}) = field_array{field_idx}{idx};
    end
  end

end
