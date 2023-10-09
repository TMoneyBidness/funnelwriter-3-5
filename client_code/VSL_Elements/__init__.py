from ._anvil_designer import VSL_ElementsTemplate
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

from ..Headlines import Headlines

############################################################################################################
# LOADING

class VSL_Elements(VSL_ElementsTemplate):
  def __init__(self,home_form=None, **properties):
    # Call the parent class's __init__ method
    self.home_form = home_form
    print("Inside VSL_Elements, home_form is:", self.home_form)

    super().__init__(**properties)

    anvil.users.login_with_form()
    self.chosen_company_profile = None
    self.chosen_product_name = None
    self.chosen_company_profile = None
    self.chosen_product_name = None
    self.chosen_product_research = None
    self.chosen_avatar = None
    self.chosen_tone = None
    self.chosen_script = None
    self.chosen_final_headline = None
    self.chosen_final_subheadline = None
    self.loading_info.visible = False

    self.update_company_assets_box_visibility()
    
    # Initialize task_id attribute
    self.task_id = None

    # WORKSPACE MANAGEMENT
    # Load the active workspace:
    self.load_active_workspace()
    # Get the User Table
    self.user_table = self.get_user_table()
    print(f"CURRENT USER TABLE IS: {self.user_table}")  

    # COMPANY NAME
    # Retrieve the row with 'variable' column containing 'company_name'
    company_name_row = self.user_table.search(variable='company_name')[0]
    self.company_name_input.text = company_name_row['variable_value']

    # PRODUCT NAME
    product_name_rows = [
    self.user_table.search(variable='product_1_latest')[0],
    self.user_table.search(variable='product_2_latest')[0],
    self.user_table.search(variable='product_3_latest')[0],
    self.user_table.search(variable='product_4_latest')[0],
    self.user_table.search(variable='product_5_latest')[0]
    ]
    # Filter out rows where 'variable_value' (product profile) is not empty
    non_empty_rows = [row for row in product_name_rows if row['variable_value']]
    # Extract the values from the non-empty rows
    product_names = [row['variable_title'] for row in non_empty_rows]
    # Assign the values to the company_profile_dropdown
    self.product_name_dropdown.items = product_names
   
    # AVATARS
    avatar_rows_custom = [
    self.user_table.search(variable='avatar_1_product_1_latest')[0],
    self.user_table.search(variable='avatar_2_product_1_latest')[0],
    self.user_table.search(variable='avatar_3_product_1_latest')[0],
    self.user_table.search(variable='avatar_1_product_2_latest')[0],
    self.user_table.search(variable='avatar_2_product_2_latest')[0],
    self.user_table.search(variable='avatar_3_product_2_latest')[0],
    self.user_table.search(variable='avatar_1_product_3_latest')[0],
    self.user_table.search(variable='avatar_2_product_3_latest')[0],
    self.user_table.search(variable='avatar_3_product_3_latest')[0],
    self.user_table.search(variable='avatar_1_product_4_latest')[0],
    self.user_table.search(variable='avatar_2_product_4_latest')[0],
    self.user_table.search(variable='avatar_3_product_4_latest')[0],
    self.user_table.search(variable='avatar_1_product_5_latest')[0],
    self.user_table.search(variable='avatar_2_product_5_latest')[0],
    self.user_table.search(variable='avatar_3_product_5_latest')[0],
    ]
    # CHANGE ALL THE 'VARIABLE_TITLE' to VARIABLE_VALUE
    # Filter out rows where 'variable_value' (avatar) is not empty
    non_empty_rows = [row for row in avatar_rows_custom if row['variable_value']] # <<<<<<<<<<<<<<<<<-------------------------------------HERE
    # Extract the values from the non-empty rows
    avatars_custom = [row['variable_value'] for row in non_empty_rows] # <<<<<<<<<<<<<<<<<-------------------------------------HERE
    # Create a list of tuples for the avatar_dropdown items
    avatar_dropdown_items = [(avatar, avatar) for avatar in avatars_custom]
    # Assign the values to the avatar_dropdown
    self.avatar_dropdown.items = avatar_dropdown_items

    # BRAND TONE
    brand_tone_urls = self.user_table.search(variable='brand_tone')
    brand_tone_extracted = [row['variable_title'] for row in brand_tone_urls]
    brand_tone_stock = [row['tone'] for row in app_tables.stock_tones.search() if row['tone']]

    # Create a list of tuples for the brand_tone_dropdown items
    brand_tone_dropdown_items = [(tone, tone) for tone in brand_tone_stock] + [(title, title) for title in brand_tone_extracted]
    # Assign the values to the brand_tone_dropdown
    self.brand_tone_dropdown.items = brand_tone_dropdown_items

   # SCRIPT FORMAT
    self.script_format_dropdown.items = ['Who, What, Where, How', 'Star, Story, Solution', 'The Perfect Webinar']

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

