from ._anvil_designer import HomeTemplate
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

#############################################
from ..Company import Company
from ..Workspace_1 import Workspace_1
from ..Workspace_2 import Workspace_2
from ..Workspace_3 import Workspace_3
from ..Product import Product
from ..BrandTone import BrandTone
from ..Avatars import Avatars
from ..VSL_Elements import VSL_Elements
from ..VideoSalesLetter import VideoSalesLetter
from ..FinalProduct import FinalProduct
from ..FinalProduct_Export import FinalProduct_Export


active_workspace = None
####################

class Home(HomeTemplate):
  def __init__(self,**properties):
    self.init_components(**properties)
    # Set Form properties and Data Bindings.
    
    if not anvil.users.get_user():  # Only prompt login if user isn't already logged in
        anvil.users.login_with_form()

    self.update_company_assets_box_visibility()
      
    # Check if user is logged in
    if anvil.users.get_user():
        self.initialize_default_workspace()
    
    for component in self.get_components():
      # Check if the component is a Timer
      if isinstance(component, anvil.Timer):
          # Stop the timer by setting its interval to None
          component.interval = None

    self.update_workspace_button_text()
    

  def update_company_assets_box_visibility(self):
    user = anvil.users.get_user()

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
            self.company_assets_box.visible = True
        else:
            self.company_assets_box.visible = False
    else:
        print("User not logged in or active_workspace not in user")  # Check if this gets printed

  def update_workspace_button_text(self):
    # Get the current user
    current_user = anvil.users.get_user()
    
    # Get the names of the workspace tables associated with the user
    workspace_1_table_name = current_user['workspace_1']
    workspace_2_table_name = current_user['workspace_2']
    workspace_3_table_name = current_user['workspace_3']

    # Initialize variables to store workspace names
    workspace_1_name = None
    workspace_2_name = None
    workspace_3_name = None

    # Check if workspace tables exist and retrieve their names
    if workspace_1_table_name:
        workspace_1_table = getattr(app_tables, workspace_1_table_name)
        workspace_1_row = workspace_1_table.search(variable='company_name')[0]
        workspace_1_name = workspace_1_row['variable_value']

    if workspace_2_table_name:
        workspace_2_table = getattr(app_tables, workspace_2_table_name)
        workspace_2_row = workspace_2_table.search(variable='company_name')[0]
        workspace_2_name = workspace_2_row['variable_value']

    if workspace_3_table_name:
        workspace_3_table = getattr(app_tables, workspace_3_table_name)
        workspace_3_row = workspace_3_table.search(variable='company_name')[0]
        workspace_3_name = workspace_3_row['variable_value']

    # Update button text based on workspace names
    if workspace_1_name:
        self.workspace_1_button.text = workspace_1_name
    else:
        self.workspace_1_button.text = "WORKSPACE 1"

    if workspace_2_name:
        self.workspace_2_button.text = workspace_2_name
    else:
        self.workspace_2_button.text = "WORKSPACE 2"

    if workspace_3_name:
        self.workspace_3_button.text = workspace_3_name
    else:
        self.workspace_3_button.text = "WORKSPACE 3"



              
