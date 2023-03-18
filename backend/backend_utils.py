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

all_building_blocks = { mol: _mol2image(mol) for mol in starting_mols_full }