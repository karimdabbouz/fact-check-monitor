from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get('/')
def read_root(request: Request):
    return {'message': 'Faktencheck-Aggregator API', 'version': '1.0'}


@app.get('/topic-counts')
def get_topic_counts(request: Request):
    '''
    TODO
    Retrieve a list of topic counts for a given time period and optional medium.
    '''
    return {'message': 'Topic counts', 'version': '1.0'}