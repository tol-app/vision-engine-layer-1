import webbrowser

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

#search_tm = ["never", "gonna", "give", "you", "up"]

def google_search(search_terms):
    google_base_link = "https://www.google.com/search?q="

    url = google_base_link + " ".join(search_terms)
    print(url)

    webbrowser.open(url)