from ._anvil_designer import Company_newTemplate
from anvil import *
import stripe.checkout
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
import anvil.js

#############################################

from ..Product import Product
from ..BrandTone import BrandTone
from ..Avatars import Avatars
from ..VSL_Elements import VSL_Elements
from ..VideoSalesLetter import VideoSalesLetter
from ..FinalProduct import FinalProduct
####################


class Company_new(Company_newTemplate):
   def __init__(self, **properties):
    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    # Initialize counter
    anvil.users.login_with_form()
    self.indeterminate_company_research.visible = False
    self.free_navigate_label.visible = False
    self.status.text = 'Idle'

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Load the latest company profile
    row_company_profile_latest = user_table.search(variable='company_profile_latest')
    if row_company_profile_latest:
      company_profile_latest = row_company_profile_latest[0]['variable_value']
      self.company_profile_textbox.text = company_profile_latest
    else:
      # Handle case where the row does not exist for the current user
      print("No row found for 'company_profile_latest'")

    # Load the latest company name
    row_company_name = user_table.search(variable='company_name')
    if row_company_name:
      company_name = row_company_name[0]['variable_value']
      self.company_name_input.text = company_name

    # Load the latest company name
    row_company_url = user_table.search(variable='company_url')
    if row_company_url:
      company_url = row_company_url[0]['variable_value']
      self.company_url_input.text = company_url

    # Check if any of the final company profile is empty
    row_company_profile = user_table.search(variable='company_profile')
    if not row_company_profile:
      # If any of the company profiles are empty, disable the button
      self.nav_button_company_to_products.enabled = False
    else:
      # If all company profiles are saved, enable the button and navigate to the 'Products' form
      self.nav_button_company_to_products.enabled = True

    def form_show(self, **event_args):
      # Load the company profile on form show
      self.company_profile_textbox.load_data()
      self.company_name_input.load_data()
      self.company_url_input.load_data()
  
  
    def company_research_button_click(self, **event_args):
      with anvil.server.no_loading_indicator:
        # This method should handle the UI logic
        print("Research button clicked")
        # Start the progress bar with a small value
        count_timer = 0
        self.youtube_intro_video.visible = True
        # print("Before setting status:", self.status.text)
        # self.status.text = 'Researching'
        # print("After setting status:", self.status.text)
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        user_table = getattr(app_tables, user_table_name)
  
      # Check if either the company name or company URL input is empty
        if not self.company_name_input.text or not self.company_url_input.text:
          anvil.js.window.alert("Please fill out both the company name and company URL before proceeding")
        else:
          self.indeterminate_company_research.visible = True
          self.free_navigate_label.visible = True
          self.status.text = 'Researching'
  
          # Save company name
          company_name_row = user_table.get(variable='company_name')
          company_name_row['variable_value'] = self.company_name_input.text
          company_name_row.update()
          company_name = self.company_name_input.text
  
          # Save company URL
          company_url_row = user_table.get(variable='company_url')
          company_url_row['variable_value'] = self.company_url_input.text
          company_url_row.update()
          company_url = self.company_url_input.text
  
          # Launch the background task and store the task ID
          self.task_id = anvil.server.call('launch_company_summary', company_name, company_url)
          print("Task ID:", self.task_id)
  
          # # Call the function extract_my_brand_tone asynchronously
          # self.extract_my_brand_tone()
  
          # Loop to check the status of the background task
          while True:
  
            # Check if the background task is complete
            task_status = anvil.server.call('get_task_status', self.task_id)
            print("Task status:", task_status)
  
            if task_status is not None and task_status == "completed":
              # Get the result of the background task
              company_context = anvil.server.call('get_task_result', self.task_id)
              # Update the textbox with the result
              print("Company Context:", company_context)
              self.company_profile_textbox.text = company_context
  
              # Save this generated version as the latest version
              row_company_profile_latest = user_table.search(variable='company_profile_latest')
              row_company_profile_latest[0]['variable_value'] = company_context
              row_company_profile_latest[0].update()
  
              self.status.text = 'Complete'
              self.indeterminate_company_research.visible = False
              self.free_navigate_label.visible = False
              break  # Exit the loop
  
            # Sleep for 1 second before checking again
            time.sleep(2)
  
  
    def edit_company_profile_component_click(self, **event_args):
      self.company_profile_textbox.read_only = False
  
    def save_company_profile_component_click(self, **event_args):
      # Get the current user
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
  
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
  
      # Check if the company profile textbox is not empty and doesn't have the placeholder text
      if self.company_profile_textbox.text.strip() and self.company_profile_textbox.text.strip() != "AI agents will populate your company profile here!":
        company_profile_row = user_table.get(variable='company_profile')
        company_profile_row['variable_value'] = self.company_profile_textbox.text
        company_profile_row.update()
        self.nav_button_company_to_products.enabled = True
        self.nav_button_company_to_products.background = "#6750A4"  # Set the background color to green
        self.nav_button_company_to_products.foreground = "#1E192B"
  
        # Save this generated version as the latest version
        # Save company name
        company_name_row = user_table.get(variable='company_name')
        company_name_row['variable_value'] = self.company_name_input.text
        company_name_row.update()
        company_name = self.company_name_input.text
  
        # Save company URL
        company_url_row = user_table.get(variable='company_url')
        company_url_row['variable_value'] = self.company_url_input.text
        company_url_row.update()
        company_url = self.company_url_input.text
  
        row_company_profile_latest = user_table.search(variable='company_profile_latest')
        row_company_profile_latest[0]['variable_value'] = self.company_profile_textbox.text
        row_company_profile_latest[0].update()
        self.nav_button_company_to_products.enabled = True
      else:
        # Handle case where no profile name is selected
        anvil.js.window.alert("Please build your company profile before proceeding")
        self.nav_button_company_to_products.enabled = False
        self.nav_button_company_to_products.background = "#EADDFF"
  
  
    def load_company_profile_component_click(self, **event_args):
      # Get the current user
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
  
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
  
      company_profile_row = user_table.get(variable='company_profile')
  
      # Load the Company Profile from the profile row
      self.company_profile_textbox.text = company_profile_row['variable_value']
  
      # Load the Company Name and URL from the user_table
      company_name_row = user_table.get(variable='company_name')
      company_url_row = user_table.get(variable='company_url')