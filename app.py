from flask import Flask, render_template, request
from city_councilor_info import get_district_info, get_at_large_info
import pandas as pd
import os

app = Flask(__name__)

# Load address data once at startup
addresses_df = pd.read_csv('addresses_district.csv')
addresses_df['Full Address'] = addresses_df['Street number'].astype(str) + ' ' + addresses_df['Street name']

def normalize_address(address):
    abbreviations = {
        'avenue': 'ave', 'street': 'st', 'boulevard': 'blvd', 'drive': 'dr',
        'lane': 'ln', 'road': 'rd', 'court': 'ct', 'circle': 'cir', 'place': 'pl',
        'terrace': 'ter', 'parkway': 'pkwy', 'square': 'sq', 'heights': 'hts',
        'north': 'n', 'south': 's', 'east': 'e', 'west': 'w',
        'northeast': 'ne', 'northwest': 'nw', 'southeast': 'se', 'southwest': 'sw'
    }
    words = address.lower().split()
    normalized_words = [abbreviations.get(word, word) for word in words]
    return ' '.join(normalized_words)

def find_address_info(address):
    address_lower = normalize_address(address)
    addresses_df['Normalized Address'] = addresses_df['Full Address'].apply(normalize_address)
    match = addresses_df[addresses_df['Normalized Address'] == address_lower]
    if not match.empty:
        row = match.iloc[0]
        return {
            'District': row['District'],
            'Ward': row['Ward'],
            'Precinct': row['Precinct'],
            'Polling Location': row['Polling location']
        }
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    info = None
    district_data = None
    at_large_data = None
    address = ""
    if request.method == 'POST':
        address = request.form['address']
        info = find_address_info(address)
        if info:
            district_data = get_district_info(info['District'])
            at_large_data = get_at_large_info()
            if at_large_data and 'school_committee' in at_large_data:
                if not isinstance(at_large_data['school_committee'], list):
                    at_large_data['school_committee'] = [at_large_data['school_committee']]
        else:
            info = {}
    # Capitalize each word in the entered address for display
    display_address = address.title() if address else ""
    # Get all available image filenames (without extension)
    image_folder = os.path.join(app.static_folder, 'images')
    available_images = set()
    if os.path.exists(image_folder):
        available_images = {os.path.splitext(f)[0] for f in os.listdir(image_folder) if f.endswith('.jpg')}
    return render_template('index.html', info=info, district_data=district_data, at_large_data=at_large_data, entered_address=display_address, available_images=available_images)

if __name__ == '__main__':
    app.run(debug=True)