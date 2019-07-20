import spacy
import en_core_web_md
import re


class TextParser:
    art_words = ['statue', 'tool', 'portrait',
                 'peisage', 'treasure',
                 'blade', 'painting', 'axe',
                 'jewelry', 'fresco', 'arrow', 'the work']

    def __init__(self):
        spacy.load("en_core_web_md")
        self.model = en_core_web_md.load()

    def get_named_entities(self, text):
        return self.model(text)

    def pipe(self, documents):
        return self.model.pipe(documents)

    def get_dates(self, text):
        return [x for x in self.model(text).ents if x.label_ == 'DATE']

    def get_locations(self, text):
        location_tags = ['GPE', 'FAC']
        return [x for x in self.model(text).ents if x.label_ in location_tags]

    def get_locations_with_priorities(self, text):
        location_tags = ['GPE', 'FAC', 'ORG']
        return [(x, location_tags.index(x.label_) + 1) for x in self.model(text).ents if x.label_ in location_tags]

    def _calc_score(self, date, loc, entity_location):
        def get_distance(first, second):
            var1 = first[0] - second[1]
            var2 = first[1] - second[0]
            return min(var1, var2)

        location, priority = loc
        date_location = (date.start, date.start + len(date))
        location_location = (location.start, location.start + len(location))
        try:
            date_distance = get_distance(entity_location, date_location)
        except:
            print("Problem with date")
            return float("-inf")
        location_distance = get_distance(entity_location, location_location)
        if date_distance == 0 or location_distance == 0:
            return float("-inf")
        return (1/date_distance) + (1/priority*location_distance)

    def get_single_date_location_pair(self, text, entity_location):
        dates = self.get_dates(text)
        locations = self.get_locations_with_priorities(text)
        if not any(dates) or not any(locations):
            return {}
        score = float("-inf")
        pair = None
        for date in dates:
            for loc in locations:
                if date.start == entity_location[0] or loc[0].start == entity_location[0]:
                    continue
                loc_score = self._calc_score(date, loc, entity_location)
                if loc_score > score:
                    pair = {date:loc[0]}
        return pair

    def get_sentences_with_artifacts(self, text, additional_words=[]):
        def get_start_end_tuple(wor, sentence):
            start = sentence.lower().find(wor)
            end = start + len(wor)
            return start, end

        answer = []
        indicators = TextParser.art_words + additional_words
        for word in indicators:
            to_append = re.findall(rf"([^.]*?{word}[^.]*\.)", text, flags=re.IGNORECASE)
            answer.extend([(x, get_start_end_tuple(word, x)) for x in to_append])

        return answer

    def parse_entity_movement(self, text, aliases):
        return self.get_text_date_location_per_sentence(self.get_sentences_with_artifacts(text, aliases))

    def get_text_date_location_per_sentence(self, text_location_tuple):
        return [self.get_single_date_location_pair(*x) for x in text_location_tuple]
