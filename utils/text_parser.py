import spacy
import en_core_web_md


class TextParser:
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

    def _calc_score(self, date, loc):
        location, priority = loc
        distance = abs(date.start - location.start)
        return 1 / (distance * priority)

    def get_single_date_location_pair(self, text):
        dates = self.get_dates(text)
        locations = self.get_locations_with_priorities(text)
        if not any(dates) or not any(locations):
            return {}
        score = 0
        pair = None
        for date in dates:
            for loc in locations:
                loc_score = self._calc_score(date, loc)
                if loc_score > score:
                    pair = {date:loc[0]}
        return pair

    def get_text_date_location_per_sentence(self, text):
        return [self.get_single_date_location_pair(x) for x in text.split('.') if x]

    def get_entities(self, text):
        return [(x.text, x.label_, x.start) for x in self.model(text).ents]
