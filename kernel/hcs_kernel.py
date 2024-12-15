import re
from graphviz import Digraph

class HCSProcessor:
    def parse_hcs(self, input_text):
        entities = set()
        actions = []
        feedback = []
        nested_entities = {}

        lines = input_text.splitlines()

        for line in lines:
            line = line.strip()

            if ':' in line:
                entities_part, actions_part = line.split(':', 1)
                entities_part = entities_part.strip()
                actions_part = actions_part.strip()

                if '/' in actions_part:
                    actions_list, feedback_list = actions_part.split('/', 1)
                    actions_list = actions_list.strip().split()
                    feedback_list = feedback_list.strip().split()
                else:
                    actions_list = actions_part.split()
                    feedback_list = []

                entity_list = [e for e in re.split(r'\s+', entities_part) if e != '-']

                if len(entity_list) > 2:
                    raise ValueError(f"Expected exactly 2 entities before the colon, but got {entity_list}")

                controlling_entity, target_entity = map(str.strip, entity_list)
                entities.add(controlling_entity)
                entities.add(target_entity)

                for action in actions_list:
                    actions.append((controlling_entity, target_entity, action))

                for fb in feedback_list:
                    feedback.append((target_entity, controlling_entity, fb))

            elif '[' in line and ']' in line:
                main_entity, nested = re.match(r'(.*?)\[(.*)\]', line).groups()
                main_entity = main_entity.strip()
                nested_entities_list = nested.strip().split()

                entities.add(main_entity)
                nested_entities[main_entity] = nested_entities_list

                for ne in nested_entities_list:
                    entities.add(ne)

            else:
                entity_list = [e for e in re.split(r'\s+', line) if e != '-']
                for entity in entity_list:
                    entities.add(entity)

        return list(entities), actions, feedback, nested_entities

    def draw_hcs(self, entities, actions, feedback, nested_entities):
        dot = Digraph(format='svg')

        # Track which entities have already been drawn
        drawn_entities = set()

        # Draw top-level entities that are not nested within any other entity
        for entity in entities:
            if entity not in nested_entities and not any(entity in children for children in nested_entities.values()):
                dot.node(entity, shape='rectangle')
                drawn_entities.add(entity)

        # Draw nested entities within their parent entities
        for parent, children in nested_entities.items():
            if parent not in drawn_entities:
                with dot.subgraph(name=f'cluster_{parent}') as sub:
                    sub.attr(label=parent)
                    for child in children:
                        sub.node(child, shape='rectangle')
                        drawn_entities.add(child)
                drawn_entities.add(parent)

        # Draw actions (control) and feedback arrows
        for (src, tgt, action) in actions:
            dot.edge(src, tgt, label=action)

        for (src, tgt, fb) in feedback:
            dot.edge(src, tgt, label=fb, color='red')

        return dot.pipe().decode('utf-8')

    def process(self, dsl_input):
        entities, actions, feedback, nested = self.parse_hcs(dsl_input)
        return self.draw_hcs(entities, actions, feedback, nested)

def load_ipython_extension(ipython):
    """Register the %%hcs magic when the extension loads."""
    from IPython.core.magic import register_cell_magic
    
    @register_cell_magic
    def hcs(line, cell):
        processor = HCSProcessor()
        svg_output = processor.process(cell)
        from IPython.display import SVG, display
        display(SVG(svg_output))
