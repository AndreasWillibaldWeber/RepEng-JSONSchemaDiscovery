DIR=$(notdir ${PWD})

all: compile rename clean

compile:
	pdflatex main.tex
clean:
	rm *.aux *.log *.out
rename:
	mv main.pdf ${DIR}.pdf