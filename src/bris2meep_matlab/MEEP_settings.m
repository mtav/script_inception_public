function MEEP_settings(FILE, resolution, simSize)
    fprintf(FILE, ';preamble - some interesting settings\n');
    fprintf(FILE, '(set! filename-prefix false)\n');
    fprintf(FILE, '(set! output-single-precision? true)\n');
    fprintf(FILE, '(set-param! resolution %2.4f)\r\n',resolution);
    fprintf(FILE, '\n');
    fprintf(FILE, ';simulation size\n');
    fprintf(FILE, '(define-param sx %2.5f) ; x size\n',simSize(1));
    fprintf(FILE, '(define-param sy %2.5f) ; y size\n',simSize(2));
    fprintf(FILE, '(define-param sz %2.5f) ; z size\n',simSize(3));
    fprintf(FILE, ['(set! geometry-lattice (make lattice (size ',num2str(simSize(:)','%2.5f '),')))\r\n']);
    fprintf(FILE, '\r\n');
end
