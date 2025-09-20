import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager


load_dotenv(override=True)

async def run(query: str, to_email: str):
    async for chunk in ResearchManager().run(query, to_email):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    to_email_textbox = gr.Textbox(label="Pl provide your email", type="email")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")

    run_button.click(fn=run, inputs=[query_textbox, to_email_textbox], outputs=report)
    query_textbox.submit(fn=run, inputs=[query_textbox, to_email_textbox], outputs=report)

ui.launch(inbrowser=True)
