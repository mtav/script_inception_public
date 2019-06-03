{
  Program to test the mode filtered probe numbering used in Bristol FDTD 2003
}
program ModeFilteredProbe_IDs;
  var
    snap_serial_number : integer;
    probe_ident : string = '_id_';
    filename : string;
    plane_id : string;
    N : integer;
  
  {
  MAXIMUM NUMBER OF SNAPSHOTS: TODO
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN TO FIRST ID: TODO
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: TODO
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): TODO
  }
  
begin
  //N := 26+256*27+1;
  //N := 26+166*27+1;
  //N:=1;
  //writeln(N);
  //N := 26+(126-(ord('a')-1))*27;
  //N := 78;
  N := 43; //to prevent \ in filenames
  //N:=4508;
  for  snap_serial_number := 1  to  N  do
  begin

    plane_id := chr(snap_serial_number + ord('0'));
    filename := 'i'+plane_id+probe_ident+'00.prn';

    //writeln(snap_serial_number,':',plane_id);
    //writeln(plane_id);
    writeln(filename)
    
  end
  
end.
