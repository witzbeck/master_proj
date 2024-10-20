paper.pdf: paper.tex
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

preclean: 
	rm -f *.toc *.aux *.bbl *.blg *.log *.out *.pdf *fdb_latexmk *fls *synctex.gz

cleanup: 
	rm -f *.toc *.aux *.bbl *.blg *.log *.out *fdb_latexmk *fls *synctex.gz
