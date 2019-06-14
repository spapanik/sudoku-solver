# Compiler
CC = g++
CFLAGS = -g -Wall -Wextra -Ofast

# Directories
BUILDDIR = build
BINDIR = bin
DIRS = $(BUILDDIR) $(BINDIR)

# FILES
REQUIRED = constants sudoku utils
OBJ = $(foreach file,$(REQUIRED),$(BUILDDIR)/$(file).o)


# files
$(BINDIR)/ssolve: src/main.cpp $(OBJ) | $(BINDIR)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILDDIR)/%.o: src/%.cpp | $(BUILDDIR)
	$(CC) $(CFLAGS) -c -o $@ $^

# directories
$(DIRS):
	mkdir -p $@

# cleanup
.PHONY: clean
clean:
	-rm $(BUILDDIR)/*
	-rm $(BINDIR)/*
