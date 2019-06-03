function filename_cellarray = circleRectCombo(fileBaseName, mag, dwell, rep, beamCurrent, circleCentro2D, circleRadius, circleSectionHeight, rectCentro2D, rectSize2D)
  % function filename_cellarray = circleRectCombo(fileBaseName, mag, dwell, rep, beamCurrent, circleCentro2D, circleRadius, circleSectionHeight, rectCentro2D, rectSize2D)
  % ex: filename_cellarray = circleRectCombo('test.str', 50000, 100, 1, 70, [0,0], 2, -1, 0.25, -1); readStrFile(filename_cellarray,50000);

  % rep Repetitions - try 1.
  % mag Magnification - set value from 20 to 200000.
  % (x=0,y=0) = center of the screen
  % x = horizontal axis, from left to right
  % y = vertical axis, from bottom to top

  % upper case = pixels
  % lower case = microns

  % positioning example:
  %  circleCentro2D=[0,-0.20]; circleRadius=0.5; circleSectionHeight=0.10; rectCentro2D=[0.30,0]; rectSize2D=[0.5,0.25]; fileBaseName='test.str'; mag=getMagFromScreenSizeInMicrons(1); dwell=1; rep=1; beamCurrent=1000;
  %  filename_cellarray = circleRectCombo(fileBaseName, mag, dwell, rep, beamCurrent, circleCentro2D, circleRadius, circleSectionHeight, rectCentro2D, rectSize2D);
  %  readStrFile(filename_cellarray, mag);

  % fileBaseName='tmp';mag=30000;dwell=123;rep=18;holes_X=[1,2,3];holes_Y=[2,3,4];holes_Size_X=[0.1,0.2,0.3];holes_Size_Y=[0.2,0.3,0.4];holes_Type=[0,1,2];separate_files=true;beamCurrent=11;

  % ex: filename_cellarray = circleRectCombo('/tmp/test.str', 304000/4096, 123, 1, 1, [0,0], 10, 1, 5, 1)
  %  readStrFile(filename_cellarray, 304000/4096)
  %  dwelltime=round(800*30*scale); mag=50000; filename_cellarray = circleRectCombo('test.str', mag, dwelltime, 1, 11, [-0.1,-1.5+ 0.24160], 1.5, 0.2, [0,0], [1,1]); readStrFile(filename_cellarray,mag);

  filename_cellarray = {};
  if exist('beamCurrent','var')==0; beamCurrent = 1; end;

  [res, HFW] = getResolution(mag);
  disp(['Resolution = ',num2str(res),' mum/pxl']);

  dwell_vector_circle_section=[]
  X_circle_section =[]
  Y_circle_section=[]
  
  dwell_vector_rectangle=[]
  X_rectangle=[]
  Y_rectangle=[]
  
  % get points
  %[dwell_vector_circle_section,X_circle_section,Y_circle_section] = spiralHoleCircular(beamCurrent,res,dwell,circleCentro2D(1),circleCentro2D(2), circleRadius, rectW);
  [dwell_vector_circle_section,X_circle_section,Y_circle_section] = circleSection(beamCurrent, res, dwell, circleCentro2D, circleRadius, circleRadius-circleSectionHeight);
  
  %beamCurrent
  %res
  %dwell
  %circleCentro2D(1)
  %circleCentro2D(2)
  %2*circleRadius
  %rectW
  [dwell_vector_rectangle,X_rectangle,Y_rectangle] = ZigZagHoleRectangular(beamCurrent, res, dwell, rectCentro2D(1), rectCentro2D(2), rectSize2D(1), rectSize2D(2));

  total_dwell_vector = [dwell_vector_circle_section, dwell_vector_rectangle];
  total_X = [X_circle_section, X_rectangle];
  total_Y = [Y_circle_section, Y_rectangle];
  
  % Write to file.
  [ folder, basename, ext ] = fileparts(fileBaseName);
  if strcmp(ext,'.str')
      filename = fullfile(folder, [ basename, '.str']);
  else
      filename = [fileBaseName, '.str'];
  end
  disp(['Creating ',filename]);
  fid = fopen(filename,'w+');
  fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(total_X));
  fprintf(fid,'%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
  fclose(fid);
  filename_cellarray{end+1}=filename;
    
end
