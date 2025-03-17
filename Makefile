# Define path WITHOUT quotes (note: no trailing space)
BASE_BLENDER_DIR := /c/Program\ Files/Blender\ Foundation/Blender

# Use escaped spaces and wildcard * for version folders
LATEST_BLENDER_FOLDER := $(shell ls -1d $(BASE_BLENDER_DIR)* | sort | tail -n 1)

# Full Unix-style path to blender.exe
BLENDER := $(LATEST_BLENDER_FOLDER)/blender.exe

# Convert to Windows-style path
BLENDER_WIN := $(shell cygpath -w "$(BLENDER)")

print-blender:
	@echo BASE_BLENDER_DIR: $(BASE_BLENDER_DIR)
	@echo LATEST_BLENDER_FOLDER: $(LATEST_BLENDER_FOLDER)
	@echo BLENDER path: $(BLENDER_WIN)

run:
	"$(BLENDER_WIN)" --background --python ./scripts/render.py -- $(CURDIR)

clean:
	rm -rf output
	mkdir output