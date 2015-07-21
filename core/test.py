import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser
import DictSentiment

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
print ds.single_review_sentiment_score(content)
