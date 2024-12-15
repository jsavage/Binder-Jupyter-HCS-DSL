from IPython.core.magic import register_cell_magic
from IPython.display import display, HTML

@register_cell_magic
def hcs(line, cell):
    mermaid_code = convert_hcs_to_mermaid(cell)
    html_output = f'''
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    <div class="mermaid">
    {mermaid_code}
    </div>
    '''
    display(HTML(html_output))
