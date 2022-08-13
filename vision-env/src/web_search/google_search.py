import webbrowser

def join_data(labels = [], colors = []):
    for i in range(len(labels)):
        label_joint = "+".join(labels[i])
    for j in range(len(colors)):
        color_joint = "+".join(colors[j])

    return label_joint + " " + color_joint

def generate_url(keywords, search_type):
    if search_type == '--shopping':
        pre_url  = "https://www.google.com/search?q="
        post_url = "h&source=lmns&tbm=shop"

        return pre_url + keywords + post_url
    elif search_type == '--images':
        pre_url = "https://www.google.com/search?q="
        post_url = "&newwindow=1&tbm=isch&source=lnms"

        return pre_url + keywords + post_url
    else:
        url = "https://www.google.com/search?q="

        return url + keywords

def google_search(labels, colors, search_type):
    keyword_list = join_data(labels, colors)
    print(keyword_list)
    url = generate_url(keyword_list, search_type)
    webbrowser.open(url)
    print(url)


## TEST ZONE - KEEP AWAY!
#lbl = ["shirt", "long", "sleeve"]
#clr = ["blue", "light"]
#google_search([lbl], [clr], "--images")