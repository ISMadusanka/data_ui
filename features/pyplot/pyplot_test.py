import os
import io
import pandas as pd
from h2o_wave import main, app, Q, ui, data
import numpy as np

@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        await render_upload_form(q)
        q.client.initialized = True
    elif q.args.csv_file:
        await handle_file_upload(q)
    elif q.args.plot_type:
        await handle_plot(q)
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
            ui.button(name='plot', label='Generate Plot', primary=True),
        ]
    )
    await q.page.save()

async def handle_plot(q: Q):
    df = q.client.df
    plot_type = q.args.plot_type

    if plot_type == 'line':
        await render_line_plot(q, df)
    elif plot_type == 'scatter':
        await render_scatter_plot(q, df)
    elif plot_type == 'bar':
        await render_bar_plot(q, df, vertical=True)
    elif plot_type == 'barh':
        await render_bar_plot(q, df, vertical=False)
    elif plot_type == 'hist':
        await render_histogram(q, df)
    elif plot_type == 'pie':
        await render_pie_chart(q, df)
    elif plot_type == 'boxplot':
        await render_box_plot(q, df)
    elif plot_type == 'violinplot':
        await render_violin_plot(q, df)
    elif plot_type == 'heatmap':
        await render_heatmap(q, df)
    elif plot_type == 'pcolor':
        await render_pcolor(q, df)
    elif plot_type == 'pcolormesh':
        await render_pcolormesh(q, df)
    elif plot_type == 'contour':
        await render_contour_plot(q, df)
    elif plot_type == 'contourf':
        await render_filled_contour_plot(q, df)
    elif plot_type == 'surface':
        await render_surface_plot(q, df)
    elif plot_type == 'wireframe':
        await render_wireframe_plot(q, df)
    elif plot_type == 'scatter3d':
        await render_scatter3d_plot(q, df)
    elif plot_type == 'errorbar':
        await render_error_bar_plot(q, df)
    elif plot_type == 'stem':
        await render_stem_plot(q, df)
    elif plot_type == 'stackplot':
        await render_stack_plot(q, df)
    elif plot_type == 'quiver':
        await render_quiver_plot(q, df)
    elif plot_type == 'polar':
        await render_polar_plot(q, df)
    elif plot_type == 'semilogx':
        await render_semilogx_plot(q, df)
    elif plot_type == 'semilogy':
        await render_semilogy_plot(q, df)
    elif plot_type == 'loglog':
        await render_loglog_plot(q, df)

# Line Plot
async def render_line_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Line Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='line', x='=x', y='=y')])
    )
    await q.page.save()

# Scatter Plot
async def render_scatter_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Scatter Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='point', x='=x', y='=y')])
    )
    await q.page.save()

# Bar Plot
async def render_bar_plot(q: Q, df: pd.DataFrame, vertical=True):
    # Determine the x and y values based on the orientation of the plot
    x = '=x' if vertical else '=y'
    y = '=y' if vertical else '=x'
    
    # Set the title based on the orientation
    title = 'Bar Plot' if vertical else 'Horizontal Bar Plot'
    
    # Create the plot card
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title=title,
        data=data('x y', len(df), rows=[(x_val, y_val) for x_val, y_val in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='interval', x=x, y=y)])
    )
    
    # Save the page
    await q.page.save()


async def render_histogram(q: Q, df: pd.DataFrame):
    # Calculate histogram data
    counts, bin_edges = np.histogram(df.iloc[:, 0], bins='auto')

    # Prepare the data in the format required by h2o_wave
    histogram_data = [(counts[i], bin_edges[i], bin_edges[i + 1]) for i in range(len(counts))]

    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Histogram',
        data=data('frequency low high', len(histogram_data), rows=histogram_data),
        plot=ui.plot([ui.mark(type='interval', y='=frequency', x1='=low', x2='=high', y_min=0)])
    )
    await q.page.save()


# Pie Chart
async def render_pie_chart(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Pie Chart',
        data=data('category value', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='arc', x='=value', color='=category', y='=sum(value)', stroke='white')])
    )
    await q.page.save()