##### USER MANAGEMENT
  
  def initialize_default_workspace(self):
    # Get the current user
    current_user = anvil.users.get_user()
    
    # Determine the workspace ID
    if current_user and 'active_workspace' in current_user and current_user['active_workspace']:
        workspace_id = current_user['active_workspace']
    else:
        # Set default workspace to 'workspace_1'
        workspace_id = 'workspace_1'
        if current_user:
            # Update the 'active_workspace' column in the user table
            current_user['active_workspace'] = workspace_id
            # Update the user table with the changes
            current_user.update()
        # Load the appropriate workspace form
    if workspace_id == 'workspace_1':
        Workspace_form = Workspace_1(home_form=self)
        self.workspace_1_button.background = '#4a90e2'
    elif workspace_id == 'workspace_2':
        Workspace_form = Workspace_2(home_form=self)
        self.workspace_1_button.background = '#4a90e2'
    elif workspace_id == 'workspace_3':
        Workspace_form = Workspace_3(home_form=self)
        self.workspace_1_button.background = '#4a90e2'
    else:
        raise ValueError(f"Unknown workspace: {workspace_id}")        

    # Display the workspace form in the content panel
    self.content_panel.clear()
    self.content_panel.add_component(Workspace_form)

    # Load the appropriate workspace form
    if workspace_id == 'workspace_1':
        Workspace_form = Workspace_1(home_form=self)
        self.workspace_1_button.background = '#4a90e2'
    elif workspace_id == 'workspace_2':
        Workspace_form = Workspace_2(home_form=self)
        self.workspace_1_button.background = '#4a90e2'
    elif workspace_id == 'workspace_3':
        Workspace_form = Workspace_3(home_form=self)
        self.workspace_1_button.background = '#4a90e2'
    else:
        raise ValueError(f"Unknown workspace: {workspace_id}")  

  
  def button_workspace_1_click(self, **event_args):
      global active_workspace
      active_workspace = 'workspace_1'
      self.set_active_workspace('workspace_1')  # Reset active workspace to 'workspace_1'
      self.update_company_assets_box_visibility()
      self.workspace_1_button.background = '#4a90e2'
      self.workspace_2_button.background = ''
      self.workspace_3_button.background = ''
      Workspace_1_form = Workspace_1(home_form=self)
      self.content_panel.clear()  # Clear the content panel
      self.content_panel.add_component(Workspace_1_form)  # Add the new component
  
  def button_workspace_2_click(self, **event_args):
      global active_workspace
      active_workspace = 'workspace_2'
      self.set_active_workspace('workspace_2')  # Reset active workspace to 'workspace_2'
      self.update_company_assets_box_visibility()
      self.workspace_1_button.background = ''
      self.workspace_2_button.background = '#4a90e2'
      self.workspace_3_button.background = ''
      Workspace_2_form = Workspace_2(home_form=self)
      self.content_panel.clear()  # Clear the content panel
      self.content_panel.add_component(Workspace_2_form)  # Add the new component
  
  def button_workspace_3_click(self, **event_args):
      global active_workspace
      active_workspace = 'workspace_3'
      self.set_active_workspace('workspace_3')  # Reset active workspace to 'workspace_3'
      self.update_company_assets_box_visibility()
      self.workspace_1_button.background = ''
      self.workspace_2_button.background = ''
      self.workspace_3_button.background = '#4a90e2'
      Workspace_3_form = Workspace_3(home_form=self)
      self.content_panel.clear()  # Clear the content panel
      self.content_panel.add_component(Workspace_3_form)  # Add the new component
  
  def get_user_table(self):
    current_user = anvil.users.get_user()
    global active_workspace
    workspace_id = self.get_active_workspace()
    user_table_name = current_user[workspace_id]
    return getattr(app_tables, user_table_name)

  def set_active_workspace(self, workspace_id):
    """Set the active workspace for the current user."""
    # Get the current user
    current_user = anvil.users.get_user()
    # Update the 'active_workspace' column in the user table
    current_user['active_workspace'] = workspace_id
    # Update the user table with the changes
    current_user.update()
    # Also, update the global variable
    global active_workspace
    active_workspace = workspace_id
    
  def get_active_workspace(self):
    global active_workspace
    return active_workspace

###### NAVIGATION
  
  def home_asset_link_click(self, **event_args):
    home = Home()
    self.content_panel.clear()
    self.content_panel.add_component(home)

  def company_asset_link_click(self, **event_args):
    company_form = Company(home_form=self)
    self.content_panel.clear()  # Clear the content panel
    self.content_panel.add_component(company_form)  # Add the new component

  def product_asset_link_click(self, **event_args):
    product=Product(home_form=self)
    self.content_panel.clear()
    self.content_panel.add_component(product)

  def brand_tone_asset_link_click(self, **event_args):
    brand_tone_form = BrandTone(home_form=self)
    self.content_panel.clear()
    self.content_panel.add_component(brand_tone_form)
  
  def avatars_asset_link_click(self, **event_args):
    avatars=Avatars(home_form=self)
    self.content_panel.clear()
    self.content_panel.add_component(avatars)

  def finalproduct_page_link_click(self, **event_args):
    finalproduct=FinalProduct()
    self.content_panel.clear()
    self.content_panel.add_component(finalproduct)

  def nav_button_to_company_click(self, **event_args):
    company = Company(home_form=self)
    self.content_panel.clear()
    self.content_panel.add_component(company)

## FUNNELS
  def VSL_page_link_click(self, **event_args):
    vsl_elements = VSL_Elements(home_form=self)
    self.content_panel.clear()
    self.content_panel.add_component(vsl_elements)

  def final_product_link_click(self, **event_args):
    final_product_export = FinalProduct_Export(home_form=self)
    self.content_panel.clear()
    self.content_panel.add_component(final_product_export)

   
