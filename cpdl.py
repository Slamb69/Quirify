import requests

# to get a dictionary out of each one of these result objects (r1, r2, etc),
# you can call .json() on the object:
# EX:
# r1.json()




# General search -- the different terms can all go in as
# the value for the 'gsrsearch' key
payload = {'gsrsearch': 'Ecco Gesualdo'}

# making the request
r1 = requests.get(
    'http://www1.cpdl.org/wiki/api.php?action=query&format=json&prop=info&generator=search',
    params=payload
)


# parsing a full page, specifying the id of the page to parse
r2 = requests.get(
    'http://www1.cpdl.org/wiki/api.php?action=parse&format=json&pageid=3788'
)


# parsing a page for just the image names, for a particular page_id
payload = {
    'prop': 'images',
    'pageid': 3788,
}

r3 = requests.get(
    'http://www1.cpdl.org/wiki/api.php?action=parse&format=json',
    params=payload,
)

# You could also just hardcode the prop=images and pageid in the url:
# r = requests.get('http://www.cpdl.org/wiki/api.php?action=parse&format=json&prop=images&pageid=3788')



# Getting an image url by image name
payload = {
    'titles': 'File:Peetrino-Ardenti miei sospiri.pdf',
    'iiprop': 'url',
}

r4 = requests.get(
    'http://www1.cpdl.org/wiki/api.php?action=query&format=json&prop=imageinfo',
    params=payload,
) 

# Test = searching by CPDL #, in CPDL - this was URL for # 28188:
# http://www2.cpdl.org/wiki/index.php?search=cpdl+%2328188&title=Special%3ASearch&go=Go
# And for # 21767:
# http://www2.cpdl.org/wiki/index.php?search=cpdl+%2321767&title=Special%3ASearch&go=Go