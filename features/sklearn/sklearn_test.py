from h2o_wave import main, app, Q, ui
import pandas as pd
import io
import os

@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        await render_upload_form(q)
        q.client.initialized = True
    elif q.args.csv_file:
        await handle_file_upload(q)
    elif q.args.apply_operation:
        await handle_operation(q)
    elif q.args.restart:
        q.client.initialized = False
        await render_upload_form(q)
    await q.page.save()

async def render_upload_form(q: Q):
    q.page['upload'] = ui.form_card(
        box='1 1 4 4',
        items=[
            ui.file_upload(name='csv_file', label='Upload a CSV file', multiple=False),
            ui.text_l("Please upload a CSV file to proceed."),
        ]
    )
    await q.page.save()

async def handle_file_upload(q: Q):
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

    q.page['result'] = ui.form_card(
        box='1 3 4 4',
        items=[
            ui.text(f'DataFrame uploaded with {len(df)} rows and {len(df.columns)} columns.'),
            ui.dropdown(name='operation', label='Select Operation', choices=[
                ui.choice(name='scale_standard', label='Standard Scaling'),
                ui.choice(name='scale_minmax', label='Min-Max Scaling'),
                ui.choice(name='impute', label='Impute Missing Values'),
                ui.choice(name='onehot', label='One-Hot Encoding'),
                ui.choice(name='normalize', label='Normalize Data'),
                ui.choice(name='binarize', label='Binarize Data'),
                ui.choice(name='polynomial_features', label='Generate Polynomial Features'),
                ui.choice(name='remove_outliers', label='Remove Outliers'),
                ui.choice(name='show_outliers', label='Show Outliers'),
            ]),
            ui.button(name='apply_operation', label='Apply Operation', primary=True),
        ]
    )
    await q.page.save()

async def handle_operation(q: Q):
    df = q.client.df

    if q.args.operation == 'scale_standard':
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df.select_dtypes(include=['float64', 'int64']))
        df_scaled = pd.DataFrame(scaled_data, columns=df.select_dtypes(include=['float64', 'int64']).columns)
        await display_dataframe(q, df_scaled)
    
    elif q.args.operation == 'scale_minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df.select_dtypes(include=['float64', 'int64']))
        df_scaled = pd.DataFrame(scaled_data, columns=df.select_dtypes(include=['float64', 'int64']).columns)
        await display_dataframe(q, df_scaled)
    
    elif q.args.operation == 'impute':
        from sklearn.impute import SimpleImputer
        imputer = SimpleImputer(strategy='mean')
        imputed_data = imputer.fit_transform(df.select_dtypes(include=['float64', 'int64']))
        df_imputed = pd.DataFrame(imputed_data, columns=df.select_dtypes(include=['float64', 'int64']).columns)
        await display_dataframe(q, df_imputed)
    
    elif q.args.operation == 'onehot':
        from sklearn.preprocessing import OneHotEncoder
        encoder = OneHotEncoder(sparse=False)
        encoded_data = encoder.fit_transform(df.select_dtypes(include=['object']))
        df_encoded = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(df.select_dtypes(include=['object']).columns))
        await display_dataframe(q, df_encoded)

    elif q.args.operation == 'normalize':
        from sklearn.preprocessing import Normalizer
        normalizer = Normalizer()
        normalized_data = normalizer.fit_transform(df.select_dtypes(include=['float64', 'int64']))
        df_normalized = pd.DataFrame(normalized_data, columns=df.select_dtypes(include=['float64', 'int64']).columns)
        await display_dataframe(q, df_normalized)

    elif q.args.operation == 'binarize':
        from sklearn.preprocessing import Binarizer
        binarizer = Binarizer()
        binarized_data = binarizer.fit_transform(df.select_dtypes(include=['float64', 'int64']))
        df_binarized = pd.DataFrame(binarized_data, columns=df.select_dtypes(include=['float64', 'int64']).columns)
        await display_dataframe(q, df_binarized)
    
    elif q.args.operation == 'polynomial_features':
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree=2)
        poly_features = poly.fit_transform(df.select_dtypes(include=['float64', 'int64']))
        df_poly = pd.DataFrame(poly_features, columns=poly.get_feature_names_out(df.select_dtypes(include=['float64', 'int64']).columns))
        await display_dataframe(q, df_poly)

    elif q.args.operation == 'remove_outliers':
        from sklearn.ensemble import IsolationForest
        iso_forest = IsolationForest(contamination=0.1)
        numeric_data = df.select_dtypes(include=['float64', 'int64'])
        preds = iso_forest.fit_predict(numeric_data)
        df_no_outliers = df[(preds != -1)]
        await display_dataframe(q, df_no_outliers)
    
    elif q.args.operation == 'show_outliers':
        from sklearn.ensemble import IsolationForest
        iso_forest = IsolationForest(contamination=0.1)
        numeric_data = df.select_dtypes(include=['float64', 'int64'])
        preds = iso_forest.fit_predict(numeric_data)
        df_outliers = df[(preds == -1)]
        await display_dataframe(q, df_outliers)

    await q.page.save()

async def display_dataframe(q: Q, df: pd.DataFrame):
    columns = [ui.table_column(name=col, label=col) for col in df.columns]
    rows = [ui.table_row(name=str(i), cells=[str(x) for x in row]) for i, row in df.iterrows()]

    q.page['data'] = ui.form_card(
        box='1 5 10 10',
        items=[
            ui.table(name='data_table', columns=columns, rows=rows, downloadable=True),
            ui.button(name='restart', label='Upload Another File', primary=True),
        ]
    )
    await q.page.save()
