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
def run_inference():
    with db_context() as s:
        task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
        task.status = 1
        s.commit()
    rtn = subprocess.run(f"python run.py --product {task.product}" + 
                                      f" --route_topk {task.route_topk}"
                                      f" --exp_topk {task.exp_topk}"
                                      f" --iterations {task.iterations}"
                                      f" --beam_size {task.beam_size}"
                                      f" --retrieval {task.retrieval}"
                                      f" --starting_mols {task.starting_mols}"
                                      f" --retrieving_db {task.retrieval_db}", capture_output=True, shell=True)

    """
    planner = RSPlanner(
        cuda=True,
        iterations=iterations,
        expansion_topk=expansion_topk,
        route_topk=route_topk,
        beam_size=beam_size,
        retrieval=retrieval,
        starting_mols=starting_mols,
        retrieving_db = 'data/train_canonicalized.txt'
    )
    raw_reactions = planner.plan(MolToSmiles(MolFromSmiles(product)))
    """
    result = [r2r(r) for r in raw_reactions]

    with db_context() as s:
        task = s.query(Task).filter(Task.task_id == run_inference.request.id).first()
        task.result = json.dumps(result)
        task.end_at = datetime.now()
        task.status = 0
        s.commit()
    return result