__author__ = "Richard O'Dwyer"
__email__ = "richard@richard.do"
__license__ = "None"

import re

def process_log(log):
    requests = get_requests(log)
    files = get_files(requests)
    totals = file_occur(files)
    return totals

def get_requests(f):
    log_line = f.read()
    pat = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s' #IP address
           '\[(.+)\]\s' #datetime
           '"GET\s(.+)\s\w+/.+"\s\d+\s' #requested file
           '\d+\s"(.+)"\s' #referrer
           '"(.+)"' #user agent
        )
    requests = find(pat, log_line, None)
    return requests

def find(pat, text, match_item):
    match = re.findall(pat, text)
    if match:
        return match
    else:
        return False

def get_files(requests):
    #get requested files with req
    requested_files = []
    for req in requests:
        #req[2] for req file match, change to
        #data you want to count totals
        requested_files.append(req[2])
    return requested_files

def file_occur(files):
    #file occurrences in requested files
    d = {}
    for file in files:
        d[file] = d.get(file,0)+1
    return d

if __name__ == '__main__':

    #nginx access log, standard format
    log_file = open('20150217-access.log', 'r')

    #return dict of files and total requests
    library = process_log(log_file)

    blacklist = {
        "tag",
        "wp-content",
        "wp-includes",
        "wp-admin",
        "wp-activate",
        "assets",
        "badges",
        "contacto",
        "usuarios",
        "page",
        "category",
        "Admin",
        "admin",
        "author",
        "images",
        "sitemap.xml",
        "robots.txt",
        "?"
    }


    postdictionary = {}

    for key in library.keys():
        print "key: %s , value: %s" % (key, library[key])
        filterkey = key.split('/')[1]

        if filterkey in blacklist:
            continue
        elif filterkey[:1] in blacklist:
            continue
        else:
            if filterkey in postdictionary:
                postdictionary[filterkey] = postdictionary[filterkey] + library[key]
                continue
            else:
                postdictionary[filterkey] = library[key]


    for key3 in postdictionary.keys():
            print "key: %s , value: %s" % (key3, postdictionary[key3])

    print len(postdictionary)
