# chem_semantics.py
from chem_utils import is_metal, is_nonmetal, get_charge, get_name
from chem_parser import Molecule, Reaction

class Semantics:
    def __init__(self):
        pass

    def get_element_counts(self, molecule):
        counts = {}
        for sym, count in molecule.elements:
            counts[sym] = counts.get(sym, 0) + count
        return counts

    def classify_compound(self, molecule):
        counts = self.get_element_counts(molecule)
        elements = list(counts.keys())
        
        # Check for Hydrocarbon or Organic Compound (C, H, and optionally O)
        if set(elements) <= {'C', 'H', 'O'} and 'C' in elements and 'H' in elements:
            return 'Hydrocarbon'
        
        # Check for Acid (Starts with H, rest are non-metals usually)
        # Simplified: Starts with H and has other stuff
        if molecule.elements[0][0] == 'H' and len(elements) > 1:
             # Exclude Water (H2O) from being called an acid for this context if needed, 
             # but technically it can act as one. Let's keep it simple.
             if 'O' in elements and len(elements) == 2 and counts['H']==2 and counts['O']==1:
                 return 'Water'
             return 'Acid'

        # Check for Base (Ends with OH, usually Metal + OH)
        # We need to check if the last part is OH.
        # Our parser flattens (OH)2 -> O2 H2. 
        # So we check if O and H are present and usually a metal.
        has_metal = any(is_metal(e) for e in elements)
        if has_metal and 'O' in elements and 'H' in elements:
            # Heuristic: Metal Hydroxide
            return 'Base'
        
        # Check for Single Compound (for decomposition)
        # e.g. Metal Carbonate or Chlorate.
        # For MVP: "single compound with O"
        if len(elements) >= 2 and 'O' in elements and not 'H' in elements: # Exclude acids/bases
             return 'OxygenatedCompound'

        if len(elements) == 1 and elements[0] == 'O' and counts['O'] == 2:
            return 'OxygenGas'

        return 'Unknown'

    def predict_products(self, reactants):
        # reactants is a list of Molecule objects
        if not reactants:
            return [], "No reactants"

        classifications = [self.classify_compound(r) for r in reactants]
        
        # Rule 1: Combustion
        # Hydrocarbon + O2 -> CO2 + H2O
        # Also handle Hydrogen + O2 -> H2O
        if 'OxygenGas' in classifications:
            if 'Hydrocarbon' in classifications and len(reactants) == 2:
                return [Molecule([('C', 1), ('O', 2)]), Molecule([('H', 2), ('O', 1)])], "Combustion"
            
            # Check for Hydrogen
            hydrogen_indices = [i for i, r in enumerate(reactants) if list(self.get_element_counts(r).keys()) == ['H']]
            if hydrogen_indices and len(reactants) == 2:
                 return [Molecule([('H', 2), ('O', 1)])], "Combustion (Hydrogen)"

        # Rule 2: Acid-Base Neutralization
        # Acid + Base -> Salt + Water
        if 'Acid' in classifications and 'Base' in classifications:
            if len(reactants) == 2:
                # Identify Acid and Base
                acid = reactants[classifications.index('Acid')]
                base = reactants[classifications.index('Base')]
                
                # Form Water
                water = Molecule([('H', 2), ('O', 1)])
                
                # Form Salt
                # Salt = Metal from Base + Anion from Acid
                # Extract Metal from Base
                base_elements = self.get_element_counts(base)
                metal = None
                for e in base_elements:
                    if is_metal(e):
                        metal = e
                        break
                
                # Extract Anion from Acid (everything except H)
                acid_elements = acid.elements
                anion_parts = []
                for sym, count in acid_elements:
                    if sym != 'H':
                        anion_parts.append((sym, count))
                
                if metal and anion_parts:
                    # Simplified salt formation
                    salt_elements = [(metal, 1)] + anion_parts
                    salt = Molecule(salt_elements)
                    return [salt, water], "Acid-Base Neutralization"

        # Rule 3: Decomposition
        # Single Compound (w/ Oxygen) -> Oxide + O2
        # Example: 2HgO -> 2Hg + O2 (We don't handle stoichiometry balancing yet, just product prediction)
        # HgO -> Hg + O2
        if len(reactants) == 1 and classifications[0] == 'OxygenatedCompound':
            comp = reactants[0]
            # Split into Metal/NonMetal + O2
            # Find the non-oxygen part
            other_elements = []
            for sym, count in comp.elements:
                if sym != 'O':
                    other_elements.append((sym, count)) # Keep original count? Or reset?
            
            if other_elements:
                # If it's a metal, it might form a metal oxide or just metal?
                # Prompt says: "decomposition to oxide + O2" OR "single compound with O -> decomposition to oxide + O2"
                # Wait, if it's already an oxide (like HgO), it decomposes to Metal + O2?
                # Or KClO3 -> KCl + O2.
                # Let's assume KClO3 -> KCl + O2 style.
                # So we strip O and return the rest + O2.
                rest = Molecule(other_elements)
                oxygen = Molecule([('O', 2)])
                return [rest, oxygen], "Decomposition"

        # Rule 4: Synthesis (Simple Combination)
        # Metal + Non-Metal -> Ionic Compound
        if len(reactants) == 2:
            # Check if we have one Metal and one Non-Metal
            # We need to extract the core element from each reactant (ignoring subscripts like Cl2)
            r1_counts = self.get_element_counts(reactants[0])
            r2_counts = self.get_element_counts(reactants[1])
            
            if len(r1_counts) == 1 and len(r2_counts) == 1:
                elem1 = list(r1_counts.keys())[0]
                elem2 = list(r2_counts.keys())[0]
                
                metal, nonmetal = None, None
                
                if is_metal(elem1) and is_nonmetal(elem2):
                    metal, nonmetal = elem1, elem2
                elif is_nonmetal(elem1) and is_metal(elem2):
                    metal, nonmetal = elem2, elem1
                
                if metal and nonmetal:
                    # Balance charges
                    m_charge = abs(get_charge(metal))
                    nm_charge = abs(get_charge(nonmetal))
                    
                    # Swap charges for subscripts (e.g. Al+3, O-2 -> Al2 O3)
                    # Simplify if divisible? (e.g. Mg+2, O-2 -> Mg2O2 -> MgO)
                    # MVP: Just swap.
                    
                    # LCM simplification logic
                    def gcd(a, b):
                        while b:
                            a, b = b, a % b
                        return a
                    
                    divisor = gcd(m_charge, nm_charge)
                    m_subscript = nm_charge // divisor
                    nm_subscript = m_charge // divisor
                    
                    product_elements = [(metal, m_subscript), (nonmetal, nm_subscript)]
                    return [Molecule(product_elements)], "Synthesis"

        return [], "No matching rule found"

    def validate_reaction(self, reaction):
        """
        Validate a chemical reaction for:
        1. Invalid combinations (e.g., metal + metal)
        2. Atom conservation (Law of Conservation of Mass)
        """
        # Check for Metal + Metal reaction (e.g. Na + K)
        if len(reaction.reactants) >= 2:
            # Check if all reactants are single metals
            all_metals = True
            for r in reaction.reactants:
                # Check if molecule is just a metal atom (or multiple of them)
                elements = [e[0] for e in r.elements]
                if not (len(elements) == 1 and is_metal(elements[0])):
                    all_metals = False
                    break
            
            if all_metals:
                return False, "Unsupported: Metal-Metal reaction"

        for mol in reaction.reactants + reaction.products:
            elements = [e[0] for e in mol.elements]
            metals = [e for e in elements if is_metal(e)]
            nonmetals = [e for e in elements if is_nonmetal(e)]
            
            if len(metals) > 1 and len(nonmetals) == 0:
                # Metal + Metal (Alloy?) - usually not in simple inorganic reactions
                return False, f"Unsupported: Metal-Metal combination in {mol}"
        
        # Check atom conservation if products exist
        if reaction.products:
            is_conserved, msg = self.validate_atom_conservation(reaction)
            if not is_conserved:
                return False, msg
            
        return True, "Valid"
    
    def validate_atom_conservation(self, reaction):
        """
        Check if atoms are conserved according to the Law of Conservation of Mass.
        Returns (is_valid, message)
        """
        if not reaction.products:
            return True, "No products to validate"
        
        # Count atoms in reactants
        reactant_atoms = {}
        for mol in reaction.reactants:
            for sym, count in mol.elements:
                reactant_atoms[sym] = reactant_atoms.get(sym, 0) + count
        
        # Count atoms in products
        product_atoms = {}
        for mol in reaction.products:
            for sym, count in mol.elements:
                product_atoms[sym] = product_atoms.get(sym, 0) + count
        
        # Compare
        if reactant_atoms != product_atoms:
            return False, f"Atoms not conserved. Reactants: {reactant_atoms}, Products: {product_atoms}"
        
        return True, "Atoms conserved"
