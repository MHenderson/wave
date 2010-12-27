#!/bin/bash
jemdoc=~/bin/jemdoc.py
build_dir=~/Documents/Wave/Homepage
mkdir -p $build_dir

files_to_copy="jemdoc.css
               doc"

files="index"

function copy {
    cp -r $1 $build_dir
}

function jem {
    python $jemdoc -o $build_dir/ $1.jemdoc
}

for file in $files_to_copy; do
    copy $file
done

for file in $files; do
    jem $file
done

