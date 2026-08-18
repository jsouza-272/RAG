#!/bin/bash

unzip zips/datasets_public.zip
unzip zips/moulinette.zip
unzip zips/vllm-0.10.1.zip

mv vllm-0.10.1 data/raw
mv datasets_public data	