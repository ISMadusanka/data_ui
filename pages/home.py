from h2o_wave import Q, ui
from utils.ui import add_card, clear_cards

async def homePage(q: Q):
    clear_cards(q)
    for i in range(12):
        add_card(q, f'item{i}', ui.wide_info_card(
            box=ui.box('grid', width='400px'),
            name='',
            title='Tile',
            caption='Lorem ipsum dolor sit amet'
        ))