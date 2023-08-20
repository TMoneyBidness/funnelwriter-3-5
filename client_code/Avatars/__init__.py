from ._anvil_designer import AvatarsTemplate
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

from ..BrandTone import BrandTone
############################################################################################################
# LOADING
class Avatars(AvatarsTemplate):
  def __init__(self, **properties):
    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    self.task_ids = []
    self.task_info = []
    task_info = []
    anvil.users.login_with_form()

    # Get the table for the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    self.all_avatars_product_1_button.visible = False
    self.all_avatars_product_2_button.visible = False
    self.all_avatars_product_3_button.visible = False
    self.all_avatars_product_4_button.visible = False
    self.all_avatars_product_5_button.visible = False

    self.indeterminate_10.visible = False
    self.indeterminate_20.visible = False
    self.indeterminate_30.visible = False
    self.indeterminate_40.visible = False
    self.indeterminate_50.visible = False

    self.add_product_1.visible = False
    self.add_product_2.visible = False 
    self.add_product_3.visible = False 
    self.add_product_4.visible = False 
    

    # Stop Timers
    for component in self.get_components():
        # Check if the component is a Timer
        if isinstance(component, anvil.Timer):
            # Stop the timer by setting its interval to None
            component.interval = None
          
    self.avatar_product_1_timer.enabled = False
    self.avatar_product_1_timer.interval = 0  
    self.avatar_product_2_timer.enabled = False
    self.avatar_product_2_timer.interval = 0
    self.avatar_product_3_timer.enabled = False
    self.avatar_product_3_timer.interval = 0  
    self.avatar_product_4_timer.enabled = False
    self.avatar_product_4_timer.interval = 0 
    self.avatar_product_5_timer.enabled = False
    self.avatar_product_5_timer.interval = 0  
    self.task_check_timer_regenerate_avatar_1_product_1.interval = 0
    self.task_check_timer_regenerate_avatar_2_product_1.interval = 0
    self.task_check_timer_regenerate_avatar_3_product_1.interval = 0
    self.task_check_timer_regenerate_avatar_1_product_2.interval = 0
    self.task_check_timer_regenerate_avatar_2_product_2.interval = 0
    self.task_check_timer_regenerate_avatar_3_product_2.interval = 0
    self.task_check_timer_regenerate_avatar_1_product_3.interval = 0
    self.task_check_timer_regenerate_avatar_2_product_3.interval = 0
    self.task_check_timer_regenerate_avatar_3_product_3.interval = 0
    self.task_check_timer_regenerate_avatar_1_product_4.interval = 0
    self.task_check_timer_regenerate_avatar_2_product_4.interval = 0
    self.task_check_timer_regenerate_avatar_3_product_4.interval = 0
    self.task_check_timer_regenerate_avatar_1_product_5.interval = 0
    self.task_check_timer_regenerate_avatar_2_product_5.interval = 0
    self.task_check_timer_regenerate_avatar_3_product_5.interval = 0

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Show Panels
    self.whole_panel.visible=True
    self.whole_panel_2.visible=True
    #Hide Panels of Products 2-5
    self.product_1_input_section.visible = False
    self.product_2_input_section.visible = False
    self.product_3_input_section.visible = False
    self.product_4_input_section.visible = False
    self.product_5_input_section.visible = False
        
    for i in range(1, 6):
      row_product_latest = user_table.search(variable=f'product_{i}_latest')
      # row_product_url_latest = user_table.search(variable=f'product_{i}_url')
        
      if row_product_latest:
          # Update the text box for the current product
          product_latest_name = row_product_latest[0]['variable_title']
          # product_latest_url = row_product_url_latest[0]['variable_value']

          getattr(self, f'product_{i}_name_input').text = product_latest_name
          # getattr(self, f'product_{i}_url').text = product_latest_url

          if product_latest_name:
            getattr(self, f'product_{i}_input_section').visible = True
            getattr(self, f'add_avatar_1_product_{i}').visible = True
            # if i != 1:
              # getattr(self, f'add_product_{i-1}').visible = False
              # pass

          
          # Now, load the avatars associated with that product. There may be 1 avatar only, or there are 3. The cells might be empty!
          # Load the avatars associated with that product
          for j in range(1, 4):
              row_avatar_product_latest = user_table.get(variable=f'avatar_{j}_product_{i}_latest')
              avatar_product_latest = row_avatar_product_latest['variable_value']
              avatar_product_latest_name = row_avatar_product_latest['variable_title']
      
              # Check if the avatar cell is not empty
              if avatar_product_latest and avatar_product_latest.strip():
                  getattr(self, f'avatar_{j}_product_{i}_input').text = avatar_product_latest
                  getattr(self, f'avatar_{j}_product_{i}_name').text = avatar_product_latest_name
                  getattr(self, f'avatar_{j}_product_{i}_input_section').visible = True
                  # Since the avatar cell exists, the button should be invisible
                  getattr(self, f'add_avatar_1_product_{i}').visible = False
                  
              else:
                  # Make the section invisible if the avatar cell is empty
                  getattr(self, f'avatar_{j}_product_{i}_input_section').visible = False

      # else:
      #   getattr(self, f'product_{i}_input_section').visible = False
                

    # Check if any of the final avatars are empty
    final_avatar_rows = [
        user_table.search(variable='avatar1')[0],
        user_table.search(variable='avatar2')[0],
        user_table.search(variable='avatar3')[0],
        user_table.search(variable='avatar4')[0],
        user_table.search(variable='avatar5')[0]]
    
    # Check if any of the avatar descriptions are empty
    if any(not row['variable_value'] for row in final_avatar_rows if row and 'variable_value' in row):
        # If any of the avatar descriptions are empty, disable the button
        self.nav_button_avatars_to_brand_tone.enabled = False
    else:
        # If all avatar descriptions are saved, enable the button
        self.nav_button_avatars_to_brand_tone.enabled = True

# ADDING PRODUCTS / AVATAR PANELS

# Base Panel
  def add_avatar_1_product_1_click(self, **event_args):
    self.avatar_1_product_1_input_section.visible = True
    self.add_avatar_1_product_1.visible = False
  def add_avatar_2_product_1_click(self, **event_args):
    self.avatar_2_product_1_input_section.visible = True
    self.add_avatar_2_product_1.visible = False
  def add_avatar_3_product_1_click(self, **event_args):
    self.avatar_3_product_1_input_section.visible = True
    self.add_avatar_3_product_1.visible = False 
  # def add_product_2_panel_click(self, **event_args):
  #   self.product_2_input_section.visible = True

# Panel 2 / Product 2
  def add_avatar_1_product_2_click(self, **event_args):
    self.avatar_1_product_2_input_section.visible = True
    self.add_avatar_1_product_2.visible = False
  def add_avatar_2_product_2_click(self, **event_args):
    self.avatar_2_product_2_input_section.visible = True
    self.add_avatar_2_product_2.visible = False
  def add_avatar_3_product_2_click(self, **event_args):
    self.avatar_3_product_2_input_section.visible = True
    self.add_avatar_2_product_2.visible = False
    self.add_avatar_3_product_2.visible = False
  # def add_product_3_panel_click(self, **event_args):
  #   self.product_3_input_section.visible = True

# Panel 3 / Product 3
  def add_avatar_1_product_3_click(self, **event_args):
    self.avatar_1_product_3_input_section.visible = True
    self.add_avatar_1_product_3.visible = False
  def add_avatar_2_product_3_click(self, **event_args):
    self.avatar_2_product_3_input_section.visible = True
    self.add_avatar_2_product_3.visible = False
  def add_avatar_3_product_3_click(self, **event_args):
    self.avatar_3_product_3_input_section.visible = True
    self.add_avatar_2_product_3.visible = False
    self.add_avatar_3_product_3.visible = False
  # def add_product_4_panel_click(self, **event_args):
  #   self.product_4_input_section.visible = True
    
# Panel 4 / Product 4
  def add_avatar_1_product_4_click(self, **event_args):
    self.avatar_1_product_4_input_section.visible = True
    self.add_avatar_1_product_4.visible = False
  def add_avatar_2_product_4_click(self, **event_args):
    self.avatar_2_product_4_input_section.visible = True
    self.add_avatar_2_product_4.visible = False
  def add_avatar_3_product_4_click(self, **event_args):
    self.avatar_3_product_4_input_section.visible = True
    self.add_avatar_2_product_4.visible = False
    self.add_avatar_3_product_4.visible = False
  # def add_product_5_panel_click(self, **event_args):
  #   self.product_5_input_section.visible = True

