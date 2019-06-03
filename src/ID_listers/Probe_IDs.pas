{
  Program to test the probe numbering used in Bristol FDTD 2003
}
program probe_IDs;
  var
    probe_serial_number : integer;
    probe_ident : string = '_id_';
    ilo,ihi : integer;
    filename : string;
    probe_id : string;
    N : integer;
  
  {
  MAXIMUM NUMBER OF SNAPSHOTS: TODO
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN TO FIRST ID: TODO
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: TODO
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 789
  }
  
begin
  //N := 26+256*27+1;
  //N := 26+166*27+1;
  //N:=1;
  //writeln(N);
  //N := 26+(126-(ord('a')-1))*27;
  //N := 789;
  N := 439; //to prevent \ in filenames
  //N:=4508;
  for  probe_serial_number := 1  to  N  do
  begin

    ilo:=probe_serial_number mod 10;
    ihi:=probe_serial_number div 10;

    probe_id := chr(ihi + ord('0'))+chr(ilo + ord('0'));
    filename := 'p' + probe_id + probe_ident + '.prn';
    //writeln(probe_serial_number,':',probe_id);
    writeln(filename)
    
  end
  
end.
