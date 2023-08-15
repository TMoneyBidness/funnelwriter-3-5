from ._anvil_designer import ProductTemplate
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
import json

from ..Avatars import Avatars

############################################################################################################
# LOADING
class Product(ProductTemplate):
  def __init__(self, **properties):
    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    anvil.users.login_with_form()
    # Set the initial value of the progress bar to 0

    self.indeterminate_all_products.visible = False
    self.indeterminate_1.visible = False
    self.indeterminate_2.visible = False
    self.indeterminate_3.visible = False
    self.indeterminate_4.visible = False
    self.indeterminate_5.visible = False

     # Hide Generate all 5 Products Button
    self.column_panel_5_products.visible = False 
   
   # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Load the latest info for products 1 to 5
    for i in range(1, 6):
        row_product_latest = user_table.search(variable=f'product_{i}_latest')
        row_product_url = user_table.search(variable=f'product_{i}_url')
    
        if row_product_latest:
            product_latest_description = row_product_latest[0]['variable_value']
            product_latest_title = row_product_latest[0]['variable_title']
            product_url = row_product_url[0]['variable_value']
            # Update the text box for the current product
            getattr(self, f'product_profile_{i}_textbox').text = product_latest_description
            getattr(self, f'product_{i}_name_input').text = product_latest_title
            getattr(self, f'product_{i}_url_input').text = product_url 
    
        else:
            # Handle case where the row does not exist for the current user
            print(f"No row found for 'product_{i}_latest'")
    
        # Check if any of the final company profile is empty
        any_final_product_rows = [
            user_table.search(variable='product_1')[0],
            user_table.search(variable='product_2')[0],
            user_table.search(variable='product_3')[0],
            user_table.search(variable='product_4')[0],
            user_table.search(variable='product_5')[0]
        ]

        # Check if at least one of the product descriptions is not empty
        if any(row['variable_value'] or row['variable_title'] for row in any_final_product_rows):
            # If any of the product descriptions are not empty, enable the button
            self.nav_button_products_to_avatars.enabled = True
        else:
            # If all product descriptions are empty, disable the button
            self.nav_button_products_to_avatars.enabled = False

#-- GENERATE THE 5 PREVIEWS ------------#######################################################################

  def all_products_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("All Products Generator button clicked")
      self.indeterminate_all_products.visible = True
      # Start the progress bar with a small value

      # Load stuff
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']

      # PRODUCT PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_url_row = user_table.search(variable='company_profile')[0]
      company_url = company_url_row['variable_value']

      products_grouped_row = user_table.get(variable='all_products_grouped')
      
      # Launch the background task
      self.task_id = anvil.server.call('launch_all_products_generator', company_profile, company_url)
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
              all_products_json = anvil.server.call('get_task_result', self.task_id)
              print("All 5 Products Generated")
              # Convert the JSON string back to a dictionary
              all_products = json.loads(all_products_json)
              # Update the text boxes with the products
              self.product_profile_1_textbox.text = all_products['product_1']
              self.product_profile_2_textbox.text = all_products['product_2']
              self.product_profile_3_textbox.text = all_products['product_3']
              self.product_profile_4_textbox.text = all_products['product_4']
              self.product_profile_5_textbox.text = all_products['product_5']

              # Update the variable_table with the JSON string
              products_grouped_row['variable_value'] = all_products_json
              self.indeterminate_all_products.visible = False
              products_grouped_row.update()

              for product_number in range(1, 6):
                product_latest_variable = f'product_{product_number}_latest'
                product_variable_value = all_products[f'product_{product_number}']
        
                product_latest_row = user_table.search(variable=product_latest_variable)[0]
                product_latest_row['variable_value'] = product_variable_value
                product_latest_row.update()
              break  # Exit the loop

            elif task_status == "failed":
              # Handle the case where the background task failed
              print("Task failed")
              self.indeterminate_all_products.visible = False
              break  # Exit the loop

          # Sleep for 1 second before checking again
          time.sleep(1)