# Panel 5 / Product 5
  def add_avatar_1_product_5_click(self, **event_args):
    self.avatar_1_product_5_input_section.visible = True
    self.add_avatar_1_product_5.visible = False
  def add_avatar_2_product_5_click(self, **event_args):
    self.avatar_2_product_5_input_section.visible = True
    self.add_avatar_2_product_5.visible = False
  def add_avatar_3_product_5_click(self, **event_args):
    self.avatar_3_product_5_input_section.visible = True
    self.add_avatar_2_product_5.visible = False
    self.add_avatar_3_product_5.visible = False 

#-- GENERATE THE AVATAR DEEP DIVES FOR EACH PRODUCT ------------#######################################################

#######----------- PRODUCT 1 --------##########
  def all_avatars_product_1_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
         
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_1_name_row = user_table.search(variable='product_1')[0]
      product_1_name = product_1_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_1_profile_row = user_table.search(variable='product_1')[0]
      product_1_profile = product_1_profile_row['variable_title']

       # START THE LOOPS
      task_ids = []
      self.task_info.clear() 
      
      for i in range(1, 4):
            avatar_input_text = getattr(self, f'avatar_{i}_product_1_input').text

            # Check input and skip if empty
            if not avatar_input_text or not avatar_input_text.strip():
                print(f"Skipping avatar {i} due to empty input.")
                continue

            # Update rows in the database
            for variable_name in [f'avatar_{i}_product_1_preview', f'avatar_{i}_product_1_latest']:
                rows = user_table.search(variable=variable_name)
                if rows:
                    row = rows[0]
                    row['variable_value'] = avatar_input_text
                    row['variable_title'] = getattr(self, f'avatar_{i}_product_1_name').text
                    row.update()
                else:
                    print(f"No database entry for {variable_name}")

            # Launch the background task
            task_id = anvil.server.call(f'launch_deepdive_avatar_{i}_product_1_generator', product_1_name, product_1_profile, getattr(self, f'avatar_{i}_product_1_name').text, avatar_input_text)
            print(f"Task ID for avatar_{i}_product_1:", task_id)
            self.task_info.append((task_id, i))

      self.avatar_product_1_timer.enabled = True
      print(f"self.avatar_product_1_timer started")

  def avatar_product_1_timer_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
        all_tasks_complete = True  
        tasks_to_remove = []
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
      
        for task_id, avatar_num in self.task_info:
            status = anvil.server.call('get_task_status', task_id)
            
            if status == 'completed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_1 completed!")
                
                # Get the result of the background task
                avatar_generation = anvil.server.call('get_task_result', task_id)
                
                # Update the textbox with the result
                getattr(self, f'avatar_{avatar_num}_product_1_input').text = avatar_generation
                
                if avatar_num == 1:  # Only for avatar_1; adjust as needed
                    self.indeterminate_10.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_1_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_1_name').text
                    avatar_latest_row.update()

                if avatar_num == 2:  # Only for avatar_1; adjust as needed
                    self.indeterminate_10.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_1_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_1_name').text
                    avatar_latest_row.update()

                if avatar_num == 3:  # Only for avatar_1; adjust as needed
                    self.indeterminate_10.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_1_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_1_name').text
                    avatar_latest_row.update()
                
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'failed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_1 failed!")
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'not_found':
                print(f"Task {task_id} for avatar_{avatar_num}_product_1 not found!")
                tasks_to_remove.append((task_id, avatar_num))
                
            else:
                print(f"Task {task_id} for avatar_{avatar_num}_product_1 still running...")
                all_tasks_complete = False
    
        # Remove tasks that are completed, failed, or not found
        for task in tasks_to_remove:
            self.task_info.remove(task)
    
        # If all tasks are complete, you can stop the timer
        if all_tasks_complete:
          self.avatar_product_1_timer.enabled = False

