import pandas as pd
from googletrans import Translator
from transformers import pipeline
import matplotlib.pyplot as plt

# Initialize the translator
translator = Translator()

# Initialize the sentiment analysis pipeline
# sentiment_pipe = pipeline("text-classification", model="juliensimon/reviews-sentiment-analysis")
pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",batch_size=8)
sentiLabels= ['positive','negative','neutral']
# Initialize the intent analysis pipeline
# intent_pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",batch_size=8)

# Define candidate labels for intent analysis
candidate_labels = ['praise', 'question', 'humor', 'criticism', 'emotion']

def detect_translate_and_analyze(comments):
    results = []
    for comment in comments:
        try:
            # Detect the language and translate the comment
            detected = translator.detect(comment)
            detected_language = detected.lang
            translation = translator.translate(comment, src=detected_language, dest='en')
            translated_text = translation.text

            # Perform sentiment analysis
            sentiment = pipe(translated_text,candidate_labels=sentiLabels)
            sentiment_label = sentiment['labels'][0]

            # Perform intent analysis
            intent = pipe(translated_text, candidate_labels)
            intent_label = intent['labels'][0]

            results.append({
                'Original': comment,
                'Language': detected_language,
                'Translation': translated_text,
                'Sentiment': sentiment_label,
                'Intent': intent_label
            })
        except Exception as e:
            # Perform sentiment analysis on the original comment
            sentiment = pipe(comment,sentiLabels)
            sentiment_label = sentiment[0]['label']

            # Perform intent analysis on the original comment
            intent = pipe(comment, candidate_labels)
            intent_label = intent['labels'][0]

            results.append({
                'Original': comment,
                'Language': 'en',
                'Translation': comment,
                'Sentiment': sentiment_label,
                'Intent': intent_label
            })

    # Create a DataFrame from the results
    df = pd.DataFrame(results)

    # Plot the sentiment distribution
    plt.figure(figsize=(10, 5))
    plt.hist(df['Sentiment'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.savefig('sentiment.png')
    

    #plot the intent distribution
    plt.figure(figsize=(10, 5))
    plt.hist(df['Intent'],color='lightgreen')
    plt.title('Intent Distribution')
    plt.xlabel('Intent')
    plt.ylabel('Frequency')
    plt.savefig('intent.png')
    

    return df