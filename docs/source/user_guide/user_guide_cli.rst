User Guide for the CLI
==============================

This guide provides comprehensive instructions for installing, configuring, and using the READRetro Command-Line Interface (CLI).
All commands should generally be run from the root of your `READRetro` project directory. Set `CUDA_VISIBLE_DEVICES` to specify which GPU(s) to use.

Single-step Planning and Evaluation (`eval_single.py`)
------------------------------------------------------------------------------------------------------------

   This script evaluates the performance of the single-step retrosynthesis models.

   * **Ensemble Model (Default):**

       .. code-block:: bash

          CUDA_VISIBLE_DEVICES=0 python eval_single.py

   * **Retroformer Only:**

       .. code-block:: bash

          CUDA_VISIBLE_DEVICES=0 python eval_single.py -m retroformer

   * **Graph2SMILES Only:**
       The `-s` argument specifies the beam size for Graph2SMILES.

       .. code-block:: bash

          CUDA_VISIBLE_DEVICES=0 python eval_single.py -m g2s -s 200

   Replace `0` with your desired GPU ID. The script will output Top-K accuracy metrics.

Multi-step Planning
------------------------------------------------------------------------------------------------------------

   * **Planning for Multiple Products (`run_mp.py`):**
       This script is used for running multi-step predictions on a list of molecules, often utilizing multiprocessing for efficiency.

       .. code-block:: bash

          CUDA_VISIBLE_DEVICES=0 python run_mp.py

       You may need to edit `run_mp.py` to:
       * Specify the input file containing SMILES strings.
       * Adjust `num_threads` based on your GPU capacity and number of CPU cores. Lower it if you encounter out-of-memory errors.
       * Modify other hyperparameters like iteration limits, beam sizes, etc.

   * **Planning for a Single Product (`run.py`):**
       Use this script for predicting pathways for a single target molecule.

       .. code-block:: bash

          CUDA_VISIBLE_DEVICES=0 python run.py 'YOUR_TARGET_SMILES_STRING'

       Example:

       .. code-block:: bash

          CUDA_VISIBLE_DEVICES=0 python run.py 'O=C1C=C2C=CC(O)CC2O1'

       Modify hyperparameters directly within `run.py` or via command-line arguments if supported by the script version.

   * **Using the Pip Command (`run_readretro`):**
       If you installed READRetro via pip, you can use the `run_readretro` command.

       .. code-block:: bash

          run_readretro -rc path/to/retroformer_model.pt -gc path/to/g2s_model.pt 'YOUR_TARGET_SMILES_STRING'

       Example using typical checkpoint paths after data setup:

       .. code-block:: bash

          run_readretro -rc retroformer/saved_models/biochem.pt -gc g2s/saved_models/biochem.pt 'O=C1C=C2C=CC(O)CC2O1'

       * `-rc`: Path to the Retroformer model checkpoint.
       * `-gc`: Path to the Graph2SMILES model checkpoint.
       * You must also ensure the corresponding vocabulary files (e.g., `vocab.txt` or `vocab.pt`) are correctly located relative to the checkpoints or specify their paths if the script requires it, especially when using custom-trained models. Default paths are usually configured for the provided Zenodo models.
       * Additional options (e.g., for iteration count, beam size) might be available. Use `run_readretro --help` if available, or refer to the underlying `run.py` script for configurable parameters.

Multi-step Evaluation (`eval.py`)
------------------------------------------------------------------------------------------------------------

   This script evaluates the accuracy of the planned multi-step pathways against a ground truth dataset.

   .. code-block:: bash

      python eval.py path/to/your_prediction_result_file.txt

   Example:

   .. code-block:: bash

      python eval.py result/debug.txt

   The script will output metrics such as success rate, hit rate of building blocks, and exact pathway match rate.

Using `demo.ipynb`
------------------

The `demo.ipynb` Jupyter notebook, typically found in the root of the GitHub repository, provides a comprehensive guide to:
* Reproducing figures and tables from the original READRetro publication.
* Step-by-step examples of running predictions.
* Instructions for training your own single-step models (Retroformer, Graph2SMILES) and integrating them into the multi-step planning framework.
