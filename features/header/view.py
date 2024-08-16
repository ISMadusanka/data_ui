from h2o_wave import ui

header = ui.header_card(
    box='header',
    title='My app',
    subtitle="Let's conquer the world",
    image='https://wave.h2o.ai/img/h2o-logo.svg',
    secondary_items=[
        ui.tabs(
            name='tabs',
            value=f'#{q.args["#"]}' if 'q' in locals() and q.args.get('#') else '#home',
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
        ui.persona(
            title='John Doe',
            subtitle='Developer',
            size='xs',
            image='https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        ),
    ]
)
