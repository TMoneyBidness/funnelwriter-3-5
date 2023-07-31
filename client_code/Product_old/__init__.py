from ._anvil_designer import Product_oldTemplate
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

############################################################################################################
# LOADING
class Product_old(Product_oldTemplate):
  def __init__(self, **properties):
    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    # Set the initial value of the progress bar to 0
    self.indeterminate_progress_products.visible = False
    anvil.users.login_with_form()
    # Any code you write here will run before the form opens.
  
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
   # Get the variable_title values for the specific profiles
    variable_titles_product_profiles = []

    # Search for the rows with product_profile_1
    rows_product_profile_1 = user_table.search(variable='product_profile_1')
    if rows_product_profile_1:
        variable_titles_product_profiles.append(rows_product_profile_1[0]['variable_title'])

    # Search for the rows with product_profile_2
    rows_product_profile_2 = user_table.search(variable='product_profile_2')
    if rows_product_profile_2:
        variable_titles_product_profiles.append(rows_product_profile_2[0]['variable_title'])
    
    # Search for the rows with product_profile_3
    rows_product_profile_3 = user_table.search(variable='product_profile_3')
    if rows_product_profile_3:
        variable_titles_product_profiles.append(rows_product_profile_3[0]['variable_title'])

    # Search for the rows with product_profile_4
    rows_product_profile_4 = user_table.search(variable='product_profile_4')
    if rows_product_profile_4:
        variable_titles_product_profiles.append(rows_product_profile_4[0]['variable_title'])\
      
     # Search for the rows with product_profile_5
    rows_product_profile_5 = user_table.search(variable='product_profile_5')
    if rows_product_profile_5:
        variable_titles_product_profiles.append(rows_product_profile_5[0]['variable_title'])

    # Update the dropdown items with the variable_titles
    self.product_profile_dropdown.items = variable_titles_product_profiles
    self.load_product_profile_dropdown.items = variable_titles_product_profiles

  
  def form_show(self, **event_args):
  # Load the company profile on form show
   self.load_product_profile()

  def product_research_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Research button clicked")
      # Start the progress bar with a small value
      self.indeterminate_progress_products.visible = True

      # Get the table for the current user
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      user_table = getattr(app_tables, user_table_name)
      
      # Search for the rows with company_url
      rows_company_url = user_table.search(variable='company_url')
      company_url = rows_company_url[0]['variable_value']
      
      rows_company_name = user_table.search(variable='company_name')
      company_name = rows_company_name[0]['variable_value']
      
      product_to_sell = self.product_name_input.text
      
      self.task_id = anvil.server.call('launch_product_research', product_to_sell, company_name, company_url)
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
                product_research = anvil.server.call('get_task_result', self.task_id)
                # Update the textbox with the result
                print("product_research :", product_research )
                self.product_profile_textbox.text = product_research
                self.indeterminate_progress_products.visible = False
                break  # Exit the loop
            elif task_status == "failed":
                # Get the error message
                task_error = anvil.server.call('get_task_result', self.task_id)
                print("Task error:", task_error)
                self.indeterminate_progress_products.visible = False
                break  # Exit the loop
    
        # Sleep for 2 second before checking again
        time.sleep(2)
            
  def edit_product_profile_component_click(self, **event_args):
    self.product_profile_textbox.read_only = False   

  def save_product_profile_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Prompt the user to select a profile name from the dropdown
    selected_profile_name = self.product_profile_dropdown.selected_value

    # Check if a profile name is selected
    if selected_profile_name:
        # Get the row from the user_table based on the selected profile name
        profile_row = user_table.get(variable_title=selected_profile_name)

        # Update the variable_value column in the profile row
        profile_row['variable_value'] = self.product_profile_textbox.text

        # Prompt the user to enter the variable name/title
        variable_title = anvil.js.window.prompt("Save the Product Name Associated with this Product Description?")

        # Check if the user entered a variable name/title
        if variable_title is not None:
            # Update the variable_title column in the profile row
            profile_row['variable_title'] = variable_title

            # Search for the product_name_row
            product_name_rows = user_table.search(variable='product_name')

            # Check if any product_name_rows are found
            if product_name_rows:
                # Update each found row with the new value
                for product_name_row in product_name_rows:
                    product_name_row['variable_value'] = self.product_name_input.text
                    product_name_row.update()
            else:
                # Handle case where product_name_row is missing
                print("Product name not found")
        else:
            # Handle case where the user cancelled the variable name/title prompt
            print("Variable name/title input cancelled by the user")
    else:
        # Handle case where no profile name is selected
        print("No profile name selected")


  def load_product_profile(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Prompt the user to select a profile name from the dropdown
    selected_profile_name = self.load_product_profile_dropdown.selected_value

    # Check if a profile name is selected
    if selected_profile_name:
        # Get the row from the user_table based on the selected profile name
        profile_row = user_table.get(variable_title=selected_profile_name)

        # Load the Product Profile from the profile row
        self.product_profile_textbox.text = profile_row['variable_value']

        # Load the Product Name from the user_table
        product_name_row = user_table.get(variable='product_name')

        # Check if product_name_row exists
        if product_name_row:
            self.product_name_input.text = product_name_row['variable_value']
        else:
            # Handle case where product_name_row is missing
            print("Product name not found")
    else:
        # Handle case where no profile name is selected
        print("No profile name selected")

  # def load_product_profile(self, **event_args):
  #   # Get the current user
  #   current_user = anvil.users.get_user()
  #   user_email = current_user['email']  # Change 'email' to 'username' if you are using usernames
  #   # Get the row for the current user from the variable_table
  #   row = app_tables.variable_table.get(owner=user_email)  # Change 'owner' to the appropriate column name if different
    
  #   if row:
  #       product_profile_loaded = row['product_profile']
  #       print("Contents:", product_profile_loaded)
  #       # Set the contents as the text of the rich text box
  #       self.product_profile_textbox.text = product_profile_loaded

  #       product_name_loaded = row['product_name']
  #       print("Contents:", product_name_loaded)
  #       # Set the contents as the text of the rich text box
  #       self.product_name_input.text = product_name_loaded
  #   else:
  #       # Handle case where the row does not exist for the current user
  #       print("No row found for the current user")
    
  def company_asset_link_click(self, **event_args):
    company=Company()
    self.content_panel.clear()
    self.content_panel.add_component(company)

  def product_profile_textbox_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass


