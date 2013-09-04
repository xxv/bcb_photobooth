#!/bin/sh

cd badges && find . -type f -print0 | sort -z -d|xargs -0 pdfjoin -o ../all.pdf
