import pandas as pd
import interface

if __name__ == '__main__':
    filepath = interface.main_loop()

    interface.make_discussions(filepath)