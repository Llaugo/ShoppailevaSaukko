import csv

def readLayout(file):
    # Reads a CSV containing one or more room layouts separated by empty rows.
    # Returns a list of layouts, where each layout is a list of rows,
    # and each row is a list of ints indicating tile types.
    layouts = []
    currentLayout = []
    splitFile = file.split('/')
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Detect a separator line: all entries empty
            if all(cell.strip() == '' for cell in row):
                if currentLayout:
                    layouts.append(currentLayout) # Save and reset currentLayout
                    currentLayout = []
            else:
                # Convert each cell to int
                currentLayout.append([int(cell) for cell in row])
        # Append the last layout if it wasn't followed by a separator
        if currentLayout:
            layouts.append(currentLayout)
    return layouts