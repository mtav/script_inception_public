;BUG?: with-prefix does not seem to work properly for to-appended stuff
    (run-until 1
      (with-prefix "prefix" 
        (to-appended "ez"
          (at-every 0.6
            output-efield-z
          )
        )
      (at-beginning output-epsilon)
      )
    )
