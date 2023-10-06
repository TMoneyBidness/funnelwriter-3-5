from ._anvil_designer import BrandToneTemplate
from anvil import *
import time
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..VSL_Elements import VSL_Elements
############################################################################################################
# LOADING
class BrandTone(BrandToneTemplate):
  def __init__(self, **properties):
    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    self.brand_tone_dropdown.items = [(row['tone'], row) for row in app_tables.stock_tones.search()]
    self.indeterminate_brand_tone.visible = False
     # Set the click event handler for nav_button_tone_to_VSL_elements
    self.nav_button_tone_to_VSL_elements.set_event_handler('click', self.nav_button_tone_to_VSL_elements_click)

    #$
    self.home_form = None  # Initialize as None
    #$

    # WORKSPACE MANAGEMENT
    # Load the active workspace:
    self.load_active_workspace()
    # Get the User Table
    self.user_table = self.get_user_table()
    print(f"CURRENT USER TABLE IS: {self.user_table}")   

  # Load the latest brand tone
    brand_tone_url_row = self.user_table.search(variable='company_url')
    brand_tone_row = self.user_table.search(variable='brand_tone')
    if brand_tone_url_row:
        brand_tone_url = brand_tone_url_row[0]['variable_value']
        self.brand_tone_url_input.text = brand_tone_url
      
        brand_tone = brand_tone_row[0]['variable_value']
        self.brand_tone_textbox.text = brand_tone
        self.nav_button_tone_to_VSL_elements.enabled = True
    else:
        # Handle case where the row does not exist for the current user
        print("No row found for 'brand_tone_url'")
        self.nav_button_tone_to_VSL_elements.enabled = False
#$
  def set_home_form_reference(self, home_form):
    self.home_form = home_form
  #$
  
  def form_show(self, **event_args):
    # Load the brand tone profile on form show
    self.load_brand_tone_profile()

  def brand_tone_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Research button clicked")
      # Start the progress bar
      self.indeterminate_brand_tone.visible = True
      brand_tone_url = self.brand_tone_url_input.text
      
      # Get the current user 
      # current_user = anvil.users.get_user() 
      # user_table_name = current_user['user_id']
      # user_table = getattr(app_tables, user_table_name)
     
      # Save the brand tone URL
      brand_tone_url_latest_row = list(self.user_table.search(variable='brand_tone_url'))
      
      # Check if the row exists before updating it
      if brand_tone_url_latest_row:
          brand_tone_url_latest_row[0]['variable_value'] = brand_tone_url
          brand_tone_url_latest_row[0].update()
      
      self.task_id = anvil.server.call('launch_brand_tone_research', brand_tone_url)
      print("Task ID:", self.task_id)

     # Loop to check the status of the background task
    while True:
      with anvil.server.no_loading_indicator:
     
        # Check if the background task is complete
        task_status = anvil.server.call('get_task_status', self.task_id)
        print("Task status:", task_status)
  
        if task_status is not None:
          if task_status == "completed":
            # Get the result of the background task
            brand_tone_research = anvil.server.call('get_task_result', self.task_id)
            # Update the textbox with the result
            print("Brand Tone:", brand_tone_research  )
            self.brand_tone_textbox.text = brand_tone_research 
            self.indeterminate_brand_tone.visible = False
            break  # Exit the loop
          elif task_status == "failed":
            # Get the error message
            task_error = anvil.server.call('get_task_result', self.task_id)
            print("Task error:", task_error)
            self.indeterminate_brand_tone.visible = False
            break  # Exit the loop
  
        # Sleep for 1 second before checking again
        time.sleep(2)

  ########----------------- USER MANAGEMENT

  # def initialize_default_workspace(self):
  #   global active_workspace
  #   active_workspace = 'workspace_1'
  #   self.active_workspace = 'workspace_1'

  # def button_workspace_1_click(self, **event_args):
  #   global active_workspace
  #   active_workspace = 'workspace_1'
  #   self.reload_home_form()

  # def button_workspace_2_click(self, **event_args):
  #   global active_workspace
  #   active_workspace = 'workspace_2'
  #   self.reload_home_form()

  # def button_workspace_3_click(self, **event_args):
  #   global active_workspace
  #   active_workspace = 'workspace_3'
  #   self.reload_home_form()

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

