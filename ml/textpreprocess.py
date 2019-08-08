from sklearn.model_selection import train_test_split
import pandas as pd
import jieba
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

def load():
    # load the user_dict for jieba
    jieba.load_userdict("jieba_dict/user_dict.txt") 

    # read the data from csvfile by pd
    train_data = pd.read_csv("data/train3.csv", names=['label','short']).astype(str)

    
    # using jieba to cut the word
    cut = lambda x : list(jieba.cut(x))
    train_data['word'] = train_data['short'].apply(cut)
    train_data.to_csv('out.csv',encoding='utf-8')

    # make the tokenizer and covert the words to number index
    train_tokenizer = Tokenizer()
    train_tokenizer.fit_on_texts(train_data['word'])
    words = train_tokenizer.word_index

    # Split the data to test and train group
    x_train, x_test, l_train, l_test = train_test_split(train_data['word'], train_data['label'], test_size=0.1)

    # covert the word to seqence of number
    x_train_word_ids = train_tokenizer.texts_to_sequences(x_train)
    x_test_word_ids = train_tokenizer.texts_to_sequences(x_test)

    # uniform the length of the data
    x_train_padded_seqs = pad_sequences(x_train_word_ids, maxlen=20)
    x_test_padded_seqs = pad_sequences(x_test_word_ids, maxlen=20)

    return words, x_train_padded_seqs, x_test_padded_seqs, l_train, l_test

    

if __name__ == "__main__":
    load()

