# Compiler
CC = g++
CFLAGS = -g -Wall -Wextra -Ofast

# Directories
BUILDDIR = build
BINDIR = bin
DIRS = $(BUILDDIR) $(BINDIR)

# FILES
REQUIRED = main constants sudoku utils
OBJ = $(foreach file,$(REQUIRED),$(BUILDDIR)/$(file).o)


# files
$(BINDIR)/ssolve: $(OBJ) | $(BINDIR)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILDDIR)/%.o: src/%.cpp | $(BUILDDIR)
	$(CC) $(CFLAGS) -c -o $@ $^

# directories
$(DIRS):
	mkdir -p $@

# cleanup
.PHONY: clean
clean:
	find $(BUILDDIR) -type f -delete
	find $(BINDIR) -type f -delete
