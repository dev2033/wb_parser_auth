import json
import os

from fastapi import APIRouter, FastAPI, BackgroundTasks, HTTPException

from logger import logger
from parser_wildberris import wb_parser
from schemas import DataCsv


app = FastAPI()
router = APIRouter()


@logger.catch
@router.post("/csv-json")
async def upload_csv_json(csv_data: DataCsv, bg: BackgroundTasks):
    with open('state_parsing.json', 'r') as state:
        if os.path.exists('results/data_out.json'):
            os.remove('results/data_out.json')
        data = csv_data.json()
        data_json = json.loads(data)
        file = json.loads(state.read())
        state_parser = file.get('parser_state')
        if not state_parser:
            raise HTTPException(405, "Parsing process in progress! "
                                     "Please wait...")
        else:
            bg.add_task(wb_parser, data_json)
            return csv_data


@logger.catch
@router.get('/get_data_json')
async def get_data_json():
    with open('results/data_out.json', 'r') as file:
        result_json = json.loads(file.read())
        return result_json


app.include_router(router)


