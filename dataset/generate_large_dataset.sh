#!/bin/bash

if [! -f "dataset.txt" ]; then
    echo "dataset.txt not found"
    exit 1
fi

for ((i = 1; i <= 1024 * 32; i++)); do
    cat dataset.txt >> large_dataset.txt
done

echo "done"