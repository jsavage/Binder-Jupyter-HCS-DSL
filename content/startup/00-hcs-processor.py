from IPython.core.magic import register_cell_magic
from IPython.display import display, HTML

def initialize_mermaid():
    return HTML("""
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>
    """)

initialize_mermaid()

def convert_hcs_to_mermaid(hcs_input):
    mermaid_lines = ['graph TD', 'linkStyle default interpolate basis']
    feedback_count = 0
    total_links = 0
    
    # Extract subgraph components from DSL
    for line in hcs_input.splitlines():
        if '[' in line and ']' in line:
            parent, children = line.split('[')
            children = children.rstrip(']').strip()
            components = children.split()
            # Create subgraph
            mermaid_lines.append(f'subgraph {parent.strip()}')
            for comp in components:
                mermaid_lines.append(f'    {comp}[{comp}]')
            mermaid_lines.append('end')
    
    # Process relationships
    for line in hcs_input.splitlines():
        if ':' in line:
            entities_part, actions = line.split(':', 1)
            source, target = [e.strip() for e in entities_part.split()]
            actions = actions.strip()
            if source == 'Person':
                source = 'Person([Person])'
            if actions:
                if '/' in actions:
                    actions_list, feedback = actions.split('/', 1)
                    if actions_list.strip():
                        actions_list = actions_list.strip().split(',')
                        for action in actions_list:
                            if action.strip():
                                mermaid_lines.append(f'{source}-->|{action.strip()}|{target}')
                                total_links += 1
                    if feedback.strip():
                        feedback_list = feedback.strip().split(',')
                        for fb in feedback_list:
                            if fb.strip():
                                mermaid_lines.append(f'{target}-->|{fb.strip()}|{source}')
                                mermaid_lines.append(f'linkStyle {total_links} stroke:#ff0000,color:#ff0000')
                                total_links += 1
                else:
                    actions_list = actions.strip().split(',')
                    for action in actions_list:
                        if action.strip():
                            mermaid_lines.append(f'{source}-->|{action.strip()}|{target}')
                            total_links += 1
    
    return '\n'.join(mermaid_lines)

@register_cell_magic
def hcs(line, cell):
    mermaid_code = convert_hcs_to_mermaid(cell)
    display(HTML(f'<div class="mermaid">\n{mermaid_code}\n</div>'))
