import json
from fastapi import FastAPI, Query, File, UploadFile
from celery_worker import run_inference
from uuid import uuid4
from datetime import datetime

from db.database import db_context

from db.models import Base, Task
from db.database import engine
Base.metadata.create_all(bind=engine)

from backend_utils import FILENAME_STARTING_MOLECULES, all_building_blocks, _mol2image

app = FastAPI()

with db_context() as s:
    tasks = s.query(Task).filter(Task.status > 0)
    for t in tasks:
        t.status = -1
    s.commit()

@app.post("/run")
async def run(product: str = Query(default="O=C1C=C2C=CC(O)CC2O1", title="Product SMILES"),
              building_blocks: str = Query(default="", title="Building blocks SMILES, comma seperated"),
              iterations: int = Query(ge=1, le=120, default=20, title="Number of iterations"),
              exp_topk: int = Query(ge=1, le=10, default=10, title="Number of expansions"),
              route_topk: int = Query(ge=1, le=10, default=10, title="Number of pathway generations"),
              beam_size: int = Query(ge=1, le=10, default=10, title="Beam size"),
              retrieval: bool = Query(default=True, title="Retriever usage"),
              file: UploadFile | None = None):
    try:
        task_id = uuid4().hex
        if file:
            rdb_path = f"/tmp/{task_id}_retrieval_db.txt"
            with open(rdb_path, "wb") as f:
                f.write(file.file.read())
        else:
            rdb_path = ""
        with db_context() as s:
            task = Task(
                task_id=task_id,
                product=product,
                building_blocks=building_blocks,
                route_topk=route_topk,
                exp_topk=exp_topk,
                iterations=iterations,
                beam_size=beam_size,
                retrieval=retrieval,
                retrieval_db=rdb_path,
                created_at=datetime.now(),
                status=2
            )
            s.add(task)
            s.commit()
        rtn = run_inference.apply_async([product, building_blocks, iterations, exp_topk, route_topk, beam_size, retrieval, rdb_path], task_id=task_id)
        return {"success": True, "ticket": task_id}
    except Exception as e:
        return {"success": False, "error": repr(e)}

@app.get("/result")
async def result(ticket: str):
    try:
        #job = run_inference.AsyncResult(ticket)
        with db_context() as s:
            task = s.query(Task).filter(Task.task_id == ticket).first()
            if task.status == 0:
                return {"success": True, "task_id": task.task_id, "created_at": task.created_at, "product": task.product, "pathway": json.loads(task.result), "end_at": task.end_at, "status": task.status}
            else:
                return {"success": True, "task_id": task.task_id, "created_at": task.created_at, "product": task.product, "status": task.status}
    except Exception as e:
        return {"success": False, "error": repr(e)}

@app.get("/cancel")
async def cancel(ticket: str):
    try:
        job = run_inference.AsyncResult(ticket)
        job.revoke(terminate=True)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": repr(e)}

@app.get("/building-blocks")
async def building_blocks():
    try:
        return {
            "success": True,
            "building_blocks": all_building_blocks
        }
    except Exception as e:
        return {"success": False, "error": repr(e)}


@app.get("/mol2image")
async def mol_to_image(mol: str,
                       width: int = Query(default=0, title="Image width in pixels"),
                       height: int = Query(default=0, title="Image height in pixels")):
    try:
        return {"success": True, "image": _mol2image(mol, width, height)}
    except Exception as e:
        return {"success": False, "error": repr(e)}
