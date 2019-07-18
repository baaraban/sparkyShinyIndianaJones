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
        return {x : location_tags.index(x.label_) for x in self.model(text).ents if x.label_ in location_tags}

    def get_entities(self, text):
        return [(x.text, x.label_, x.start) for x in self.model(text).ents]

