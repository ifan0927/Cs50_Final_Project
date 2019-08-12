import os 
from textpreprocess import load
from model import model

def main():
    words, x_train, x_test, l_train, l_test = load()
    model(words, x_train, x_test , l_train, l_test)

if __name__ == "__main__":
    main()
