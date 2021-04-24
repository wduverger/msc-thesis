# Get a list of all python files in the source dir
SRC = $(wildcard code/*.py)

# From that list, build a list of all target files (PDF figures)
PDF = $(subst code/,figures_generated/,$(SRC:.py=.pdf))

# Exclude __init__.pdf from that list by saying it cannot every be built
.PHONY: clean figures_generated/__init__.pdf


# To make all figures, run this task with `make figures`
figures: $(PDF)

# Empty the figures directory
clean:
	rm -rf figures_generated/*

# To generate a figure, run the corresponding python script
figures_generated/%.pdf: code/%.py
	cd code && python $*