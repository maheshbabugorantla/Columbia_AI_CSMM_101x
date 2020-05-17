from csv import writer
from text_classifier import TextClassifier


def write_results_to_file(filename, test_preds):
    with open(filename, 'w', newline='') as preds_file:
        csv_writer = writer(preds_file)
        for prediction in test_preds:
            csv_writer.writerow([prediction])


def main():

    # Vocareum Paths
    # train_path = "../resource/lib/publicdata/aclImdb/train"
    # test_path = "../resource/lib/publicdata/imdb_te.csv"

    # Local Machine Paths
    train_path = "aclImdb/train"
    test_path = "imdb_te.csv"

    sentiment_classifier = TextClassifier(
        stop_words_file='stopwords.en.txt',
        train_path=train_path,
        test_path=test_path
    )

    '''
        train a SGD classifier using unigram representation,
        predict sentiments on imdb_te.csv, and write output to
        unigram.output.txt
    '''
    sentiment_classifier.train_using_tfidf(n_gram=1)
    predictions = sentiment_classifier.test_using_tfidf(n_gram=1)
    write_results_to_file('unigram.output.txt', predictions)

    '''
        train a SGD classifier using bigram representation,
        predict sentiments on imdb_te.csv, and write output to
        bigram.output.txt
    '''

    '''
        train a SGD classifier using unigram representation
        with tf-idf, predict sentiments on imdb_te.csv, and write
        output to unigramtfidf.output.txt
    '''

    '''
        train a SGD classifier using bigram representation
        with tf-idf, predict sentiments on imdb_te.csv, and write
        output to bigramtfidf.output.txt
    '''


if __name__ == "__main__":
    main()
