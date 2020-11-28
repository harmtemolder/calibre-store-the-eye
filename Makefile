version = 0.2.3-alpha
zip_file = releases/The Eye v$(version).zip
zip_contents = *.py LICENSE *.md *.txt

all: zip

zip:
	@ echo "creating new $(zip_file)" && zip "$(zip_file)" $(zip_contents) && echo "created new $(zip_file)"
