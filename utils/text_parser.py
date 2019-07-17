import spacy
import en_core_web_md


class TextParser:
    def __init__(self):
        self.model = en_core_web_md.load()

    def get_named_entities(self, text):
        return self.model(text)

    def get_dates(self, text):
        return [x for x in self.model(text).ents if x.label_ == 'DATE']

    def get_locations(self, text):
        location_tags = ['FAC', 'GPE']
        return [x for x in self.model(text).ents if x.label_ in location_tags]

