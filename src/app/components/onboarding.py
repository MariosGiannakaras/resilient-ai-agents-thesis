"""Small self-explanatory onboarding surface for the NiceGUI application."""
from __future__ import annotations

from nicegui import ui


STEPS = (
    (
        "Dashboard",
        "See real workspace state, finalized experiments, protocol status and current machine resources.",
    ),
    (
        "New Experiment",
        "Choose among Fixed Q-Learning, Adaptive Q-Learning, SARSA, Dyna-Q and Dyna-Q+. Only protocol-approved layouts, conditions, repetitions and settings are available, and a plain-language resolved request is reviewed before launch.",
    ),
    (
        "Runs",
        "Watch truthful active-run status, the live GridWorld observer, provisional telemetry and lifecycle controls that the runtime can actually honor. Finalized history remains separate.",
    ),
    (
        "Compare",
        "Compare compatible stored evidence with distributions, counts and layout/condition breakdowns. Paired effects or confidence intervals appear only when the stored evidence actually contains them.",
    ),
    (
        "Artifacts",
        "Inspect and export stored figures, tables and manifests with provenance. Screenshots are presentation artifacts; scientific results remain the underlying versioned evidence.",
    ),
)


def open_onboarding() -> None:
    """Open a skippable in-app guide without mutating scientific state."""
    dialog = ui.dialog()
    state = {"index": 0}
    with dialog, ui.card().classes('w-[680px] max-w-[92vw] rounded-2xl p-5'):
        with ui.row().classes('w-full items-start'):
            with ui.column().classes('gap-0'):
                ui.label('Application guide').classes('text-xl font-semibold')
                ui.label('Five surfaces, one evidence boundary').classes('text-sm text-slate-500')
            ui.space()
            ui.button(icon='close', on_click=dialog.close).props('flat round dense')

        progress = ui.linear_progress(value=1 / len(STEPS)).props('rounded')
        step_label = ui.label().classes('text-xs text-primary font-semibold uppercase tracking-wide')
        title = ui.label().classes('text-lg font-semibold')
        body = ui.label().classes('text-sm leading-relaxed text-slate-600')

        def render() -> None:
            index = state['index']
            name, text = STEPS[index]
            step_label.set_text(f'Step {index + 1} of {len(STEPS)}')
            title.set_text(name)
            body.set_text(text)
            progress.set_value((index + 1) / len(STEPS))
            previous.set_enabled(index > 0)
            next_button.set_text('Finish' if index == len(STEPS) - 1 else 'Next')

        def go_previous() -> None:
            state['index'] = max(0, state['index'] - 1)
            render()

        def go_next() -> None:
            if state['index'] >= len(STEPS) - 1:
                dialog.close()
                return
            state['index'] += 1
            render()

        with ui.row().classes('w-full items-center mt-3'):
            ui.button('Skip', on_click=dialog.close).props('flat no-caps')
            ui.space()
            previous = ui.button('Previous', on_click=go_previous).props('outline no-caps')
            next_button = ui.button('Next', on_click=go_next).props('unelevated no-caps color=primary')

        render()
    dialog.open()
