#!/bin/bash

# Ensure Blender is available in the PATH
BLENDER_EXEC="blender"

# Set the Python script path and the directory containing FBX files
PYTHON_SCRIPT_PATH="C:/Users/Paul/Documents/ModelThumbnailGenerator/render.py"
FBX_DIRECTORY="C:/Users/Paul/Documents/ModelThumbnailGenerator"

# Check if texture path is provided as an argument; otherwise, leave it empty
TEXTURE_PATH=$1

if [ -z "$TEXTURE_PATH" ]; then
    # If no texture path is provided, only pass the directory argument
    echo "Running without a texture path..."
    $BLENDER_EXEC --background --python "$PYTHON_SCRIPT_PATH" -- "$FBX_DIRECTORY"
else
    # If a texture path is provided, pass both directory and texture path arguments
    echo "Running with texture path: $TEXTURE_PATH"
    $BLENDER_EXEC --background --python "$PYTHON_SCRIPT_PATH" -- "$FBX_DIRECTORY" "$TEXTURE_PATH"
fi
