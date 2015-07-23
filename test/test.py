import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser
from core import DictSentiment
import core.textprocessing as tp
import core.search_resource as sr
import core.synonyms as syno


if __name__ == "__main__":
    USAGE = "usage:    python test.py content -k [top k]"
    parser = OptionParser(USAGE)
    parser.add_option("-k", dest="topK")
    opt, args = parser.parse_args()

    if len(args) > 1:
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
    reses = sr.ResourcesIndex()
    reses.constructInvertIndexTfidf()
    reses.constructDict()
    synos = syno.Synonyms()
    synos.constructSynoymsIndex()
    #reses.countTfidf()


    while 1:
        query = raw_input('enter query: ')
        query = query.decode('utf8')
        sentiment_score =  ds.single_sentiment_score(query)
        print sentiment_score
        words = []
        for sent in ds.sentences_words:
            words = words + sent
        output = ' '.join(words)
        print 'keywords: ', output
        expandWords = []
        for word in words:
            results = synos.querySynoyms(word)
            #print word
            #for res in results:
            #    print '...', res
            expandWords = expandWords + results
        expandWords = list(set(expandWords))

        output1 = ' '.join(expandWords)
        print 'expand keywords: ', output1

        print '***********'
        reses.searchItem(words)
        print '***********'
        print 'expand result: '
        reses.searchItem(expandWords)
        print '***********'


