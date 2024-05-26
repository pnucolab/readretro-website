from celery_app import celery_task
#from retro_star.api import RSPlanner
import subprocess
from rdkit.Chem import MolFromSmiles, MolToSmiles
from db.models import Task
from db.database import db_context
import json
from datetime import datetime
from backend_utils import _mol2image, _kegg_reaction_search, _kegg_search
import time
import torch
import pandas as pd
import traceback

NUMBER_OF_GPUS = torch.cuda.device_count()
class Node:
    def __init__(self, smiles, weight, prev = None):
        self.smiles = smiles
        self.prev = prev
        self.next = []

        if "keggpath" in self.smiles:
            kegg_n = self.smiles.split("rn")[1].split("+")[0]
            kegg = self.smiles.split("keggpath=")[1]
            df = pd.read_csv('READRetro/data/map_title.csv')
            extract = df[df['ID'] == int(kegg_n)]
            self.kegg_reaction = extract["Name"].values[0]
            self.smiles = kegg
        else:
            self.kegg_reaction = None

        if self.prev is not None:
            self.weight = weight
            self.image = _mol2image(self.smiles)
            self.kegg = _kegg_search(self.smiles)
        else:
            self.kegg_reaction = None
            self.weight = None
            self.image = _mol2image(self.smiles)
            self.kegg = _kegg_search(self.smiles)
        
    def get_ec_and_reaction(self):
        if len(self.next) == 0:
            return None, None
        print([self.smiles], [n.smiles for n in self.next])
        return _kegg_reaction_search([self.smiles], [n.smiles for n in self.next])
    
    def get_end_nodes(self):
        if len(self.next) == 0:
            return [self]
        else:
            out = []
            for n in self.next:
                out += n.get_end_nodes()
            return out
    
    def __repr__(self):
        return self.smiles
    
    def __str__(self):
        return self.smiles
    
    
    
def pathways_to_json(pathways):
    out_list = []
    for pathway in sorted(set(pathways)):
        reactions = pathway.rstrip().split("|")
        root = None
        prev = []
        for reaction in reactions:
            source, weight, targets = reaction.split('>')
            targets = targets.split(".") if not "keggpath" in targets else [targets]

            if len(prev) == 0: # add a root node
                root = Node(source, weight)
                prev.append(root)
            
            for target in targets:
                found = False
                for p in prev[::-1]:
                    if p.smiles == source:
                        found = True
                        break
                if found is False:
                    raise Exception("Target not found in previous nodes")
                new_node = Node(target, weight, p)
                p.next.append(new_node)
                prev.append(new_node)
        
        out_nodes = []
        end_nodes = root.get_end_nodes()
        for n in end_nodes:
            out_nodes.append([n])
            prev = n
            while True:
                prev = prev.prev
                if prev is None:
                    break
                out_nodes[-1].append(prev)
        
        max_path_len = len(max(out_nodes, key=len))
        for i in range(len(out_nodes)):
            out_nodes[i] = out_nodes[i][::-1] + [None] * (max_path_len - len(out_nodes[i]))

        out_nodes = [list(e) for e in zip(*out_nodes)]

        for i in range(len(out_nodes)):
            for j in range(1, len(out_nodes[i]))[::-1]:
                if out_nodes[i][j-1] == out_nodes[i][j]:
                    out_nodes[i][j] = None
        
        for i in range(len(out_nodes)):
            for j in range(len(out_nodes[i]))[::-1]:
                if out_nodes[i][j] is not None:
                    out_nodes[i] = out_nodes[i][:j+1]
                    break

        out_list.append([])
        for nodes in out_nodes:
            out_list[-1].append([None if n is None else {"smiles":n.smiles, "reaction": n.get_ec_and_reaction(), "kegg": n.kegg, "weight": n.weight, "image": n.image, "kegg_reaction":n.kegg_reaction, "next":[j.smiles for j in n.next]} for n in nodes])

        for p in out_list:
            max_length = max(len(sub_array) for sub_array in p)
            for sub_array in p:
                while len(sub_array) < max_length:
                    sub_array.append(None)
                
    return out_list


@celery_task.task
def run_inference(product: str, building_blocks: str, iterations: int, exp_topk: int, route_topk: int, beam_size: int, retrieval: bool,  path_retrieval: bool, retrieval_db: str, model_type: str):
    task_id = run_inference.request.id
    gpu_id = -1
    while True:
        gpu_occupied = [False for _ in range(NUMBER_OF_GPUS)]
        with db_context() as s:
            task = s.query(Task).filter(Task.task_id == task_id).first()
            for task_running in s.query(Task).filter(Task.status == 1).all():
                gpu_occupied[task_running.gpu_id] = True
            if not all(gpu_occupied):
                task.gpu_id = gpu_id = gpu_occupied.index(False)
                task.status = 1
                s.commit()
                break
        time.sleep(1)
    try:
        
        if model_type == "retriever_only":
            retrieval = True
        cmd = f"cd READRetro && CUDA_VISIBLE_DEVICES={gpu_id} python run.py \"{product}\"" \
                + f" --route_topk {route_topk}" \
                + f" --exp_topk {exp_topk}" \
                + f" --iterations {iterations}" \
                + f" --beam_size {beam_size}" \
                + f" --retrieval {str(retrieval).lower()}" \
                + f" --path_retrieval {str(path_retrieval).lower()}" \
                + f" --model_type {model_type}"
        if retrieval_db != "":
            cmd += f" --db_path {retrieval_db}"
        if building_blocks != "":
            blocks = f"/tmp/{task_id}_blocks.csv"
            with open(blocks, "w") as f:
                f.write("mol\n")
                f.write(building_blocks.replace(',', '\n'))
            cmd += f" --blocks {blocks}"
        
        print("Executing command:")
        print(cmd)
        res = subprocess.run(cmd, capture_output=True, shell=True)
        if res.returncode != 0:
            print("Execution Error:")
            print(res.stderr.decode("utf-8"))
            with db_context() as s:
                task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
                task.end_at = datetime.now()
                task.status = -2
                s.commit()
            return []

        lines = res.stdout.decode("utf-8").strip().split('\n')[:-1] # remove the last line (execution time)

        #lines = data.strip().split('\n')[:-1]
        if lines[0] == "None":
            pathways = []
        else:
            pathways = [l.split()[-1] for l in lines]   # remove the first column (pathway index)
        
        subprocess.run(f"rm -f /tmp/{task_id}*", capture_output=True, shell=True)

        with db_context() as s:
            task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
            task.result = json.dumps(pathways_to_json(pathways))
            task.end_at = datetime.now()
            task.status = 0
            s.commit()
    except Exception as e:
        print("Python Error:")
        print(e)
        traceback.print_exc()
        with db_context() as s:
            task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
            task.end_at = datetime.now()
            task.status = -2
            s.commit()
        return []
    return pathways_to_json(pathways)