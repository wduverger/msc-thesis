# Get a list of all python files in the source dir
# From that list, build a list of all target files (PDF figures)
SRC = $(wildcard code/*.py)
PDF = $(subst code/,figures_generated/,$(SRC:.py=.pdf))


.PHONY: clean figures_generated/__init__.pdf

# Compile figures
figures: $(PDF)
figures_generated/%.pdf: code/%.py
	cd code && python $*.py
	
# Compile latex
thesis: thesis-web thesis-print

TEX_COMPILE = xelatex -interaction=errorstopmode thesis.tex > /dev/null
TEX_CHAIN = $(TEX_COMPILE) && bibtex thesis && $(TEX_COMPILE) && $(TEX_COMPILE)

thesis-web:
	cd latex && \
		sed -ie "s/\\documentclass\[.*\]{mystyle}/\\documentclass[web]{mystyle}/" thesis.tex && \
		$(TEX_CHAIN) && \
		cp thesis.pdf "../MSc thesis Wouter Duverger.pdf"

thesis-print:
	cd latex && \
		sed -ie "s/\\documentclass\[.*\]{mystyle}/\\documentclass[print]{mystyle}/" thesis.tex && \
		$(TEX_CHAIN) && \
		cp -p thesis.pdf "../MSc thesis Wouter Duverger (print).pdf"
	
# Clean compiled files
clean:
	rm -f *.pdf
	rm figures_generated/*
	rm -f latex/text/*.aux
	rm -f latex/*.aux
	rm -f latex/*.fdb_latexmk
	rm -f latex/*.fls
	rm -f latex/*.log
	rm -f latex/*.out
	rm -f latex/*.toc
	rm -f latex/*.run.xml
	rm -f latex/*-blx.bib
	rm -f latex/*.blg
	rm -f latex/*.bbl
	rm -f latex/*.synctex.gz
	rm -f latex/*.pdf