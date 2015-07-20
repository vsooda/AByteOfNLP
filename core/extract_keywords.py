import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser

USAGE = "usage:    python extract_keyword.py [file name] -k [top k]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]

if opt.topK is None:
    topK = 10
else:
    topK = int(opt.topK)

content = open(file_name, 'rb').read()

weighted = False
if weighted :
#jieba.analyse.set_idf_path("../extra_dict/idf.txt.big");
#tags = jieba.analyse.extract_tags(content, topK=topK)
    tags = jieba.analyse.textrank(content, withWeight=True)
    for x, w in tags :
        print('%s %s' %(x, w))
else:
    tags = jieba.analyse.textrank(content, topK=topK)
    print(",".join(tags))
