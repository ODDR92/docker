import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Load the data
df = pd.read_csv('ceo_interviews.csv')

# Create a new DataFrame with alternating rows merged
df['Title'] = df['Title'].iloc[::2].reset_index(drop=True)
df['Content'] = df['Content'].iloc[1::2].reset_index(drop=True)

# Drop any rows that still have missing data
df = df.dropna()

# Initialize a WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Define a list of standard stopwords to remove
stopwords_list = set(stopwords.words('english'))

# Define a list of custom stop words
custom_stopwords = set(['bezos', 'dimon', 'jeff', 'narrator', 'bezos', 'dimon', 'jeff', 'narrator', 'jamie', 'tim', 'cook', 'satya', 'nadella', 'larry', 'page', 'elon', 'musk'])

def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Tokenize the text
    words = word_tokenize(text)
    # Remove standard stopwords, custom stop words, and lemmatize the words
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords_list and word not in custom_stopwords]
    return words

# Apply the preprocessing to the 'Content' column
df['Content'] = df['Content'].apply(preprocess_text)

# Join the list of words back into a string
df['Content'] = df['Content'].apply(' '.join)

# Initialize a CountVectorizer
vectorizer = CountVectorizer()

# Create the document-term matrix
dtm = vectorizer.fit_transform(df['Content'])

# Convert the document-term matrix into a DataFrame for easier viewing
dtm_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names_out())

# Initialize the LDA model
lda = LatentDirichletAllocation(n_components=5, random_state=0)

# Fit the model to the data
lda.fit(dtm)

# Print the top words for each topic
for index, topic in enumerate(lda.components_):
    print(f'Top 10 words for Topic #{index}:')
    print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])