#-- FUNCTION TO DEEP DIVE EACH PRODUCT ------------#######################################################################
  def generate_product_1_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Product Generator Initiated")
    
      self.nav_button_products_to_avatars.enabled = False

      # Stop the Function if there's no product name
      if not self.product_1_name_input.text:
        anvil.js.window.alert("Please name your product before generating the full description.")
        return
      else:
        self.indeterminate_1.visible = True
        # Load stuff        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
    
          # COMPANY PROFILE
        company_name_row = user_table.search(variable='company_name')[0]
        company_name= company_name_row['variable_value']
        
        # COMPANY PROFILE
        # Retrieve the row with 'variable' column containing 'company_profile'
        company_profile_row = user_table.search(variable='company_profile')[0]
        company_profile = company_profile_row['variable_value']
    
        # COMPANY URL
        # Retrieve the row with 'variable' column containing 'company_profile'
        company_url_row = user_table.search(variable='company_url')[0]
        company_url = company_url_row['variable_value']
    
        # PRODUCT NAME
        product_1_name = self.product_1_name_input.text
        product_1_name_row = user_table.search(variable='product_1_name_latest')[0]
        product_1_name_row['variable_value'] = product_1_name
        product_1_name_row.update()

        # PRODUCT URL
        product_1_url = self.product_1_url_input.text
        product_1_url_row = user_table.get(variable=f"product_1_url")
        product_1_url_row['variable_value'] = product_1_url
        product_1_url_row.update()
            
        # PRODUCT EXCERPT / PREVIEW
        product_1_preview = self.product_profile_1_textbox.text
        product_1_latest = self.product_profile_1_textbox.text
        product_1_preview_row = user_table.search(variable='product_1_preview')[0]
        product_1_preview_row['variable_value'] = product_1_preview
        product_1_preview_row.update()
        # Save it it as the latest as well
        product_1_latest_row = user_table.search(variable='product_1_latest')[0]
        product_1_latest_row['variable_value'] = product_1_latest
        product_1_latest_row.update()
              
        self.task_id = anvil.server.call('launch_deepdive_product_1_generator',company_name,product_1_name,product_1_url,product_1_preview)
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
              product_1_generation = anvil.server.call('get_task_result', self.task_id)
              
              # Update the textbox with the result
              print("Product:", product_1_generation)
              self.product_profile_1_textbox.text = product_1_generation
    
              # Save it in the table:
              product_1_latest_row = user_table.search(variable='product_1_latest')[0]
              product_1_latest_row['variable_value'] = product_1_generation
        
              self.indeterminate_1.visible = False
              break  # Exit the loop
              
            elif task_status == "failed":
              # Get the error message
              task_error = anvil.server.call('get_task_result', self.task_id)
              print("Task error:", task_error)
              self.indeterminate_1.visible = False
              break  # Exit the loop
    
          # Sleep for 1 second before checking again
          time.sleep(2)

  def generate_product_2_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        # This method should handle the UI logic
        print("Deep Product Generator Initiated")
        # Start the progress bar with a small value
       # Stop the Function if there's no product name
        if not self.product_2_name_input.text:
          anvil.js.window.alert("Please name your product before generating the full description.")
          return
        else:
          self.indeterminate_2.visible = True

          # Load stuff
          current_user = anvil.users.get_user()
          user_table_name = current_user['user_id']
          # Get the table for the current user
          user_table = getattr(app_tables, user_table_name)
  
          # COMPANY PROFILE
          company_name_row = user_table.search(variable='company_name')[0]
          company_name = company_name_row['variable_value']
  
          # COMPANY PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_profile_row = user_table.search(variable='company_profile')[0]
          company_profile = company_profile_row['variable_value']
  
          # PRODUCT PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_url_row = user_table.search(variable='company_url')[0]
          company_url = company_url_row['variable_value']
  
          # PRODUCT NAME
          product_2_name = self.product_2_name_input.text
          product_2_name_row = user_table.search(variable='product_2_name_latest')[0]
          product_2_name_row['variable_value'] = product_2_name

          # PRODUCT URL
          product_2_url = self.product_2_url_input.text
          product_2_url_row = user_table.get(variable=f"product_2_url")
          product_2_url_row['variable_value'] = product_2_url
          product_2_url_row.update()
  
          # PRODUCT EXCERPT / PREVIEW
          product_2_preview = self.product_profile_2_textbox.text
          product_2_latest = self.product_profile_2_textbox.text  
          product_2_preview_row = user_table.search(variable='product_2_preview')[0]
          product_2_preview_row['variable_value'] = product_2_preview
          product_2_preview_row.update()
          # Save it as the latest as well
          product_2_latest_row = user_table.search(variable='product_2_latest')[0]
          product_2_latest_row['variable_value'] = product_2_preview
          product_2_latest_row.update()
  
          self.task_id = anvil.server.call('launch_deepdive_product_2_generator', company_name,product_1_name,product_1_url,product_1_preview)
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
                          product_2_generation = anvil.server.call('get_task_result', self.task_id)
  
                          # Update the textbox with the result
                          print("Product:", product_2_generation)
                          self.product_profile_2_textbox.text = product_2_generation
  
                          # Save it in the table:
                          product_2_latest_row = user_table.search(variable='product_2_latest')[0]
                          product_2_latest_row['variable_value'] = product_2_generation
  
                          self.indeterminate_2.visible = False
                          break  # Exit the loop
  
                      elif task_status == "failed":
                          # Get the error message
                          task_error = anvil.server.call('get_task_result', self.task_id)
                          print("Task error:", task_error)
                          self.indeterminate_2.visible = False
                          break  # Exit the loop
  
                  # Sleep for 1 second before checking again
                  time.sleep(2)

  def generate_product_3_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        # This method should handle the UI logic
        print("Deep Product Generator Initiated")
        # Start the progress bar with a small value
     
      # Stop the Function if there's no product name
        if not self.product_3_name_input.text:
          anvil.js.window.alert("Please name your product before generating the full description.")
          return
        else:
          self.indeterminate_3.visible = True    

          # Load stuff
          current_user = anvil.users.get_user()
          user_table_name = current_user['user_id']
          # Get the table for the current user
          user_table = getattr(app_tables, user_table_name)
  
          # COMPANY PROFILE
          company_name_row = user_table.search(variable='company_name')[0]
          company_name = company_name_row['variable_value']
  
          # COMPANY PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_profile_row = user_table.search(variable='company_profile')[0]
          company_profile = company_profile_row['variable_value']
  
          # PRODUCT PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_url_row = user_table.search(variable='company_url')[0]
          company_url = company_url_row['variable_value']
  
          # PRODUCT NAME
          product_3_name = self.product_3_name_input.text
          product_3_name_row = user_table.search(variable='product_3_name_latest')[0]
          product_3_name_row['variable_value'] = product_3_name

         # PRODUCT URL
          product_3_url = self.product_3_url_input.text
          product_3_url_row = user_table.get(variable=f"product_3_url")
          product_3_url_row['variable_value'] = product_3_url
          product_3_url_row.update()
          
  
          # PRODUCT EXCERPT / PREVIEW
          product_3_preview = self.product_profile_3_textbox.text
          product_3_latest = self.product_profile_3_textbox.text
          product_3_preview_row = user_table.search(variable='product_3_preview')[0]
          product_3_preview_row['variable_value'] = product_3_preview
          product_3_preview_row.update()
          # Save it as the latest as well
          product_3_latest_row = user_table.search(variable='product_3_latest')[0]
          product_3_latest_row['variable_value'] = product_3_preview
          product_3_latest_row.update()
  
          self.task_id = anvil.server.call('launch_deepdive_product_3_generator',  company_name,product_3_name,product_3_url,product_3_preview)
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
                          product_3_generation = anvil.server.call('get_task_result', self.task_id)
  
                          # Update the textbox with the result
                          print("Product:", product_3_generation)
                          self.product_profile_3_textbox.text = product_3_generation
  
                          # Save it in the table:
                          product_3_latest_row = user_table.search(variable='product_3_latest')[0]
                          product_3_latest_row['variable_value'] = product_3_generation
  
                          self.indeterminate_3.visible = False
                          break  # Exit the loop
  
                      elif task_status == "failed":
                          # Get the error message
                          task_error = anvil.server.call('get_task_result', self.task_id)
                          print("Task error:", task_error)
                          self.indeterminate_3.visible = False
                          break  # Exit the loop
  
                  # Sleep for 1 second before checking again
                  time.sleep(2)

  def generate_product_4_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        # This method should handle the UI logic
        print("Deep Product Generator Initiated")
        # Start the progress bar with a small value
         # Stop the Function if there's no product name
        if not self.product_4_name_input.text:
          anvil.js.window.alert("Please name your product before generating the full description.")
          return
        else:
          self.indeterminate_4.visible = True

          # Load stuff
          current_user = anvil.users.get_user()
          user_table_name = current_user['user_id']
          # Get the table for the current user
          user_table = getattr(app_tables, user_table_name)
  
          # COMPANY PROFILE
          company_name_row = user_table.search(variable='company_name')[0]
          company_name = company_name_row['variable_value']
  
          # COMPANY PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_profile_row = user_table.search(variable='company_profile')[0]
          company_profile = company_profile_row['variable_value']
  
          # PRODUCT PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_url_row = user_table.search(variable='company_url')[0]
          company_url = company_url_row['variable_value']
  
          # PRODUCT NAME
          product_4_name = self.product_4_name_input.text
          product_4_name_row = user_table.search(variable='product_4_name_latest')[0]
          product_4_name_row['variable_value'] = product_4_name

             # PRODUCT URL
          product_4_url = self.product_4_url_input.text
          product_4_url_row = user_table.get(variable=f"product_4_url")
          product_4_url_row['variable_value'] = product_4_url
          product_4_url_row.update()
  
          # PRODUCT EXCERPT / PREVIEW
          product_4_preview = self.product_profile_4_textbox.text
          product_4_latest = self.product_profile_4_textbox.text
          product_4_preview_row = user_table.search(variable='product_4_preview')[0]
          product_4_preview_row['variable_value'] = product_4_preview
          product_4_preview_row.update()
          # Save it as the latest as well
          product_4_latest_row = user_table.search(variable='product_4_latest')[0]
          product_4_latest_row['variable_value'] = product_4_preview
          product_4_latest_row.update()
  
          self.task_id = anvil.server.call('launch_deepdive_product_4_generator', company_name,product_4_name,product_4_url,product_4_preview)
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
                          product_4_generation = anvil.server.call('get_task_result', self.task_id)
  
                          # Update the textbox with the result
                          print("Product:", product_4_generation)
                          self.product_profile_4_textbox.text = product_4_generation
  
                          # Save it in the table:
                          product_4_latest_row = user_table.search(variable='product_4_latest')[0]
                          product_4_latest_row['variable_value'] = product_4_generation
  
                          self.indeterminate_4.visible = False
                          break  # Exit the loop
  
                      elif task_status == "failed":
                          # Get the error message
                          task_error = anvil.server.call('get_task_result', self.task_id)
                          print("Task error:", task_error)
                          self.indeterminate_4.visible = False
                          break  # Exit the loop
  
                  # Sleep for 1 second before checking again
                  time.sleep(2)
  
  def generate_product_5_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        # This method should handle the UI logic
        print("Deep Product Generator Initiated")
       
        # Stop the Function if there's no product name
        if not self.product_5_name_input.text:
          anvil.js.window.alert("Please name your product before generating the full description.")
          return
        else:
          self.indeterminate_5.visible = True

          # Load stuff
          current_user = anvil.users.get_user()
          user_table_name = current_user['user_id']
          # Get the table for the current user
          user_table = getattr(app_tables, user_table_name)
  
          # COMPANY PROFILE
          company_name_row = user_table.search(variable='company_name')[0]
          company_name = company_name_row['variable_value']
  
          # COMPANY PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_profile_row = user_table.search(variable='company_profile')[0]
          company_profile = company_profile_row['variable_value']
  
          # PRODUCT PROFILE
          # Retrieve the row with 'variable' column containing 'company_profile'
          company_url_row = user_table.search(variable='company_url')[0]
          company_url = company_url_row['variable_value']
  
          # PRODUCT NAME
          product_5_name = self.product_5_name_input.text
          product_5_name_row = user_table.search(variable='product_5_name_latest')[0]
          product_5_name_row['variable_value'] = product_5_name

          # PRODUCT URL
          product_5_url = self.product_5_url_input.text
          product_5_url_row = user_table.get(variable=f"product_5_url")
          product_5_url_row['variable_value'] = product_5_url
          product_5_url_row.update()
  
          # PRODUCT EXCERPT / PREVIEW
          product_5_preview = self.product_profile_5_textbox.text
          product_5_latest = self.product_profile_5_textbox.text
          product_5_preview_row = user_table.search(variable='product_5_preview')[0]
          product_5_preview_row['variable_value'] = product_5_preview
          product_5_preview_row.update()
          # Save it as the latest as well
          product_5_latest_row = user_table.search(variable='product_5_latest')[0]
          product_5_latest_row['variable_value'] = product_5_preview
          product_5_latest_row.update()
  
          self.task_id = anvil.server.call('launch_deepdive_product_5_generator',  company_name,product_5_name,product_5_url,product_5_preview)
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
                          product_5_generation = anvil.server.call('get_task_result', self.task_id)
  
                          # Update the textbox with the result
                          print("Product:", product_5_generation)
                          self.product_profile_5_textbox.text = product_5_generation
  
                          # Save it in the table:
                          product_5_latest_row = user_table.search(variable='product_5_latest')[0]
                          product_5_latest_row['variable_value'] = product_5_generation
  
                          self.indeterminate_5.visible = False
                          break  # Exit the loop
  
                      elif task_status == "failed":
                          # Get the error message
                          task_error = anvil.server.call('get_task_result', self.task_id)
                          print("Task error:", task_error)
                          self.indeterminate_5.visible = False
                          break  # Exit the loop
  
                  # Sleep for 1 second before checking again
                  time.sleep(2)

  

