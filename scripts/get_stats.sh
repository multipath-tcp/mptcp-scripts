#!/bin/bash

BASE="v4.1.26"
OLD="v0.90"
NEW="HEAD"

echo "Number of commits in this release"
git log --oneline ^${BASE} ${OLD}..${NEW} | wc -l

echo "Contributors (ordered)"
git shortlog -s -n ^${BASE} ${OLD}..${NEW} | sort -n -r

echo "What's their affiliation?"
git log --format="%an %ae" ^${BASE} ${OLD}..${NEW} | sort | uniq -c | sort -n -r

echo "Who reported bugs?"
git log ^${BASE} ${OLD}..${NEW} | grep Reported-by | sort | uniq -c | sort -n -r
