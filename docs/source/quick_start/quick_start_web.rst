Quick Start to use the READRetro website
==============================

This section provides instructions for using the command-line interface based on the official code repository.

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

