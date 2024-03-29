import pandas as pd
import requests

FILENAME_STARTING_MOLECULES = 'READRetro/data/building_block.csv'
starting_mols_full = list(pd.read_csv(FILENAME_STARTING_MOLECULES)['mol'])

def _mol2image(mol, width=0, height=0):
    if 'kegg.jp' in mol:
            return None 
    from rdkit.Chem import MolFromSmiles, Draw
    from io import BytesIO
    from base64 import b64encode
    #if '.' in mol:
        #mol =  mol.split('.')
        #return [_mol2image(s) for s in mol]
    mol = MolFromSmiles(mol)
    img = Draw.MolToImage(mol)
    if width > 0 or height > 0:
        if width <= 0:
            width = int(img.size[0] * height / img.size[1])
        if height <= 0:
            height = int(img.size[1] * width / img.size[0])
        img = img.resize((width, height))
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    return b64encode(img_bytes.getvalue()).decode("utf-8")

bb_df = pd.read_csv("buildingblock.csv")
all_building_blocks = []
for c, sdf in bb_df.groupby("CLASS", sort=False):
    cl = {
        "class": c,
        "molecules": []
    }
    for mol in starting_mols_full:
        entry = sdf[sdf.SMILES == mol]
        if len(entry):
            cl["molecules"].append({
                "smiles": mol,
                "name": entry["NAME"].values[0],
                "image": _mol2image(mol)
            })
    all_building_blocks.append(cl)

mnx_df = pd.read_csv("neutralize_cano_smi_mnxid.tsv", sep="\t")

def _neutralize_atoms(smi):
    from rdkit.Chem import MolFromSmiles, MolFromSmarts, MolToSmiles    
    try:
        mol = MolFromSmiles(smi)
        pattern = MolFromSmarts("[+1!h0!$([*]~[-1,-2,-3,-4]),-1!$([*]~[+1,+2,+3,+4])]")
        at_matches = mol.GetSubstructMatches(pattern)
        at_matches_list = [y[0] for y in at_matches]
        if len(at_matches_list) > 0:
            for at_idx in at_matches_list:
                atom = mol.GetAtomWithIdx(at_idx)
                chg = atom.GetFormalCharge()
                hcount = atom.GetTotalNumHs()
                atom.SetFormalCharge(0)
                atom.SetNumExplicitHs(hcount - chg)
                atom.UpdatePropertyCache()
        return MolToSmiles(mol, isomericSmiles=True)
    except:
        return smi

def _mnx_search(smi):
    #if '.' in smi:
        #smi = smi.split('.')
        #return [_mnx_search(s) for s in smi]
    blk_found = False
    for blk in all_building_blocks:
        for mol in blk["molecules"]:
            if mol["smiles"] == smi:
                blk_found = True
                name = mol["name"]
    extract = mnx_df[mnx_df['SMILES'] == _neutralize_atoms(smi)]
    if not len(extract):
        return None, None
    else:
        mnx_id = extract["ID"].values[0]
        if not blk_found:
            name = extract["name"].values[0]
        return mnx_id, name

rdb_df = pd.read_csv("READRetro/data/train_canonicalized.txt", sep=">>", header=None, names=["reactant", "product"])

def _rdb_search(mol1, mol2):
    extract = rdb_df[(rdb_df['reactant'] == _neutralize_atoms(mol1)) & (rdb_df['product'] == _neutralize_atoms(mol2))]
    if len(extract):
        return True
    else:
        return False

reaction_kegg_db = "READRetro/data/kegg_reaction.pickle"
reaction_df = pd.read_pickle(reaction_kegg_db)


neutral_kegg_db = "READRetro/data/kegg_neutral_iso_smi.csv"
kegg_df = pd.read_csv(neutral_kegg_db)

def _kegg_search(smi: str) -> tuple:
    extract = kegg_df[kegg_df['SMILES'] == smi]
    if not len(extract):
        return None
    else:
        id = extract["ID"].values[0]
        return id
    
def _kegg_reaction_search(reactants: list, products: list) -> list:
    """
    Retrieve the Rname values from reaction_df based on given reactants and products.

    Args:
        reactants: List of reactants.
        products: List of products.

    Returns:
        List of Rname values.

    """
    # Get the KEGG IDs for reactants and products
    reactants_kegg_ids = []
    products_kegg_ids = []

    
    for compounds in reactants:
        if (compounds == None) or ('kegg.jp' in compounds):
            pass
        else:
            compound = _neutralize_atoms(compounds)
            kegg_id = _kegg_search(compound)
            reactants_kegg_ids.append(kegg_id)


    for compounds in products:
        if (compounds == None) or ('kegg.jp' in compounds):
            pass
        else:
            compound = _neutralize_atoms(compounds)
            kegg_id = _kegg_search(compound)
            products_kegg_ids.append(kegg_id)

    # Create a boolean mask for filtering rows
    reactants_mask = reaction_df['Reactants'].apply(lambda x: all(item in x for item in reactants_kegg_ids))
    products_mask = reaction_df['Products'].apply(lambda x: all(item in x for item in products_kegg_ids))

    # print(reaction_df[reactants_mask],reaction_df[products_mask])
    # Apply the masks to filter the dataframe
    filtered_df = reaction_df[reactants_mask & products_mask]

    # Get the Rname values for the filtered rows
    rnames = filtered_df['Rname'].tolist()
    ecs = [reaction_df['EC'][reaction_df['Rname']== rname].to_list()[0] for rname in rnames]

    if len(ecs)==0:
        if (len(reactants_kegg_ids)==1)&(len(products_kegg_ids)==1):
            if (reactants_kegg_ids[0] != None)&(products_kegg_ids[0] != None):
                url = f"http://rest.genome.jp/ezyme/{reactants_kegg_ids[0]}/{products_kegg_ids[0]}/version=1"
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Error: HTTP {response.status_code}")
                    ecs = []
                else:
                    lines = response.text.strip().split('\n')
                    lines = [line for line in lines if not line.startswith("#")]
                    if (lines == ['\tNA']) or (len(lines) == 0):
                        print("No data found")
                        ecs = []
                    else:
                        highest_score, highest_ec = max((float(line.split()[0]), line.split()[1]) for line in lines if line.split()[0] != 'NA')
                        ecs =  [highest_ec]
    if (rnames == []):
        rnames = None
    if (ecs == []):
        ecs = None
    else:
        n_ecs = list()
        for i in ecs:
            while len(i.split(".")) < 4:
                i += ".-"
        n_ecs.append(i)
        ecs = n_ecs

    return rnames, ecs
