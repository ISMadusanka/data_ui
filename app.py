from h2o_wave import main, app, Q, ui, on, run_on, data
from typing import Optional, List
from features.header.view import header
from layouts.main_layout import main_layout
from utils.ui import add_card, clear_cards
from pages.home import homePage
from pages.pandas import pandasPage
from pages.pandas import handle_upload


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
    q.page['header'] = header
    if q.args['#'] is None:
        await homePage(q)





@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        q.client.df = None
        q.client.cards = set()
        await init(q)
        q.client.initialized = True
        
    if q.args.csv_file:
        await handle_upload(q)
    else:
        await run_on(q)
        
    await q.page.save()
