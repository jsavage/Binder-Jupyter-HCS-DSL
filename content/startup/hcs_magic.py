from IPython.core.magic import register_cell_magic
from IPython.display import display, HTML

@register_cell_magic
def hcs(line, cell):
    mermaid_code = convert_hcs_to_mermaid(cell)
    html_output = f'''
    <script src="https://unpkg.com/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    <div class="mermaid">
    {mermaid_code}
    </div>
    '''
    display(HTML(html_output))

def convert_hcs_to_mermaid(hcs_input):
    mermaid_lines = ['graph TD', 'linkStyle default interpolate basis']
    feedback_count = 0
    total_links = 0
    
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
