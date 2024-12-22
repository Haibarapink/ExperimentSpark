#!/bin/bash

if [! -f "skew_dataset.txt" ]; then
    echo "skew_dataset.txt not found"
    exit 1
fi

for ((i = 1; i <= 1024 * 5; i++)); do
    cat skew_dataset.txt >> large_skew_dataset.txt
done

echo "done"