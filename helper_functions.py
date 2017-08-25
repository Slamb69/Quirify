"""Helper functions for Music Project"""


def parse_search_results(results):
    """Converts search results page id and title data into a dictionary and
       returns its items as a list of tuples."""

    pages = results['query']['pages']

    data = {}

    for page_id, page in pages.items():
        title = page['title']
        data[page_id] = title

    return data.items()


def parse_page_results(results):
    """Returns each page's results."""
    # Get the page title.
    page_title = results['parse']['title']
    # Pull data from the page's html - first, get the page "text" from the json.
    page_txt = results['parse']['text']['*']

    # Make beautiful soup from page text's html
    soup = BeautifulSoup(page_txt, "lxml")


    orig_lang = None
    orig_poem = None
    eng_txt = None
    lyricist = None
    orig_num_voices = None
    orig_voicing = None
    genre = None
    orig_inst = None


    # Get general info about the piece:
    for each in soup('b'):
        if "Composer:" in each.contents:
            composer = each.next_element.next_element.next_element.string
        if "Lyricist:" in each.contents:
            lyricist = each.next_element.next_element.next_element.string
        if "Number of voices:" in each.contents:
            orig_num_voices = int((each.next_element.next_element.string)
                                  .replace("vv", "").replace("v", ""))
        if "Voicing:" in each.contents:
            orig_voicing = each.next_element.next_element.next_element.string
######### GENRE IS A TUPLE = OKAY, or need ", ".join(genre) for a string?
        if "Genre:" in each.contents:
            genre = (each.next_element.next_element.next_element.string,
                     each.next_element.next_element.next_element.next_element.next_element.next_element.string)
        if "Language:" in each.contents:
            orig_lang = each.next_element.next_element.next_element.string
        if "Instruments:" in each.contents:
            orig_inst = each.next_element.next_element.next_element.string
        if "Description:" in each.contents:
            description = each.parent.get_text().replace("Description: ", '')


    # Get the year published.
    pub_year = soup.find('a', title=(re.compile("Category:\d\d\d\d works"))).string

    # Get the original language's text, if any provided.
    if soup.big.contents[1]:
        orig_poem = soup('div', 'poem')[0]

    # Look to see if there are any texts in English - if so, pull that 'poem', too.
    if soup('big') and orig_lang != 'English':
        for i, each in enumerate(soup('big')):
            if 'English' in each.contents[1]:
                eng_txt = soup('div', 'poem')[i]

    # Get CPDL numbers for each piece's sheet music / midi
    cpdl_nums = map(lambda x: x.string, soup('font'))

    # Get all the image files from the page, and cut out the first 2 items, we
    # then have all of the sheet music and audio files.
    images = results['parse']['images']
    images = images[2:]

    ######## TESTING = TRYING TO GET ALL URLs IN ONE QUERY...BETTER/FASTER? ######

    # Make sure there are images - if not, return 'no files' message to user.
    if images != []:
        pieces_dict_list = []

        # Create a number to assign each file to a group, in order, that will later
        # correlate to the order of the CPDL #s list.
        i = 1

        pieces_dict = {'pdf': (images[0], i)}
        # Since all records have the pdf first, then audio files, using pdf to
        # split list of "images", AKA files!

        for image in images[1:]:
            if image.split('.')[-1] == 'pdf':
                i += 1
                pieces_dict_list.append(pieces_dict)
                pieces_dict = {'pdf': (image, i)}
            else:
                pieces_dict[str(image.split('.')[-1])] = (image, i)
        pieces_dict_list.append(pieces_dict)

        imagelist = []

        for each in images:
            prep = "File:" + each
            imagelist.append(prep)

        # Sort the image files so the sorted results are in the same order, and
        # can be associated later.
        imagesort = sorted(imagelist)

        filelist = "|".join(imagesort)

        urls = get_urls(filelist, len(imagesort))

####### ADD STUFF TO DATABASE HERE!!! BUT GET ALL STUFF FIRST... ###########
    else:
        pass # ADD HERE = maybe alert/flash that no files + user upload option?




    # Get each piece of sheet music (.pdf) and audio files for each "user/editor"
    # and save as a dict of files by each cpdl #

    # OOPS - some pages have no PDF, links to a WEB PAGE...don't really want to
    # offer files on these, just show piece data??? Hmm...decide! For now,
    # # proceeding with what to do if there ARE pdf (sheet music) files.
    # if images != []:
    #     pieces_dict = {'pdf': get_file_url(images[0])}
    #     # Since all records have the pdf first, then audio files, using pdf to
    #     # split list of "images", AKA files!
    #     for image in images[1:]:
    #         if image.split('.')[-1] == 'pdf':
    #             pieces_dict_list.append(pieces_dict)
    #             pieces_dict = {'pdf': get_file_url(image)}
    #         else:
    #             pieces_dict[str(image.split('.')[-1])] = get_file_url(image)
    #     pieces_dict_list.append(pieces_dict)
    # else:
    #     pass # ADD HERE = maybe alert/flash that no files + user upload option?

#     # Using unique cpdl numbers as the keys, join up the above files data as the
#     # values, using zip.
#     pieces_by_cpdl = {cpdl: piece for cpdl, piece in zip(cpdl_nums,
#                                                          pieces_dict_list)}

#     # One way to get the text titles for the text/translations:
#     text_titles = map(lambda x: list(x[0].descendants)[1],
#                       filter(lambda x: x, map(lambda x: x('big'), soup('b'))))

#     # ****** Not yet returning full page results!! Need to finish getting all
#     # page data from API's json!! *******************
#     return pieces_by_cpdl
#     # data = {}

#     # for page_id, page in pages.items():
#     #     title = page['title']
#     #     data[page_id] = title

    # return urls


# def get_file_url(image):
#     """Takes an image name, sends request to cpdl, and returns the image's url."""
#     # Puts the image into the payload.
#     payload = {
#         'titles': 'File:' + image,
#         'iiprop': 'url',
#     }
#     # Sends request to cpdl.org & captures the request's results as r4.
#     r4 = requests.get(
#         'http://www1.cpdl.org/wiki/api.php?action=query&format=json&prop=imageinfo',
#         params=payload,
#     )

#     # Gets the url data from the results json and saves it as 'url'.
#     url = r4.json()['query']['pages'].values()[0]['imageinfo'][0]['url']

#     return url


def get_urls(filelist, num):
    """Takes names of all page's images, sorts them, sends arequest to cpdl, and
        returns each image's url, sorted to match the initial list's order."""
    # Puts the image filelist into the payload.
    payload = {
        'titles': filelist,
        'iiprop': 'url',
    }
    # Sends request to cpdl.org & captures the request's results as r4.
    r4 = requests.get(
        'http://www1.cpdl.org/wiki/api.php?action=query&format=json&prop=imageinfo',
        params=payload,
    )

    # Gets the url data from the results json and saves it as 'urls_raw'.
    urls_raw = []

    for i in range(num):
        url = r4.json()['query']['pages'].values()[i-1]['imageinfo'][0]['url']
        urls_raw.append(url)

    urls = sorted(urls_raw, key=lambda x: x.split('/')[7])

    return urls


def add_piece(data):
    """Adds piece to the database."""


def add_sheet(data):
    """Adds a sheet to the database."""


def add_file(data):
    """Adds a file to the database."""



