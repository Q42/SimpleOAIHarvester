#!/usr/bin/env bash

./identify.py $1
./list-metadataformats.py $1
./list-sets.py $1
#./list-identifiers.py $1
./get-record.py $1 oai:rijksmuseum.nl:sk-a-4881 oai_dc
#./list-records.py $1 oai_dc