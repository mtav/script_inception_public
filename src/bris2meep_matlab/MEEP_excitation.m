function MEEP_excitation(FILE, excFrequency, excWidth, excComponent, excCenter, excSize)
    fprintf(FILE, ';excitations specification\r\n');
    fprintf(FILE, '(set! sources\r\n');
    fprintf(FILE, '(list\r\n');
    fprintf(FILE, '(make source\r\n');
    fprintf(FILE, ['(src (make gaussian-src (frequency ',num2str(excFrequency,'%2.7f'),') (width ',num2str(excWidth,'%2.7f'),')\r\n']);
    fprintf(FILE, '))\r\n');
    fprintf(FILE, ['(component ',excComponent,')\r\n']);
    fprintf(FILE, ['(center ',num2str(excCenter,'%2.5f '),')\r\n']);
    fprintf(FILE, ['(size ',num2str(excSize,'%2.5f '),'))\r\n']);
    fprintf(FILE, ')\r\n');
    fprintf(FILE, ')\r\n');
end
