.PHONY: all clean

all: partOne partTwo

%: %.hs
	ghc -dynamic -O2 $<

partOne: partOne.hs

partTwo: partTwo.hs

clean:
	rm -f part{One,Two}{,.o,.hi}
