import pandas as pd
import json

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

def find_address_info(address):
    try:
        # Read the CSV file
        addresses_df = pd.read_csv('addresses_district.csv')
        
        # Combine street number and street name into full address for matching
        addresses_df['Full Address'] = addresses_df['Street number'].astype(str) + ' ' + addresses_df['Street name']
        
        # Convert input address to lowercase for case-insensitive matching
        address_lower = address.lower()
        
        # Find the matching row
        match = addresses_df[addresses_df['Full Address'].str.lower() == address_lower]
        
        if not match.empty:
            # Get the first matching row
            row = match.iloc[0]
            return {
                'District': row['District'],
                'Ward': row['Ward'],
                'Precinct': row['Precinct'],
                'Street Number': row['Street number'],
                'Street Name': row['Street name'],
                'Polling Location': row['Polling location']
            }
        else:
            # If no exact match, show similar addresses
            similar = addresses_df[addresses_df['Full Address'].str.lower().str.contains(address_lower.split()[-1])]
            if not similar.empty:
                print("\nNo exact match found. Similar addresses:")
                for _, row in similar.head().iterrows():
                    print(f"{row['Street number']} {row['Street name']}")
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Get address from user
address = input("Enter an address (e.g., '99 Suffolk Street'): ")

# Find and display information
result = find_address_info(address)

if result:
    print("\nAddress Information:")
    print(f"District: {result['District']}")
    print(f"Ward: {result['Ward']}")
    print(f"Precinct: {result['Precinct']}")
    print(f"Street Number: {result['Street Number']}")
    print(f"Street Name: {result['Street Name']}")
    print(f"Polling Location: {result['Polling Location']}")
else:
    print("\nAddress not found.")