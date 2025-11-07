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

# Calculate the intersection of two widgets.
# Return the intersection rectangle and None if no intersection.
def intersect_rects(a, b):
    #ax, ay, aw, ah = rect_in_window(a)
    #bx, by, bw, bh = rect_in_window(b)
    x1 = max(a.x, b.x)
    y1 = max(a.y, b.y)
    x2 = min(a.x + a.width, b.x + b.width)
    y2 = min(a.y + a.height, b.y + b.height)
    w, h = x2 - x1, y2 - y1
    return (x1, y1, w, h) if (w > 0 and h > 0) else None

def rect_in_window(w):
    x1, y1 = w.to_window(*w.pos)
    x2, y2 = w.to_window(w.right, w.top)
    return x1, y1, x2 - x1, y2 - y1