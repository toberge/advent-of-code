.PHONY: all clean

all: part_one part_two

%: %.hs
	ghc -dynamic -O2 $<

part_one: part_one.hs

part_two: part_two.hs

clean:
	rm -f part_{one,two}{,.o,.hi}
