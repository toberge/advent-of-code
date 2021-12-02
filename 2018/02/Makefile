.PHONY: all clean run

all: Main

Main: Main.hs
	ghc -dynamic Main.hs

run: Main
	./Main input.dat

clean:
	rm -f Main Main.o Main.hi
