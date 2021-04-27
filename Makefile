# Get a list of all python files in the source dir
# From that list, build a list of all target files (PDF figures)
SRC = $(wildcard code/*.py)
PDF = $(subst code/,figures_generated/,$(SRC:.py=.pdf))

.PHONY: figures_generated/__init__.pdf


report: 
	cd latex && \
	xelatex -interaction=errorstopmode 'Wouter Duverger MSc thesis.tex' && \
	bibtex 'Wouter Duverger MSc thesis' && \
	xelatex -interaction=errorstopmode 'Wouter Duverger MSc thesis.tex' && \
	xelatex -interaction=errorstopmode 'Wouter Duverger MSc thesis.tex'


figures: $(PDF)
figures_generated/%.pdf: code/%.py
	cd code && python $*.py

clean-report:
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