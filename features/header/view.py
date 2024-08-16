from h2o_wave import main, app, Q
from h2o_wave import ui

# def header(q:Q):
#     return (ui.header_card(
#     box='header',
#     title='Data Science UI',
#     subtitle="UI for Data Science with H2O Wave",
#     image='https://wave.h2o.ai/img/h2o-logo.svg',
#     secondary_items=[
#         ui.tabs(
#             name='tabs',
#             value=f'#{q.args["#"]}' if 'q' in locals() and q.args.get('#') else '#home',
#             link=True,
#             items=[
#                 ui.tab(name='#home', label='Home'),
#                 ui.tab(name='#pandas', label='Pandas'),
#                 ui.tab(name='#opencv', label='OpenCV'),
#                 ui.tab(name='#page4', label='Form'),
#             ]
#         ),
#     ],
#     items=[
#         # ui.persona(
#         #     title='John Doe',
#         #     subtitle='Developer',
#         #     size='xs',
#         #     image='https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
#         # ),
#     ]
#     ))


def header(q: Q):
    # Check if q.args exists and is a dictionary
    tab_value = '#home'  # Default to #home
    if q.args and isinstance(q.args, dict) and q.args.get('#'):
        tab_value = f'#{q.args["#"]}'

    return ui.header_card(
        box='header',
        title='Data Science UI',
        subtitle="UI for Data Science with H2O Wave",
        image='https://wave.h2o.ai/img/h2o-logo.svg',
        secondary_items=[
            ui.tabs(
                name='tabs',
                value=tab_value,
                link=True,
                items=[
                    ui.tab(name='#home', label='Home'),
                    ui.tab(name='#pandas', label='Pandas'),
                    ui.tab(name='#opencv', label='OpenCV'),
                    ui.tab(name='#page4', label='Form'),
                ]
            ),
        ],
        items=[
            # ui.persona(
            #     title='John Doe',
            #     subtitle='Developer',
            #     size='xs',
            #     image='https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
            # ),
        ]
    )
