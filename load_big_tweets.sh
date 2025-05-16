#!/bin/sh

files='/data/tweets/geoTwitter21-01-08.zip'

echo '================================================================================'
echo 'load pg_normalized'
echo '================================================================================'
time echo "$files" | parallel python3 load_tweets.py --db "postgresql://hello_flask:hello_flask@localhost:3334/hello_flask_dev" --inputs {} 
