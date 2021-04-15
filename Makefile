# Get a list of all files in the source dir
SRC = $(wildcard code/*.py)

# From that list, build a list of all target files (PDF figures)
PDF = $(subst code/,figures_generated/,$(SRC:.py=.pdf))

# Exclude __init__.pdf from that list by saying it cannot every be built
.PHONY: figures_generated/__init__.pdf 

# To make all figures, add the list of pdf files as dependencies to the main task
all: $(PDF)

# To generate a figure, run the corresponding python script
figures_generated/%.pdf: code/%.py
	cd code && python $(subst code/,,$<)