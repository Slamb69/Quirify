"""Helper functions for Music Project"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Concert, Event, Instrument, Owner, PerformanceGroup,
                   Performer, Piece, AudioFile, Provider, Setlist, SheetMusic,
                   Roster, PerformerInstrument, Assignment, AssignedSet, Genre,
                   PieceGenre, UserPiece, UserSheet, UserAudioFile,
                   connect_to_db, db)

import requests
# To get text from CPDL pages, need Beautiful Soup!!
from bs4 import BeautifulSoup
# For Beautiful Soup, need lxml's html
from lxml import html
# For Beautiful Soup, need regex
import re

def parse_search_results(results):
    """Converts search results page id and title data into a dictionary and
       returns its items as a list of tuples."""

    pages = results['query']['pages']

    data = {}

    for page_id, page in pages.items():
        title = page['title']
        data[page_id] = title

    return data.items()


def parse_page_results(results, pg_id):
    """Returns each page's results."""
    # Get the page title.
    ttl = results['parse']['title']
    # Pull data from the page's html - first, get the page "text" from the json.
    page_txt = results['parse']['text']['*']

    # Make beautiful soup from page text's html
    soup = BeautifulSoup(page_txt, "lxml")

    # Abbreviated vars for brevity to pass into function - see "add_piece"
    # function (or for loop below) for longer / clearer variable names.
    ol = None
    to = None
    te = None
    lrc = None
    onv = None
    ov = None
    genre = None
    oi = None
    desc = None
    genres = []
    editors = []
    ed_notes = []
    copyrights = []


    # Get general info about the piece for PIECE table & GENRE table:
    for each in soup('b'):
        if "Composer:" in each.contents:
            comp = each.next_element.next_element.next_element.string
        if "Lyricist:" in each.contents:
            lrc = each.next_element.next_element.next_element.string
        if "Number of voices:" in each.contents:
            onv = int((each.next_element.next_element.string)
                      .replace("vv", "").replace("v", ""))
        if "Voicing:" in each.contents:
            ov = each.next_element.next_element.next_element.string
####### GENRE IS A LIST, need to iterate & add each individually to GENRE table.
        if "Genre:" in each.contents:
            genres = map(lambda x: x.string, each.parent('a')[1:])
        if "Language:" in each.contents:
            ol = each.next_element.next_element.next_element.string
        if "Instruments:" in each.contents:
            oi = each.next_element.next_element.next_element.string
        if "Description:" in each.contents:
            desc = each.parent.get_text().replace("Description: ", '')
####### Editors IS A LIST, need to iterate & add each individually to SHEET table.
        if "Editor:" in each.contents:
            editor = each.next_element.next_element.next_element.string
            editors.append(editor)
####### Ed_notes IS A LIST, need to iterate & add each individually to SHEET table.
        if "Edition notes:" in each.contents:
            ednote = each.parent.get_text().replace("Edition notes: ", '')
            ed_notes.append(ednote)
####### Copyrights IS A LIST, need to iterate & add each individually to SHEET table.
        if "copyright:" in each.contents:
            copyright = each.next_element.next_element.next_element.string
            copyrights.append(copyright)

    # Get the year published for PIECE table.
    pb_yr = soup.find('a', title=(re.compile("Category:\d\d\d\d works"))).string

    # Get the original language's text, if any provided, for PIECE table.
    if soup.big.contents[1]:
        to = soup('div', 'poem')[0]

    # Look to see if any text in English. If so, add related 'poem' to PIECE table.
    if soup('big') and ol != 'English':
        for i, each in enumerate(soup('big')):
            if 'English' in each.contents[1]:
                te = soup('div', 'poem')[i]

    # Add the piece to Piece table and return the piece_id.
    piece_id = add_piece(ttl, pg_id, comp, lrc, pb_yr, onv, ov, ol, oi, to, te, desc)

    # Add Genres to database, if they don't exist already, and get new genre_id.
    if genres:
        existing_genres = db.session.query(Genre.name).all()
        genre_ids = []

        for name in genres:
            if name not in existing_genres:
                genre_id = add_genre(name)
                genre_ids.append(genre_id)
        # Add piece & genre ids to the PieceGenre association table, if not there.
        piece_genres = PieceGenre.query.filter_by(piece_id=piece_id).all()

        for gid in genre_ids:
            if genre_id not in piece_genres:
                add_piece_genre(piece_id, gid)

