from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import common_texts
model = Doc2Vec(None, None, dm=1, dbow_words=0, corpus_file=None)