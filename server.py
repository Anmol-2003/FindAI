from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model = None 
tokenizer = None
app = FastAPI()

# app.add_middleware(
#     CORSMiddleware, 
#     allow_origins = ["*"], 
#     allow_credentials = True, 
#     allow_methods = ['POST', 'GET'], 
#     allow_headers = ['Content-Type']
# )
class Response(BaseModel):
    percentage : float = Field(description='AI Generated Plag percentage')
    label : str = Field(default='ChatGPT')

class Request(BaseModel):
    text : str = Field(..., min_length = 10)

async def inference(text):
    token = tokenizer(text, truncation= True, padding='max_length', max_length=512, return_tensors='pt')
    output = model(**token)
    logits = output.logits
    probabilities = torch.softmax(logits, dim = 1)
    return {'Percentage' : round(probabilities[0][1].item(), 2) * 100, 'Label' : 'CHatGPT'}

@app.get('/')
async def buffer():
    return {'message' : "Server Responding fine", "code" : 200} 

@app.post('/detect')
async def inferText(data : Request): # the data that the /detect api route is receiving as a req body is being validated by the class Data using pydantic
    text = data.text
    prediction = await inference(text)
    r = Response(
        percentage=prediction['Percentage'], 
    )
    response = jsonable_encoder(r)
    return JSONResponse(content=response, status_code=200)

@app.on_event("startup")
def startup():
    global model, tokenizer
    model = AutoModelForSequenceClassification.from_pretrained("microsoft/deberta-v3-base", num_labels = 2)
    tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-base")
    model.load_state_dict(torch.load("./findAI_HC3.pt", map_location = torch.device("cpu")))
    print("Server Initialized...")
    
if __name__ == "__main__":
    app.run()


