import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class CalHealth:
    def __init__(self, folder_path) -> None:
        self.health_dict = self.load_csv_files(folder_path)

    def load_csv_files(self, folder_path):
        health_dict = {}
        # Traverse through all files in the directory
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                age_range = self.extract_age_range(file_name)
                df = pd.read_csv(file_path, skiprows=1)

                if age_range not in health_dict:
                    health_dict[age_range] = dict()
                for _, row in df.iterrows():
                    height = row.iloc[0]
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

        return health_dict

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

        return "No matching health result found."


app = FastAPI()
calhealth = CalHealth("./data/health")


class HealthCheckRequest(BaseModel):
    age: int
    height: float
    gender: str
    weight: float


@app.post("/health-check")
def health_check(request: HealthCheckRequest):
    result = calhealth.search_health_result(
        age=request.age,
        height=request.height,
        gender=request.gender,
        weight=request.weight)

    if result == "No matching health result found.":
        raise HTTPException(status_code=404, detail=result)
    return {"health_status": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
