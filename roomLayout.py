import csv


def readLayouts(path):
    """Read integer room layouts separated by fully empty CSV rows."""

    layouts = []
    currentLayout = []
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if all(cell.strip() == "" for cell in row):
                if currentLayout:
                    layouts.append(currentLayout)
                    currentLayout = []
            else:
                currentLayout.append([int(cell) for cell in row])
    if currentLayout:
        layouts.append(currentLayout)
    return layouts
