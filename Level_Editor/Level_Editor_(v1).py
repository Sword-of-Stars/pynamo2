import os

#===== Change cwd to current script =====#
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

if __name__ == "__main__":

    #===== Load pynamogui =====#
    import pynamogui as pyn

    #sys.stdout = pyn.TracePrints() # debugging feature

    gui = pyn.gui

    while True:
        gui.run()