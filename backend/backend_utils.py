import pandas as pd

FILENAME_STARTING_MOLECULES = 'DualRetro_release/data/building_block.csv'
starting_mols_full = list(pd.read_csv(FILENAME_STARTING_MOLECULES)['mol'])

def _mol2image(mol, width=0, height=0):
    from rdkit.Chem import MolFromSmiles, Draw
    from io import BytesIO
    from base64 import b64encode
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
        return MolToSmiles(mol,isomericSmiles=False)
    except:
        return smi

def _mnx_search(smi):
    extract = mnx_df[mnx_df['SMILES'] == _neutralize_atoms(smi)]
    if not len(extract):
        return None, None
    else:
        mnx_id, name = extract["ID"].values[0], extract["name"].values[0]
        return mnx_id, name

rdb_df = pd.read_csv("DualRetro_release/utils/files/train_canonicalized.txt", sep=">>", header=None, names=["reactant", "product"])

def _rdb_search(mol1, mol2):
    extract = rdb_df[(rdb_df['reactant'] == _neutralize_atoms(mol1)) & (rdb_df['product'] == _neutralize_atoms(mol2))]
    if len(extract):
        return True
    else:
        return False