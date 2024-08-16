from h2o_wave import main, app, Q, ui, on, run_on
import pandas as pd
import io
import os
from utils.ui import add_card, clear_cards

async def pandasPage(q: Q):
    clear_cards(q)

    if q.client.df is None or q.client.df.empty:  # Check if DataFrame is None or empty
        add_card(q, 'upload', ui.form_card(
            box=ui.box('grid', width='400px'),
            items=[
                ui.file_upload(name='csv_file', label='Upload a CSV file', multiple=False),
            ]
        ))
    else:
        df = q.client.df
        add_card(q, 'options', ui.form_card(
            box=ui.box('grid', width='400px'),
            items=[
                ui.text(f"DataFrame:\n{df.head().to_string()}"),
                ui.dropdown(name='operation', label='Choose operation', choices=[
                    ui.choice(name='head', label='View Head'),
                    ui.choice(name='tail', label='View Tail'),
                    ui.choice(name='describe', label='Describe'),
                ]),
                ui.button(name='perform', label='Perform Operation', primary=True),
            ]
        ))

        if q.args.perform:
            result = ""
            if q.args.operation == 'head':
                result = df.head().to_string()
            elif q.args.operation == 'tail':
                result = df.tail().to_string()
            elif q.args.operation == 'describe':
                result = df.describe().to_string()
            
            add_card(q, 'result', ui.form_card(
                box=ui.box('grid', width='400px'),
                items=[
                    ui.text(f"Result:\n{result}"),
                ]
            ))

    await q.page.save()




async def handle_upload(q: Q):
    if q.args.csv_file:
        try:
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)

            file_path = q.args.csv_file[0]
            local_path = await q.site.download(file_path, upload_dir)

            with open(local_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            file_like = io.StringIO(file_content)
            df = pd.read_csv(file_like)

            q.client.df = df

            os.remove(local_path)

            await pandasPage(q)

        except Exception as e:
            await show_error(q, f"Error loading CSV file: {str(e)}")

    else:
        await show_error(q, "No CSV file uploaded.")

async def show_error(q: Q, message: str):
    q.page['error'] = ui.form_card(
        box='grid',
        items=[ui.text(message)]
    )
    await q.page.save()

