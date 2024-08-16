from h2o_wave import ui

main_layout = ui.meta_card(box='', layouts=[ui.layout(
        breakpoint='xs', 
        min_height='100vh', 
        zones=[
            ui.zone('header'),
            ui.zone('content', zones=[
                ui.zone('horizontal', direction=ui.ZoneDirection.ROW),
                ui.zone('vertical'),
                ui.zone('grid', direction=ui.ZoneDirection.ROW, wrap='stretch', justify='center')
            ]),
        ]
    )])