import requests
import re
import argparse

class Args:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def getURL(self):
        if "://" not in self.url:
            return "http://" + self.url
        else:
            return self.url
    pass

def getHTML(url):
    r = requests.get(url)
    return r.text

def doReplace(text: str, tag: str):
    return text.replace(tag, "")

def stringFilter(start_tag: str, start_tag_2: str, end_tag: str, matched: list):
    imbeded_html = re.search(rf"^(.*?) ", matched[0])
    if imbeded_html != start_tag_2:
        finds = matched
        filtered = doReplace(finds, start_tag)
        filtered = doReplace(filtered, end_tag)
        return filtered
    matched = re.sub(rf"^(.*?)>", start_tag, matched[0])
    finds = matched
    filtered = doReplace(finds, start_tag)
    filtered = doReplace(filtered, end_tag)

def filterHTML(html, tag):
    start_tag = f"<{tag}>"
    start_tag_2 = f"<{tag}"
    end_tag = f"</{tag}>"
    #matched = re.search(rf"{start_tag}(.*){end_tag}", html)
    comp = re.compile(rf"{start_tag}(.*?){end_tag}")
    matched = comp.findall(html)
    #print(matched)
    if not matched:
        #matched = re.search(rf"{start_tag_2}(.*){end_tag}", html)
        comp2 = re.compile(rf"{start_tag_2}(.*?){end_tag}")
        matched = comp2.findall(html)
        #print(matched)
    if (len(matched) > 0):
        finds = []
        for match in matched:
            imbeded_html = re.search(rf"^(.*?) ", match)
            #print(imbeded_html)
            if imbeded_html != None and imbeded_html.group(0) != start_tag_2 and imbeded_html.group() != " ":
                filtered = doReplace(match, start_tag)
                filtered = doReplace(filtered, end_tag)
                finds.append(filtered)
            else:
                matched = re.sub(rf"^(.*?)>", start_tag, match)
                filtered = doReplace(matched, start_tag)
                filtered = doReplace(filtered, end_tag)
                finds.append(filtered)
        return "\n".join(finds)
    else:
        #stringFilter(start_tag, start_tag_2, end_tag, matched)
        return "Nothing found!"

def writeText(text, filename="output.txt"):
    file = open(filename, "w")
    file.write(text)
    file.close
    print(f"Wrote Ouput to {filename}!")


def getArgs():
    desc = "Filter text in a specific html tag"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('tag', type=str, help="The HTML tag wrapping the text")
    parser.add_argument('url', type=str, help="The target url")
    parser.add_argument('-o', metavar="filename", type=str, help="Ouput filtered text to file")
    #parser.print_help()
    args = Args()
    parser.parse_args(namespace=args)
    if (args.o != None):
        return (args.getURL(), args.tag, args.o + ".txt")
    else:
        return (args.getURL(), args.tag, False)
    

def main():
    (url, tag, outfile) = getArgs()
    print("Filtering html tag(s):", tag)
    html = getHTML(url)
    text = filterHTML(html, tag)
    if outfile:
        writeText(text, outfile)
    else:
        print("Output:", text)
    return

if __name__ == "__main__":
    main()