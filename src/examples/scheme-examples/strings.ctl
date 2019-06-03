;; Passing string via CLI:
;; $ asd=789
;; $ mpb filename-prefix=\"abc-${asd}-\"
;; command-line param: filename-prefix="abc-789-"
;; mpb> (run)

;; ; string building:
;; mpb> (string-concatenate (list "ABHBHB" "HUHUHUHUH" "UYYYYYY"))
;; "ABHBHBHUHUHUHUHUYYYYYY"
;; mpb> (define c 23.89)
;; mpb> (define a 12.22)
;; mpb> (define b -7655)
;; mpb> (string-append "huhuh" "/kikik" (number->string a) "-uhuindex-" (number->string c) "olo fuhdsufh ->" (number->string b))
;; "huhuh/kikik12.22-uhuindex-23.89olo fuhdsufh ->-7655"
;; mpb> 

; string formatting
; cf: https://www.gnu.org/software/guile/manual/html_node/Formatted-Output.html
(print (format #f "~,3f" 3.12576) "\n") ; 3 decimals
(format #t "~,3f" 3.12576)
(print "\n")
(format #t "~5,'0d" 12) ; zero-padding
(print "\n")
(exit)
