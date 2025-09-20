from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, input_guardrail, GuardrailFunctionOutput
from typing import Dict
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from pydantic import BaseModel

# %%
load_dotenv(override=True)

# %%
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
mistral_api_key = os.getenv('MISTRAL_API_KEY')


instructions1 = "You are a deep research agent working for PROLIM, \
a company that provides Digital Transformation solutions, powered by AI, for Product Manufacturing companies. \
You will perform deep research on the topic using the mistral_tool agent and provide a detailed report."

instructions2 = "You are a deep research agent working for PROLIM, \
a company that provides Digital Transformation solutions, powered by AI, for Product Manufacturing companies. \
You will perform deep research on the topic using the gemini_tool agent and provide a detailed report."

instructions3 = "You are a deep research agent working for PROLIM, \
a company that provides Digital Transformation solutions, powered by AI, for Product Manufacturing companies. \
You will perform deep research on the topic using the openai_tool agent and provide a detailed report."


MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

mistral_client = AsyncOpenAI(base_url=MISTRAL_BASE_URL, api_key=mistral_api_key)
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
openai_client = AsyncOpenAI(api_key=openai_api_key)

mistral_model = OpenAIChatCompletionsModel(model="mistral", openai_client=mistral_client)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)
openai_model = OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=openai_client)

# %%
research_agent1 = Agent(name="Mistral Research Agent", instructions=instructions1, model=mistral_model)
research_agent2 =  Agent(name="Gemini Research Agent", instructions=instructions2, model=gemini_model)
research_agent3  = Agent(name="OpenAI Research Agent",instructions=instructions3,model=openai_model)

# %%
description = "Write a cold sales email"

tool1 = research_agent1.as_tool(tool_name="research_agent1", tool_description=description)
tool2 = research_agent2.as_tool(tool_name="research_agent2", tool_description=description)
tool3 = research_agent3.as_tool(tool_name="research_agent3", tool_description=description)

# %%
@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("arun.gansi@gmail.com")  # Change to your verified sender
    to_email = To("arun.ganesan@prolim.com")  # Change to your recipient
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

# %%
subject_instructions = "You can write a subject for a cold sales email. \
You are given a message and you need to write a subject for an email that is likely to get a response."

html_instructions = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design."

subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model="gpt-4o-mini")
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model="gpt-4o-mini")
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

# %%
email_tools = [subject_tool, html_tool, send_html_email]

# %%
instructions ="You are an email formatter and sender. You receive the body of an email to be sent. \
You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. \
Finally, you use the send_html_email tool to send the email with the subject and HTML body."


emailer_agent = Agent(
    name="Email Manager",
    instructions=instructions,
    tools=email_tools,
    model="gpt-4o-mini",
    handoff_description="Convert an email to HTML and send it")

# %%
tools = [tool1, tool2, tool3]
handoffs = [emailer_agent]

# %%
sales_manager_instructions = """
You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
You can use the tools multiple times if you're not satisfied with the results from the first try.
 
3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must hand off exactly ONE email to the Email Manager — never more than one.
"""


sales_manager = Agent(
    name="Sales Manager",
    instructions=sales_manager_instructions,
    tools=tools,
    handoffs=handoffs,
    model="gpt-4o-mini")

message = "Send out a cold sales email addressed to Dear CEO from Alice"

with trace("Automated SDR"):
    result = await Runner.run(sales_manager, message)

# %% [markdown]
# ## Check out the trace:
# 
# https://platform.openai.com/traces

# %%
class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

guardrail_agent = Agent( 
    name="Name check",
    instructions="Check if the user is including someone's personal name in what they want you to do.",
    output_type=NameCheckOutput,
    model="gpt-4o-mini"
)

# %%
@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered=is_name_in_message)

# %%
careful_sales_manager = Agent(
    name="Sales Manager",
    instructions=sales_manager_instructions,
    tools=tools,
    handoffs=[emailer_agent],
    model="gpt-4o-mini",
    input_guardrails=[guardrail_against_name]
    )

message = "Send out a cold sales email addressed to Dear CEO from Alice"

with trace("Protected Automated SDR"):
    result = await Runner.run(careful_sales_manager, message)

# %% [markdown]
# ## Check out the trace:
# 
# https://platform.openai.com/traces

# %%

message = "Send out a cold sales email addressed to Dear CEO from Head of Business Development"

with trace("Protected Automated SDR"):
    result = await Runner.run(careful_sales_manager, message)

# %% [markdown]
# <table style="margin: 0; text-align: left; width:100%">
#     <tr>
#         <td style="width: 150px; height: 150px; vertical-align: middle;">
#             <img src="../assets/exercise.png" width="150" height="150" style="display: block;" />
#         </td>
#         <td>
#             <h2 style="color:#ff7800;">Exercise</h2>
#             <span style="color:#ff7800;">• Try different models<br/>• Add more input and output guardrails<br/>• Use structured outputs for the email generation
#             </span>
#         </td>
#     </tr>
# </table>

# %% [markdown]
# 


