Quick Start to use the CLI
==============================

This section provides instructions for using the command-line interface based on the official code repository:
`https://github.com/SeulLee05/READRetro <https://github.com/SeulLee05/READRetro>`_

Installation
---------------------------------------

Follow these steps to set up your environment and install READRetro.

**1. Set Up Conda Environment (Recommended)**

   Create a new Conda environment specifically for READRetro to avoid conflicts with other Python packages:

   .. code-block:: bash

      conda create -n readretro python=3.8 -y
      conda activate readretro

**2. Install Dependencies and READRetro Package**

   * **Option A: Install via Pip (includes core dependencies):**
       This is the simplest way to get started.

       .. code-block:: bash

          pip install readretro==1.2.0

       *Note: This pip installation attempts to install core dependencies. You might still need to manually ensure PyTorch with CUDA support is correctly installed if you plan to use a GPU.*
       To install PyTorch with specific CUDA version (e.g., 11.3):

       .. code-block:: bash

          conda install pytorch==1.12.0 cudatoolkit=11.3 -c pytorch
          # Then install other dependencies if not covered by readretro pip package
          pip install easydict pandas tqdm numpy==1.22 OpenNMT-py==2.3.0 networkx==2.5
          conda install -c conda-forge rdkit=2019.09 # Ensure RDKit is compatible

   * **Option B: Install from Source (for development or specific modifications):**
       Clone the repository and install dependencies.

       .. code-block:: bash

          git clone https://github.com/SeulLee05/READRetro.git
          cd READRetro
          # Install dependencies as listed in Option A (PyTorch, RDKit, others)
          # or use a provided requirements.txt if available in the repository
          # pip install -r requirements.txt

Data Setup (`READRetro_data`)
------------------------------------------------------------------------------

The READRetro models and evaluation scripts require specific data files, including pre-trained model weights, datasets for evaluation, and scripts.

1.  **Download Data:**
    Download the `READRetro_data` folder from Zenodo: `https://zenodo.org/records/11485641 <https://zenodo.org/records/11485641>`_.

2.  **Directory Structure:**
    The expected directory structure within `READRetro_data` is:

    ::

        READRetro_data/
        ├── data.sh
        ├── data/
        │   ├── model_train_data/
        │   └── multistep_data/
        ├── model/
        │   ├── bionavi/
        │   ├── g2s/
        │   │   └── saved_models/
        │   ├── megan/
        │   └── retroformer/
        │       └── saved_models/
        ├── result/
        └── scripts/

3.  **Place and Prepare Data**

       * Move the downloaded `READRetro_data` folder into your main `READRetro` project directory (e.g., if you cloned the GitHub repo, it should be `READRetro/READRetro_data`).
       
       * Navigate into the `READRetro_data` directory and run the setup script:

        .. code-block:: bash

           cd READRetro_data
           sh data.sh
           cd ..  # Go back to the main READRetro directory

4.  **Verify Data Paths**

    Ensure that the symbolic links or copied data are correctly pointing to the locations expected by the scripts.
    
       * `READRetro/retroformer/saved_models` should correspond to `READRetro_data/model/retroformer/saved_models`.
       
       * `READRetro/g2s/saved_models` should correspond to `READRetro_data/model/g2s/saved_models`.
       
       * `READRetro/data` should correspond to `READRetro_data/data/multistep_data`.
       
       * Other paths like `result/` and `scripts/` should also align.

    The directories `READRetro_data/model/bionavi/`, `READRetro_data/model/megan/`, and `READRetro_data/data/model_train_data/` are typically needed for reproducing results from the original manuscript.

Model Preparation
-----------------------------------------------------------------------------------------------

* **Using Pre-trained Models** 

  The `READRetro_data` bundle from Zenodo includes pre-trained model checkpoints for Retroformer and Graph2SMILES, which are placed in the correct directories by the `data.sh` script. These are generally located under `READRetro/retroformer/saved_models/` and `READRetro/g2s/saved_models/`.

* **Training Your Own Models** 

    If you wish to train your own models, refer to the official repositories for

    * Graph2SMILES: `https://github.com/coleygroup/Graph2SMILES <https://github.com/coleygroup/Graph2SMILES>`_
    * Retroformer: `https://github.com/yuewan2/Retroformer <https://github.com/yuewan2/Retroformer>`_
    
    The `demo.ipynb` often included in the READRetro repository provides more detailed instructions on training and using custom models. Ensure your custom model checkpoints and vocabulary files are placed where the READRetro scripts expect them.