# Box Plot
async def render_box_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Box Plot',
        data=data('x', len(df), rows=[(x,) for x in df.iloc[:, 0]]),
        plot=ui.plot([ui.mark(type='box', x='=x', y='=y', y_min=0)])
    )
    await q.page.save()

# Violin Plot
async def render_violin_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Violin Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='violin', x='=x', y='=y')])
    )
    await q.page.save()

# Heatmap
async def render_heatmap(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Heatmap',
        data=data('x y value', len(df), rows=[(x, y, v) for x, y, v in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])]),
        plot=ui.plot([ui.mark(type='rect', x='=x', y='=y', color='=value')])
    )
    await q.page.save()

# Pseudocolor Plot
async def render_pcolor(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Pseudocolor Plot',
        data=data('x y value', len(df), rows=[(x, y, v) for x, y, v in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])]),
        plot=ui.plot([ui.mark(type='rect', x='=x', y='=y', color='=value')])
    )
    await q.page.save()

# Pseudocolor Plot (with grid)
async def render_pcolormesh(q: Q, df: pd.DataFrame):
    await render_pcolor(q, df)

# Contour Plot
async def render_contour_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Contour Plot',
        data=data('x y value', len(df), rows=[(x, y, v) for x, y, v in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])]),
        plot=ui.plot([ui.mark(type='line', x='=x', y='=y', color='=value')])
    )
    await q.page.save()

# Filled Contour Plot
async def render_filled_contour_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Filled Contour Plot',
        data=data('x y value', len(df), rows=[(x, y, v) for x, y, v in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])]),
        plot=ui.plot([ui.mark(type='area', x='=x', y='=y', color='=value')])
    )
    await q.page.save()

# 3D Surface Plot
async def render_surface_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='3D Surface Plot',
        data=data('x y value', len(df), rows=[(x, y, v) for x, y, v in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])]),
        plot=ui.plot([ui.mark(type='area', x='=x', y='=y', color='=value')])
    )
    await q.page.save()

# 3D Wireframe Plot
async def render_wireframe_plot(q: Q, df: pd.DataFrame):
    await render_surface_plot(q, df)

# 3D Scatter Plot
async def render_scatter3d_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='3D Scatter Plot',
        data=data('x y z', len(df), rows=[(x, y, z) for x, y, z in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])]),
        plot=ui.plot([ui.mark(type='point', x='=x', y='=y', color='=z')])
    )
    await q.page.save()

# Error Bar Plot
async def render_error_bar_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Error Bar Plot',
        data=data('x y error', len(df), rows=[(x, y, err) for x, y, err in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])]),
        plot=ui.plot([ui.mark(type='interval', x='=x', y='=y', y0='=y-error', y1='=y+error')])
    )
    await q.page.save()

# Stem Plot
async def render_stem_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Stem Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='rule', x='=x', y0=0, y1='=y')])
    )
    await q.page.save()

# Stack Plot
async def render_stack_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Stack Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='area', x='=x', y='=y', stack='auto')])
    )
    await q.page.save()

# Quiver Plot
async def render_quiver_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Quiver Plot',
        data=data('x y u v', len(df), rows=[(x, y, u, v) for x, y, u, v in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, 3])]),
        plot=ui.plot([ui.mark(type='vector', x='=x', y='=y', x1='=u', y1='=v')])
    )
    await q.page.save()

# Polar Plot
async def render_polar_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Polar Plot',
        data=data('angle radius', len(df), rows=[(theta, r) for theta, r in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='line', x='=angle', y='=radius', coord='polar')])
    )
    await q.page.save()

# Logarithmic Plot (x-axis)
async def render_semilogx_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Semilogx Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='line', x='=log(x)', y='=y')])
    )
    await q.page.save()

# Logarithmic Plot (y-axis)
async def render_semilogy_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Semilogy Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='line', x='=x', y='=log(y)')])
    )
    await q.page.save()

# Logarithmic Plot (both axes)
async def render_loglog_plot(q: Q, df: pd.DataFrame):
    q.page['plot'] = ui.plot_card(
        box='1 5 4 4',
        title='Loglog Plot',
        data=data('x y', len(df), rows=[(x, y) for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])]),
        plot=ui.plot([ui.mark(type='line', x='=log(x)', y='=log(y)')])
    )
    await q.page.save()
