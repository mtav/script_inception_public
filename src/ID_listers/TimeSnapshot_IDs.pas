{
  Program to test the time snapshot numbering used in Bristol FDTD 2003
}
program TimeSnapshot_IDs;
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
  N := 439; //to prevent \ in filenames
  //N:=4508;
  for  snap_serial_number := 1  to  N  do
  begin

    snap_time_number:=1;

    ilo:=snap_time_number mod 10;ihi:=snap_time_number div 10;

    if snap_serial_number<10 then begin
      plane_id := chr(snap_serial_number + ord('0'));
      filename := snap_plane + plane_id + probe_ident + chr(ihi + ord('0')) + chr(ilo + ord('0')) + '.prn';
    end
    else begin
      plane_id := chr((snap_serial_number div 10) + ord('0'))+chr((snap_serial_number mod 10) + ord('0'));
      filename := snap_plane + plane_id + probe_ident + chr(ihi + ord('0')) + chr(ilo + ord('0')) + '.prn';
    end;

    //writeln(snap_serial_number,':',plane_id);
    writeln(filename)
    
  end
  
end.
