#!/bin/bash

VENV_PATH="./venv/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
else
    echo "Virtual environment not found at $VENV_PATH"
    exit 1
fi

if [ -f "get_svg.py" ]; then
    python3 get_svg.py
else
    echo "get_svg.py not found!"
    exit 1
fi

