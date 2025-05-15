Quick Start to use the READRetro website
============================================================

This section provides instructions for using the web interface located at `https://readretro.net <https://readretro.net>`_.
The official code repository for the web interface is `https://github.com/pnucolab/readretro-website <https://github.com/pnucolab/readretro-website>`_.

Overview of the Website Interface
------------------------------------------------------------------------

The READRetro website is designed for intuitive interaction. The main page is divided into several key areas:

* **Input Area:** Primarily managed through tabs: "Arguments", "Building Blocks", and "Retrieval DB".
* **Submission Control:** A "Submit" button to initiate predictions.
* **Results Display Area:** Where predicted pathways and related information are shown after a job completes.

Submitting a Prediction Job
------------------------------------------------------------------

Predictions are configured and submitted primarily through the "Arguments" tab, with optional customizations in other tabs.

**1. Arguments Tab (Main Configuration)**

   * **Experiment Information**
       * **Title (Optional):** You can assign a custom title to your prediction job for easier identification.
       * **Target molecule in SMILES (Required):** Input the SMILES string of your target natural product. SMILES strings can be obtained from chemical databases like `PubChem <https://pubchem.ncbi.nlm.nih.gov/>`_.

   * **Options** (Fine-tune the prediction process)
       * **Number of iterations:** Maximum number of expansion steps in the pathway search (Default: 100). Increasing this may find longer pathways but takes more time.
       * **Number of pathway generation:** The number of top-ranked pathways to be displayed (Default: 10).
       * **Number of expansions:** The number of candidate precursors considered at each retrosynthetic step (Default: 10). Higher values increase search breadth.
       * **Beam size:** The beam size used by the underlying single-step deep learning models (Retroformer, Graph2SMILES) (Default: 10).
       * **Reaction Retriever (Switch):**
           * **ON (Default):** Allows the model to use its internal database of known biochemical reactions. This helps in recognizing established metabolic steps (improves memorability).
           * **OFF:** The model will rely solely on the generative deep learning models to predict steps, potentially finding more novel or alternative reactions.
       * **Pathway Retriever (Switch):**
           * **ON (Default):** Enables retrieval of entire known pathways or pathway segments from databases like KEGG if an intermediate matches. This can quickly complete parts of the retrosynthesis.
           * **OFF:** Disables retrieval of full pathway segments.
       * **Model type (Dropdown):**
           * **Ensemble (Retroformer + Graph2SMILES) (Default):** Uses a combination of both deep learning models, generally providing the best performance.
           * **Retroformer:** Uses only the Retroformer model.
           * **Graph2SMILES:** Uses only the Graph2SMILES model.

**2. Building Blocks Tab (Optional Customization)**

   * **Viewing Defaults** 

        By default, READRetro uses a predefined set of 40 common metabolic precursors as the target end-points for retrosynthesis. You can view this list here.
   
   * **Customization** 

        You can add or remove building blocks from this list. This is useful if you want the pathways to terminate at specific, known precursors relevant to your biological system or if you want to explore pathways to non-standard starting materials.

**3. Retrieval DB Tab (Optional Customization for Advanced Users)**

   * **Viewing Database** 

        This tab allows inspection of the reactions included in the Reaction Retriever's database.

   * **Modification** 

        Advanced users can modify this database by adding new reactions or removing existing ones. This can be used to incorporate very specific domain knowledge or to force the exploration of pathways that avoid certain known reactions.
