import nltk
from nltk.tokenize import WhitespaceTokenizer, WordPunctTokenizer, TreebankWordTokenizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet as wn
import spacy

# Tải các gói cần thiết
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger_eng')


class TextProcessor:
    def __init__(self) -> None:
        self.tokens = None 
        self.nlp = spacy.load("en_core_web_sm") 

    def tokenize(self, text : str ,  method: str = "whitespace") -> list[str]:
        """
        Tokenizes the text based on the specified method.

        Args:
            method (str): The tokenization method to use. Options are "whitespace", "word_punct", and "treebank".

        Returns:
            List[str]: A list of tokens obtained from the specified tokenization method.
        """
        if method == "whitespace":
            tokenizer = WhitespaceTokenizer()
        elif method == "word_punct":
            tokenizer = WordPunctTokenizer()
        elif method == "treebank":
            tokenizer = TreebankWordTokenizer()
        else:
            raise ValueError("Invalid tokenization method. Choose from 'whitespace', 'word_punct', or 'treebank'.")

        self.tokens = tokenizer.tokenize(text)
        return self.tokens

    def stem_text(self , tokens : list[str] ) -> list[str]:
        """
        Stems the tokens obtained from tokenization.

        Returns:
            List[str]: A list of stemmed tokens.
        """
        stemmer = PorterStemmer()
        stems = [stemmer.stem(word.lower()) for word in tokens]  # Convert to lowercase
        return stems
    # cach 1 : dung model trong spacy 
    def lemmatize_text(self , tokens : list[str]) -> list[str]:
        """
        Lemmatizes the tokens using spaCy's lemmatization.

        Returns:
            List[str]: A list of lemmatized tokens.
        """
        doc = self.nlp(" ".join(tokens)) 
        lemas = [token.lemma_ for token in doc]  
        return lemas
    # cach 2 : van dung nltk

    def get_wordnet_pos(self, word: str) -> str:
        """
        Converts POS tags to WordNet format.

        Args:
            word (str): The word for which to determine the POS tag.

        Returns:
            str: The corresponding WordNet POS tag.
        """
        tag = nltk.pos_tag([word])[0][1][0].lower()  # Get the first character of the POS tag
        tag_dict = {
            'a': wn.ADJ,       # adjective
            's': wn.ADJ_SAT,   # satellite
            'r': wn.ADV,       # adverb
            'n': wn.NOUN,      # noun
            'v': wn.VERB       # verb
        }
        return tag_dict.get(tag, wn.NOUN)

    def lemmatization(self , tokens : list[str]) -> list[str]:
        """
        Performs lemmatization on the tokens obtained from tokenization.

        Raises:
            ValueError: If tokenization has not been performed before lemmatization.

        Returns:
            List[str]: List of lemmatized tokens.
        """
        if not self.tokens:
            raise ValueError("Tokenization not performed. Please call the tokenize method first.")
        
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token, pos=self.get_wordnet_pos(token)) for token in tokens]
        return lemmatized_tokens
    
