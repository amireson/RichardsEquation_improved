all: run001/ts.pkl run002/ts.pkl run003/ts.pkl

run001/ts.pkl: run001/pars.json run001/BC.json run001/IC.json run001/grid.json lib/*
	bash run.sh run001

run002/ts.pkl: run002/pars.json run002/BC.json run002/IC.json run002/grid.json lib/*
	bash run.sh run002

run003/ts.pkl: run003/pars.json run003/BC.json run003/IC.json run003/grid.json lib/*
	bash run.sh run003

run001/pars.json: 
	python PrepareInputFiles.py

run002/pars.json: 
	python PrepareInputFiles.py

run003/pars.json: 
	python PrepareInputFiles.py

clean:
	rm Run001/*
	rmdir Run001
	rm Run002/*
	rmdir Run002
	rm Run003/*
	rmdir Run003
