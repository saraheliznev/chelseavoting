import pandas as pd
import json
from city_councilor_info import get_district_info, get_at_large_info

# Read the CSV file
addresses_df = pd.read_csv('addresses_district.csv')

# Print column names to verify structure
print("Columns in CSV:", addresses_df.columns.tolist())

# Combine street number and street name into full address
addresses_df['Full Address'] = addresses_df['Street number'].astype(str) + ' ' + addresses_df['Street name']

# Create a dictionary mapping addresses to districts
address_to_district = dict(zip(addresses_df['Full Address'].str.lower(), addresses_df['District']))

# Save to JSON file
with open('address_districts.json', 'w') as f:
    json.dump(address_to_district, f, indent=2)

print("Created address_districts.json with", len(address_to_district), "addresses")

# Print a few sample entries to verify
print("\nSample entries:")
for addr, dist in list(address_to_district.items())[1500:1505]:
    print(f"Address: {addr}, District: {dist}")

def normalize_address(address):
    # Dictionary of common address abbreviations
    abbreviations = {
        'avenue': 'ave',
        'street': 'st',
        'boulevard': 'blvd',
        'drive': 'dr',
        'lane': 'ln',
        'road': 'rd',
        'court': 'ct',
        'circle': 'cir',
        'place': 'pl',
        'terrace': 'ter',
        'parkway': 'pkwy',
        'square': 'sq',
        'heights': 'hts',
        'north': 'n',
        'south': 's',
        'east': 'e',
        'west': 'w',
        'northeast': 'ne',
        'northwest': 'nw',
        'southeast': 'se',
        'southwest': 'sw'
    }
    
    # Convert to lowercase and split into words
    words = address.lower().split()
    
    # Replace full words with abbreviations
    normalized_words = []
    for word in words:
        # Check if the word is in our abbreviations dictionary
        if word in abbreviations:
            normalized_words.append(abbreviations[word])
        else:
            normalized_words.append(word)
    
    return ' '.join(normalized_words)

def find_district_by_address(address):
    try:
        # Read the CSV file
        addresses_df = pd.read_csv('addresses_district.csv')
        
        # Combine street number and street name into full address for matching
        addresses_df['Full Address'] = addresses_df['Street number'].astype(str) + ' ' + addresses_df['Street name']
        
        # Normalize both the input address and the addresses in the database
        address_lower = normalize_address(address)
        addresses_df['Normalized Address'] = addresses_df['Full Address'].apply(normalize_address)
        
        # Find the matching row
        match = addresses_df[addresses_df['Normalized Address'] == address_lower]
        
        if not match.empty:
            return match.iloc[0]['District']  # Return just the district number
        else:
            # If no exact match, show similar addresses
            similar = addresses_df[addresses_df['Normalized Address'].str.contains(address_lower.split()[-1])]
            if not similar.empty:
                print("\nNo exact match found. Similar addresses:")
                for _, row in similar.head().iterrows():
                    print(f"{row['Street number']} {row['Street name']}")
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    # Get address from user
    address = input("Enter an address (e.g., '99 Suffolk St' or '99 Suffolk Street'): ")
    
    # Find district number
    district = find_district_by_address(address)
    
    if district:
        # Get and print district information
        district_data = get_district_info(district)
        at_large_data = get_at_large_info()
        
        if district_data:
            print(f"\nDistrict {district} Representatives:")
            
            # Print City Councilor information
            print("\nCity Councilor:")
            councilor = district_data['city_councilor']
            print(f"Name: {councilor['name']}")
            print(f"Phone: {councilor['phone']}")
            print(f"Email: {councilor['email']}")
            print(f"Address: {councilor['address']}")
            if 'social_media' in councilor:
                print("Social Media:")
                for platform, link in councilor['social_media'].items():
                    print(f"- {platform}: {link}")
            
            # Print School Committee information
            print("\nSchool Committee Member:")
            committee = district_data['school_committee']
            print(f"Name: {committee['name']}")
            print(f"Phone: {committee['phone']}")
            print(f"Email: {committee['email']}")
            print(f"Address: {committee['address']}")
            if 'social_media' in committee:
                print("Social Media:")
                for platform, link in committee['social_media'].items():
                    print(f"- {platform}: {link}")
    
        
        print("\nAt-Large City Councilors:")
        for councilor in at_large_data['city_councilors']:
            print(f"\nName: {councilor['name']}")
            print(f"Phone: {councilor['phone']}")
            print(f"Email: {councilor['email']}")
            print(f"Address: {councilor['address']}")
            if 'social_media' in councilor:
                print("Social Media:")
                for platform, link in councilor['social_media'].items():
                    print(f"- {platform}: {link}")
        
        print("\nAt-Large School Committee Member:")
        committee = at_large_data['school_committee']
        print(f"Name: {committee['name']}")
        print(f"Phone: {committee['phone']}")
        print(f"Email: {committee['email']}")
        print(f"Address: {committee['address']}")
        if 'social_media' in committee:
            print("Social Media:")
            for platform, link in committee['social_media'].items():
                print(f"- {platform}: {link}")
    else:
        print("\nAddress not found.")

if __name__ == "__main__":
    main()