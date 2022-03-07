.PHONY: all debug

all: debug

install:
	test -d env || python3 -m venv env
	. env/bin/activate; pip install -Ur requirements.txt

debug:
	. env/bin/activate; FLASK_APP=app.py FLASK_ENV=development flask run --host=0.0.0.0 --port=8080

production:
	. env/bin/activate; FLASK_APP=app.py FLASK_ENV=production flask run --host=0.0.0.0 --port=8080

clean:
	rm -rf env
	rm -rf __pycache__