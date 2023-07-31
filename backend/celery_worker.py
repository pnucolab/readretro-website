from celery_app import celery_task
#from retro_star.api import RSPlanner
import subprocess
from rdkit.Chem import MolFromSmiles, MolToSmiles
from db.models import Task
from db.database import db_context
import json
from datetime import datetime
from backend_utils import _mnx_search, _mol2image, _kegg_reaction_search
import time
import torch

NUMBER_OF_GPUS = torch.cuda.device_count()

def r2r(raw_reaction):
    keggpath = None
    if "keggpath" in raw_reaction:
        raw_reaction, keggpath = raw_reaction.split(">keggpath=")
    reactions = [r.split('>') for r in raw_reaction.split('|')]
    print("reactions",reactions)
    reactants = [r[0] for r in reactions]
    products = [r[-1] for r in reactions]
    kegg_reactions = [_kegg_reaction_search(reactants, products)]
    print("kegg_reactions",kegg_reactions)
    molecules = [r[0] for r in reactions] + [reactions[-1][-1]]
    molecules = [{"smiles": m, "image": _mol2image(m), "mnx_info": _mnx_search(m)} for m in molecules]
    print("molecules",molecules)
    scores = [r[1] for r in reactions]
    return {"molecules": molecules, "scores": scores, "kegg_reactions": kegg_reactions, "kegg_path": keggpath}

@celery_task.task
def run_inference(product: str, building_blocks: str, iterations: int, exp_topk: int, route_topk: int, beam_size: int, retrieval: bool, retrieval_db: str, model_type: str):
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
        if lines[0] == "None":
            raw_reactions = []
        else:
            raw_reactions = [r.split()[-1] for r in lines]
            raw_reactions = sorted(set(raw_reactions))
        result = [r2r(r) for r in raw_reactions]
        print(result)


        subprocess.run(f"rm -f /tmp/{task_id}*", capture_output=True, shell=True)

        with db_context() as s:
            task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
            task.result = json.dumps(result)
            task.end_at = datetime.now()
            task.status = 0
            s.commit()
    except Exception as e:
        print("Python Error:")
        print(e)
        with db_context() as s:
            task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
            task.end_at = datetime.now()
            task.status = -2
            s.commit()
        return []
    return result