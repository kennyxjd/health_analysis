import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import logging
from typing import Callable

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CalNameHealth:
    def __init__(self, file_path):
        self.health_name_dict = self.load_csv_name_files(file_path)

    def load_csv_name_files(self, file_path):
        health_name_dict = {}
        df = pd.read_csv(file_path, skiprows=1)
        for _, row in df.iterrows():
            health_name_dict[row.iloc[1]] = {'name': row.iloc[0],
                                             'gender': row.iloc[2],
                                             'age': row.iloc[3],
                                             'height': row.iloc[4],
                                             'weight': row.iloc[5],
                                             'weight_status': row.iloc[6],
                                             'eye': row.iloc[7],
                                             'eye_status': row.iloc[8]}
        return health_name_dict

    def check_info(self, name):
        result = ''
        for id in self.health_name_dict.keys():
            name_temp = self.health_name_dict[id]['name']
            if name_temp == name:
                gender = self.health_name_dict[id]['gender']
                age = self.health_name_dict[id]['age']
                height = self.health_name_dict[id]['height']
                weight = self.health_name_dict[id]['weight']
                weight_status = self.health_name_dict[id]['weight_status']
                eye = self.health_name_dict[id]['eye']
                eye_status = self.health_name_dict[id]['eye_status']
                info = f"姓名：{name} 学号：{id} 性别：{gender} 年龄：{age} 身高：{height} 体重：{weight} 体重情况：{weight_status} " \
                       f"视力：{eye} 视力状态：{eye_status} \n"
                result += info
        if result == '':
            return '没有查询到该学生'
        else:
            return result

class CalHealth:
    def __init__(self, folder_path) -> None:
        self.range = dict()
        self.health_dict = self.load_csv_files(folder_path)
        self.out_range_info = self.out_range_format()

    def load_csv_files(self, folder_path):
        health_dict = {}

        # Traverse through all files in the directory
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                age_range = self.extract_age_range(file_name)
                height_list = []
                df = pd.read_csv(file_path, skiprows=1)
                if age_range not in health_dict:
                    health_dict[age_range] = dict()
                for _, row in df.iterrows():
                    height = row.iloc[0]
                    height_list.append(height)
                    info = {
                        "boy": {
                            "median_weight": row.iloc[1],
                            "underweight_deviation": row.iloc[2],
                            "overweight_deviation": row.iloc[3],
                            "obese_deviation": row.iloc[4],
                            "severely_obese_deviation": row.iloc[5],
                        },
                        "girl": {
                            "median_weight": row.iloc[6],
                            "underweight_deviation": row.iloc[7],
                            "overweight_deviation": row.iloc[8],
                            "obese_deviation": row.iloc[9],
                            "severely_obese_deviation": row.iloc[10],
                        },
                    }

                    health_dict[age_range][height] = info

                self.range[age_range] = [min(height_list), max(height_list)]

        return health_dict

    def out_range_format(self):
        out_range_info = "请按提示输入正确的年龄和身高范围 》 "
        for age_range, height_range in self.range.items():
            out_range_info += f"年龄范围：{age_range[0]}岁 - {age_range[1]}岁，身高范围：{height_range[0]}cm - {height_range[1]}cm  "
        return out_range_info

    def extract_age_range(self, file_name):
        """Helper function to extract age range from file name like '3-5.csv'"""
        base_name = os.path.splitext(file_name)[0]  # Remove the file extension
        min_age, max_age = map(int, base_name.split("-"))
        return min_age, max_age

    def in_range(self, value, range_tuple):
        """Helper function to check if a value is within a given range tuple (min, max)"""
        return range_tuple[0] <= value < range_tuple[1]

    def determine_health_status(self, weight_records, weight):
        """Determine the health status based on weight deviations"""
        (
            median_weight,
            underweight_deviation,
            overweight_deviation,
            obese_deviation,
            severely_obese_deviation,
        ) = weight_records.values()

        if weight < median_weight - underweight_deviation:
            return "偏瘦"
        elif weight < median_weight + overweight_deviation:
            return "正常"
        elif weight < median_weight + obese_deviation:
            return "超重"
        elif weight < median_weight + severely_obese_deviation:
            return "肥胖"
        else:
            return "过度肥胖"

    def search_health_result(self, age, height, gender, weight):
        for age_range, records in self.health_dict.items():
            if self.in_range(age, age_range):
                height_records = records[height]
                weight_records = height_records[gender]
                return self.determine_health_status(weight_records, weight)

        return self.out_range_info

app = FastAPI()
calhealth = CalHealth("./data/health")
calhealthname = CalNameHealth("./data/stu_info/health_name.csv")

class HealthCheckRequest(BaseModel):
    age: int
    height: float
    gender: str
    weight: float

class HealthNameCheckRequest(BaseModel):
    name: str

# @app.middleware("http")
# async def log_request_middleware(request: Request, call_next: Callable):
#     body = await request.body()
#     logger.info(f"Request body: {body.decode('utf-8')}")
#     response = await call_next(request)
#     return response

@app.post("health-name-check")
async def health_name_check(request: HealthNameCheckRequest):
    logger.info("=" * 70)
    logger.info(f"Received health-name check request: {request}")
    try:
        result = calhealthname.check_info(
            name=request.name)

        if result == "No matching health result found.":
            logger.warning(f"No matching health result found for request: {request}")
            raise HTTPException(status_code=404, detail=result)
        logger.info(f"Health check result: {result}")
        return JSONResponse(content={"health_status": result})

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        logger.error(f"Validation error details: {e.errors()}")
        raise HTTPException(status_code=422, detail=e.errors())

@app.post("/health-check")
async def health_check(request: HealthCheckRequest):
    logger.info("=" * 70)
    logger.info(f"Received health check request: {request}")
    try:
        result = calhealth.search_health_result(
            age=request.age,
            height=request.height,
            gender=request.gender,
            weight=request.weight)

        if result == "No matching health result found.":
            logger.warning(f"No matching health result found for request: {request}")
            raise HTTPException(status_code=404, detail=result)
        logger.info(f"Health check result: {result}")
        return JSONResponse(content={"health_status": result})

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        logger.error(f"Validation error details: {e.errors()}")
        raise HTTPException(status_code=422, detail=e.errors())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
