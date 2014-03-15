#encoding=utf-8
""" Copyright 2014 Louis Lepper """

""" This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import urllib.request
import re
from bs4 import BeautifulSoup
import jieba

web_address = sys.argv[1]

req = urllib.request.Request(web_address)

try:
	response = urllib.request.urlopen(req)
except urllib.error.URLError as e:
	print(e.reason())
	sys.exit(0)
except urllib.error.HTTPError as e:
	print(e.reason())
	sys.exit(0)

soup = BeautifulSoup(response.read()) #Do I need error checking here?


texts = soup.findAll(text=True)

def visible_text(element): #This *should* just return text that's visible on screen
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title','a']:
        return ''

    result = re.sub('<!--.*-->|\r|\n', '', str(element), flags=re.DOTALL)
    result = re.sub('\s{2,}|&nbsp;', ' ', result)
    return result

visible_elements = [visible_text(elem) for elem in texts]
visible_text = ''.join(visible_elements)

# regex string to match chinese characters = '[\U00004E00-\U00009FFF\U00003400-\U00004DFF\U00020000-\U0002A6DF\U0000F900-\U0000FaFF\U0002F800-\U0002FA1F]'

visible_chinese_text = re.sub('[^(\U00004E00-\U00009FFF\U00003400-\U00004DFF\U00020000-\U0002A6DF\U0000F900-\U0000FaFF\U0002F800-\U0002FA1F)]', '', visible_text)

visible_chinese_text = re.sub('[\(\)]', "", visible_chinese_text)

#English text taken out, amongst various punctuation marks. Brackets seem to remain though.

#Now we need to segment the chinese characters by words:
#print(visible_text)
#print(visible_chinese_text)

seg_list = jieba.cut(visible_chinese_text,cut_all=True)
print("\n".join(seg_list))





