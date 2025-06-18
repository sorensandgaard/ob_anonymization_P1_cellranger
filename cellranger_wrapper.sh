#!/bin/bash

# Load the CellRanger module (adjust version as needed)
module load CellRanger/8.0.1

# Call cellranger with all passed arguments
cellranger "$@"
