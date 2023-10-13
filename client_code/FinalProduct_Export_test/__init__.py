from ._anvil_designer import FinalProduct_Export_testTemplate
from anvil import *
import stripe.checkout
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
class FinalProduct_Export_test(FinalProduct_Export_testTemplate):
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


  def download_vsl_pdf_click(self, **event_args):
    print("download_vsl_pdf_click has been clicked!")

    # Reset the VSL Media Objectst
    vsl_script_row = self.user_table.search(variable='vsl_script')[0]
    vsl_script_row['variable_title'] = ""
    vsl_script_row.update()

    self.task_id = anvil.server.call('launch_download_vsl_pdf',self.user_table)
    print("Server side VSL function launch function called! Task_ID =", self.task_id)

    # Start the Check Status Timers
    self.check_status_download_pdf_timer.enabled = True
    self.check_status_download_pdf_timer.interval = 3


  def check_status_download_pdf(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
      row = self.user_table.get(variable='vsl_script')

      if row['variable_title'] is None or row['variable_title'] == '':
        print("Still working on Generating the PDF!")
      elif row['variable_title'] is not None and row['variable_title'] != '':
        print("PDF VSL Format Generated!")
        self.check_status_download_pdf_timer.enabled = False
        self.check_status_download_pdf_timer.interval = 0

        # Launch the downloader
        self.download_VSL_pdf()

  def download_VSL_pdf(self, **event_args):
    row = self.user_table.get(variable='vsl_script')
    media_object = row['variable_title']
    anvil.media.download(media_object)



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
