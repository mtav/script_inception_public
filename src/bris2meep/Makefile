EXE=bris2meep
SRCDIR=source
SRC=$(SRCDIR)/bris_sim.cpp $(SRCDIR)/bris_translate.cpp $(SRCDIR)/main.cpp

all:
	g++ -o $(EXE) -I$(SRCDIR) $(SRC)

clean:
	rm -f *.o *.exe $(EXE) $(SRCDIR)/*.o $(SRCDIR)/*.exe $(SRCDIR)/$(EXE)
