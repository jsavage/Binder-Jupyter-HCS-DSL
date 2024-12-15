from IPython.core.magic import register_cell_magic

@register_cell_magic
def hcs(line, cell):
    processor = HCSProcessor()
    svg_output = processor.process(cell)
    display(SVG(svg_output))
