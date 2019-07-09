from pprint import pprint
import en_core_web_sm
from collections import namedtuple


def article_to_events(article):
    # based on: https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
    def extract_event(sentence):
        dates, gpes = [], []
        doc = nlp(str(sentence))
        for X in doc.ents:
            if X.label_ == "DATE":
                dates.append(X.text)
            if X.label_ == "GPE":
                gpes.append(X.text)
        return dates, gpes

    nlp = en_core_web_sm.load()
    article = nlp(article)
    sentences = [x for x in article.sents]
    Event = namedtuple('Event', 'sentence_idx dates gpes')
    events = []

    for idx, sentence in enumerate(sentences):
        dates, gpes = extract_event(sentence)
        if not dates or not gpes:
            events.append(Event(idx, None, None))
        else:
            events.append(Event(idx, dates, gpes))
    return events


test_paragraph = 'Tombs from the Spring and Autumn period belonging to the dukes of the Jin state in Quwo were ' \
                 'discovered in which the body was covered with small jade pieces once interwoven with silk.[1]    ' \
                 'For many years, many archaeologists suspected that records of jade burial suits were only legends.[citation ' \
                 'needed] The discovery in 1968 of two complete jade suits in the tombs of Liu Sheng and Dou Wan in Mancheng, ' \
                 'Hebei, finally proved their existence. The jade suits of Liu Sheng and Dou Wan consisted of 2,498 plates of ' \
                 'solid jade connected with two and a half pounds of gold wires.  ' \
                 'In 1973, a jade burial suit belonging to Prince Huai of the Western Han Dynasty was discovered in Dingxian, ' \
                 'Hebei. It consisted of 1,203 pieces of jade and 2,580 grams of gold thread.[2][3]  ' \
                 'In 1983, a jade suit was found in the tomb of Zhao Mo, the second king of Southern Yue, in Guangzhou. The red ' \
                 'silk thread used to bind the 2,291 jade plates represented Zhao Mos immersion into local culture. It is ' \
                 'exhibited in the local Museum of the Mausoleum of the Nanyue King.[4]  ' \
                 'In 1991, a jade burial suit was excavated from a group of monumental tombs of the King of Chu, Liu Wu, ' \
                 'in Xuzhou. This magnificent, life-sized jade and gold burial suit is the finest to have survived, ' \
                 'thereby possessing a high value for artistic appreciation. [5]  ' \
                 'It is now believed that jade burial suits were actually relatively common among the wealthiest aristocrats of ' \
                 'the Han Dynasty, but that over the years most have been lost due to the activities of grave robbers." '
events = article_to_events(test_paragraph)
pprint(events)
