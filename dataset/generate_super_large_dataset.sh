#!/bin/bash

if [! -f "dataset.txt" ]; then
    echo "dataset.txt not found"
    exit 1
fi

bash ./generate_large_dataset.sh

for ((i = 1; i <= 1024; i++)); do
    cat large_dataset.txt >> super_large_dataset.txt
done

echo "done"