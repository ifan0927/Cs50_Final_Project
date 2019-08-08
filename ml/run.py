import os 
from model import model 
from textpreprocess import load

def main():
    words, x_train, x_test, l_train, l_test = load()
    model(words, x_train, x_test , l_train, l_test)

if __name__ == "__main__":
    main()