#-- SAVE / LOAD EACH AVATAR ------------#######################################################################

  def save_product_1_button_click(self, **event_args):
    # Save the title and description
    final_product_description = self.product_profile_1_textbox.text
    final_product_title = self.product_1_name_input.text

    # Check if both title and description are filled out
    if not final_product_title or not final_product_description:
        # Show an alert if any of them is empty
        anvil.js.window.alert("Product Title and Description cannot be empty.")
        return

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    product_number = "product_1"
    
    product_row = user_table.get(variable=product_number)

    if product_row:
        product_row['variable_value'] = final_product_description
        product_row['variable_title'] = final_product_title 
        product_row.update()

        # Save it as the latest as well
        product_1_latest_description_row = user_table.search(variable='product_1_latest')[0]
        product_1_latest_description_row['variable_value'] = final_product_description
        product_1_latest_description_row['variable_title'] = final_product_title
        product_1_latest_description_row.update()

        # Enable the button for navigation
        self.nav_button_products_to_avatars.enabled = True
    else:
        # Handle case where the row does not exist for the current user
        print("No row found for the current user")
 
  def save_product_2_button_click(self, **event_args):
    # Save the title and description
    final_product_description = self.product_profile_2_textbox.text
    final_product_title = self.product_2_name_input.text

    # Check if both title and description are filled out
    if not final_product_title or not final_product_description:
        # Show an alert if any of them is empty
        anvil.js.window.alert("Product Title and Description cannot be empty.")
        return

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    product_number = "product_2"
    product_row = user_table.get(variable=product_number)

    if product_row:
        product_row['variable_value'] = final_product_description
        product_row['variable_title'] = final_product_title 
        product_row.update()

        # Save it as the latest as well
        product_2_latest_description_row = user_table.search(variable='product_2_latest')[0]
        product_2_latest_description_row['variable_value'] = final_product_description
        product_2_latest_description_row['variable_title'] = final_product_title
        product_2_latest_description_row.update()

        # Enable the button for navigation
        self.nav_button_products_to_avatars.enabled = True
    else:
        # Handle case where the row does not exist for the current user
        print("No row found for the current user")

  def save_product_3_button_click(self, **event_args):
    # Save the title and description
    final_product_description = self.product_profile_3_textbox.text
    final_product_title = self.product_3_name_input.text

    # Check if both title and description are filled out
    if not final_product_title or not final_product_description:
        # Show an alert if any of them is empty
        anvil.js.window.alert("Product Title and Description cannot be empty.")
        return

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    product_number = "product_3"
    product_row = user_table.get(variable=product_number)

    if product_row:
        product_row['variable_value'] = final_product_description
        product_row['variable_title'] = final_product_title 
        product_row.update()

        # Save it as the latest as well
        product_3_latest_description_row = user_table.search(variable='product_3_latest')[0]
        product_3_latest_description_row['variable_value'] = final_product_description
        product_3_latest_description_row['variable_title'] = final_product_title
        product_3_latest_description_row.update()

        # Enable the button for navigation
        self.nav_button_products_to_avatars.enabled = True
    else:
        # Handle case where the row does not exist for the current user
        print("No row found for the current user")

  def save_product_4_button_click(self, **event_args):
    # Save the title and description
    final_product_description = self.product_profile_4_textbox.text
    final_product_title = self.product_4_name_input.text

    # Check if both title and description are filled out
    if not final_product_title or not final_product_description:
        # Show an alert if any of them is empty
        anvil.js.window.alert("Product Title and Description cannot be empty.")
        return

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    product_number = "product_4"
    product_row = user_table.get(variable=product_number)

    if product_row:
        product_row['variable_value'] = final_product_description
        product_row['variable_title'] = final_product_title 
        product_row.update()

        # Save it as the latest as well
        product_4_latest_description_row = user_table.search(variable='product_4_latest')[0]
        product_4_latest_description_row['variable_value'] = final_product_description
        product_4_latest_description_row['variable_title'] = final_product_title
        product_4_latest_description_row.update()

        # Enable the button for navigation
        self.nav_button_products_to_avatars.enabled = True
    else:
        # Handle case where the row does not exist for the current user
        print("No row found for the current user")

  def save_product_5_button_click(self, **event_args):
    # Save the title and description
    final_product_description = self.product_profile_5_textbox.text
    final_product_title = self.product_5_name_input.text

    # Check if both title and description are filled out
    if not final_product_title or not final_product_description:
        # Show an alert if any of them is empty
        anvil.js.window.alert("Product Title and Description cannot be empty.")
        return

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    product_number = "product_5"
    product_row = user_table.get(variable=product_number)

    if product_row:
        product_row['variable_value'] = final_product_description
        product_row['variable_title'] = final_product_title 
        product_row.update()

        # Save it as the latest as well
        product_5_latest_description_row = user_table.search(variable='product_5_latest')[0]
        product_5_latest_description_row['variable_value'] = final_product_description
        product_5_latest_description_row['variable_title'] = final_product_title
        product_5_latest_description_row.update()

        # Enable the button for navigation
        self.nav_button_products_to_avatars.enabled = True
    else:
        # Handle case where the row does not exist for the current user
        print("No row found for the current user")

  ### LOAD AVATARS ---------------#############################

  def load_product_1_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
    
    # Choose our product number
    selected_product_number = "product_1"
    
    product_row = user_table.get(variable=selected_product_number)

    # Check if 'variable_title' and 'variable_value' columns are not empty
    if product_row and product_row['variable_title'] and product_row['variable_value']:
        product_description_loaded = product_row['variable_value']
        product_title_loaded = product_row['variable_title']
        self.product_profile_1_textbox.text = product_description_loaded 
        self.product_1_name_input.text = product_title_loaded  
    else:
        # Load nothing and print an alert
        anvil.js.window.alert("No product found")

  def load_product_2_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
    
    # Choose our product number
    selected_product_number = "product_2"
    
    product_row = user_table.get(variable=selected_product_number)

    # Check if 'variable_title' and 'variable_value' columns are not empty
    if product_row and product_row['variable_title'] and product_row['variable_value']:
        product_description_loaded = product_row['variable_value']
        product_title_loaded = product_row['variable_title']
        self.product_profile_2_textbox.text = product_description_loaded 
        self.product_2_name_input.text = product_title_loaded  
    else:
        # Load nothing and print an alert
        anvil.js.window.alert("No product found")

  def load_product_3_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
    
    # Choose our product number
    selected_product_number = "product_3"
    
    product_row = user_table.get(variable=selected_product_number)

    # Check if 'variable_title' and 'variable_value' columns are not empty
    if product_row and product_row['variable_title'] and product_row['variable_value']:
        product_description_loaded = product_row['variable_value']
        product_title_loaded = product_row['variable_title']
        self.product_profile_3_textbox.text = product_description_loaded 
        self.product_3_name_input.text = product_title_loaded  
    else:
        # Load nothing and print an alert
        anvil.js.window.alert("No product found")

  def load_product_4_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
    
    # Choose our product number
    selected_product_number = "product_4"
    
    product_row = user_table.get(variable=selected_product_number)

    # Check if 'variable_title' and 'variable_value' columns are not empty
    if product_row and product_row['variable_title'] and product_row['variable_value']:
        product_description_loaded = product_row['variable_value']
        product_title_loaded = product_row['variable_title']
        self.product_profile_4_textbox.text = product_description_loaded 
        self.product_4_name_input.text = product_title_loaded  
    else:
        # Load nothing and print an alert
        anvil.js.window.alert("No product found")
      
  def load_product_5_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
    
    # Choose our product number
    selected_product_number = "product_5"
    
    product_row = user_table.get(variable=selected_product_number)

    # Check if 'variable_title' and 'variable_value' columns are not empty
    if product_row and product_row['variable_title'] and product_row['variable_value']:
        product_description_loaded = product_row['variable_value']
        product_title_loaded = product_row['variable_title']
        self.product_profile_5_textbox.text = product_description_loaded 
        self.product_5_name_input.text = product_title_loaded  
    else:
        # Load nothing and print an alert
        anvil.js.window.alert("No product found")