########----------------- 
# LOCK IT ALL IN
  def save_funnel_settings_component_click(self, **event_args):
     # Call the submit_button_click method to perform the validation and action
    if not self.submit_button_click():
        return  # Stop the function execution if validation failed

    self.loading_info.visible = True
    self.save_funnel_settings_component.visible = False
    
    # Get the current user
    # current_user = anvil.users.get_user()
    # user_table_name = current_user['user_id']
    # # Get the table for the current user
    # user_table = getattr(app_tables, user_table_name)

    # COMPANY NAME
    row_company_name = self.user_table.search(variable='company_name')
    company_name = row_company_name[0]['variable_value']
    self.chosen_company_name = company_name
    print('chosen_company_name:', self.chosen_company_name)

    row_chosen_company_name = self.user_table.search(variable='chosen_company_name')
    row_chosen_company_name[0]['variable_value'] = self.chosen_company_name
    row_chosen_company_name[0].update()

   # COMPANY PROFILE
    row_company_profile = self.user_table.search(variable='company_profile')
    company_profile = row_company_profile[0]['variable_value']
    self.chosen_company_profile = company_profile
    print('chosen_company_profile:', self.chosen_company_profile)
    # Save it to the table
    row_chosen_company_profile = self.user_table.search(variable='chosen_company_profile')
    row_chosen_company_profile[0]['variable_value'] = self.chosen_company_profile
    row_chosen_company_profile[0].update()

    # PRODUCT NAME
    self.chosen_product_name = self.product_name_dropdown.selected_value
    print('chosen_product_name:', self.chosen_product_name)
    # Save it to the table
    row_chosen_product_name = self.user_table.search(variable='chosen_product_name')
    row_chosen_product_name[0]['variable_value'] = self.chosen_product_name
    row_chosen_product_name[0].update()

    # PRODUCT RESEARCH
    selected_product_research_name = self.product_name_dropdown.selected_value
    selected_product_research_name_row = self.user_table.search(variable_title=selected_product_research_name)
    self.chosen_product_research = selected_product_research_name_row[0]['variable_value']
    print('chosen_product_research:', self.chosen_product_research)
    # Save it to the table
    row_chosen_product_research = self.user_table.search(variable='chosen_product_research')
    row_chosen_product_research[0]['variable_value'] = self.chosen_product_research
    row_chosen_product_research[0].update()

    # AVATARS
    selected_avatar_value = self.avatar_dropdown.selected_value
    # Check if the selected avatar value is from the stock avatars table
    self.chosen_avatar = anvil.server.call('get_chosen_variable_avatar', self.user_table, selected_avatar_value)
    print('Avatar:', self.chosen_avatar)

    row_chosen_avatar = self.user_table.search(variable='chosen_avatar')
    row_chosen_avatar[0]['variable_value'] = self.chosen_avatar
    row_chosen_avatar[0].update()

    # BRAND TONES
    selected_tone_value = self.brand_tone_dropdown.selected_value
    # Check if the selected avatar value is from the stock tonestable
    stock_tone_rows = app_tables.stock_tones.search(tone=selected_tone_value)
    if stock_tone_rows and len(stock_tone_rows) > 0:
      self.chosen_tone = stock_tone_rows[0]['value']
      print('Stock Tone:', self.chosen_tone)
    else:
      print('No Stock Tone Found')
      # Check if the selected avatar value is from the custom avatars table
      self.chosen_tone = anvil.server.call('get_chosen_variable_value', self.user_table, selected_tone_value)
      print('Custom Tone:', self.chosen_tone)

    row_chosen_tone = self.user_table.search(variable='chosen_tone')
    row_chosen_tone[0]['variable_value'] = self.chosen_tone
    row_chosen_tone[0].update()

    # SCRIPT
    selected_script_title = self.script_format_dropdown.selected_value
    # Search for rows where 'script_title' matches the selected value
    script_row = app_tables.example_scripts.search(script_title=selected_script_title)

    # Check if the search returned any matching rows
    if script_row:
      # Access the first matching row (assuming script_title values are unique)
      self.chosen_script = script_row[0]['script_contents']
    else:
      # Handle the case where no matching script_title was found
      print("No script found with the selected title")

    # Save the script contents and title
    row_chosen_script = self.user_table.search(variable='chosen_script')
    row_chosen_script[0]['variable_value'] = self.chosen_script
    row_chosen_script[0]['variable_title'] = selected_script_title
    row_chosen_script[0].update()


    # Call the navigation
    self.nav_button_VSL_Elements_to_headline()

  def validate_dropdown_selections(self):
    if not self.product_name_dropdown.selected_value:
        anvil.alert("Please select a product name.")
        return False

    if not self.avatar_dropdown.selected_value:
        anvil.alert("Please select an avatar.")
        return False

    if not self.brand_tone_dropdown.selected_value:
        anvil.alert("Please select a brand tone.")
        return False

    if not self.script_format_dropdown.selected_value:
        anvil.alert("Please select a script format.")
        return False

    # All dropdowns have a selected value, return True
    return True


  def submit_button_click(self, **event_args):
    # Validate the dropdown selections
    if not self.validate_dropdown_selections():
        return False
    # All dropdowns have a selected value, proceed with the action
    # Your code to handle the form submission or other actions here
    return True


  
###----------NAVIGATION---------------####
    
  # # Define the event handler for nav_button_tone_to_VSL_elements click
  # def nav_button_VSL_Elements_to_headline(self, **event_args):
  #       headlines = Headlines()
  #       self.content_panel.clear()
  #       self.content_panel.add_component(headlines)

  def nav_button_VSL_Elements_to_headline(self, **event_args):
    #anvil.open_form('Headlines')
    headlines = Headlines()
    self.whole_content_panel.clear()
    self.whole_content_panel.add_component(headlines)

  def update_company_assets_box_visibility(self):
    user = anvil.users.get_user()
    print("Before accessing company_assets_box in VSL_Elements, home_form is:", self.home_form)

    if user:
        # Get the column name from the 'active_workspace' value
        workspace_column_name = user['active_workspace']
        
        # Use the column name to fetch the actual table name
        actual_table_name = user[workspace_column_name]
        workspace_table = getattr(app_tables, actual_table_name)

        # Retrieve the first (and likely only) row.
        
        first_run_row = workspace_table.search(variable='first_run_complete')
        should_display_box = first_run_row[0]['variable_value']
        if should_display_box == 'Yes':
            self.home_form.company_assets_box.visible = True

        else:
            self.home_form.company_assets_box.visible = False
    else:
        print("User not logged in or active_workspace not in user")  # Check if this gets printed