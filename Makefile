BLENDER := "C:/Program Files/Blender Foundation/Blender 4.3/blender.exe"

SCRIPT := ./scripts/render.py
ROOT_DIRECTORY := $(CURDIR)

run:
	$(BLENDER) --background --python $(SCRIPT) -- $(ROOT_DIRECTORY)