###----------NAVIGATION---------------####
  def nav_button_products_to_avatars_click(self, **event_args):
    self.navigate_to_avatars()
  
  def navigate_to_avatars(self):
    avatars = Avatars()
    self.content_panel.clear()
    self.content_panel.add_component(avatars)
     # anvil.open_form('Avatars')

# OLD FUNCTIONS

# OLD PRODUCT GENERATORS:

#-- FUNCTION TO GENERATE ALL 5 PRODUCTS EACH PRODUCT ------------#######################################################################
 #  def generate_product_1_button_click(self, **event_args):
 #    with anvil.server.no_loading_indicator:
 #      # This method should handle the UI logic
 #      print("Deep Product Generator Initiated")
    
 #      self.nav_button_products_to_avatars.enabled = False

 #      # Stop the Function if there's no product name
 #      if not self.product_1_name_input.text:
 #        anvil.js.window.alert("Please name your product before generating the full description.")
 #        return
 #      else:
 #        self.indeterminate_1.visible = True
 #        # Load stuff        
 #        current_user = anvil.users.get_user()
 #        user_table_name = current_user['user_id']
 #        # Get the table for the current user
 #        user_table = getattr(app_tables, user_table_name)
    
 #          # COMPANY PROFILE
 #        company_name_row = user_table.search(variable='company_name')[0]
 #        company_name= company_name_row['variable_value']
        
 #        # COMPANY PROFILE
 #        # Retrieve the row with 'variable' column containing 'company_profile'
 #        company_profile_row = user_table.search(variable='company_profile')[0]
 #        company_profile = company_profile_row['variable_value']
    
 #        # COMPANY URL
 #        # Retrieve the row with 'variable' column containing 'company_profile'
 #        company_url_row = user_table.search(variable='company_url')[0]
 #        company_url = company_url_row['variable_value']
    
 #        # PRODUCT NAME
 #        product_1_name = self.product_1_name_input.text
 #        product_1_name_row = user_table.search(variable='product_1_name_latest')[0]
 #        product_1_name_row['variable_value'] = product_1_name
    
 #        # PRODUCT EXCERPT / PREVIEW
 #        product_1_preview = self.product_profile_1_textbox.text
 #        product_1_latest = self.product_profile_1_textbox.text
 #        product_1_preview_row = user_table.search(variable='product_1_preview')[0]
 #        product_1_preview_row['variable_value'] = product_1_preview
 #        product_1_preview_row.update()
 #        # Save it it as the latest as well
 #        product_1_latest_row = user_table.search(variable='product_1_latest')[0]
 #        product_1_latest_row['variable_value'] = product_1_latest
 #        product_1_latest_row.update()
              
 #        self.task_id = anvil.server.call('launch_deepdive_product_1_generator', company_name,company_profile,company_url,product_1_name,product_1_preview)
 #        print("Task ID:", self.task_id)
    
 #        # Loop to check the status of the background task
 #      while True:
 #        with anvil.server.no_loading_indicator:
    
 #        # Check if the background task is complete
 #          task_status = anvil.server.call('get_task_status', self.task_id)
 #          print("Task status:", task_status)
    
 #          if task_status is not None:
 #            if task_status == "completed":
 #          # Get the result of the background task
 #              product_1_generation = anvil.server.call('get_task_result', self.task_id)
              
 #              # Update the textbox with the result
 #              print("Product:", product_1_generation)
 #              self.product_profile_1_textbox.text = product_1_generation
    
 #              # Save it in the table:
 #              product_1_latest_row = user_table.search(variable='product_1_latest')[0]
 #              product_1_latest_row['variable_value'] = product_1_generation
        
 #              self.indeterminate_1.visible = False
 #              break  # Exit the loop
              
 #            elif task_status == "failed":
 #              # Get the error message
 #              task_error = anvil.server.call('get_task_result', self.task_id)
 #              print("Task error:", task_error)
 #              self.indeterminate_1.visible = False
 #              break  # Exit the loop
    
 #          # Sleep for 1 second before checking again
 #          time.sleep(2)

 #  def generate_product_2_button_click(self, **event_args):
 #    with anvil.server.no_loading_indicator:
 #        # This method should handle the UI logic
 #        print("Deep Product Generator Initiated")
 #        # Start the progress bar with a small value
 #       # Stop the Function if there's no product name
 #        if not self.product_2_name_input.text:
 #          anvil.js.window.alert("Please name your product before generating the full description.")
 #          return
 #        else:
 #          self.indeterminate_2.visible = True

 #          # Load stuff
 #          current_user = anvil.users.get_user()
 #          user_table_name = current_user['user_id']
 #          # Get the table for the current user
 #          user_table = getattr(app_tables, user_table_name)
  
 #          # COMPANY PROFILE
 #          company_name_row = user_table.search(variable='company_name')[0]
 #          company_name = company_name_row['variable_value']
  
 #          # COMPANY PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_profile_row = user_table.search(variable='company_profile')[0]
 #          company_profile = company_profile_row['variable_value']
  
 #          # PRODUCT PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_url_row = user_table.search(variable='company_url')[0]
 #          company_url = company_url_row['variable_value']
  
 #          # PRODUCT NAME
 #          product_2_name = self.product_2_name_input.text
 #          product_2_name_row = user_table.search(variable='product_2_name_latest')[0]
 #          product_2_name_row['variable_value'] = product_2_name
  
 #          # PRODUCT EXCERPT / PREVIEW
 #          product_2_preview = self.product_profile_2_textbox.text
 #          product_2_latest = self.product_profile_2_textbox.text  
 #          product_2_preview_row = user_table.search(variable='product_2_preview')[0]
 #          product_2_preview_row['variable_value'] = product_2_preview
 #          product_2_preview_row.update()
 #          # Save it as the latest as well
 #          product_2_latest_row = user_table.search(variable='product_2_latest')[0]
 #          product_2_latest_row['variable_value'] = product_2_preview
 #          product_2_latest_row.update()
  
 #          self.task_id = anvil.server.call('launch_deepdive_product_2_generator', company_name, company_profile, company_url, product_2_name, product_2_preview)
 #          print("Task ID:", self.task_id)
  
 #          # Loop to check the status of the background task
 #          while True:
 #              with anvil.server.no_loading_indicator:
  
 #                  # Check if the background task is complete
 #                  task_status = anvil.server.call('get_task_status', self.task_id)
 #                  print("Task status:", task_status)
  
 #                  if task_status is not None:
 #                      if task_status == "completed":
 #                          # Get the result of the background task
 #                          product_2_generation = anvil.server.call('get_task_result', self.task_id)
  
 #                          # Update the textbox with the result
 #                          print("Product:", product_2_generation)
 #                          self.product_profile_2_textbox.text = product_2_generation
  
 #                          # Save it in the table:
 #                          product_2_latest_row = user_table.search(variable='product_2_latest')[0]
 #                          product_2_latest_row['variable_value'] = product_2_generation
  
 #                          self.indeterminate_2.visible = False
 #                          break  # Exit the loop
  
 #                      elif task_status == "failed":
 #                          # Get the error message
 #                          task_error = anvil.server.call('get_task_result', self.task_id)
 #                          print("Task error:", task_error)
 #                          self.indeterminate_2.visible = False
 #                          break  # Exit the loop
  
 #                  # Sleep for 1 second before checking again
 #                  time.sleep(2)

 #  def generate_product_3_button_click(self, **event_args):
 #    with anvil.server.no_loading_indicator:
 #        # This method should handle the UI logic
 #        print("Deep Product Generator Initiated")
 #        # Start the progress bar with a small value
     
 #      # Stop the Function if there's no product name
 #        if not self.product_3_name_input.text:
 #          anvil.js.window.alert("Please name your product before generating the full description.")
 #          return
 #        else:
 #          self.indeterminate_3.visible = True    

 #          # Load stuff
 #          current_user = anvil.users.get_user()
 #          user_table_name = current_user['user_id']
 #          # Get the table for the current user
 #          user_table = getattr(app_tables, user_table_name)
  
 #          # COMPANY PROFILE
 #          company_name_row = user_table.search(variable='company_name')[0]
 #          company_name = company_name_row['variable_value']
  
 #          # COMPANY PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_profile_row = user_table.search(variable='company_profile')[0]
 #          company_profile = company_profile_row['variable_value']
  
 #          # PRODUCT PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_url_row = user_table.search(variable='company_url')[0]
 #          company_url = company_url_row['variable_value']
  
 #          # PRODUCT NAME
 #          product_3_name = self.product_3_name_input.text
 #          product_3_name_row = user_table.search(variable='product_3_name_latest')[0]
 #          product_3_name_row['variable_value'] = product_3_name
  
 #          # PRODUCT EXCERPT / PREVIEW
 #          product_3_preview = self.product_profile_3_textbox.text
 #          product_3_latest = self.product_profile_3_textbox.text
 #          product_3_preview_row = user_table.search(variable='product_3_preview')[0]
 #          product_3_preview_row['variable_value'] = product_3_preview
 #          product_3_preview_row.update()
 #          # Save it as the latest as well
 #          product_3_latest_row = user_table.search(variable='product_3_latest')[0]
 #          product_3_latest_row['variable_value'] = product_3_preview
 #          product_3_latest_row.update()
  
 #          self.task_id = anvil.server.call('launch_deepdive_product_3_generator', company_name, company_profile, company_url, product_3_name, product_3_preview)
 #          print("Task ID:", self.task_id)
  
 #          # Loop to check the status of the background task
 #          while True:
 #              with anvil.server.no_loading_indicator:
  
 #                  # Check if the background task is complete
 #                  task_status = anvil.server.call('get_task_status', self.task_id)
 #                  print("Task status:", task_status)
  
 #                  if task_status is not None:
 #                      if task_status == "completed":
 #                          # Get the result of the background task
 #                          product_3_generation = anvil.server.call('get_task_result', self.task_id)
  
 #                          # Update the textbox with the result
 #                          print("Product:", product_3_generation)
 #                          self.product_profile_3_textbox.text = product_3_generation
  
 #                          # Save it in the table:
 #                          product_3_latest_row = user_table.search(variable='product_3_latest')[0]
 #                          product_3_latest_row['variable_value'] = product_3_generation
  
 #                          self.indeterminate_3.visible = False
 #                          break  # Exit the loop
  
 #                      elif task_status == "failed":
 #                          # Get the error message
 #                          task_error = anvil.server.call('get_task_result', self.task_id)
 #                          print("Task error:", task_error)
 #                          self.indeterminate_3.visible = False
 #                          break  # Exit the loop
  
 #                  # Sleep for 1 second before checking again
 #                  time.sleep(2)

 #  def generate_product_4_button_click(self, **event_args):
 #    with anvil.server.no_loading_indicator:
 #        # This method should handle the UI logic
 #        print("Deep Product Generator Initiated")
 #        # Start the progress bar with a small value
 #         # Stop the Function if there's no product name
 #        if not self.product_4_name_input.text:
 #          anvil.js.window.alert("Please name your product before generating the full description.")
 #          return
 #        else:
 #          self.indeterminate_4.visible = True

 #          # Load stuff
 #          current_user = anvil.users.get_user()
 #          user_table_name = current_user['user_id']
 #          # Get the table for the current user
 #          user_table = getattr(app_tables, user_table_name)
  
 #          # COMPANY PROFILE
 #          company_name_row = user_table.search(variable='company_name')[0]
 #          company_name = company_name_row['variable_value']
  
 #          # COMPANY PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_profile_row = user_table.search(variable='company_profile')[0]
 #          company_profile = company_profile_row['variable_value']
  
 #          # PRODUCT PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_url_row = user_table.search(variable='company_url')[0]
 #          company_url = company_url_row['variable_value']
  
 #          # PRODUCT NAME
 #          product_4_name = self.product_4_name_input.text
 #          product_4_name_row = user_table.search(variable='product_4_name_latest')[0]
 #          product_4_name_row['variable_value'] = product_4_name
  
 #          # PRODUCT EXCERPT / PREVIEW
 #          product_4_preview = self.product_profile_4_textbox.text
 #          product_4_latest = self.product_profile_4_textbox.text
 #          product_4_preview_row = user_table.search(variable='product_4_preview')[0]
 #          product_4_preview_row['variable_value'] = product_4_preview
 #          product_4_preview_row.update()
 #          # Save it as the latest as well
 #          product_4_latest_row = user_table.search(variable='product_4_latest')[0]
 #          product_4_latest_row['variable_value'] = product_4_preview
 #          product_4_latest_row.update()
  
 #          self.task_id = anvil.server.call('launch_deepdive_product_4_generator', company_name, company_profile, company_url, product_4_name, product_4_preview)
 #          print("Task ID:", self.task_id)
  
 #          # Loop to check the status of the background task
 #          while True:
 #              with anvil.server.no_loading_indicator:
  
 #                  # Check if the background task is complete
 #                  task_status = anvil.server.call('get_task_status', self.task_id)
 #                  print("Task status:", task_status)
  
 #                  if task_status is not None:
 #                      if task_status == "completed":
 #                          # Get the result of the background task
 #                          product_4_generation = anvil.server.call('get_task_result', self.task_id)
  
 #                          # Update the textbox with the result
 #                          print("Product:", product_4_generation)
 #                          self.product_profile_4_textbox.text = product_4_generation
  
 #                          # Save it in the table:
 #                          product_4_latest_row = user_table.search(variable='product_4_latest')[0]
 #                          product_4_latest_row['variable_value'] = product_4_generation
  
 #                          self.indeterminate_4.visible = False
 #                          break  # Exit the loop
  
 #                      elif task_status == "failed":
 #                          # Get the error message
 #                          task_error = anvil.server.call('get_task_result', self.task_id)
 #                          print("Task error:", task_error)
 #                          self.indeterminate_4.visible = False
 #                          break  # Exit the loop
  
 #                  # Sleep for 1 second before checking again
 #                  time.sleep(2)
  
 #  def generate_product_5_button_click(self, **event_args):
 #    with anvil.server.no_loading_indicator:
 #        # This method should handle the UI logic
 #        print("Deep Product Generator Initiated")
       
 #        # Stop the Function if there's no product name
 #        if not self.product_5_name_input.text:
 #          anvil.js.window.alert("Please name your product before generating the full description.")
 #          return
 #        else:
 #          self.indeterminate_5.visible = True

 #          # Load stuff
 #          current_user = anvil.users.get_user()
 #          user_table_name = current_user['user_id']
 #          # Get the table for the current user
 #          user_table = getattr(app_tables, user_table_name)
  
 #          # COMPANY PROFILE
 #          company_name_row = user_table.search(variable='company_name')[0]
 #          company_name = company_name_row['variable_value']
  
 #          # COMPANY PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_profile_row = user_table.search(variable='company_profile')[0]
 #          company_profile = company_profile_row['variable_value']
  
 #          # PRODUCT PROFILE
 #          # Retrieve the row with 'variable' column containing 'company_profile'
 #          company_url_row = user_table.search(variable='company_url')[0]
 #          company_url = company_url_row['variable_value']
  
 #          # PRODUCT NAME
 #          product_5_name = self.product_5_name_input.text
 #          product_5_name_row = user_table.search(variable='product_5_name_latest')[0]
 #          product_5_name_row['variable_value'] = product_5_name
  
 #          # PRODUCT EXCERPT / PREVIEW
 #          product_5_preview = self.product_profile_5_textbox.text
 #          product_5_latest = self.product_profile_5_textbox.text
 #          product_5_preview_row = user_table.search(variable='product_5_preview')[0]
 #          product_5_preview_row['variable_value'] = product_5_preview
 #          product_5_preview_row.update()
 #          # Save it as the latest as well
 #          product_5_latest_row = user_table.search(variable='product_5_latest')[0]
 #          product_5_latest_row['variable_value'] = product_5_preview
 #          product_5_latest_row.update()
  
 #          self.task_id = anvil.server.call('launch_deepdive_product_5_generator', company_name, company_profile, company_url, product_5_name, product_5_preview)
 #          print("Task ID:", self.task_id)
  
 #          # Loop to check the status of the background task
 #          while True:
 #              with anvil.server.no_loading_indicator:
  
 #                  # Check if the background task is complete
 #                  task_status = anvil.server.call('get_task_status', self.task_id)
 #                  print("Task status:", task_status)
  
 #                  if task_status is not None:
 #                      if task_status == "completed":
 #                          # Get the result of the background task
 #                          product_5_generation = anvil.server.call('get_task_result', self.task_id)
  
 #                          # Update the textbox with the result
 #                          print("Product:", product_5_generation)
 #                          self.product_profile_5_textbox.text = product_5_generation
  
 #                          # Save it in the table:
 #                          product_5_latest_row = user_table.search(variable='product_5_latest')[0]
 #                          product_5_latest_row['variable_value'] = product_5_generation
  
 #                          self.indeterminate_5.visible = False
 #                          break  # Exit the loop
  
 #                      elif task_status == "failed":
 #                          # Get the error message
 #                          task_error = anvil.server.call('get_task_result', self.task_id)
 #                          print("Task error:", task_error)
 #                          self.indeterminate_5.visible = False
 #                          break  # Exit the loop
  
 #                  # Sleep for 1 second before checking again
 #                  time.sleep(2)
                
 # # # Load the latest info
 #    # row_product_1_latest = user_table.search(variable='product_1_latest')
 #    # row_product_1_name_latest = user_table.search(variable='product_1_name_latest')
    
 #    # if row_product_1_latest:
 #    #     product_1_latest = row_product_1_latest[0]['variable_value']
 #    #     self.product_profile_1_textbox.text = product_1_latest
 #    #     product_1_name_latest = row_product_1_name_latest[0]['variable_value']
 #    #     self.product_1_name_input.text = product_1_name_latest
 #    # else:
 #    #     # Handle case where the row does not exist for the current user
 #    #     print("No row found for 'product_1_latest'")


      
 #  # def form_show(self, **event_args):
 #  #   # Load the company profile on form show
 #  #   self.company_profile_textbox.load_data()
 #  #   self.company_name_input.load_data()
 #  #   self.company_url_input.load_data()