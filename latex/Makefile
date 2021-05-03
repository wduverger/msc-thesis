thesis.pdf: thesis.tex text/*.tex
	xelatex -interaction=errorstopmode thesis.tex 
	bibtex thesis
	xelatex -interaction=errorstopmode thesis.tex 
	xelatex -interaction=errorstopmode thesis.tex

clean:
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