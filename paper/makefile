paper.pdf: paper.tex
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

clean: 
	rm -f *.aux *.bbl *.blg *.log *.out *.pdf *fdb_latexmk *fls *synctex.gz