######### SHEET & AUDIOFILE TABLES DATA #########################################

    # Get CPDL numbers for each piece's sheet music/files for SHEET and AudioFile
    # tables. 
    # NB: CPDL # list correlates to may other lists (of items or dicts). 
    #     Use this list to pull the correct index # or key for dbase entry!
    cpdl_nums = map(lambda x: x.string, soup('font'))

    # Get all the image files from the page, and cut out the first 2 items, we
    # then have all of the sheet music and audio files from the page.
    images = results['parse']['images']
    images = images[2:]

    ###### TESTING = TRYING TO GET ALL URLs IN ONE QUERY...BETTER/FASTER than
    # individual quesries for each file? ######

    # Make sure there are images - if not, return 'no files' message to user.
    if images != []:
        files_dict_list = []

        # Create a number to assign each file to a group, in order, that will later
        # correlate to the order of the CPDL #s list.
        i = 1

        files_dict = {'pdf': (images[0], i)}
        # Since all records have the pdf first, then audio files, using pdf to
        # split list of "images", AKA files!

        for image in images[1:]:
            if image.split('.')[-1] == 'pdf':
                i += 1
                files_dict_list.append(files_dict)
                files_dict = {'pdf': (image, i)}
            else:
                files_dict[str(image.split('.')[-1])] = (image, i)
        files_dict_list.append(files_dict)

        imagelist = []

        for each in images:
            prep = "File:" + each
            imagelist.append(prep)

        # Sort the image files so the sorted results are in the same order, and
        # can be associated later.
        imagesort = sorted(imagelist)

        filelist = "|".join(imagesort)

        urls = get_urls(filelist, len(imagesort))

        # All pieces being parsed in this way are CPDL, provider id 1.   
        prid = 1  

        add_sheet(pid, prid, url, cpdl, ed, ednotes, lic)

####### ADD STUFF TO DATABASE HERE!!! BUT GET ALL STUFF FIRST... ###########
    else:
        pass # ADD HERE = maybe alert/flash that no sheets/files yet for the
        # piece, & give user an upload option?




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


def add_piece(ttl, pg_id, comp, lrc, pb_yr, onv, ov, ol, oi, to, te, desc):
    """Adds piece to the database."""

    piece = Piece(title=ttl,
                  page_id=pg_id,
                  composer=comp,
                  lyricist=lrc,
                  publication_year=pb_yr,
                  original_num_voices=onv,
                  original_voicing=ov,
                  original_language=ol,
                  original_instrumentation=oi,
                  text_original=to,
                  text_english=te,
                  description=desc)

    # Add to the session.
    db.session.add(piece)

    # Commit the session/data to the dbase.
    db.session.commit()

    return piece.piece_id


def add_genre(name):
    """Adds genres to the database."""

    genre = Genre(name=name)

    # Add to the session.
    db.session.add(genre)

    # Commit the session/data to the dbase.
    db.session.commit()

    return genre.genre_id


def add_piece_genre(piece_id, genre_id):
    """Adds piece's genre association to the database."""

    piece_genre = PieceGenre(piece_id=piece_id,
                             genre_id=genre_id)
    # Add to the session.
    db.session.add(piece_genre)

    # Commit the session/data to the dbase.
    db.session.commit()


def add_sheet(pid, prid, url, cpdl, ed, ednotes, lic):
    """Adds a sheet to the database."""

    sheet = SheetMusic(piece_id=pid,
                       provider_id=prid,
                       music_url=url,
                       cpdl_num=cpdl,
                       editor=ed,
                       edition_notes=ednotes,
                       license_type=lic)

    # Add to the session.
    db.session.add(sheet)

    # Commit the session/data to the dbase.
    db.session.commit()

    return sheet.sheet_id


def add_file(data):
    """Adds a file to the database."""


