from h2o_wave import main, app, Q, ui, on, run_on, data
from typing import Optional, List
from features.header.view import header
from layouts.main_layout import main_layout
from utils.ui import add_card, clear_cards
from pages.home import homePage
from pages.pandas import pandasPage
from pages.opencv import opencvPage
from pages.pyplot import pyplotPage
from pages.opencv import handle_image_upload
from pages.pandas import handle_pandas_upload
from pages.pandas import handle_pandas_operation
from pages.pandas import perform_pandas_operations
from pages.pyplot import select_columns_for_pyplot
from pages.pyplot import handle_plot
from pages.pyplot import handle_pyplot_upload


@on('#page1')
async def page1(q: Q):
    clear_cards(q)  # When routing, drop all the cards except the main ones (header, sidebar, meta).
    for i in range(3):
        add_card(q, f'info{i}', ui.tall_info_card(
            box='horizontal',
            name='',
            title='Speed',
            caption='The models are performant thanks to...',
            icon='SpeedHigh'
        ))
    add_card(q, 'article', ui.tall_article_preview_card(
        box=ui.box('vertical', height='600px'),
        title='How does magic work',
        image='https://images.pexels.com/photos/624015/pexels-photo-624015.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        content='''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac sodales felis. Duis orci enim, iaculis at augue vel, mattis imperdiet ligula. Sed a placerat lacus, vitae viverra ante...
        '''
    ))

@on('#pyplot')
async def pyplot(q: Q):
    await pyplotPage(q)


@on('#opencv')
async def opencv(q: Q):
    await opencvPage(q)


@on('#pandas')
async def pandas(q: Q):
    await pandasPage(q)
    

@on('#home')
async def home(q: Q):
    await homePage(q)


async def init(q: Q) -> None:
    #main layout
    q.page['meta'] = main_layout

    #header component
    hdr = header(q)
    q.page['header'] = hdr
    if q.args['#'] is None:
        await homePage(q)





@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        q.client.df = None
        q.client.cards = set()
        await init(q)
        q.client.initialized = True
    
    if q.args.image_file:
        await handle_image_upload(q)

    if q.args.csv_file:
        await handle_pandas_upload(q)
    if q.args.csv_file_pyplot:
        await handle_pyplot_upload(q)
    if q.args.plot_type:
        await select_columns_for_pyplot(q)
    if q.args.column_selection:
        await handle_plot(q)
    #pandas operations
    if q.args.apply_operation:
        await handle_pandas_operation(q)
    
    if await perform_pandas_operations(q):
        pass
    
    else:
        await run_on(q)
        
    await q.page.save()
