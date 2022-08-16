import webbrowser

def join_data(labels = str, colors = str):
    keyword = labels + "+" + colors

    return keyword

def generate_url(browser, option, keywords):
    if browser == "google":
        if option == '-shopping':
            pre_url  = "https://www.google.com/search?q="
            post_url = "&source=lmns&tbm=shop"

            return pre_url + keywords + post_url
        elif option == '-images':
            pre_url = "https://www.google.com/search?q="
            post_url = "&newwindow=1&tbm=isch&source=lnms"

            return pre_url + keywords + post_url
        else:
            url = "https://www.google.com/search?q="

    elif browser == "amazon":
        url = "https://www.amazon.it/s?k="

        return url + keywords

def search(browser, option, labels, colors):
    keywords = join_data(labels, colors)
    print(keywords)
    url = generate_url(browser, option, keywords)
    webbrowser.open(url)
    print(url)

if __name__ == "__main__":
    browser = "google"
    option = "-shopping"
    labels = "shirt+long+sleeve"
    colors = "blue\n"
    search(browser, option, labels, colors)