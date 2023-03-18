from celery_app import celery_task
#from retro_star.api import RSPlanner
import subprocess
from rdkit.Chem import MolFromSmiles, MolToSmiles
from db.models import Task
from db.database import db_context
import json
from datetime import datetime

def r2r(raw_reaction):
    reactions = [r.split('>') for r in raw_reaction.split('|')]
    molecules = [r[0] for r in reactions] + [reactions[-1][-1]]
    return molecules

@celery_task.task
def run_inference(product: str, building_blocks: str, iterations: int, exp_topk: int, route_topk: int, beam_size: int, retrieval: bool, retrieval_db: str):
    task_id = run_inference.request.id
    with db_context() as s:
        task = s.query(Task).filter(Task.task_id == task_id).first()
        task.status = 1
        s.commit()
    cmd = f"cd DualRetro_release && python run.py \"{product}\"" \
            + f" --route_topk {route_topk}" \
            + f" --exp_topk {exp_topk}" \
            + f" --iterations {iterations}" \
            + f" --beam_size {beam_size}" \
            + f" --retrieval {str(retrieval).lower()}"
    if retrieval_db != "":
        cmd += f" --db_path {retrieval_db}"
    if building_blocks != "":
        blocks = f"/tmp/{task_id}_blocks.csv"
        with open(blocks, "w") as f:
            f.write("mol\n")
            f.write(building_blocks.replace(',', '\n'))
        cmd += f" --blocks {blocks}"
    print(cmd)
    rtn = subprocess.run(cmd, capture_output=True, shell=True).stdout.decode("utf-8").strip()
    if rtn == "None":
        raw_reactions = []
    else:
        raw_reactions = [r.split()[-1] for r in rtn.split("\n")[:-1]]
    result = [r2r(r) for r in raw_reactions]

    with db_context() as s:
        task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
        task.result = json.dumps(result)
        task.end_at = datetime.now()
        task.status = 0
        s.commit()
    return result