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


# Global variable that will be updated as every progress message is printed
LATEST_STATUS = Progress(-1,-1,-1,-1) # -1's indicate uninitialized

def set_status(cells_done, total_cells, 
               current_sheet, total_sheets):
    global LATEST_STATUS
    LATEST_STATUS = Progress(cells_done, total_cells, current_sheet, total_sheets)
    print('In set_status():', LATEST_STATUS)

def get_status():
    '''
    Call this function to get the progress of the upload/download
    Note: caller of this function should keep track whether he is uploading or downloading
    '''

    return LATEST_STATUS
