#!/bin/sh
grep -A25 '| ---' README.md | grep -v '| ---' \
    | cut -d'|' -f7 | sed -e '/     /d; s/[~>]//' \
    | awk -f sum.awk
