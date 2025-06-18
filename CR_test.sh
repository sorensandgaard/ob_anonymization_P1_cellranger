#!/bin/bash

exec > check_env.log 2>&1

echo "=== Checking loaded modules at runtime ==="
module list 2>&1

echo
echo "=== Checking if cellranger is in PATH ==="
which cellranger || echo "cellranger not found in PATH"

echo
echo "=== Trying to print cellranger version ==="
cellranger --version || echo "cellranger command failed"
