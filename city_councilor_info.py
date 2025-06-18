import pandas as pd
import json

district_info = {
    1: {
        'city_councilor': {
            'name': 'Todd Taylor',
            'phone': '617-872-3174',
            'email': 'toddtaylor@chelseama.gov',
            'address': '45 Nichol Street',
            'social_media': {
                'facebook': 'https://www.facebook.com/taylorforchelsea/',
                'instagram': 'https://www.instagram.com/p/CybTwxPs2m4/',
                'twitter': 'https://twitter.com/toddforchelsea'
            }
        },
        'school_committee': {
            'name': 'Shawn O\'Regan',
            'phone': '857-258-5551',
            'email': 'shawnpo626@yahoo.com',
            'address': '78 Garfield Avenue'
        }
    },
    2: {
        'city_councilor': {
            'name': 'Melinda Vega',
            'phone': '857-241-0026',
            'email': 'melindavegamaldonado@chelseama.gov',
            'address': '116 Clark Avenue',
            'social_media': {
                'instagram': 'https://www.instagram.com/melindavega4chelsea/'
            }
        },
        'school_committee': {
            'name': 'Sarah Neville',
            'phone': '603-231-1385',
            'email': 'sarah.neville.chelsea@gmail.com',
            'address': '40 Eleanor Street',
            'social_media': {
                'facebook': 'http://facebook.com/sarahforchelsea',
                'instagram': 'http://instagram.com/saraheliznev',
                'twitter': 'http://twitter.com/saraheliznev',
                'website': 'http://sarahforchelsea.com'
            }
        }
    },
    3: {
        'city_councilor': {
            'name': 'Norieliz DeJesus',
            'phone': '857-364-9036',
            'email': 'norielizdejesus@chelseama.gov',
            'address': '373 Crescent Avenue, #1',
            'social_media': {
                'instagram': 'https://www.instagram.com/norielizdejesusforchelsea/'
            }
        },
        'school_committee': {
            'name': 'Jonathan Gomez-Pereira',
            'phone': 'N/A',
            'email': 'adsf@asdf.com',
            'address': '357 Crescent Avenue'
        }
    },
    4: {
        'city_councilor': {
            'name': 'Tanairi Garcia',
            'phone': '857-391-9523',
            'email': 'tanairigarcia@chelseama.gov',
            'address': '135 Washington Avenue',
            'social_media': {
                'instagram': 'https://www.instagram.com/tanairigvforchelsea/'
            }
        },
        'school_committee': {
            'name': 'Mayra Balderas',
            'phone': 'N/A',
            'email': 'adsf@asdf.com',
            'address': '59 Addison Street'
        }
    },
    5: {
        'city_councilor': {
            'name': 'Lisa Santagate',
            'phone': 'N/A',
            'email': 'xx@chelseama.gov',
            'address': 'Xxx Ave',
            'social_media': {
                'instagram': 'https://www.instagram.com/lisasantagate/'
            }
        },
        'school_committee': {
            'name': 'Claryangeliz Covas Caraballo',
            'phone': '617-233-0172',
            'email': 'covascaraballoc@chelseaschools.com',
            'address': '22 Gerrish Avenue #312',
            'social_media': {
                'instagram': 'https://www.instagram.com/claryangeliz01/'
            }
        }
    },
    6: {
        'city_councilor': {
            'name': 'Giovanni Recupero',
            'phone': '617-386-9603',
            'email': 'giovannirecupero@chelseama.gov',
            'address': '147 Essex Street'
        },
        'school_committee': {
            'name': 'Ana Hernandez',
            'phone': '617-504-2195',
            'email': 'garcia1208@gmail.com',
            'address': '194 Congress Avenue',
            'social_media': {
                'instagram': 'https://www.instagram.com/simplyana_1208/'
            }
        }
    },
    7: {
        'city_councilor': {
            'name': 'Manuel Teshe',
            'phone': 'N/A',
            'email': 'xx@chelseama.gov',
            'address': 'xx Street',
            'social_media': {
                'facebook': 'https://www.facebook.com/profile.php?id=100093357881312',
                'instagram': 'https://www.instagram.com/one_teshe/',
                'website': 'https://www.manuelteshe.com/',
                'twitter': 'https://twitter.com/manuel_teshe'
            }
        },
        'school_committee': {
            'name': 'Lucía Henriquez',
            'phone': 'N/A',
            'email': 'x@g.com',
            'address': '165 Winnisimmet Street',
            'social_media': {
                'instagram': 'https://www.instagram.com/luciahflores/'
            }
        }
    },
    8: {
        'city_councilor': {
            'name': 'Calvin Brown',
            'phone': '617-407-4845',
            'email': 'calvintbrown@chelseama.gov',
            'address': '300 Commandants Way, #113',
            'social_media': {
                'facebook': 'https://www.facebook.com/profile.php?id=100069542276206'
            }
        },
        'school_committee': {
            'name': 'Yessenia Alfaro',
            'phone': '781-579-0020',
            'email': 'yalfaro1@gmail.com',
            'address': '12 High Street, #2',
            'social_media': {
                'instagram': 'https://www.instagram.com/yessiealfaro/'
            }
        }
    },
    'at_large': {
        'city_councilors': [
            {
                'name': 'Leo Robinson',
                'phone': '617-791-6756 or 617-889-4969',
                'email': 'lrobinson@chelseama.gov',
                'address': '83 Warren Avenue'
            },
            {
                'name': 'Roberto Jimenez-Rivera',
                'phone': '603-260-9448',
                'email': 'XX@chelseama.gov',
                'address': '40 Eleanor Street',
                'social_media': {
                    'facebook': 'https://www.facebook.com/RobertoForChelsea',
                    'instagram': 'https://www.instagram.com/hashtagroberto/',
                    'website': 'http://ElectRoberto.org'
                }
            },
            {
                'name': 'Kelly Garcia',
                'phone': '857-247-9504',
                'email': 'kellygarciaforchelsea@gmail.com',
                'address': '135 Washington Avenue #2',
                'social_media': {
                    'facebook': 'https://www.facebook.com/KellyforChelsea',
                    'instagram': 'https://www.instagram.com/kelly_for_chelsea/',
                    'website': 'https://www.kellyforchelsea.com/'
                }
            }
        ],
        'school_committee': {
            'name': 'Kati Cabral',
            'phone': '617-982-8546',
            'email': 'cabralk@chelseaschools.com',
            'address': '56 Cottage Street',
            'social_media': {
                'instagram': 'https://www.instagram.com/katicabral_ma/',
                'website': 'www.votekaticabral.com'
            }
        }
    }
}

# Function to get district information
def get_district_info(district):
    
    if district in district_info:
        return district_info[district]
    return None

# Function to get at-large information
def get_at_large_info():
    return district_info['at_large']

# # Example usage:
# def print_district_info(district):
#     info = get_district_info(district)
#     if info:
#         print(f"\nDistrict {district} Information:")
#         print("\nCity Councilor:")
#         print(f"Name: {info['city_councilor']['name']}")
#         print(f"Phone: {info['city_councilor']['phone']}")
#         print(f"Email: {info['city_councilor']['email']}")
#         print(f"Address: {info['city_councilor']['address']}")
        
#         print("\nSchool Committee Member:")
#         print(f"Name: {info['school_committee']['name']}")
#         print(f"Phone: {info['school_committee']['phone']}")
#         print(f"Email: {info['school_committee']['email']}")
#         print(f"Address: {info['school_committee']['address']}")
#     else:
#         print(f"District {district} not found")

# # Test with a district number
# district = int(input("Enter district number (1-8): "))
# print_district_info(district)