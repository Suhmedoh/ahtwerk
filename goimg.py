#!/usr/bin/python2.7
import time
import sys
import urllib2
import os.path

artist=sys.argv[2]
album=sys.argv[1]
search_keyword=[sys.argv[1] + ' ' + sys.argv[2]]
search_keyword=[search_keyword[0]+'%20']

keywords=['high quality']
keywords=[keywords[0].replace(' ','%20')]
keywords=[keywords[0]+'%20']
Num=1

def download_src(url):
    try:
        headers={}
        headers['user-Agent']="Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req=urllib2.Request(url,headers=headers)
        response=urllib2.urlopen(req)
        page=response.read()
        return page
    except:
        return"page not found"


def get_next_item(s):
    start_line=s.find('"ou"')
    if start_line == -1:
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"ou"')
        end_content = s.find('"ow"')
        content_raw = str(s[start_line+6:end_content-2])
        return content_raw, end_content

def get_all_items(page):
    items = []
    count=0
    while (count<int(Num)):
        item, end_content = get_next_item(page)
        if item == "no_links":
            count=count+1
            break
        else:
            items.append(item)     
            time.sleep(0.1)        
            page = page[end_content+5:]
            count=count+1
    return items

t0=time.time()


i= 0
while i<len(search_keyword):
    items = []
    search_keywords = search_keyword[i]
    search = search_keywords.replace(' ','%20')
    j = 0
    while j<len(keywords):
        pure_keyword = keywords[j].replace(' ','%20')
        #https://www.google.com/search?as_st=y&tbm=isch&as_q=little+scream+love+as+a+weapon+album+art&as_epq=&as_oq=&as_eq=&imgsz=&imgar=&imgc=&imgcolor=&imgtype=&cr=&as_sitesearch=&safe=images&as_filetype=&as_rights=
        url = 'https://www.google.com/search?q=' + search + pure_keyword + '&imgar=s&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html =  (download_src(url))
        time.sleep(0.1)
        items = items + (get_all_items(raw_html))
        j = j + 1
    i = i+1

t1 = time.time()    
total_time = t1-t0   


################################################################################################################
################################################################################################################
#########################change /home/jiaxsun/music/albumart/ to where ever you want to store the artwork######################
prodir='/home/jiaxsun/music/albumart/' + artist + '/' + album + '/'

if not os.path.exists(prodir):
    os.makedirs(prodir)

k=0
errorCount=0
t0=time.time()
while(k<len(items)):
    from urllib2 import Request,urlopen
    from urllib2 import URLError, HTTPError

    try:
        headers={}
        headers['user-Agent']="Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        pic=items[k]
        req = Request(pic, headers=headers)
        response = urlopen(req)
        path=os.path.join(prodir,search_keyword[0].replace('%20','')+str(k+1))
        output_file = open(prodir + "cover.jpg",'wb')
        data = response.read()
        output_file.write(data)
        response.close();

        print("completed ====> "+str(k+1))

        k=k+1;

    except IOError:   #If there is any IOError

        errorCount+=1
        print("IOError on image "+str(k+1))
        k=k+1;

    except HTTPError as e:  #If there is any HTTPError

        errorCount+=1
        print("HTTPError"+str(k))
        k=k+1;
    except URLError as e:

        errorCount+=1
        print("URLError "+str(k))
        k=k+1;
t1=time.time()
print("\n"+str(errorCount)+" ----> total Errors")