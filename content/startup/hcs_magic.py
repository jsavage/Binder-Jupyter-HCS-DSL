from IPython.core.magic import register_cell_magic
from IPython.display import display, HTML, Javascript

@register_cell_magic
def hcs(line, cell):
    mermaid_code = convert_hcs_to_mermaid(cell)
    html_output = f'''
    <div class="mermaid" id="mermaid-{id(cell)}">
    {mermaid_code}
    </div>
    '''
    js_code = f'''
    require.config({{
        paths: {{
            'mermaid': 'https://unpkg.com/mermaid@10/dist/mermaid.min'
        }}
    }});
    require(['mermaid'], function(mermaid) {{
        mermaid.initialize({{ startOnLoad: true }});
        mermaid.run();
    }});
    '''
    display(HTML(html_output))
    display(Javascript(js_code))
