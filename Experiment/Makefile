DIR=$(notdir ${PWD})

.PHONY: all compile clean rename

all: compile rename clean

compile:
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex
clean:
	rm *.aux *.log *.out *.bbl *.blg
rename:
	mv main.pdf ${DIR}.pdf