import xml.etree.ElementTree as ET
import pandas as pd


def remove_namespace(doc, namespace):
    """Remove namespace in the passed document in place."""
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.iter():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]


def xml_to_csv(path):
    tree = ET.parse(path)
    remove_namespace(tree, u'http://www.mediawiki.org/xml/export-0.10/')
    root = tree.getroot()

    output = pd.DataFrame(columns=['title', 'timestamp', 'username', 'text'])
    for i, page in enumerate(root):
        title = page.find('title').text
        data = page.find('revision')
        contrib = data.find('contributor')
        username = ''
        if contrib and contrib.find('username') is not None:
            username = contrib.find('username').text
        timestamp = data.find('timestamp').text
        text = data.find('text').text
        output.loc[i] = [title, timestamp, username, text]

    return output

xml_to_csv('data/Persian.xml').to_csv('data/out.csv')