########----------------- 
  
  def edit_brand_tone_component_click(self, **event_args):
    self.brand_tone_textbox.read_only = False

  def save_brand_tone_component_click(self, **event_args):
    brand_tone_title = anvil.js.window.prompt("What would you like to call this Brand Tone?")

    brand_tone = self.brand_tone_textbox.text
    
    brand_tone_lookup = "brand_tone"
    brand_tone_row = self.user_table.get(variable=brand_tone_lookup)
    
    # company_name_row = self.user_table.get(variable='company_name') # - THis saves it as the company name
    # brand_tone_title = company_name_row['variable_value'] 
    
    if brand_tone_row:
        brand_tone_row['variable_value'] = brand_tone
        if variable_title:
            brand_tone_row['variable_title'] = brand_tone_title
        brand_tone_row.update()
        self.nav_button_tone_to_VSL_elements.enabled = True
    else:
        # Handle case where the row does not exist for the current user
        print("No row found for the current user")
      
  
  def load_brand_tone_component_click(self, **event_args):
    # Get the current user
    # current_user = anvil.users.get_user()
    # user_table_name = current_user['user_id']
    # # Get the table for the current user
    # user_table = getattr(app_tables, user_table_name)

    # Get the profile row from the self.user_table
    profile_row = self.user_table.get(variable='brand_tone')

    # Check if the profile row exists
    if profile_row:
        self.brand_tone_textbox.text = profile_row['variable_value']
    else:
        # Handle case where the profile row does not exist
        print("No profile row found for the current user")

        
  def brand_tone_dropdown_change(self, **event_args):
    selected_row = self.brand_tone_dropdown.selected_value
    print("Selected Row:", selected_row)

    if selected_row:
        tone = selected_row['tone']
        print("Selected Tone:", tone)

        # Find the corresponding row in the stock_tones table
        stock_tone_row = app_tables.stock_tones.get(tone=tone)
        print("Stock Tone Row:", stock_tone_row)

        if stock_tone_row:
            value = stock_tone_row['value']
            print("Value:", value)
            self.brand_tone_textbox.text = value
        else:
            # Handle case where the row is not found in the stock_tones table
            self.brand_tone_textbox.text = "No value available"

  ###----------NAVIGATION---------------####

  # def nav_button_tone_to_VSL_elements(self, **event_args):
    
  #   vsl_elements = VSL_Elements()
  #   self.content_panel.clear()
  #   self.content_panel.add_component(vsl_elements)
    
  # Define the event handler for nav_button_tone_to_VSL_elements click
  def nav_button_tone_to_VSL_elements_click(self, **event_args):

    row_first_run_complete = self.user_table.get(variable='first_run_complete')
    row_first_run_complete['variable_value'] = 'Yes' 
    row_first_run_complete.update()

    self.update_company_assets_box_visibility()
    
    self.nav_button_tone_to_VSL_elements.enabled = True
  
    vsl_elements = VSL_Elements()
    self.content_panel.clear()
    self.content_panel.add_component(vsl_elements)

  def update_company_assets_box_visibility(self):
    if self.home_form:
        # Show the company_assets_box on the Home form sidebar
        self.home_form.company_assets_box.visible = True
    else:
        print("Home form reference is missing.")


    
  # def update_company_assets_box_visibility(self):
  #   user = anvil.users.get_user()

  #   if user:
  #       # Get the column name from the 'active_workspace' value
  #       workspace_column_name = user['active_workspace']
        
  #       # Use the column name to fetch the actual table name
  #       actual_table_name = user[workspace_column_name]
  #       workspace_table = getattr(app_tables, actual_table_name)

  #       # Retrieve the first (and likely only) row.
        
  #       first_run_row = workspace_table.search(variable='first_run_complete')
  #       should_display_box = first_run_row[0]['variable_value']
  #       if should_display_box == 'Yes':
  #           self.company_assets_box.visible = True
  #       else:
  #           self.company_assets_box.visible = False
  #   else:
  #       print("User not logged in or active_workspace not in user")  # Check if this gets printed



 # # BRAND TONE  
 #    # Get the stock tones from the stock_tones table
 #    stock_tones = [(row['tone'], row['tone']) for row in app_tables.stock_tones.search()]
    
 #    # Get the custom tones from the user table
 #    brand_tone_urls = user_table.search(variable='brand_tone')
 #    custom_tones = [(row['variable_title'], row['variable_title']) for row in brand_tone_urls]
    
 #    # Combine the stock tones and custom tones
 #    brand_tone_dropdown_items = stock_tones + custom_tones
    
 #    # Assign the values to the brand_tone_dropdown
 #    self.brand_tone_dropdown.items = brand_tone_dropdown_items
    
 #    self.indeterminate_brand_tone.visible = False
 #     # Set the click event handler for nav_button_tone_to_VSL_elements
 #    self.nav_button_tone_to_VSL_elements.set_event_handler('click', self.nav_button_tone_to_VSL_elements_click)


 #  # Load the latest brand tone
 #    brand_tone_url_row = user_table.search(variable='brand_tone_url')
 #    brand_tone_row = user_table.search(variable='brand_tone')
 #    if brand_tone_url_row:
 #        brand_tone_url = brand_tone_url_row[0]['variable_value']
 #        self.brand_tone_url_input.text = brand_tone_url
      
 #        brand_tone = brand_tone_row[0]['variable_value']
 #        self.brand_tone_textbox.text = brand_tone
 #        self.nav_button_tone_to_VSL_elements.enabled = True
 #    else:
 #        # Handle case where the row does not exist for the current user
 #        print("No row found for 'brand_tone_url'")
 #        self.nav_button_tone_to_VSL_elements.enabled = False

  







