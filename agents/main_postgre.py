from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.postgres import PostgresTools
from dotenv import load_dotenv
import os

load_dotenv()


# Initialize PostgresTools with connection details
postgres_tools = PostgresTools(
    host="dpg-d20i113uibrs73880sjg-a.oregon-postgres.render.com",
    port=5432,
    db_name="dbname_h6nw",
    user="dbname_h6nw_user",
    password="9POGGouJpvbRr5VZQuLXCsCdQN1L2FT7",
    table_schema="public",
)

# Create an agent with the PostgresTools
agent = Agent(tools=[postgres_tools],
              model=Groq(id="llama-3.3-70b-versatile"))

agent.print_response("Fale todas as tabelas do banco de dados", markdown=True)

agent.print_response("""
Faça uma query para pegar todas as colunas de bitcoin na tabela bitcoin_dados
""")

agent.print_response("""
Faça uma análise super complexa sobre o bitcoin usando os dados da tabela bitcoin_dados
""")