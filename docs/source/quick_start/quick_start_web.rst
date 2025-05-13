Quick Start to use the READRetro website
============================================================

This section provides instructions for using the web interface located at `https://readretro.net <https://readretro.net>`_.
The official code repository for the web interface is `https://github.com/pnucolab/readretro-website <https://github.com/pnucolab/readretro-website>`_.

Using the Web Interface
-----------------------

1.  **Navigate to the Website:**
    Open your web browser and go to `https://readretro.net <https://readretro.net>`_. You will see the main interface for READRetro.

2.  **Input Target Molecule (Arguments Tab):**
    The "Arguments" tab is typically selected by default.
    * **Experiment Information:**
        * **(Optional)** Enter a "Title" for your experiment.
        * **Target molecule in SMILES:** This is a required field. Input the SMILES (Simplified Molecular Input Line Entry System) string of the natural product you want to analyze. You can often find SMILES strings for compounds in databases like PubChem.
    * **Options:** You can adjust several parameters to customize the prediction:
        * **Number of iterations:** Sets the maximum number of expansion steps the algorithm will perform (Default: 100).
        * **Number of pathway generation:** Specifies how many top-ranked pathways to display (Default: 10).
        * **Number of expansions:** The number of candidate precursors considered at each expansion step (similar to beam size for single-step retrosynthesis) (Default: 10).
        * **Beam size:** Beam size for the underlying single-step retrosynthesis models (Default: 10).
        * **Reaction Retriever:** Toggle ON/OFF to use or ignore the database of known reactions (Default: ON).
        * **Pathway Retriever:** Toggle ON/OFF to use or ignore the KEGG pathway retrieval for known intermediates (Default: ON).
        * **Model type:** Choose the generative model to use (Default: Ensemble of Retroformer + Graph2SMILES). Other options might include individual models.

3.  **(Optional) Customize Building Blocks (Building Blocks Tab):**
    * Click on the "Building Blocks" tab.
    * Here, you can view the default set of 40 common metabolic precursors that READRetro uses as termination points for the retrosynthetic pathways.
    * You can modify this list, for example, by adding specific intermediates known to be relevant to your target plant or pathway.

4.  **(Optional) Customize Retrieval Database (Retrieval DB Tab):**
    * Click on the "Retrieval DB" tab.
    * This section allows advanced users to modify the reaction database used by the Reaction Retriever. You can add more prior knowledge reactions or remove specific reactions if you want to explore alternative pathways.

5.  **Submit for Prediction:**
    * Once you have entered the SMILES string and adjusted any desired options, click the **"Submit"** button (or an equivalent button like "Run READRetro") to start the pathway prediction process. Each task is assigned a unique Job ID for efficient management.

6.  **View and Interpret Results (Result Page):**
    * After processing, the predicted biosynthetic pathways are displayed on the Result Page. The design integrates interactive cards and arrows for an intuitive visual representation.
    * **Pathway Visualization (Arrows):**
        Arrows are color-coded to convey information about the prediction source:
        * **Red arrows:** Indicate generated steps (novel predictions by the READRetro model). This is the default color for a predicted step not found in retrieval databases.
        * **Blue arrows:** Indicate that the single-step retrosynthesis reaction exists in the retrieval database.
        * **Green arrows:** Specifically mark data retrieved by the Pathway Retriever (sequences of reactions from KEGG).
    * **Information on Arrows:**
        Above and below each arrow, additional information is displayed:
        * **EC numbers:** Enzyme Commission numbers classifying the enzymes based on the reactions they catalyze. These are clickable and link directly to the relevant entries in the BRENDA Enzyme Database.
        * **KEGG pathway information:** Identifies biological pathways related to the compounds. These are clickable and link directly to the relevant KEGG pathway maps.
    * **Compound Representation (Cards):**
        Each compound in the pathway is represented by a card containing detailed information:
        * **Default color:** Typically red.
        * **Blue color:** Indicates the molecule is confirmed in the KEGG database.
        * **Yellow color:** Applied when a user highlights a specific compound using the interface's interactive features.
        * **Details on card:** SMILES notation, KEGG entry (clickable, redirecting to the KEGG COMPOUND Database page), and structural diagrams.
    * **Interactive Features:**
        The Result Page includes features to enhance user interactivity:
        * **Highlighting compounds:** Allows users to focus on specific molecules within the predicted pathways.
        * **Changing pathway direction:** Users can toggle the display of pathways (e.g., retrosynthetic or biosynthetic direction).
    * **Saving Results:**
        The interface provides two main ways to save or re-access your findings:
        * **Unique Result Link:** Each prediction generates a unique web link. The link follows the format ``https://readretro.net/result/`` followed by your specific **[job id]**  (e.g., ``https://readretro.net/result/d0bc0da8ebb245bb87e8aa161fbbd2d6``). You can bookmark or share this link to access the specific result page again later.
        * **Download Result Button:** A "Download result" button allows you to download the predicted pathway information as a ``.txt`` file for offline storage and analysis.
