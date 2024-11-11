def load_run_from_reduction_table(window_main, row: int, col: int, run: str):
    """Add run number in reduction table cell and press Enter to load a run"""
    window_main.ui.reductionTable.setCurrentCell(row, col)
    window_main.ui.reductionTable.currentItem().setText(run)
    window_main.ui.table_reduction_cell_enter_pressed()
