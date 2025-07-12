from fastapi import FastAPI
import shopping

app = FastAPI()


@app.get("/")
def read_main():
    return {"msg": "Hello World"}


def get_pricing(obj):
    return obj["pricing"]


@app.get("/pricing")
def pricing(keyword: str, sort_by: str = None):
    elite_data = shopping.query_elite(keyword)
    pchome_data = shopping.query_pchome(keyword)
    data = pchome_data + elite_data
    if sort_by == "-pricing":
        data.sort(key=get_pricing)
        # data = sorted(data, key=get_pricing)
    return data
