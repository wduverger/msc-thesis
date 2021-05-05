thesis.pdf: thesis.tex text/*.tex
	xelatex -interaction=errorstopmode thesis.tex 
	bibtex thesis
	xelatex -interaction=errorstopmode thesis.tex 
	xelatex -interaction=errorstopmode thesis.tex

clean:
	rm -f text/*.aux
	rm -f *.aux
	rm -f *.fdb_latexmk
	rm -f *.fls
	rm -f *.log
	rm -f *.out
	rm -f *.toc
	rm -f *.run.xml
	rm -f *-blx.bib
	rm -f *.blg
	rm -f *.bbl
	rm -f *.synctex.gz