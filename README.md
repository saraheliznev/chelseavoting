# Address Shape Finder

This tool allows you to determine which shape/polygon from a shapefile an address falls within. It uses GeoPandas for shapefile processing and Nominatim for address geocoding.

## Requirements

- Python 3.7+
- Required Python packages (install using `pip install -r requirements.txt`):
  - geopandas
  - geopy
  - pandas
  - shapely

## Setup

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Make sure you have your shapefile ready (`.shp`, `.shx`, `.dbf`, `.prj`, and `.cpg` files should all be in the same directory)
2. Run the script:
   ```bash
   python address_shape_finder.py
   ```
3. When prompted, enter the path to your `.shp` file
4. Enter addresses to find which shape they fall within
5. Type 'quit' to exit the program

## Example

```
Enter the path to your .shp file: /path/to/your/shapefile.shp

Enter an address (or 'quit' to exit): 1600 Pennsylvania Avenue NW, Washington, DC
Address found in shape with attributes:
name: District 1
population: 50000
...

Enter an address (or 'quit' to exit): quit
```

## Notes

- The tool uses Nominatim for geocoding, which has usage limits. For production use, consider using a commercial geocoding service.
- Make sure your shapefile is in a coordinate system that matches your expected input (the tool assumes WGS84 coordinates for addresses).
- The tool will return all attributes associated with the shape that contains the given address. 