# harvest.py

Example implementation of an OAI harvester as a python script.

## Requirements

This script is written in Python and therefore requires that you have already intalled a Pyhton interpreter on your system. I also assume that you've managed to get the python executable to be in your PATH.

The script has been tested with Python 2.7.2

You can check your version by entering the following on your shell / command prompt.

```
python
```


## API key
Also, before you can use the API, you must obtain a key first by registering here:

http://www.rijksmuseum.nl/api

or in English:

http://www.rijksmuseum.nl/api?lang=en


## basic usage

To harvest the data from the Rijksmuseum just run the script as follows:

```
python harvest.py <API KEY>
```


## resuming a harvest

Sometimes an error occurs while harvesting the data. To resume just pass in the name of the last downloaded file as the second parameter.

```
python harvest.py <API KEY> <LAST DOWNLOADED FILE>
```

## harvesting images

To harvest images along-side the xml you can use the harvest-images.py script. The script works exactly the same:

```
python harvest-images.py <API KEY>
```
or:

```
python harvest-images.py <API KEY> <LAST DOWNLOADED FILE>
```

## contribute
Feedback is very much appreciated, so please don't hesitate to send suggestions, bug reports and (most importantly) pull requests. 

## License
MIT license
