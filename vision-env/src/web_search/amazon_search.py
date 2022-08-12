import webbrowser

def join_data(labels = [], colors = []):
    for i in range(len(labels)):
        label_joint = "+".join(labels[i])
    for j in range(len(colors)):
        color_joint = "+".join(colors[j])

    return label_joint + " " + color_joint

def generate_url(keywords):
    url = "https://www.amazon.it/s?k="

    return url + keywords

def amazon_search(labels, colors):
    keyword_list = join_data(labels, colors)

    # C'mon Jeffrey you can do it!
    jeff_net = generate_url(keyword_list)
    webbrowser.open(jeff_net)
    print(jeff_net)

if __name__ == "__main__":
    amazon_search([""], [""])


## NOTHING TO SEE HERE...
lbl = ["jeff", "besos", "halloween", "costume"]
clr = ["orange"]
amazon_search([lbl], [clr])