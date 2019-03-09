'''
Extra functions added for interfacing with Limitless application
'''

class Progress:
    def __init__(self, 
            cells_done, total_cells, 
            current_sheet, total_sheets):

        # Integer denoting the number of cells done
        self.cells_done = cells_done

        # Integer denoting total cells in current sheet
        self.total_cells = total_cells

        # Integer denoting current sheet
        self.current_sheet = current_sheet # Counting starts at 1, not 0

        # Integer denoting total sheets
        self.total_sheets = total_sheets

    def __repr__(self):
        return  ('Progress(cells_done={:d}, total_cells={:d},' 
                 ' current_sheet={:d}, total_sheets={:d})'
                 .format(self.cells_done, self.total_cells, 
                         self.current_sheet, self.total_sheets)
                )

    def percent(self):
        # a is sheet progress, ie how many sheets are done
        a = ((self.current_sheet - 1) / self.total_sheets) * 100

        # b is cell progress, ie how much of current sheet is done
        b = (self.cells_done / self.total_cells) * (100 / self.total_sheets)

        return a + b



# Global variable that will be updated as every progress message is printed
LATEST_STATUS = Progress(0, 10, 1, 100) # -1's indicate uninitialized

def set_status(cells_done, total_cells, 
               current_sheet, total_sheets):
    global LATEST_STATUS
    LATEST_STATUS = Progress(cells_done, total_cells, current_sheet, total_sheets)
    #print('In set_status():', LATEST_STATUS)


def init_progress():
	global LATEST_STATUS
	LATEST_STATUS = Progress(0, 10, 1, 100)

def get_status():
    '''
    Call this function to get the progress of the upload/download
    Note: caller of this function should keep track whether he is uploading or downloading
    '''
    #global LATEST_STATUS
    return LATEST_STATUS

def test_percent():
    params = [
        # vals is Progress attrs, ans is expected ans
        dict(vals=[1000, 1000, 1, 5], ans=20),
        dict(vals=[500, 1000, 1, 5], ans=10),
        dict(vals=[0, 12, 3, 4], ans=50),
        dict(vals=[12, 12, 3, 4], ans=75),
        dict(vals=[100, 100, 4, 4], ans=100),
        dict(vals=[5, 10, 2, 10], ans=15)
    ]

    for d in params:
        p = Progress(*d['vals'])
        ans = d['ans']
        per = int(p.percent())
        print('Actual: {:3d}, Expected: {:3d}, Equal={!r}'.format(per, ans, per == ans))
        assert per == ans

if __name__ == '__main__':
    test_percent()
    