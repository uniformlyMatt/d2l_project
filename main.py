import pandas as pd
import interface
import discussions as disc

if __name__ == '__main__':
    filepath, grad_program = interface.main_loop()

    disc.make_discussions(filepath, grad_program)