import os
import io
import pandas as pd
from h2o_wave import main, app, Q, ui, data
import numpy as np
import base64
import matplotlib.pyplot as plt
from utils.ui import add_card, clear_cards



async def pyplotPage(q: Q):
    clear_cards(q)

    add_card(q, 'upload', ui.form_card(
        box=ui.box('grid', width='400px'),
        items=[
            ui.file_upload(name='csv_file_pyplot', label='Upload a CSV file', multiple=False),
        ]
    ))

    await q.page.save()



async def handle_pyplot_upload(q: Q):
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)

    file_path = q.args.csv_file_pyplot[0]
    local_path = await q.site.download(file_path, upload_dir)

    with open(local_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    file_like = io.StringIO(file_content)
    df = pd.read_csv(file_like)
    q.client.df = df

    os.remove(local_path)

    add_card(q, 'result', ui.form_card(
        box=ui.box('grid', width='400px'),
        items=[
            ui.text(f'DataFrame uploaded with {len(df)} rows and {len(df.columns)} columns.'),
            ui.dropdown(name='plot_type', label='Select Plot Type', choices=[
                ui.choice(name='line', label='Line Plot'),
                ui.choice(name='scatter', label='Scatter Plot'),
                ui.choice(name='bar', label='Vertical Bar Plot'),
                ui.choice(name='barh', label='Horizontal Bar Plot'),
                ui.choice(name='hist', label='Histogram'),
                ui.choice(name='pie', label='Pie Chart'),
                ui.choice(name='boxplot', label='Box Plot'),
                ui.choice(name='violinplot', label='Violin Plot'),
                ui.choice(name='heatmap', label='Heatmap'),
                ui.choice(name='pcolor', label='Pseudocolor Plot'),
                ui.choice(name='pcolormesh', label='Pseudocolor Plot (with grid)'),
                ui.choice(name='contour', label='Contour Plot'),
                ui.choice(name='contourf', label='Filled Contour Plot'),
                ui.choice(name='surface', label='3D Surface Plot'),
                ui.choice(name='wireframe', label='3D Wireframe Plot'),
                ui.choice(name='scatter3d', label='3D Scatter Plot'),
                ui.choice(name='errorbar', label='Error Bar Plot'),
                ui.choice(name='stem', label='Stem Plot'),
                ui.choice(name='stackplot', label='Stack Plot'),
                ui.choice(name='quiver', label='Quiver Plot'),
                ui.choice(name='polar', label='Polar Plot'),
                ui.choice(name='semilogx', label='Logarithmic Plot (x-axis)'),
                ui.choice(name='semilogy', label='Logarithmic Plot (y-axis)'),
                ui.choice(name='loglog', label='Logarithmic Plot (both axes)'),
            ]),
            ui.button(name='plot', label='Next', primary=True),
        ]
    )
)
    


    await q.page.save()


# Line Plot
async def render_line_plot(q: Q, df: pd.DataFrame, col_x: str, col_y: str):
    add_card(q, 'plot',ui.plot_card(
        box=ui.box('sec_horizontal'),
        title='Line Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df[col_x], df[col_y])]),
        plot=ui.plot([ui.mark(type='line', x='=x', y='=y')])
    ))
    await q.page.save()

# Scatter Plot
async def render_scatter_plot(q: Q, df: pd.DataFrame, col_x: str, col_y: str):
    add_card(q, 'plot',ui.plot_card(
        box=ui.box('sec_horizontal'),
        title='Scatter Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df[col_x], df[col_y])]),
        plot=ui.plot([ui.mark(type='point', x='=x', y='=y')])
    ))
    await q.page.save()

# Bar Plot
async def render_bar_plot(q: Q, df: pd.DataFrame, col_x: str, col_y: str, vertical=True):
    x = '=x' if vertical else '=y'
    y = '=y' if vertical else '=x'
    title = 'Bar Plot' if vertical else 'Horizontal Bar Plot'
    add_card(q, 'plot',ui.plot_card(
        box=ui.box('sec_horizontal'),
        title=title,
        data=data('x y', len(df), rows=[(x_val, y_val) for x_val, y_val in zip(df[col_x], df[col_y])]),
        plot=ui.plot([ui.mark(type='interval', x=x, y=y)])
    ))
    await q.page.save()

# Pie Chart
async def render_pie_chart(q: Q, df: pd.DataFrame, col_label: str, col_value: str):
    pie_data = [(str(label), float(value)) for label, value in zip(df[col_label], df[col_value])]
    add_card(q, 'plot', ui.plot_card(
        box=ui.box('sec_horizontal'),
        title='Pie Chart',
        data=data('label value', len(pie_data), rows=pie_data),
        plot=ui.plot([ui.mark(type='arc', x='=value', color='=label')])
    ))
    await q.page.save()

# Histogram
async def render_histogram(q: Q, series: pd.Series):
    hist_data, bin_edges = np.histogram(series.dropna(), bins=10)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    add_card(q, 'plot', ui.text_card(
        box=ui.box('sec_horizontal'),
        title='Histogram',
        data=data('x y', len(bin_centers), rows=[(x, y) for x, y in zip(bin_centers, hist_data)]),
        plot=ui.plot([ui.mark(type='interval', x='=x', y='=y')])
    ))
    await q.page.save()

# Box Plot
async def render_box_plot(q: Q, series: pd.Series):
    fig, ax = plt.subplots()
    ax.boxplot(series.dropna())
    ax.set_title('Box Plot')
    fig_path = save_figure_as_base64(fig)
    add_card(q, 'plot',  ui.image_card(
        box=ui.box('sec_horizontal'),
        title='Box Plot',
        type='png',
        image=fig_path
    ))
    await q.page.save()

# Function to save Matplotlib figure as a base64 string
def save_figure_as_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return f'data:image/png;base64,{image_base64}'

# Special Plot for other plot types
async def render_special_plot(q: Q, df: pd.DataFrame, plot_type: str):
    fig, ax = plt.subplots()

    if plot_type == 'violinplot':
        ax.violinplot(df.select_dtypes(include='number').values, showmeans=False, showmedians=True)
        ax.set_title('Violin Plot')
    elif plot_type == 'heatmap':
        cax = ax.imshow(df.corr(), cmap='viridis', interpolation='nearest')
        fig.colorbar(cax)
        ax.set_title('Heatmap')
    elif plot_type == 'pcolor':
        ax.pcolor(df.select_dtypes(include='number').values, cmap='viridis')
        ax.set_title('Pseudocolor Plot')
    elif plot_type == 'pcolormesh':
        ax.pcolormesh(df.select_dtypes(include='number').values, cmap='viridis')
        ax.set_title('Pseudocolor Plot (with grid)')
    elif plot_type == 'contour':
        ax.contour(df.select_dtypes(include='number').values)
        ax.set_title('Contour Plot')
    elif plot_type == 'contourf':
        ax.contourf(df.select_dtypes(include='number').values)
        ax.set_title('Filled Contour Plot')
    elif plot_type == 'surface':
        from mpl_toolkits.mplot3d import Axes3D
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(range(df.shape[0]), range(df.shape[1]))
        ax.plot_surface(X, Y, df.select_dtypes(include='number').values)
        ax.set_title('3D Surface Plot')
    elif plot_type == 'wireframe':
        from mpl_toolkits.mplot3d import Axes3D
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(range(df.shape[0]), range(df.shape[1]))
        ax.plot_wireframe(X, Y, df.select_dtypes(include='number').values)
        ax.set_title('3D Wireframe Plot')
    elif plot_type == 'scatter3d':
        from mpl_toolkits.mplot3d import Axes3D
        ax = fig.add_subplot(111, projection='3d')
        x, y, z = df.select_dtypes(include='number').values.T
        ax.scatter(x, y, z)
        ax.set_title('3D Scatter Plot')
    elif plot_type == 'errorbar':
        ax.errorbar(df.index, df.iloc[:, 0], yerr=df.iloc[:, 1] if df.shape[1] > 1 else 0.1)
        ax.set_title('Error Bar Plot')
    elif plot_type == 'stem':
        ax.stem(df.index, df.iloc[:, 0])
        ax.set_title('Stem Plot')
    elif plot_type == 'stackplot':
        ax.stackplot(df.index, df.select_dtypes(include='number').values.T)
        ax.set_title('Stack Plot')
    elif plot_type == 'quiver':
        ax.quiver(df.index, df.iloc[:, 0], df.index, df.iloc[:, 1])
        ax.set_title('Quiver Plot')
    elif plot_type == 'polar':
        theta = np.linspace(0, 2. * np.pi, len(df))
        r = df.iloc[:, 0]
        ax.plot(theta, r)
        ax.set_title('Polar Plot')
    elif plot_type == 'semilogx':
        ax.semilogx(df.index, df.iloc[:, 0])
        ax.set_title('Logarithmic Plot (x-axis)')
    elif plot_type == 'semilogy':
        ax.semilogy(df.index, df.iloc[:, 0])
        ax.set_title('Logarithmic Plot (y-axis)')
    elif plot_type == 'loglog':
        ax.loglog(df.index, df.iloc[:, 0])
        ax.set_title('Logarithmic Plot (both axes)')

    fig_path = save_figure_as_base64(fig)
    add_card(q, 'plot',  ui.image_card(
        box=ui.box('sec_horizontal'),
        title=plot_type.title(),
        type='png',
        image=fig_path
    ))
    await q.page.save()



async def handle_plot(q: Q):
    df = q.client.df
    plot_type = q.client.plot_type
    col_x = q.args.column_x
    col_y = q.args.column_y if hasattr(q.args, 'column_y') else None

    if plot_type == 'line':
        await render_line_plot(q, df, col_x, col_y)
    elif plot_type == 'scatter':
        await render_scatter_plot(q, df, col_x, col_y)
    elif plot_type == 'bar':
        await render_bar_plot(q, df, col_x, col_y, vertical=True)
    elif plot_type == 'barh':
        await render_bar_plot(q, df, col_x, col_y, vertical=False)
    elif plot_type == 'hist':
        await render_histogram(q, df[col_x])
    elif plot_type == 'pie':
        await render_pie_chart(q, df, col_x, col_y)
    elif plot_type == 'boxplot':
        await render_box_plot(q, df[col_x])
    else:
        await render_special_plot(q, df, plot_type)
    await q.page.save()

async def select_columns_for_pyplot(q: Q):
    df = q.client.df
    plot_type = q.args.plot_type
    q.client.plot_type = plot_type

    if plot_type in ['line', 'scatter', 'bar', 'barh']:
        add_card(q, 'select_columns_for_pyplot', ui.form_card(
            box=ui.box('grid', width='400px'),
            items=[
                ui.dropdown(name='column_x', label='Select X-axis column', choices=[ui.choice(name=col, label=col) for col in df.columns]),
                ui.dropdown(name='column_y', label='Select Y-axis column', choices=[ui.choice(name=col, label=col) for col in df.columns]),
                ui.button(name='column_selection', label='Generate Plot', primary=True),
            ]
        ))
    elif plot_type in ['hist', 'boxplot']:
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        add_card(q, 'select_columns_for_pyplot', ui.form_card(
            box=ui.box('grid', width='400px'),
            items=[
                ui.dropdown(name='column_x', label=f'Select Column for {plot_type.title()}', choices=[ui.choice(name=col, label=col) for col in numeric_columns]),
                ui.button(name='column_selection', label='Generate Plot', primary=True),
            ]
        ))
    elif plot_type == 'pie':
        add_card(q, 'select_columns_for_pyplot', ui.form_card(
            box=ui.box('grid', width='400px'),
            items=[
                ui.dropdown(name='column_x', label='Select Label column', choices=[ui.choice(name=col, label=col) for col in df.columns]),
                ui.dropdown(name='column_y', label='Select Value column', choices=[ui.choice(name=col, label=col) for col in df.columns]),
                ui.button(name='column_selection', label='Generate Plot', primary=True),
            ]
        ))
       
    else:
        await handle_plot(q)  # For other plots that don't need column selection
    await q.page.save()


