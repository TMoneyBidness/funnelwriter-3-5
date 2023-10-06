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
import anvil.media

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
   
    # WORKSPACE MANAGEMENT
    # Load the active workspace:
    self.load_active_workspace()
    # Get the User Table
    self.user_table = self.get_user_table()
    print(f"CURRENT USER TABLE IS: {self.user_table}")

    final_headline_rows = self.user_table.search(variable='chosen_final_headline')
    self.main_headline_textbox.text = final_headline_rows[0]['variable_value']

    final_subheadline_rows = self.user_table.search(variable='chosen_final_subheadline')
    self.subheadline_textbox.text = final_subheadline_rows[0]['variable_value']

    secondary_headline_rows = self.user_table.search(variable='chosen_final_secondary_headline')
    self.secondary_headline_textbox.text = secondary_headline_rows[0]['variable_value']

    vsl_script_rows = self.user_table.search(variable='vsl_script')
    self.video_sales_script_textbox.text = vsl_script_rows[0]['variable_value']

    vsl_theme_1_rows = self.user_table.search(variable='vsl_theme_1')
    self.excerpt_textbox_1.text = vsl_theme_1_rows[0]['variable_value']

    vsl_theme_2_rows = self.user_table.search(variable='vsl_theme_2')
    self.excerpt_textbox_2.text = vsl_theme_2_rows[0]['variable_value']

    vsl_theme_3_rows = self.user_table.search(variable='vsl_theme_3')
    self.excerpt_textbox_3.text = vsl_theme_3_rows[0]['variable_value']

    vsl_theme_4_rows = self.user_table.search(variable='vsl_theme_4')
    self.excerpt_textbox_4.text = vsl_theme_4_rows[0]['variable_value']

########----------------- GENERATE A FINAL PDF
    
  # def download_VSL_pdf_click(self, **event_args):
  #   media_object = anvil.server.call('create_VSL_pdf',timeout=30)
  #   anvil.media.download(media_object)

  def generate_product_1_button_click(self, **event_args):
       
      # Reset the VSL Media Objectst
      vsl_script_row = self.user_table.search(variable='vsl_script')[0]
      vsl_script_row['variable_title'] = ""
      vsl_script_row.update()
      
        # COMPANY PROFILE
      company_name_row = self.user_table.search(variable='company_name')[0]
      company_name= company_name_row['variable_value']
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = self.user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
  
      # COMPANY URL
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_url_row = self.user_table.search(variable='company_url')[0]
      company_url = company_url_row['variable_value']
  
      # PRODUCT NAME
      product_name = self.product_1_name_input.text
      product_name_row = self.user_table.search(variable='product_1_name_latest')[0]
      product_name_row['variable_value'] = product_name
      product_name_row.update()

      # PRODUCT URL
      product_url = self.product_1_url_input.text
      product_url_row = self.user_table.get(variable=f"product_1_url")
      product_url_row['variable_value'] = product_url
      product_url_row.update()
          
      # PRODUCT EXCERPT / PREVIEW
      product_preview = self.product_profile_1_textbox.text
      # product_1_latest = self.product_profile_1_textbox.text
      product_preview_row = self.user_table.search(variable='product_1_preview')[0]
      product_preview_row['variable_value'] = product_preview
      product_preview_row.update()
      
      # Start the Check Status Timers
      self.check_status_timer_product_1.enabled = True
      self.check_status_timer_product_1.interval = 3
      
      self.task_id = anvil.server.call('launch_deepdive_product_1_generator',self.user_table,company_name,product_name,product_url,product_preview)
      print("Task ID:", self.task_id)
   
  def check_status_product_1_summary(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        # current_user = anvil.users.get_user()
        # user_table_name = current_user['user_id']
        # # Get the table for the current user
        # user_table = getattr(app_tables, user_table_name)
        row = self.user_table.get(variable='product_1_latest')
     
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on the Product Summary!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Product Summary Generated!")
            self.check_status_timer_product_1.enabled = False
            self.check_status_timer_product_1.interval = 0
                          
            # Update the box
            self.product_profile_1_textbox.text = row['variable_value']
            self.indeterminate_1.visible = False
  


 

    
########----------------- USER MANAGEMENT

  def initialize_default_workspace(self):
    global active_workspace
    active_workspace = 'workspace_1'
    self.active_workspace = 'workspace_1'

  def button_workspace_1_click(self, **event_args):
    global active_workspace
    active_workspace = 'workspace_1'
    self.reload_home_form()

  def button_workspace_2_click(self, **event_args):
    global active_workspace
    active_workspace = 'workspace_2'
    self.reload_home_form()

  def button_workspace_3_click(self, **event_args):
    global active_workspace
    active_workspace = 'workspace_3'
    self.reload_home_form()

  def get_user_table(self):
    current_user = anvil.users.get_user()
    global active_workspace
    workspace_id = self.get_active_workspace()
    user_table_name = current_user[workspace_id]
    return getattr(app_tables, user_table_name)

  def set_active_workspace(self, workspace_id):
    """Set the active workspace for the current session."""
    anvil.server.session['active_workspace'] = workspace_id

  def get_active_workspace(self):
    global active_workspace
    return active_workspace

  def load_active_workspace(self):
    global active_workspace
    # Get the active workspace from the user's table
    current_user = anvil.users.get_user()
    active_workspace = current_user['active_workspace']
    # Update the global variable
    self.active_workspace = active_workspace