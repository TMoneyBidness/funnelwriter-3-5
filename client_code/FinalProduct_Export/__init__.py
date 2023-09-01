from ._anvil_designer import FinalProduct_ExportTemplate
from anvil import *
import time
import json
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import tables

from ..VideoSalesLetter import VideoSalesLetter


############################################################################################################

PROMPT_TITLE = "FunnelWriter.AI needs a title to SAVE AS"

## LOADING
class FinalProduct_Export(FinalProduct_ExportTemplate):
  def __init__(self, **properties):
    # Find the example script
    anvil.users.login_with_form()

    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    # Initialize counter
   
    # Load stuff
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    final_headline_rows = user_table.search(variable='chosen_final_headline')
    self.main_headline_textbox.text = final_headline_rows[0]['variable_value']

    final_subheadline_rows = user_table.search(variable='chosen_final_subheadline')
    self.subheadline_textbox.text = final_subheadline_rows[0]['variable_value']

    secondary_headline_rows = user_table.search(variable='chosen_final_secondary_headline')
    self.secondary_headline_textbox.text = secondary_headline_rows[0]['variable_value']

    vsl_script_rows = user_table.search(variable='vsl_script')
    self.video_sales_script_textbox.text = vsl_script_rows[0]['variable_value']

    vsl_theme_1_rows = user_table.search(variable='vsl_theme_1')
    self.excerpt_textbox_1.text = vsl_theme_1_rows[0]['variable_value']

    vsl_theme_2_rows = user_table.search(variable='vsl_theme_2')
    self.excerpt_textbox_2.text = vsl_theme_2_rows[0]['variable_value']

    vsl_theme_3_rows = user_table.search(variable='vsl_theme_3')
    self.excerpt_textbox_3.text = vsl_theme_3_rows[0]['variable_value']

    vsl_theme_4_rows = user_table.search(variable='vsl_theme_4')
    self.excerpt_textbox_4.text = vsl_theme_4_rows[0]['variable_value']

