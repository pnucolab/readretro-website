Quick Start to use the CLI
==============================

This section provides instructions for using the command-line interface based on the official code repository:
`https://github.com/SeulLee05/READRetro <https://github.com/SeulLee05/READRetro>`_

Installation
----------------------------------------------------
Run the following commands to install the dependencies using Conda:

.. code-block:: bash

   conda create -n readretro python=3.8
   conda activate readretro
   conda install pytorch==1.12.0 cudatoolkit=11.3 -c pytorch
   pip install easydict pandas tqdm numpy==1.22 OpenNMT-py==2.3.0 networkx==2.5
   conda install -c conda-forge rdkit=2019.09

Alternatively, you can install the ``readretro`` package through pip:

.. code-block:: bash

   conda create -n readretro python=3.8 -y
   conda activate readretro
   pip install readretro==1.2.0


Data Setup
----------------------------------------------------
Download the necessary data folder ``READRetro_data`` from `Zenodo <https://zenodo.org/records/11485641>`_ to ensure proper execution of the code and demonstrations in this repository.

The directory structure of ``READRetro_data`` is as follows:

::

    READRetro_data
    ├── data.sh
    ├── data
    │   ├── model_train_data
    │   └── multistep_data
    ├── model
    │   ├── bionavi
    │   ├── g2s
    │   │   └── saved_models
    │   ├── megan
    │   └── retroformer
    │       └── saved_models
    ├── result
    └── scripts


Place ``READRetro_data`` into the READRetro directory (i.e., ``READRetro/READRetro_data``) and run ``sh data.sh`` in ``READRetro_data`` to set up the data.

Ensure the data is correctly located in ``READRetro``. Verify the following:

* ``READRetro/retroformer/saved_models`` should match ``READRetro_data/model/retroformer/saved_models``.
* ``READRetro/g2s/saved_models`` should match ``READRetro_data/model/g2s/saved_models``.
* ``READRetro/data`` should match ``READRetro_data/data/multistep_data``.
* ``READRetro/result`` should match ``READRetro_data/result``.
* ``READRetro/scripts`` should match ``READRetro_data/scripts``.

The directories ``READRetro_data/model/bionavi``, ``READRetro_data/model/megan``, and ``READRetro_data/data/model_train_data`` are required for reproducing the values in the manuscript.


Model Preparation
----------------------------------------------------
We provide the trained models through Zenodo.
You can use your own models trained using the official codes (https://github.com/coleygroup/Graph2SMILES and https://github.com/yuewan2/Retroformer).
More detailed instructions can be found in ``demo.ipynb``.

Single-step Planning and Evaluation
--------------------------------------------------------------------------------------------------------

Run the following commands to evaluate the single-step performance of the models (replace ``${gpu_id}`` with your GPU ID):

.. code-block:: bash

   # Ensemble
   CUDA_VISIBLE_DEVICES=${gpu_id} python eval_single.py
   # Retroformer
   CUDA_VISIBLE_DEVICES=${gpu_id} python eval_single.py -m retroformer
   # Graph2SMILES
   CUDA_VISIBLE_DEVICES=${gpu_id} python eval_single.py -m g2s -s 200


Multi-step Planning
--------------------------------------------------------------------------------------------------------
Run the following command to plan paths of multiple products using multiprocessing:

.. code-block:: bash

   # Example: Use GPU 0
   CUDA_VISIBLE_DEVICES=0 python run_mp.py

You can modify other hyperparameters described in ``run_mp.py``. Lower ``num_threads`` if you run out of GPU capacity.

Run the following command to plan the retrosynthesis path of your own molecule:

.. code-block:: bash

   # Example: Use GPU 0 and plan for 'O=C1C=C2C=CC(O)CC2O1'
   CUDA_VISIBLE_DEVICES=0 python run.py 'O=C1C=C2C=CC(O)CC2O1'

*Using the command from pip:*

.. code-block:: bash

   # Example: Use default checkpoints for 'O=C1C=C2C=CC(O)CC2O1'
   run_readretro -rc retroformer/saved_models/biochem.pt -gc g2s/saved_models/biochem.pt 'O=C1C=C2C=CC(O)CC2O1'
   # You can replace the checkpoints with your own trained checkpoints.
   # Set the corresponding vocab file as an option if you replace checkpoints.

You can modify other hyperparameters described in ``run.py``.

Multi-step Evaluation
--------------------------------------------------------------------------------------------------------

Run the following command to evaluate the planned paths of the test molecules:

.. code-block:: bash

   # Example: Evaluate results saved in result/debug.txt
   python eval.py result/debug.txt

Demo
--------------------------------------------------------------------------------------------------------

You can reproduce the figures and tables presented in the paper or train your own models by utilizing the provided ``demo.ipynb``.

