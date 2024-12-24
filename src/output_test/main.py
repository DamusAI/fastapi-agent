#!/usr/bin/env python
import sys
import warnings
from fastapi import FastAPI
from pydantic import BaseModel
from src.output_test.crew import OutputTest

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI()

class TopicInput(BaseModel): 
    topic: str

@app.post("/topic")
async def run(topic: TopicInput):
    inputs = {
        'topic': topic.topic
    }
    output_test = OutputTest()
    crew = output_test.crew()
    
    crew_output = crew.kickoff(inputs=inputs)
    
    # If we have a Pydantic model output, convert it to dict
    if crew_output.pydantic:
        return crew_output.pydantic.model_dump()
    
    # Fallback to raw output if no Pydantic model
    return crew_output.raw


