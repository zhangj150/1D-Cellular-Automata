try:
    import Tkinter as tk
except ImportError:
    import tkinter
from rushygraphics import *
#import graphics

def main():
    root = tk.Tk()
    root.title('Cellular Automata Generator')
    root.resizable(width=False, height=False)
    window = App(root)               #for class App below
    root.mainloop()
    
class App:
    def __init__(self, master):
        #frames
        self.master = master
        self.frame = tk.Frame(self.master)
        self.buttonframe = tk.Frame(self.master)

        #graphwin
        self.g = GraphWin(self.frame, 600, 600, False)

        #creating the widgets
        self.drawbutton = tk.Button(self.buttonframe, text = 'Generate CA', font = ("Courier New", 14), command = lambda: self.RunCA(600, 600, self.g, int(self.totalistic_counter.get()), int(self.live_number.get())))
        self.clearbutton = tk.Button(self.buttonframe, text = 'Clear Window', font = ("Courier New", 14), command = self.clear)
        self.helpbutton = tk.Button(self.buttonframe, text = 'Help', font = ("Courier New", 14), command = lambda: self.help())
        self.totalistic_counter = tk.Entry(self.buttonframe)
        
        self.live_number = tk.Entry(self.buttonframe)
        self.live_number.insert(0, '3')
        self.totalistic_counter.insert(0, '1') #default value for the entry
        self.live_cells_setter = tk.Message(self.buttonframe, text='How many cells start alive?', font = ("Courier New", 14), width=150)
        self.counter_text = tk.Message(self.buttonframe, text='Set Totalistic Count', font = ("Courier New", 14), width=150)
        
        self.master.protocol('WM_DELETE_WINDOW', self.master.quit)

        #gridding stuff
        self.frame.grid(row=1, column=1, sticky=tk.N)
        self.buttonframe.grid(row=1, column=2, sticky=tk.N)
        self.drawbutton.grid(row=10, column=1, sticky=tk.N)
        self.clearbutton.grid(row=40, column=1, sticky=tk.N)
        self.helpbutton.grid(row=45, column=1, sticky=tk.N)
        self.counter_text.grid(row=50, column=1, sticky=tk.N)
        self.totalistic_counter.grid(row=55, column=1, sticky=tk.N)
        self.live_cells_setter.grid(row=56, column=1, sticky=tk.N)
        self.live_number.grid(row=60, column=1, sticky=tk.N)
        #gridding graphwin
        self.g.grid(row=1, column=1, sticky=tk.N)
    #####################################################################
    def clear(self):
        self.g.delete("all")
    
    def help(self):
        helper = tk.Toplevel()
        helper.resizable(width=False, height=False)
        helper.title('Instructions')
        instructions = '1. Set the entries accordingly\n\n 2. Click \'Generate CA\' \n\n To choose which cells start alive,\n\n click on the screen \n\n 3. To repeat, click \'Clear Window\' and repeat the instructions'
        msg = tk.Message(helper, text=instructions, font = ("Times New Roman", 14))
        msg.grid(row=1, column=1, sticky=tk.N)

    def distance(self, p1, p2):
        return ((p1.getX()-p2.getX())**2 + (p1.getY() - p2.getY())**2)**0.5
    
    def RunCA(self, xmax, ymax, g, totalistic_count, getter):
        g.setCoords(0, 0, xmax, ymax)
        
        live_cells = []
        numbercounter = 0
        while numbercounter < getter:
            selected = g.getMouse()
            x, y = selected.getX(), selected.getY()
            if x%10 < 5: x_new = x-x%10
            else: x_new = x+(10-x%10)
            if y%10 < 5: y_new = y-y%10
            else: y_new = y+(10-y%10)
            start_rect = Rectangle(Point(x_new-5, y_new-5), Point(x_new+5, y_new+5))
            start_rect.setFill('black')
            start_rect.draw(g)
            live_cells.append(Point(x_new, y_new))
            numbercounter += 1
            
        start = Point(0, ymax-10)
        while start.getY() > 0:
            while start.getX() < xmax:
                rect1 = Rectangle(Point(start.getX()-5, start.getY()-5), Point(start.getX()+5, start.getY()+5))
    
                counter = 0
                for i in live_cells:
                    if self.distance(i, start) <= 28.3/2 and start.getY() != i.getY(): counter += 1 #counter is for the totalistic count of neighborhood
                if counter == totalistic_count:       #set totalistic count here
                    rect1.setFill('black')
                    live_cells.append(rect1.getCenter())
                rect1.draw(g)
        
                start.move(10, 0)
            start = Point(0, start.getY())
            start.move(0, -10)

if __name__ == '__main__':
    main()