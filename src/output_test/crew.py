from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool	
from pydantic import BaseModel, Field
from typing import List

from dotenv import load_dotenv
load_dotenv()	

# Model for each research point
class ResearchPoint(BaseModel):
	title: str = Field(description="The title of this research point")
	content: str = Field(description="The detailed findings and insights for this point")

# Model for the research task output
class ResearchOutput(BaseModel):
	topic: str = Field(description="The main topic being researched")
	findings: List[ResearchPoint] = Field(description="List of 10 research points with their details")
	urls: List[str] = Field(description="List of URLs that were used to gather the research points")	

# Model for the final report
class FinalReport(BaseModel):
	title: str = Field(description="The title of the final report")
	summary: str = Field(description="A comprehensive summary of the overall findings")
	key_points: List[ResearchPoint] = Field(description="The list of key research points from the research task")
	conclusion: str = Field(description="A conclusion summarizing the implications and importance of the findings")
	sources: List[str] = Field(description="List of sources that were used to gather the research points")	

@CrewBase
class OutputTest():
	"""OutputTest crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[SerperDevTool()]	
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_pydantic=ResearchOutput  # Specify the output model
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_pydantic=FinalReport  # Specify the output model
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
