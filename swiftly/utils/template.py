import os
import inspect
from jinja2 import Environment, FileSystemLoader

def render_template(template_filename, data):
    """
    Renders a template using Jinja2 from a 'templates' folder in the calling script's directory.

    Parameters:
    - template_filename (str): Name of the template file inside the 'templates' folder.
    - data (dict): Dictionary containing the data to replace in the template.

    Returns:
    - str: Rendered content as a string.
    """

    # Get the directory of the calling script
    calling_script_dir = os.path.dirname(os.path.abspath(inspect.stack()[1].filename))

    # Construct the path to the 'templates' folder
    templates_folder_path = os.path.join(calling_script_dir, 'templates')

    # Set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_folder_path))

    # Load the template
    template = env.get_template(template_filename)

    # Render the template with the provided data
    rendered_content = template.render(data)

    return rendered_content

# Example usage:
# rendered_content = render_template_from_templates_folder('template.txt', {'name': 'John'})
# print(rendered_content)
