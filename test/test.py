import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser
from core import DictSentiment
import core.textprocessing as tp
import core.search_resource as sr

USAGE = "usage:    python extract_keyword.py content -k [top k]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
opt, args = parser.parse_args()

if len(args) < 1:
    print(USAGE)
    sys.exit(1)

content = args[0]
content = (content).decode('utf8')

if opt.topK is None:
    topK = 3
else:
    topK = int(opt.topK)

tags = jieba.analyse.textrank(content, withWeight=True)
for x, w in tags :
    print('%s %s' %(x, w))

ds = DictSentiment.DictSentiment()
print ds.single_sentiment_score(content)
#for words in ds.sentences_words:
#    for word in words:
#        print word


reses = sr.ResourcesIndex()
#reses.dump()
reses.constructInvertIndex()
#reses.invertIndexDump()
reses.constructDict()

words = []
for sent in ds.sentences_words:
    words = words + sent

output = ' '.join(words)
print 'keywords: ', output

reses.searchItem(words)

while 1:
    query = raw_input('enter query: ')
    query = query.decode('utf8')
    print ds.single_sentiment_score(query)
    words = []
    for sent in ds.sentences_words:
        words = words + sent
    output = ' '.join(words)
    print 'keywords: ', output
    reses.searchItem(words)

