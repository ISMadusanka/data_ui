from h2o_wave import main, app, Q, ui
import pandas as pd
import io
import os

@app('/pandas_ui')
async def serve(q: Q):
    if not q.client.initialized:
        q.client.initialized = True
        q.client.df = None
        q.client.operation = None

        q.page['upload'] = ui.form_card(
            box='1 1 4 4',
            items=[
                ui.file_upload(name='csv_file', label='Upload a CSV file', multiple=False),
            ]
        )
        await q.page.save()

    if q.args.csv_file:
        # Handle file upload
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

        # Display the uploaded DataFrame and options for operations
        q.page['result'] = ui.form_card(
            box='5 1 4 2',
            items=[
                ui.text(f'DataFrame uploaded with {len(df)} rows and {len(df.columns)} columns.'),
                ui.dropdown(name='operation', label='Select Operation', choices=[
                    ui.choice(name='head', label='Show First N Rows'),
                    ui.choice(name='describe', label='Describe Data'),
                    ui.choice(name='sort', label='Sort by Column'),
                    ui.choice(name='filter', label='Filter Rows'),
                    ui.choice(name='groupby', label='Group by Column'),
                ]),
                ui.button(name='apply_operation', label='Apply Operation', primary=True),
            ]
        )
        await q.page.save()

    if q.args.apply_operation:
        q.client.operation = q.args.operation
        if q.client.operation == 'head':
            q.page['operation'] = ui.form_card(
                box='5 3 4 2',
                items=[
                    ui.textbox(name='n', label='Number of Rows to Display', value='5'),
                    ui.button(name='perform_head', label='Show Rows', primary=True),
                ]
            )
        elif q.client.operation == 'describe':
            df_describe = q.client.df.describe().reset_index()
            await display_dataframe(q, df_describe)
        elif q.client.operation == 'sort':
            q.page['operation'] = ui.form_card(
                box='5 3 4 2',
                items=[
                    ui.dropdown(name='sort_column', label='Select Column to Sort By', choices=[ui.choice(name=col, label=col) for col in q.client.df.columns]),
                    ui.toggle(name='ascending', label='Ascending', value=True),
                    ui.button(name='perform_sort', label='Sort', primary=True),
                ]
            )
        elif q.client.operation == 'filter':
            q.page['operation'] = ui.form_card(
                box='5 3 4 2',
                items=[
                    ui.dropdown(name='filter_column', label='Select Column to Filter By', choices=[ui.choice(name=col, label=col) for col in q.client.df.columns]),
                    ui.textbox(name='filter_value', label='Filter Value'),
                    ui.button(name='perform_filter', label='Filter', primary=True),
                ]
            )
        elif q.client.operation == 'groupby':
            q.page['operation'] = ui.form_card(
                box='5 3 4 2',
                items=[
                    ui.dropdown(name='group_column', label='Select Column to Group By', choices=[ui.choice(name=col, label=col) for col in q.client.df.columns]),
                    ui.button(name='perform_groupby', label='Group By', primary=True),
                ]
            )
        await q.page.save()

    if q.args.perform_head:
        n = int(q.args.n)
        df_head = q.client.df.head(n)
        await display_dataframe(q, df_head)

    if q.args.perform_sort:
        sort_column = q.args.sort_column
        ascending = q.args.ascending == 'True'
        df_sorted = q.client.df.sort_values(by=sort_column, ascending=ascending)
        await display_dataframe(q, df_sorted)

    if q.args.perform_filter:
        filter_column = q.args.filter_column
        filter_value = q.args.filter_value
        df_filtered = q.client.df[q.client.df[filter_column].astype(str) == filter_value]
        await display_dataframe(q, df_filtered)

    if q.args.perform_groupby:
        group_column = q.args.group_column
        df_grouped = q.client.df.groupby(group_column).size().reset_index(name='counts')
        await display_dataframe(q, df_grouped)

    if q.args.restart:
        q.client.initialized = False
        await serve(q)


async def display_dataframe(q: Q, df: pd.DataFrame):
    # Create table columns
    columns = [ui.table_column(name=col, label=col) for col in df.columns]

    # Create table rows
    rows = [ui.table_row(name=str(i), cells=[str(x) for x in row]) for i, row in df.iterrows()]

    # Show the DataFrame as a table
    q.page['data'] = ui.form_card(
        box='1 5 10 10',
        items=[
            ui.table(name='data_table', columns=columns, rows=rows, downloadable=True),
            ui.button(name='restart', label='Upload Another File', primary=True),
        ]
    )
    await q.page.save()
