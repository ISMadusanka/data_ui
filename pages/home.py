from h2o_wave import Q, ui
from utils.ui import add_card, clear_cards

# menu items
menu_items = [
    {
        'name': '',
        'title': 'Pandas',
        'caption': 'Pandas for basic csv',
        'icon': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-NEICv1aGTvDRncdvM_fXoah5SNWx4pXAvg&s'
    },
    {
        'name': '',
        'title': 'OpenCV',
        'caption': 'Opencv for image processing',
        'icon': 'Data'
    },
    {
        'name': '',
        'title': 'NumPy',
        'caption': 'NumPy for numerical computing',
        'icon': 'Data'
    },
    {
        'name': '',
        'title': 'PyPlot',
        'caption': 'PyPlot for data visualization',
        'icon': 'Data'
    }
]


async def homePage(q: Q):
    clear_cards(q)

    for item in menu_items:
        add_card(q, f'item{menu_items.index(item)}', ui.wide_info_card(
            box=ui.box('grid', width='400px'),
            name='',
            title=item['title'],
            caption=item['caption'],
            icon=item['icon']
        ))

    # for i in range(12):
    #     add_card(q, f'item{i}', ui.wide_info_card(
    #         box=ui.box('grid', width='400px'),
    #         name='',
    #         title='Tile',
    #         caption='Lorem ipsum dolor sit amet'
    #     ))