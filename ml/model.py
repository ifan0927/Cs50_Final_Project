from keras.models import Sequential, load_model
from keras.layers import Dense, Embedding, Conv1D, MaxPool1D, Dropout, BatchNormalization, Flatten
from keras.utils import to_categorical
from sklearn import metrics


def model(words, x_train, x_test, l_train, l_test):
    model = Sequential()

    model.add(Embedding(len(words) + 1, 300, input_length=20))
    model.add(Conv1D(256, 5, padding='same'))
    model.add(MaxPool1D(3, 3, padding='same'))
    model.add(Conv1D(128, 5, padding='same'))
    model.add(MaxPool1D(3, 3, padding='same'))
    model.add(Conv1D(64, 3, padding='same')) 
    model.add(BatchNormalization())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    one_hot_labels = to_categorical(l_train, num_classes=3) 
    model.fit(x_train, one_hot_labels,epochs=10, batch_size=1350)
    y_predict = model.predict_classes(x_test) 
    y_predict = list(map(str, y_predict))
    print('準確率', metrics.accuracy_score(l_test, y_predict))
    