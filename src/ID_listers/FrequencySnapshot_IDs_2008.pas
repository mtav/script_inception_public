{
  Program to test the frequency snapshot numbering used in Bristol FDTD 2003
}
program FrequencySnapshot_IDs;
  var
    snap_serial_number : integer;
    probe_ident : string = '_id_';
    snap_plane : string = 'x';
    ilo,ihi : integer;
    snap_time_number : integer;
    filename : string;
    plane_id : string;
    N : integer;
    i : integer;
  
  {
  MAXIMUM NUMBER OF SNAPSHOTS: 32767 (=(2^8)*(2^8)/2 -1)
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN to aa: 6938 = 26+256*27
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: 4508 = 26+(6-(ord('a')-1)+256)*27+1 (6=character before non-printable bell character)
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 836 = 26+(126-(ord('a')-1))*27
  }
  
begin
  //N := 26+256*27+1;
  //N := 26+166*27+1;
  //N := 1;
  //N := 26+(126-(ord('a')-1))*27;
  N := 805;
  //N := 4508;
  //writeln(N);
  for  snap_serial_number := 1  to  N  do
  begin
    snap_time_number:=0;

    ilo:=snap_time_number mod 10;
    ihi:=snap_time_number div 10;

    if snap_serial_number<27 then begin
      plane_id := chr(snap_serial_number + ord('a')-1);
      filename := snap_plane + plane_id + probe_ident + chr(ihi + ord('0')) + chr(ilo + ord('0')) + '.prn';
    end
    else begin
      plane_id := chr((snap_serial_number div 26) + ord('a')-1) + chr((snap_serial_number mod 26) + ord('a'));
      filename := snap_plane + plane_id + probe_ident + chr(ihi + ord('0')) + chr(ilo + ord('0')) + '.prn';
    end;
    
    //writeln(snap_serial_number,':',plane_id);
    writeln(filename)
    
  end
        
end.
