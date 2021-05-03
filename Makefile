# Get a list of all python files in the source dir
# From that list, build a list of all target files (PDF figures)
SRC = $(wildcard code/*.py)
PDF = $(subst code/,figures_generated/,$(SRC:.py=.pdf))

.PHONY: clean_figures figures_generated/__init__.pdf

figures: $(PDF)
clean-figures:
	rm figures_generated/*

figures_generated/%.pdf: code/%.py
	cd code && python $*.py

report: 
	cd latex && make thesis.pdf