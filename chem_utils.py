# chem_utils.py

# A small subset of the periodic table for MVP purposes
# Format: Symbol: (Name, Type, Common Charge)
PERIODIC_TABLE = {
    'H':  {'name': 'Hydrogen', 'type': 'Nonmetal', 'charge': 1},
    'Li': {'name': 'Lithium', 'type': 'Metal', 'charge': 1},
    'Na': {'name': 'Sodium', 'type': 'Metal', 'charge': 1},
    'K':  {'name': 'Potassium', 'type': 'Metal', 'charge': 1},
    'Rb': {'name': 'Rubidium', 'type': 'Metal', 'charge': 1},
    'Cs': {'name': 'Cesium', 'type': 'Metal', 'charge': 1},
    'Be': {'name': 'Beryllium', 'type': 'Metal', 'charge': 2},
    'Mg': {'name': 'Magnesium', 'type': 'Metal', 'charge': 2},
    'Ca': {'name': 'Calcium', 'type': 'Metal', 'charge': 2},
    'Sr': {'name': 'Strontium', 'type': 'Metal', 'charge': 2},
    'Ba': {'name': 'Barium', 'type': 'Metal', 'charge': 2},
    'Al': {'name': 'Aluminum', 'type': 'Metal', 'charge': 3},
    'Zn': {'name': 'Zinc', 'type': 'Metal', 'charge': 2},
    'Fe': {'name': 'Iron', 'type': 'Metal', 'charge': 2}, # Variable 2/3
    'Cu': {'name': 'Copper', 'type': 'Metal', 'charge': 2}, # Variable 1/2
    'Ag': {'name': 'Silver', 'type': 'Metal', 'charge': 1},
    'Pb': {'name': 'Lead', 'type': 'Metal', 'charge': 2},
    'C':  {'name': 'Carbon', 'type': 'Nonmetal', 'charge': 4},
    'N':  {'name': 'Nitrogen', 'type': 'Nonmetal', 'charge': -3},
    'P':  {'name': 'Phosphorus', 'type': 'Nonmetal', 'charge': -3},
    'O':  {'name': 'Oxygen', 'type': 'Nonmetal', 'charge': -2},
    'S':  {'name': 'Sulfur', 'type': 'Nonmetal', 'charge': -2},
    'F':  {'name': 'Fluorine', 'type': 'Nonmetal', 'charge': -1},
    'Cl': {'name': 'Chlorine', 'type': 'Nonmetal', 'charge': -1},
    'Br': {'name': 'Bromine', 'type': 'Nonmetal', 'charge': -1},
    'I':  {'name': 'Iodine', 'type': 'Nonmetal', 'charge': -1},
}

def is_metal(symbol):
    return PERIODIC_TABLE.get(symbol, {}).get('type') == 'Metal'

def is_nonmetal(symbol):
    return PERIODIC_TABLE.get(symbol, {}).get('type') == 'Nonmetal'

def get_charge(symbol):
    return PERIODIC_TABLE.get(symbol, {}).get('charge', 0)

def get_name(symbol):
    return PERIODIC_TABLE.get(symbol, {}).get('name', 'Unknown')