#######----------- Deep dive Avatars--------##########
  def regenerate_avatar_1_product_1_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_1_name_row = user_table.search(variable='product_1')[0]
      product_1_name = product_1_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_1_profile_row = user_table.search(variable='product_1')[0]
      product_1_profile = product_1_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_1_product_1_latest_row = user_table.get(variable='avatar_1_product_1_latest')
      avatar_1_product_1_latest_row['variable_value'] = None
      avatar_1_product_1_latest_row.update()

      #Update the avatar preview
      avatar_1_product_1_preview_row = user_table.get(variable='avatar_1_product_1_preview')
      avatar_1_product_1_preview_row['variable_value'] = self.avatar_1_product_1_input.text # Avatar preview description
      avatar_1_product_1_preview_row['variable_title'] = self.avatar_1_product_1_name.text # Avatar name description
      avatar_1_product_1_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_1_product_1_generator', product_1_name, product_1_profile, self.avatar_1_product_1_name.text, self.avatar_1_product_1_input.text)
      print(f"Task ID for avatar_1_product_1:", task_id)

      self.indeterminate_10.visible = True
      self.task_check_timer_regenerate_avatar_1_product_1.enabled = True
      self.task_check_timer_regenerate_avatar_1_product_1.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_1_product_1(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_1_product_1_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 1 Product 1 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 1 Product 1 Regenerated!")
            self.task_check_timer_regenerate_avatar_1_product_1.enabled = False
            self.task_check_timer_regenerate_avatar_1_product_1.interval = 0
            self.indeterminate_10.visible = False
                
            # Update the box
            avatar_1_product_1_input = row['variable_value'] 
            self.avatar_1_product_1_input.text = avatar_1_product_1_input

##----------- Deep dive Avatars 2 ------##########          
  def regenerate_avatar_2_product_1_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_1_name_row = user_table.search(variable='product_1')[0]
      product_1_name = product_1_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_1_profile_row = user_table.search(variable='product_1')[0]
      product_1_profile = product_1_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_2_product_1_latest_row = user_table.get(variable='avatar_1_product_1_latest')
      avatar_2_product_1_latest_row['variable_value'] = None
      avatar_2_product_1_latest_row.update()

      #Update the avatar preview
      avatar_2_product_1_preview_row = user_table.get(variable='avatar_2_product_1_preview')
      avatar_2_product_1_preview_row['variable_value'] = self.avatar_2_product_1_input.text # Avatar preview description
      avatar_2_product_1_preview_row['variable_title'] = self.avatar_2_product_1_name.text # Avatar name description
      avatar_2_product_1_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_2_product_1_generator', product_1_name, product_1_profile, self.avatar_2_product_1_name.text, self.avatar_2_product_1_input.text)
      print(f"Task ID for avatar_2_product_1:", task_id)

      self.indeterminate_10.visible = True
      self.task_check_timer_regenerate_avatar_2_product_1.enabled = True
      self.task_check_timer_regenerate_avatar_2_product_1.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_2_product_1(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_2_product_1_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 2 Product 1 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 2 Product 1 Regenerated!")
            self.task_check_timer_regenerate_avatar_2_product_1.enabled = False
            self.task_check_timer_regenerate_avatar_2_product_1.interval = 0
            self.indeterminate_10.visible = False
                
            # Update the box
            avatar_2_product_1_input = row['variable_value'] 
            self.avatar_2_product_1_input.text = avatar_2_product_1_input

##----------- Deep dive Avatars 3 ------##########          
  def regenerate_avatar_3_product_1_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_1_name_row = user_table.search(variable='product_1')[0]
      product_1_name = product_1_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_1_profile_row = user_table.search(variable='product_1')[0]
      product_1_profile = product_1_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_3_product_1_latest_row = user_table.get(variable='avatar_3_product_1_latest')
      avatar_3_product_1_latest_row['variable_value'] = None
      avatar_3_product_1_latest_row.update()

      #Update the avatar preview
      avatar_3_product_1_preview_row = user_table.get(variable='avatar_3_product_1_preview')
      avatar_3_product_1_preview_row['variable_value'] = self.avatar_3_product_1_input.text # Avatar preview description
      avatar_3_product_1_preview_row['variable_title'] = self.avatar_3_product_1_name.text # Avatar name description
      avatar_3_product_1_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_3_product_1_generator', product_1_name, product_1_profile, self.avatar_3_product_1_name.text, self.avatar_3_product_1_input.text)
      print(f"Task ID for avatar_3_product_1:", task_id)

      self.indeterminate_10.visible = True
      self.task_check_timer_regenerate_avatar_3_product_1.enabled = True
      self.task_check_timer_regenerate_avatar_3_product_1.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_3_product_1(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_3_product_1_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 3 Product 1 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 3 Product 1 Regenerated!")
            self.task_check_timer_regenerate_avatar_3_product_1.enabled = False
            self.task_check_timer_regenerate_avatar_3_product_1.interval = 0
            self.indeterminate_10.visible = False
                
            # Update the box
            avatar_3_product_1_input = row['variable_value'] 
            self.avatar_3_product_1_input.text = avatar_3_product_1_input
          
#### PRODUCT 2 -----##
  def all_avatars_product_2_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_20.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_2_name_row = user_table.search(variable='product_2')[0]
      product_2_name = product_2_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_2_profile_row = user_table.search(variable='product_2')[0]
      product_2_profile = product_2_profile_row['variable_title']
  
        # START THE LOOPS
      task_ids = []
      self.task_info.clear() 
      
      for i in range(1, 4):
            avatar_input_text = getattr(self, f'avatar_{i}_product_2_input').text
  
            # Check input and skip if empty
            if not avatar_input_text or not avatar_input_text.strip():
                print(f"Skipping avatar {i} due to empty input.")
                continue
  
            # Update rows in the database
            for variable_name in [f'avatar_{i}_product_2_preview', f'avatar_{i}_product_2_latest']:
                rows = user_table.search(variable=variable_name)
                if rows:
                    row = rows[0]
                    row['variable_value'] = avatar_input_text
                    row['variable_title'] = getattr(self, f'avatar_{i}_product_2_name').text
                    row.update()
                else:
                    print(f"No database entry for {variable_name}")
  
            # Launch the background task
            task_id = anvil.server.call(f'launch_deepdive_avatar_{i}_product_2_generator', product_2_name, product_2_profile, getattr(self, f'avatar_{i}_product_2_name').text, avatar_input_text)
            print(f"Task ID for avatar_{i}_product_2:", task_id)
            self.task_info.append((task_id, i))
  
      self.avatar_product_2_timer.enabled = True
      print(f"self.avatar_product_2_timer started")

  def avatar_product_2_timer_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
        all_tasks_complete = True  
        tasks_to_remove = []
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
      
        for task_id, avatar_num in self.task_info:
            status = anvil.server.call('get_task_status', task_id)
            
            if status == 'completed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_2 completed!")
                
                # Get the result of the background task
                avatar_generation = anvil.server.call('get_task_result', task_id)
                
                # Update the textbox with the result
                getattr(self, f'avatar_{avatar_num}_product_2_input').text = avatar_generation
                
                if avatar_num == 1:  # Only for avatar_1; adjust as needed
                    self.indeterminate_20.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_2_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_2_name').text
                    avatar_latest_row.update()

                if avatar_num == 2:  # Only for avatar_1; adjust as needed
                    self.indeterminate_20.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_2_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_2_name').text
                    avatar_latest_row.update()

                if avatar_num == 3:  # Only for avatar_1; adjust as needed
                    self.indeterminate_20.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_2_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_2_name').text
                    avatar_latest_row.update()
                
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'failed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_2 failed!")
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'not_found':
                print(f"Task {task_id} for avatar_{avatar_num}_product_2 not found!")
                tasks_to_remove.append((task_id, avatar_num))
                
            else:
                print(f"Task {task_id} for avatar_{avatar_num}_product_2 still running...")
                all_tasks_complete = False
    
        # Remove tasks that are completed, failed, or not found
        for task in tasks_to_remove:
            self.task_info.remove(task)
    
        # If all tasks are complete, you can stop the timer
        if all_tasks_complete:
          self.avatar_product_2_timer.enabled = False
          self.avatar_product_2_timer.interval = 0

#######----------- Deep dive Avatars--------##########
  def regenerate_avatar_1_product_2_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_2_name_row = user_table.search(variable='product_2')[0]
      product_2_name = product_2_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_2_profile_row = user_table.search(variable='product_2')[0]
      product_2_profile = product_2_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_1_product_2_latest_row = user_table.get(variable='avatar_1_product_2_latest')
      avatar_1_product_2_latest_row['variable_value'] = None
      avatar_1_product_2_latest_row.update()

      #Update the avatar preview
      avatar_1_product_2_preview_row = user_table.get(variable='avatar_1_product_2_preview')
      avatar_1_product_2_preview_row['variable_value'] = self.avatar_1_product_2_input.text # Avatar preview description
      avatar_1_product_2_preview_row['variable_title'] = self.avatar_1_product_2_name.text # Avatar name description
      avatar_1_product_2_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_1_product_2_generator', product_2_name, product_2_profile, self.avatar_1_product_2_name.text, self.avatar_1_product_2_input.text)
      print(f"Task ID for avatar_1_product_2:", task_id)

      self.indeterminate_20.visible = True
      self.task_check_timer_regenerate_avatar_1_product_2.enabled = True
      self.task_check_timer_regenerate_avatar_1_product_2.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_1_product_2(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_1_product_2_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 1 Product 2 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 1 Product 2 Regenerated!")
            self.task_check_timer_regenerate_avatar_1_product_2.enabled = False
            self.task_check_timer_regenerate_avatar_1_product_2.interval = 0
            self.indeterminate_20.visible = False
                
            # Update the box
            avatar_1_product_2_input = row['variable_value'] 
            self.avatar_1_product_2_input.text = avatar_1_product_2_input

##----------- Deep dive Avatars 2 ------##########          
  def regenerate_avatar_2_product_2_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_20.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_2_name_row = user_table.search(variable='product_2')[0]
      product_2_name = product_2_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_2_profile_row = user_table.search(variable='product_2')[0]
      product_2_profile = product_2_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_2_product_2_latest_row = user_table.get(variable='avatar_2_product_2_latest')
      avatar_2_product_2_latest_row['variable_value'] = None
      avatar_2_product_2_latest_row.update()

      #Update the avatar preview
      avatar_2_product_2_preview_row = user_table.get(variable='avatar_2_product_2_preview')
      avatar_2_product_2_preview_row['variable_value'] = self.avatar_2_product_2_input.text # Avatar preview description
      avatar_2_product_2_preview_row['variable_title'] = self.avatar_2_product_2_name.text # Avatar name description
      avatar_2_product_2_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_2_product_2_generator', product_2_name, product_2_profile, self.avatar_2_product_2_name.text, self.avatar_2_product_2_input.text)
      print(f"Task ID for avatar_2_product_2:", task_id)

      self.indeterminate_20.visible = True
      self.task_check_timer_regenerate_avatar_2_product_2.enabled = True
      self.task_check_timer_regenerate_avatar_2_product_2.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_2_product_2(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_2_product_2_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 2 Product 2 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 2 Product 2 Regenerated!")
            self.task_check_timer_regenerate_avatar_2_product_2.enabled = False
            self.task_check_timer_regenerate_avatar_2_product_2.interval = 0
            self.indeterminate_20.visible = False
                
            # Update the box
            avatar_2_product_2_input = row['variable_value'] 
            self.avatar_2_product_2_input.text = avatar_2_product_2_input

##----------- Deep dive Avatars 3 ------##########          
  def regenerate_avatar_3_product_2_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_2_name_row = user_table.search(variable='product_2')[0]
      product_2_name = product_2_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_2_profile_row = user_table.search(variable='product_2')[0]
      product_2_profile = product_2_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_3_product_2_latest_row = user_table.get(variable='avatar_3_product_2_latest')
      avatar_3_product_2_latest_row['variable_value'] = None
      avatar_3_product_2_latest_row.update()

      #Update the avatar preview
      avatar_3_product_2_preview_row = user_table.get(variable='avatar_3_product_2_preview')
      avatar_3_product_2_preview_row['variable_value'] = self.avatar_3_product_2_input.text # Avatar preview description
      avatar_3_product_2_preview_row['variable_title'] = self.avatar_3_product_2_name.text # Avatar name description
      avatar_3_product_2_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_3_product_2_generator', product_2_name, product_2_profile, self.avatar_3_product_2_name.text, self.avatar_3_product_2_input.text)
      print(f"Task ID for avatar_3_product_2:", task_id)

      self.indeterminate_20.visible = True
      self.task_check_timer_regenerate_avatar_3_product_2.enabled = True
      self.task_check_timer_regenerate_avatar_3_product_2.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_3_product_2(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_3_product_2_latest')
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 3 Product 2 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 3 Product 2 Regenerated!")
            self.task_check_timer_regenerate_avatar_3_product_2.enabled = False
            self.task_check_timer_regenerate_avatar_3_product_2.interval = 0
            self.indeterminate_20.visible = False
                
            # Update the box
            avatar_3_product_2_input = row['variable_value'] 
            self.avatar_3_product_2_input.text = avatar_3_product_2_input


#### PRODUCT 3 -----##
  def all_avatars_product_3_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_30.visible = True
         
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_3_name_row = user_table.search(variable='product_3')[0]
      product_3_name = product_3_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_3_profile_row = user_table.search(variable='product_3')[0]
      product_3_profile = product_3_profile_row['variable_title']

       # START THE LOOPS
      task_ids = []
      self.task_info.clear() 
      
      for i in range(1, 4):
            avatar_input_text = getattr(self, f'avatar_{i}_product_3_input').text

            # Check input and skip if empty
            if not avatar_input_text or not avatar_input_text.strip():
                print(f"Skipping avatar {i} due to empty input.")
                continue

            # Update rows in the database
            for variable_name in [f'avatar_{i}_product_3_preview', f'avatar_{i}_product_3_latest']:
                rows = user_table.search(variable=variable_name)
                if rows:
                    row = rows[0]
                    row['variable_value'] = avatar_input_text
                    row['variable_title'] = getattr(self, f'avatar_{i}_product_3_name').text
                    row.update()
                else:
                    print(f"No database entry for {variable_name}")

            # Launch the background task
            task_id = anvil.server.call(f'launch_deepdive_avatar_{i}_product_3_generator', product_3_name, product_3_profile, getattr(self, f'avatar_{i}_product_3_name').text, avatar_input_text)
            print(f"Task ID for avatar_{i}_product_3:", task_id)
            self.task_info.append((task_id, i))

      self.avatar_product_3_timer.enabled = True
      print(f"self.avatar_product_3_timer started")
      
  def avatar_product_3_timer_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
        all_tasks_complete = True  
        tasks_to_remove = []
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
      
        for task_id, avatar_num in self.task_info:
            status = anvil.server.call('get_task_status', task_id)
            
            if status == 'completed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_3 completed!")
                
                # Get the result of the background task
                avatar_generation = anvil.server.call('get_task_result', task_id)
                
                # Update the textbox with the result
                getattr(self, f'avatar_{avatar_num}_product_3_input').text = avatar_generation
                
                if avatar_num == 1:  # Only for avatar_1; adjust as needed
                    self.indeterminate_30.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_3_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_3_name').text
                    avatar_latest_row.update()

                if avatar_num == 2:  # Only for avatar_1; adjust as needed
                    self.indeterminate_30.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_3_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_3_name').text
                    avatar_latest_row.update()

                if avatar_num == 3:  # Only for avatar_1; adjust as needed
                    self.indeterminate_10.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_3_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_3_name').text
                    avatar_latest_row.update()
                
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'failed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_3 failed!")
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'not_found':
                print(f"Task {task_id} for avatar_{avatar_num}_product_3 not found!")
                tasks_to_remove.append((task_id, avatar_num))
                
            else:
                print(f"Task {task_id} for avatar_{avatar_num}_product_3 still running...")
                all_tasks_complete = False
    
        # Remove tasks that are completed, failed, or not found
        for task in tasks_to_remove:
            self.task_info.remove(task)
    
        # If all tasks are complete, you can stop the timer
        if all_tasks_complete:
          self.avatar_product_3_timer.enabled = False
          self.avatar_product_3_timer.interval = 0

#######----------- Deep dive Avatars--------##########
  def regenerate_avatar_1_product_3_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_3_name_row = user_table.search(variable='product_3')[0]
      product_3_name = product_3_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_3_profile_row = user_table.search(variable='product_3')[0]
      product_3_profile = product_3_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_1_product_3_latest_row = user_table.get(variable='avatar_1_product_3_latest')
      avatar_1_product_3_latest_row['variable_value'] = None
      avatar_1_product_3_latest_row.update()

      #Update the avatar preview
      avatar_1_product_3_preview_row = user_table.get(variable='avatar_1_product_3_preview')
      avatar_1_product_3_preview_row['variable_value'] = self.avatar_1_product_3_input.text # Avatar preview description
      avatar_1_product_3_preview_row['variable_title'] = self.avatar_1_product_3_name.text # Avatar name description
      avatar_1_product_3_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_1_product_3_generator', product_3_name, product_3_profile, self.avatar_1_product_3_name.text, self.avatar_1_product_3_input.text)
      print(f"Task ID for avatar_1_product_3:", task_id)

      self.indeterminate_30.visible = True
      self.task_check_timer_regenerate_avatar_1_product_3.enabled = True
      self.task_check_timer_regenerate_avatar_1_product_3.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_1_product_3(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_1_product_3_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 1 Product 3 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 1 Product 3 Regenerated!")
            self.task_check_timer_regenerate_avatar_1_product_3.enabled = False
            self.task_check_timer_regenerate_avatar_1_product_3.interval = 0
            self.indeterminate_30.visible = False
                
            # Update the box
            avatar_1_product_3_input = row['variable_value'] 
            self.avatar_1_product_3_input.text = avatar_1_product_3_input

##----------- Deep dive Avatars 2 ------##########          
  def regenerate_avatar_2_product_3_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_30.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_3_name_row = user_table.search(variable='product_3')[0]
      product_3_name = product_3_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_3_profile_row = user_table.search(variable='product_3')[0]
      product_3_profile = product_3_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_2_product_3_latest_row = user_table.get(variable='avatar_2_product_3_latest')
      avatar_2_product_3_latest_row['variable_value'] = None
      avatar_2_product_3_latest_row.update()

      #Update the avatar preview
      avatar_2_product_3_preview_row = user_table.get(variable='avatar_2_product_3_preview')
      avatar_2_product_3_preview_row['variable_value'] = self.avatar_2_product_3_input.text # Avatar preview description
      avatar_2_product_3_preview_row['variable_title'] = self.avatar_2_product_3_name.text # Avatar name description
      avatar_2_product_3_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_2_product_3_generator', product_3_name, product_3_profile, self.avatar_2_product_3_name.text, self.avatar_2_product_3_input.text)
      print(f"Task ID for avatar_2_product_3:", task_id)

      self.indeterminate_20.visible = True
      self.task_check_timer_regenerate_avatar_2_product_3.enabled = True
      self.task_check_timer_regenerate_avatar_2_product_3.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_2_product_3(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_2_product_3_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 2 Product 3 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 2 Product 3 Regenerated!")
            self.task_check_timer_regenerate_avatar_2_product_3.enabled = False
            self.task_check_timer_regenerate_avatar_2_product_3.interval = 0
            self.indeterminate_30.visible = False
                
            # Update the box
            avatar_2_product_3_input = row['variable_value'] 
            self.avatar_2_product_3_input.text = avatar_2_product_3_input

##----------- Deep dive Avatars 3 ------##########          
  def regenerate_avatar_3_product_3_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_3_name_row = user_table.search(variable='product_3')[0]
      product_3_name = product_3_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_3_profile_row = user_table.search(variable='product_3')[0]
      product_3_profile = product_3_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_3_product_3_latest_row = user_table.get(variable='avatar_3_product_3_latest')
      avatar_3_product_3_latest_row['variable_value'] = None
      avatar_3_product_3_latest_row.update()

      #Update the avatar preview
      avatar_3_product_3_preview_row = user_table.get(variable='avatar_3_product_3_preview')
      avatar_3_product_3_preview_row['variable_value'] = self.avatar_3_product_3_input.text # Avatar preview description
      avatar_3_product_3_preview_row['variable_title'] = self.avatar_3_product_3_name.text # Avatar name description
      avatar_3_product_3_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_3_product_3_generator', product_3_name, product_3_profile, self.avatar_3_product_3_name.text, self.avatar_3_product_3_input.text)
      print(f"Task ID for avatar_3_product_3:", task_id)

      self.indeterminate_30.visible = True
      self.task_check_timer_regenerate_avatar_3_product_3.enabled = True
      self.task_check_timer_regenerate_avatar_3_product_3.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_3_product_3(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_3_product_3_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 3 Product 3 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 3 Product 3 Regenerated!")
            self.task_check_timer_regenerate_avatar_3_product_3.enabled = False
            self.task_check_timer_regenerate_avatar_3_product_3.interval = 0
            self.indeterminate_30.visible = False
                
            # Update the box
            avatar_3_product_3_input = row['variable_value'] 
            self.avatar_3_product_3_input.text = avatar_3_product_3_input


#### PRODUCT 4 -----##
  def all_avatars_product_4_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_40.visible = True
         
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_4_name_row = user_table.search(variable='product_4')[0]
      product_4_name = product_4_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_4_profile_row = user_table.search(variable='product_4')[0]
      product_4_profile = product_4_profile_row['variable_title']

       # START THE LOOPS
      task_ids = []
      self.task_info.clear() 
      
      for i in range(1, 4):
            avatar_input_text = getattr(self, f'avatar_{i}_product_4_input').text

            # Check input and skip if empty
            if not avatar_input_text or not avatar_input_text.strip():
                print(f"Skipping avatar {i} due to empty input.")
                continue

            # Update rows in the database
            for variable_name in [f'avatar_{i}_product_4_preview', f'avatar_{i}_product_4_latest']:
                rows = user_table.search(variable=variable_name)
                if rows:
                    row = rows[0]
                    row['variable_value'] = avatar_input_text
                    row['variable_title'] = getattr(self, f'avatar_{i}_product_4_name').text
                    row.update()
                else:
                    print(f"No database entry for {variable_name}")

            # Launch the background task
            task_id = anvil.server.call(f'launch_deepdive_avatar_{i}_product_4_generator', product_4_name, product_4_profile, getattr(self, f'avatar_{i}_product_4_name').text, avatar_input_text)
            print(f"Task ID for avatar_{i}_product_4:", task_id)
            self.task_info.append((task_id, i))

      self.avatar_product_4_timer.enabled = True
      print(f"self.avatar_product_4_timer started")

  def avatar_product_4_timer_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
        all_tasks_complete = True  
        tasks_to_remove = []
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
      
        for task_id, avatar_num in self.task_info:
            status = anvil.server.call('get_task_status', task_id)
            
            if status == 'completed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_4 completed!")
                
                # Get the result of the background task
                avatar_generation = anvil.server.call('get_task_result', task_id)
                
                # Update the textbox with the result
                getattr(self, f'avatar_{avatar_num}_product_1_input').text = avatar_generation
                
                if avatar_num == 1:  # Only for avatar_1; adjust as needed
                    self.indeterminate_40.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_4_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_4_name').text
                    avatar_latest_row.update()

                if avatar_num == 2:  # Only for avatar_4; adjust as needed
                    self.indeterminate_40.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_4_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_4_name').text
                    avatar_latest_row.update()

                if avatar_num == 3:  # Only for avatar_4; adjust as needed
                    self.indeterminate_40.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_4_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_4_name').text
                    avatar_latest_row.update()
                
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'failed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_4 failed!")
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'not_found':
                print(f"Task {task_id} for avatar_{avatar_num}_product_4 not found!")
                tasks_to_remove.append((task_id, avatar_num))
                
            else:
                print(f"Task {task_id} for avatar_{avatar_num}_product_4 still running...")
                all_tasks_complete = False
    
        # Remove tasks that are completed, failed, or not found
        for task in tasks_to_remove:
            self.task_info.remove(task)
    
        # If all tasks are complete, you can stop the timer
        if all_tasks_complete:
          self.avatar_product_4_timer.enabled = False
          self.avatar_product_4_timer.interval = 0

#######----------- Deep dive Avatars--------##########
  def regenerate_avatar_1_product_4_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_40.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_4_name_row = user_table.search(variable='product_4')[0]
      product_4_name = product_4_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_4_profile_row = user_table.search(variable='product_4')[0]
      product_4_profile = product_4_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_1_product_4_latest_row = user_table.get(variable='avatar_1_product_4_latest')
      avatar_1_product_4_latest_row['variable_value'] = None
      avatar_1_product_4_latest_row.update()

      #Update the avatar preview
      avatar_1_product_4_preview_row = user_table.get(variable='avatar_1_product_4_preview')
      avatar_1_product_4_preview_row['variable_value'] = self.avatar_1_product_4_input.text # Avatar preview description
      avatar_1_product_4_preview_row['variable_title'] = self.avatar_1_product_4_name.text # Avatar name description
      avatar_1_product_4_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_1_product_4_generator', product_4_name, product_4_profile, self.avatar_1_product_4_name.text, self.avatar_1_product_4_input.text)
      print(f"Task ID for avatar_1_product_2:", task_id)

      self.indeterminate_40.visible = True
      self.task_check_timer_regenerate_avatar_1_product_4.enabled = True
      self.task_check_timer_regenerate_avatar_1_product_4.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_1_product_4(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_1_product_4_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 1 Product 4 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 1 Product 4 Regenerated!")
            self.task_check_timer_regenerate_avatar_1_product_4.enabled = False
            self.task_check_timer_regenerate_avatar_1_product_4.interval = 0
            self.indeterminate_40.visible = False
                
            # Update the box
            avatar_1_product_4_input = row['variable_value'] 
            self.avatar_1_product_4_input.text = avatar_1_product_4_input

##----------- Deep dive Avatars 2 ------##########          
  def regenerate_avatar_2_product_4_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_40.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_4_name_row = user_table.search(variable='product_4')[0]
      product_4_name = product_4_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_4_profile_row = user_table.search(variable='product_4')[0]
      product_4_profile = product_4_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_2_product_4_latest_row = user_table.get(variable='avatar_2_product_4_latest')
      avatar_2_product_4_latest_row['variable_value'] = None
      avatar_2_product_4_latest_row.update()

      #Update the avatar preview
      avatar_2_product_4_preview_row = user_table.get(variable='avatar_2_product_4_preview')
      avatar_2_product_4_preview_row['variable_value'] = self.avatar_2_product_4_input.text # Avatar preview description
      avatar_2_product_4_preview_row['variable_title'] = self.avatar_2_product_4_name.text # Avatar name description
      avatar_2_product_4_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_2_product_2_generator', product_4_name, product_4_profile, self.avatar_2_product_4_name.text, self.avatar_2_product_4_input.text)
      print(f"Task ID for avatar_2_product_4:", task_id)

      self.indeterminate_40.visible = True
      self.task_check_timer_regenerate_avatar_2_product_4.enabled = True
      self.task_check_timer_regenerate_avatar_2_product_4.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_2_product_4(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_2_product_4_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 2 Product 4 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 2 Product 4 Regenerated!")
            self.task_check_timer_regenerate_avatar_2_product_4.enabled = False
            self.task_check_timer_regenerate_avatar_2_product_4.interval = 0
            self.indeterminate_40.visible = False
                
            # Update the box
            avatar_2_product_4_input = row['variable_value'] 
            self.avatar_2_product_4_input.text = avatar_2_product_4_input

##----------- Deep dive Avatars 3 ------##########          
  def regenerate_avatar_3_product_4_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_4_name_row = user_table.search(variable='product_4')[0]
      product_4_name = product_4_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_4_profile_row = user_table.search(variable='product_4')[0]
      product_4_profile = product_4_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_3_product_4_latest_row = user_table.get(variable='avatar_3_product_4_latest')
      avatar_3_product_4_latest_row['variable_value'] = None
      avatar_3_product_4_latest_row.update()

      #Update the avatar preview
      avatar_3_product_4_preview_row = user_table.get(variable='avatar_3_product_4_preview')
      avatar_3_product_4_preview_row['variable_value'] = self.avatar_3_product_4_input.text # Avatar preview description
      avatar_3_product_4_preview_row['variable_title'] = self.avatar_3_product_4_name.text # Avatar name description
      avatar_3_product_4_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_3_product_4_generator', product_4_name, product_4_profile, self.avatar_3_product_4_name.text, self.avatar_3_product_4_input.text)
      print(f"Task ID for avatar_3_product_4:", task_id)

      self.indeterminate_40.visible = True
      self.task_check_timer_regenerate_avatar_3_product_4.enabled = True
      self.task_check_timer_regenerate_avatar_3_product_4.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_3_product_4(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_3_product_4_latest')
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 3 Product 4 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 3 Product 4 Regenerated!")
            self.task_check_timer_regenerate_avatar_3_product_4.enabled = False
            self.task_check_timer_regenerate_avatar_3_product_4.interval = 0
            self.indeterminate_40.visible = False
                
            # Update the box
            avatar_3_product_4_input = row['variable_value'] 
            self.avatar_3_product_4_input.text = avatar_3_product_4_input


#### PRODUCT 5 -----##
  def all_avatars_product_5_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_50.visible = True
         
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_5_name_row = user_table.search(variable='product_5')[0]
      product_5_name = product_5_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_5_profile_row = user_table.search(variable='product_5')[0]
      product_5_profile = product_5_profile_row['variable_title']

       # START THE LOOPS
      task_ids = []
      self.task_info.clear() 
      
      for i in range(1, 4):
            avatar_input_text = getattr(self, f'avatar_{i}_product_5_input').text

            # Check input and skip if empty
            if not avatar_input_text or not avatar_input_text.strip():
                print(f"Skipping avatar {i} due to empty input.")
                continue

            # Update rows in the database
            for variable_name in [f'avatar_{i}_product_5_preview', f'avatar_{i}_product_5_latest']:
                rows = user_table.search(variable=variable_name)
                if rows:
                    row = rows[0]
                    row['variable_value'] = avatar_input_text
                    row['variable_title'] = getattr(self, f'avatar_{i}_product_5_name').text
                    row.update()
                else:
                    print(f"No database entry for {variable_name}")

            # Launch the background task
            task_id = anvil.server.call(f'launch_deepdive_avatar_{i}_product_5_generator', product_5_name, product_5_profile, getattr(self, f'avatar_{i}_product_5_name').text, avatar_input_text)
            print(f"Task ID for avatar_{i}_product_5:", task_id)
            self.task_info.append((task_id, i))

      self.avatar_product_5_timer.enabled = True
      print(f"self.avatar_product_5_timer started")

  def avatar_product_5_timer_tick(self, **event_args):
    with anvil.server.no_loading_indicator:
        all_tasks_complete = True  
        tasks_to_remove = []
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
      
        for task_id, avatar_num in self.task_info:
            status = anvil.server.call('get_task_status', task_id)
            
            if status == 'completed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_5 completed!")
                
                # Get the result of the background task
                avatar_generation = anvil.server.call('get_task_result', task_id)
                
                # Update the textbox with the result
                getattr(self, f'avatar_{avatar_num}_product_5_input').text = avatar_generation
                
                if avatar_num == 1:  # Only for avatar_1; adjust as needed
                    self.indeterminate_50.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_5_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_5_name').text
                    avatar_latest_row.update()

                if avatar_num == 2:  # Only for avatar_5; adjust as needed
                    self.indeterminate_50.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_5_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_5_name').text
                    avatar_latest_row.update()

                if avatar_num == 3:  # Only for avatar_5; adjust as needed
                    self.indeterminate_50.visible = False

                    # Update the latest as well
                    avatar_latest_row = user_table.search(variable=f'avatar_{avatar_num}_product_5_latest')[0]
                    avatar_latest_row['variable_value'] = avatar_generation
                    avatar_latest_row['variable_title'] = getattr(self, f'avatar_{avatar_num}_product_5_name').text
                    avatar_latest_row.update()
                
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'failed':
                print(f"Task {task_id} for avatar_{avatar_num}_product_5 failed!")
                tasks_to_remove.append((task_id, avatar_num))
                
            elif status == 'not_found':
                print(f"Task {task_id} for avatar_{avatar_num}_product_5 not found!")
                tasks_to_remove.append((task_id, avatar_num))
                
            else:
                print(f"Task {task_id} for avatar_{avatar_num}_product_5 still running...")
                all_tasks_complete = False
    
        # Remove tasks that are completed, failed, or not found
        for task in tasks_to_remove:
            self.task_info.remove(task)
    
        # If all tasks are complete, you can stop the timer
        if all_tasks_complete:
          self.avatar_product_5_timer.enabled = False
          self.avatar_product_5_timer.interval = 0

#######----------- Deep dive Avatars--------##########
  def regenerate_avatar_1_product_5_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_50.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_5_name_row = user_table.search(variable='product_5')[0]
      product_5_name = product_5_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_5_profile_row = user_table.search(variable='product_5')[0]
      product_5_profile = product_5_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_1_product_5_latest_row = user_table.get(variable='avatar_1_product_5_latest')
      avatar_1_product_5_latest_row['variable_value'] = None
      avatar_1_product_5_latest_row.update()

      #Update the avatar preview
      avatar_1_product_5_preview_row = user_table.get(variable='avatar_1_product_5_preview')
      avatar_1_product_5_preview_row['variable_value'] = self.avatar_1_product_5_input.text # Avatar preview description
      avatar_1_product_5_preview_row['variable_title'] = self.avatar_1_product_5_name.text # Avatar name description
      avatar_1_product_5_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_1_product_5_generator', product_5_name, product_5_profile, self.avatar_1_product_5_name.text, self.avatar_1_product_5_input.text)
      print(f"Task ID for avatar_1_product_5:", task_id)

      self.indeterminate_50.visible = True
      self.task_check_timer_regenerate_avatar_1_product_5.enabled = True
      self.task_check_timer_regenerate_avatar_1_product_5.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_1_product_5(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_1_product_5_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 1 Product 2 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 1 Product 2 Regenerated!")
            self.task_check_timer_regenerate_avatar_1_product_5.enabled = False
            self.task_check_timer_regenerate_avatar_1_product_5.interval = 0
            self.indeterminate_50.visible = False
                
            # Update the box
            avatar_1_product_5_input = row['variable_value'] 
            self.avatar_1_product_5_input.text = avatar_1_product_5_input

##----------- Deep dive Avatars 2 ------##########          
  def regenerate_avatar_2_product_5_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_50.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_5_name_row = user_table.search(variable='product_5')[0]
      product_5_name = product_5_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_5_profile_row = user_table.search(variable='product_5')[0]
      product_5_profile = product_5_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_2_product_5_latest_row = user_table.get(variable='avatar_2_product_5_latest')
      avatar_2_product_5_latest_row['variable_value'] = None
      avatar_2_product_5_latest_row.update()

      #Update the avatar preview
      avatar_2_product_5_preview_row = user_table.get(variable='avatar_2_product_5_preview')
      avatar_2_product_5_preview_row['variable_value'] = self.avatar_2_product_5_input.text # Avatar preview description
      avatar_2_product_5_preview_row['variable_title'] = self.avatar_2_product_5_name.text # Avatar name description
      avatar_2_product_5_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_2_product_2_generator', product_5_name, product_5_profile, self.avatar_2_product_5_name.text, self.avatar_2_product_5_input.text)
      print(f"Task ID for avatar_2_product_5:", task_id)

      self.indeterminate_20.visible = True
      self.task_check_timer_regenerate_avatar_2_product_5.enabled = True
      self.task_check_timer_regenerate_avatar_2_product_5.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_2_product_5(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_2_product_5_latest')
     
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 2 Product 5 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 2 Product 5 Regenerated!")
            self.task_check_timer_regenerate_avatar_2_product_5.enabled = False
            self.task_check_timer_regenerate_avatar_2_product_5.interval = 0
            self.indeterminate_50.visible = False
                
            # Update the box
            avatar_2_product_5_input = row['variable_value'] 
            self.avatar_2_product_5_input.text = avatar_2_product_5_input

##----------- Deep dive Avatars 3 ------##########          
  def regenerate_avatar_3_product_5_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_10.visible = True
          
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      self.user_table = user_table
      
      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      company_profile = company_profile_row['variable_value']
            
      # PRODUCT NAME 
      product_5_name_row = user_table.search(variable='product_5')[0]
      product_5_name = product_5_name_row['variable_title']
      
      # PRODUCT DESCRIPTION
      product_5_profile_row = user_table.search(variable='product_5')[0]
      product_5_profile = product_5_profile_row['variable_title']

      # Delete whatever is in latest, so we can check it as the status update.
      avatar_3_product_5_latest_row = user_table.get(variable='avatar_3_product_5_latest')
      avatar_3_product_5_latest_row['variable_value'] = None
      avatar_3_product_5_latest_row.update()

      #Update the avatar preview
      avatar_3_product_5_preview_row = user_table.get(variable='avatar_3_product_5_preview')
      avatar_3_product_5_preview_row['variable_value'] = self.avatar_3_product_5_input.text # Avatar preview description
      avatar_3_product_5_preview_row['variable_title'] = self.avatar_3_product_5_name.text # Avatar name description
      avatar_3_product_5_preview_row.update()
                
      # Launch the background task                                                 
      task_id = anvil.server.call(f'launch_deepdive_avatar_3_product_5_generator', product_5_name, product_5_profile, self.avatar_3_product_5_name.text, self.avatar_3_product_5_input.text)
      print(f"Task ID for avatar_3_product_5:", task_id)

      self.indeterminate_50.visible = True
      self.task_check_timer_regenerate_avatar_3_product_5.enabled = True
      self.task_check_timer_regenerate_avatar_3_product_5.interval = 3  # Check every 2seconds
 
  def check_task_status_regenerate_avatar_3_product_5(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Get the background task by its ID
        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='avatar_3_product_5_latest')
     
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Avatar 3 Product 5 Regeneration!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Avatar 3 Product 5 Regenerated!")
            self.task_check_timer_regenerate_avatar_3_product_5.enabled = False
            self.task_check_timer_regenerate_avatar_3_product_5.interval = 0
            self.indeterminate_50.visible = False
                
            # Update the box
            avatar_3_product_5_input = row['variable_value'] 
            self.avatar_3_product_5_input.text = avatar_3_product_5_input
          
        
#-- SAVE / LOAD EACH AVATAR ------------#######################################################################
  def save_product_1_avatars_button_click(self, **event_args):
    print("SAVE BUTTON PRODUCT 1 CLICKED")
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    all_empty = True
  
    for j in range(1, 4):
        avatar_description = getattr(self, f'avatar_{j}_product_1_input').text
        avatar_name = getattr(self, f'avatar_{j}_product_1_name').text
      
        # Check if both are empty for this iteration
        if not avatar_description.strip() and not avatar_name.strip():
            continue  # Skip this iteration
        # If either is empty, show alert and break
        if not avatar_description.strip() or not avatar_name.strip():
            anvil.js.window.alert("Please name the avatar, and ensure there's an avatar description.")
            break
      
        avatar_description_row = user_table.get(variable=f'avatar_{j}_product_1_latest')
        avatar_description_row['variable_value'] = avatar_description
        avatar_description_row['variable_title'] = avatar_name
        avatar_description_row.update()
          
        self.nav_button_avatars_to_brand_tone.enabled = True
        all_empty = False

    # Check if all are empty
    if all_empty:
        # This means that all avatar names and descriptions were empty. Do nothing or perform any operation if needed.
        pass

  def save_product_2_avatars_button_click(self, **event_args):
    print("SAVE BUTTON PRODUCT 2 CLICKED")
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    all_empty = True
  
    for j in range(1, 4):
        avatar_description = getattr(self, f'avatar_{j}_product_2_input').text
        avatar_name = getattr(self, f'avatar_{j}_product_2_name').text
      
        # Check if both are empty for this iteration
        if not avatar_description.strip() and not avatar_name.strip():
            continue  # Skip this iteration
        # If either is empty, show alert and break
        if not avatar_description.strip() or not avatar_name.strip():
            anvil.js.window.alert("Avatar Name and Description cannot be empty.")
            break
      
        avatar_description_row = user_table.get(variable=f'avatar_{j}_product_2_latest')
        avatar_description_row['variable_value'] = avatar_description
        avatar_description_row['variable_title'] = avatar_name
        avatar_description_row.update()
          
        self.nav_button_avatars_to_brand_tone.enabled = True
        all_empty = False

    # Check if all are empty
    if all_empty:
        # This means that all avatar names and descriptions were empty. Do nothing or perform any operation if needed.
        pass

  def save_product_3_avatars_button_click(self, **event_args):
      print("SAVE BUTTON PRODUCT 3 CLICKED")
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      user_table = getattr(app_tables, user_table_name)
  
      all_empty = True
    
      for j in range(1, 4):
          avatar_description = getattr(self, f'avatar_{j}_product_3_input').text
          avatar_name = getattr(self, f'avatar_{j}_product_3_name').text
        
          # Check if both are empty for this iteration
          if not avatar_description.strip() and not avatar_name.strip():
              continue  # Skip this iteration
          # If either is empty, show alert and break
          if not avatar_description.strip() or not avatar_name.strip():
              anvil.js.window.alert("Avatar Name and Description cannot be empty.")
              break
        
          avatar_description_row = user_table.get(variable=f'avatar_{j}_product_3_latest')
          avatar_description_row['variable_value'] = avatar_description
          avatar_description_row['variable_title'] = avatar_name
          avatar_description_row.update()
            
          self.nav_button_avatars_to_brand_tone.enabled = True
          all_empty = False
  
      # Check if all are empty
      if all_empty:
          # This means that all avatar names and descriptions were empty. Do nothing or perform any operation if needed.
          pass

  def save_product_4_avatars_button_click(self, **event_args):
      print("SAVE BUTTON PRODUCT 4 CLICKED")
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      user_table = getattr(app_tables, user_table_name)
  
      all_empty = True
    
      for j in range(1, 4):
          avatar_description = getattr(self, f'avatar_{j}_product_4_input').text
          avatar_name = getattr(self, f'avatar_{j}_product_4_name').text
        
          # Check if both are empty for this iteration
          if not avatar_description.strip() and not avatar_name.strip():
              continue  # Skip this iteration
          # If either is empty, show alert and break
          if not avatar_description.strip() or not avatar_name.strip():
              anvil.js.window.alert("Avatar Name and Description cannot be empty.")
              break
        
          avatar_description_row = user_table.get(variable=f'avatar_{j}_product_4_latest')
          avatar_description_row['variable_value'] = avatar_description
          avatar_description_row['variable_title'] = avatar_name
          avatar_description_row.update()
            
          self.nav_button_avatars_to_brand_tone.enabled = True
          all_empty = False
  
      # Check if all are empty
      if all_empty:
          # This means that all avatar names and descriptions were empty. Do nothing or perform any operation if needed.
          pass

  def save_product_5_avatars_button_click(self, **event_args):
      print("SAVE BUTTON PRODUCT 5 CLICKED")
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      user_table = getattr(app_tables, user_table_name)
  
      all_empty = True
    
      for j in range(1, 4):
          avatar_description = getattr(self, f'avatar_{j}_product_5_input').text
          avatar_name = getattr(self, f'avatar_{j}_product_5_name').text
        
          # Check if both are empty for this iteration
          if not avatar_description.strip() and not avatar_name.strip():
              continue  # Skip this iteration
          # If either is empty, show alert and break
          if not avatar_description.strip() or not avatar_name.strip():
              anvil.js.window.alert("Avatar Name and Description cannot be empty.")
              break
        
          avatar_description_row = user_table.get(variable=f'avatar_{j}_product_5_latest')
          avatar_description_row['variable_value'] = avatar_description
          avatar_description_row['variable_title'] = avatar_name
          avatar_description_row.update()
            
          self.nav_button_avatars_to_brand_tone.enabled = True
          all_empty = False
  
      # Check if all are empty
      if all_empty:
          # This means that all avatar names and descriptions were empty. Do nothing or perform any operation if needed.
          pass

###----------NAVIGATION---------------####

  def nav_button_avatars_to_brand_tone_click(self, **event_args):
      self.navigate_to_brand_tone()

    
  def navigate_to_brand_tone(self):
      brandtone = BrandTone()
      self.content_panel.clear()
      self.content_panel.add_component(brandtone)
    

#-- OLD //////     SAVE / LOAD EACH AVATAR ------------#######################################################################

#   def save_avatar1_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']
#     user_table = getattr(app_tables, user_table_name)

#     avatar_number = "avatar1"
#     avatar_row = user_table.get(variable=avatar_number)
#     avatar = self.avatar1_textbox.text
#     avatar_name = self.avatar_1_name_input.text

#     if avatar_name and avatar:  # Check both fields are not empty
#         avatar_row['variable_value'] = avatar
#         avatar_row['variable_title'] = avatar_name
#         avatar_row.update()
#         self.nav_button_avatars_to_brand_tone.enabled = True
#     else:
#         # Prompt the user to enter the variable name/title
#         anvil.js.window.alert("Avatar Name and Description cannot be empty.")

#   def save_avatar2_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']
#     user_table = getattr(app_tables, user_table_name)

#     avatar_number = "avatar2"
#     avatar_row = user_table.get(variable=avatar_number)
#     avatar = self.avatar2_textbox.text
#     avatar_name = self.avatar_2_name_input.text

#     if avatar_name and avatar:  # Check both fields are not empty
#         avatar_row['variable_value'] = avatar
#         avatar_row['variable_title'] = avatar_name
#         avatar_row.update()
#         self.nav_button_avatars_to_brand_tone.enabled = True
#     else:
#         # Prompt the user to enter the variable name/title
#         anvil.js.window.alert("Avatar Name and Description cannot be empty.")

#   def save_avatar3_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']
#     user_table = getattr(app_tables, user_table_name)

#     avatar_number = "avatar3"
#     avatar_row = user_table.get(variable=avatar_number)
#     avatar = self.avatar3_textbox.text
#     avatar_name = self.avatar_3_name_input.text

#     if avatar_name and avatar:  # Check both fields are not empty
#         avatar_row['variable_value'] = avatar
#         avatar_row['variable_title'] = avatar_name
#         avatar_row.update()
#         self.nav_button_avatars_to_brand_tone.enabled = True
#     else:
#         # Prompt the user to enter the variable name/title
#         anvil.js.window.alert("Avatar Name and Description cannot be empty.")

#   def save_avatar4_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']
#     user_table = getattr(app_tables, user_table_name)

#     avatar_number = "avatar4"
#     avatar_row = user_table.get(variable=avatar_number)
#     avatar = self.avatar4_textbox.text
#     avatar_name = self.avatar_4_name_input.text

#     if avatar_name and avatar:  # Check both fields are not empty
#         avatar_row['variable_value'] = avatar
#         avatar_row['variable_title'] = avatar_name
#         avatar_row.update()
#         self.nav_button_avatars_to_brand_tone.enabled = True
#     else:
#         # Prompt the user to enter the variable name/title
#         anvil.js.window.alert("Avatar Name and Description cannot be empty.")
      
#   def save_avatar5_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']
#     user_table = getattr(app_tables, user_table_name)

#     avatar_number = "avatar5"
#     avatar_row = user_table.get(variable=avatar_number)
#     avatar = self.avatar5_textbox.text
#     avatar_name = self.avatar_5_name_input.text

#     if avatar_name and avatar:  # Check both fields are not empty
#         avatar_row['variable_value'] = avatar
#         avatar_row['variable_title'] = avatar_name
#         avatar_row.update()
#         self.nav_button_avatars_to_brand_tone.enabled = True
#     else:
#         # Prompt the user to enter the variable name/title
#         anvil.js.window.alert("Avatar Name and Description cannot be empty.")

# ### LOAD AVATARS ---------------#############################

#   def load_avatar1_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']

#     # Get the table for the current user
#     user_table = getattr(app_tables, user_table_name)

#     avatar1_row = user_table.get(variable='avatar1')
#     avatar_1_preview_row = user_table.get(variable='avatar_1_preview')
       
#     # Check if an avatar number is available
#     if avatar1_row['variable_value']:
#         avatar_loaded = avatar1_row['variable_value']
#         print("Contents:", avatar_loaded)
#         # Set the contents as the text of the rich text box
#         avatar_name_loaded = avatar1_row['variable_title']
#         self.avatar_1_name_input.text = avatar_name_loaded
#         self.avatar1_textbox.text = avatar_loaded
    
#     elif avatar_1_preview_row['variable_value']:
#         # Handle case where the row does not exist for the current user
#         avatar_preview_loaded = avatar_1_preview_row['variable_value']
#         print("Contents:", avatar_preview_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar1_textbox.text = avatar_preview_loaded
#     else:
#         # Handle case where no avatar preview is available
#         print("No avatar preview found")

#   def load_avatar2_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']

#     # Get the table for the current user
#     user_table = getattr(app_tables, user_table_name)

#     avatar2_row = user_table.get(variable='avatar2')
#     avatar_2_preview_row = user_table.get(variable='avatar_2_preview')
    
#     # Check if an avatar number is available
#     if avatar2_row['variable_value']:
#         avatar_loaded = avatar2_row['variable_value']
#         print("Contents:", avatar_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar2_textbox.text = avatar_loaded
        
#         avatar_name_loaded = avatar2_row['variable_title']
#         self.avatar_2_name_input.text = avatar_name_loaded
    
#     elif avatar_2_preview_row['variable_value']:
#         # Handle case where the row does not exist for the current user
#         avatar_preview_loaded = avatar_2_preview_row['variable_value']
#         print("Contents:", avatar_preview_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar2_textbox.text = avatar_preview_loaded
#     else:
#         # Handle case where no avatar preview is available
#         print("No avatar preview found")

#   def load_avatar3_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']

#     # Get the table for the current user
#     user_table = getattr(app_tables, user_table_name)

#     avatar3_row = user_table.get(variable='avatar3')
#     avatar_3_preview_row = user_table.get(variable='avatar_3_preview')
    
#     # Check if an avatar number is available
#     if avatar3_row['variable_value']:
#         avatar_loaded = avatar3_row['variable_value']
#         print("Contents:", avatar_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar3_textbox.text = avatar_loaded

#         avatar_name_loaded = avatar3_row['variable_title']
#         self.avatar_3_name_input.text = avatar_name_loaded
    
#     elif avatar_3_preview_row['variable_value']:
#         # Handle case where the row does not exist for the current user
#         avatar_preview_loaded = avatar_3_preview_row['variable_value']
#         print("Contents:", avatar_preview_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar3_textbox.text = avatar_preview_loaded
#     else:
#         # Handle case where no avatar preview is available
#         print("No avatar preview found")

#   def load_avatar4_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']

#     # Get the table for the current user
#     user_table = getattr(app_tables, user_table_name)

#     avatar4_row = user_table.get(variable='avatar4')
#     avatar_4_preview_row = user_table.get(variable='avatar_4_preview')
    
#     # Check if an avatar number is available
#     if avatar4_row['variable_value']:
#         avatar_loaded = avatar4_row['variable_value']
#         print("Contents:", avatar_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar4_textbox.text = avatar_loaded

#         avatar_name_loaded = avatar5_row['variable_title']
#         self.avatar_5_name_input.text = avatar_name_loaded
    
#     elif avatar_4_preview_row['variable_value']:
#         # Handle case where the row does not exist for the current user
#         avatar_preview_loaded = avatar_4_preview_row['variable_value']
#         print("Contents:", avatar_preview_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar4_textbox.text = avatar_preview_loaded
#     else:
#         # Handle case where no avatar preview is available
#         print("No avatar preview found")

#   def load_avatar5_button_click(self, **event_args):
#     # Get the current user
#     current_user = anvil.users.get_user()
#     user_table_name = current_user['user_id']

#     # Get the table for the current user
#     user_table = getattr(app_tables, user_table_name)

#     avatar5_row = user_table.get(variable='avatar5')
#     avatar_5_preview_row = user_table.get(variable='avatar_5_preview')
    
#     # Check if an avatar number is available
#     if avatar5_row['variable_value']:
#         avatar_loaded = avatar5_row['variable_value']
#         print("Contents:", avatar_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar5_textbox.text = avatar_loaded

#         avatar_name_loaded = avatar5_row['variable_title']
#         self.avatar_5_name_input.text = avatar_name_loaded
    
#     elif avatar_5_preview_row['variable_value']:
#         # Handle case where the row does not exist for the current user
#         avatar_preview_loaded = avatar_5_preview_row['variable_value']
#         print("Contents:", avatar_preview_loaded)
#         # Set the contents as the text of the rich text box
#         self.avatar5_textbox.text = avatar_preview_loaded
#     else:
#         # Handle case where no avatar preview is available
#         print("No avatar preview found")


 

####----------------------------OLD CODE------------------------##########

# Initial Load:
# self.avatars_dropdown.items = [(row['avatar'], row) for row in app_tables.stock_avatars.search()]






