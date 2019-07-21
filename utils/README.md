# Utilities

This folder contains supportive code for our project:
- time_utils.py - contains function which maps written location to datetime format. This was non-trivial task and we didn't find existing solution for Python.
We used js package for which we built python wrapper. To use it you should have node installed on your machine
- location_utils.py - contains function which allows to get latitude and longtitude for given location. Calls Google Api
- os_utils.py - contains function for finding file in project which matches regex expression
- text_parser.py - encapsulates our final NLP model. Because we didn't achieved success with word disambiguation, it's working as following.
We have predefined set of keywords which can be used for entity description('painting', 'the work', etc.). For every text we find all the sentences which contains those words or artifact title.
Then for each sentence we perform NER task and taking all the 'DATE' class objects. Also, we take all the locations. Locations can be marked with - 'GPE', 'FAC' and 'ORG' tags.
For each of these tag we have priority set. 'GPE' tag is much more likely to be valid location then 'ORG' tag. Finally, we calculate score for each possible date:location pair. Score is calculated, based on
distance from date and from location and priority of possible location tag.
