import os, re, requests, urllib.request
import bs4

filename_regex = '([-\w]+.pdf)'
folder = './reports'
hint = '/docs/default-source/coronaviruse/situation-reports/'
domain = 'https://www.who.int'
url = domain + '/emergencies/diseases/novel-coronavirus-2019/situation-reports'
req = urllib.request.urlopen(url)
print('Getting HTML file')
html = req.read()
print('Parsing HTML code')
soup = bs4.BeautifulSoup(html, 'html.parser')
unfiltered_links = soup.find_all('a') # get all a-tag elements

# get all a-tag elements with convenient href
filtered_links = []
for link in unfiltered_links:
    if hint in link['href']:
        filtered_links.append(link)

# create folder, if it doesn't exist
if not os.path.exists(folder):
    print('Creating folder: ' + folder)
    os.makedirs(folder)

# iterate over list of fine links and download each one of them
for link in filtered_links:
    href = link['href']
    req = requests.get(domain+href, stream=True)
    filename = re.findall(filename_regex, href)[0]
    print('Downloading ' + filename)
    with open(folder + '/' + filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
