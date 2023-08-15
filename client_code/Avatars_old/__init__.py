from ._anvil_designer import Avatars_oldTemplate
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
class Avatars_old(Avatars_oldTemplate):
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

    self.indeterminate_10.visible = False
    self.indeterminate_all_avatars.visible = False
    self.indeterminate_1.visible = False
    self.indeterminate_2.visible = False
    self.indeterminate_3.visible = False
    self.indeterminate_4.visible = False
    self.indeterminate_5.visible = False

    # Start Timers
    self.avatar_product_1_timer.enabled = True
    self.avatar_product_1_timer.interval = 5  # Check every 5 seconds
    self.avatar_product_2_timer.enabled = True
    self.avatar_product_2_timer.interval = 5  # Check every 5 seconds
    self.avatar_product_3_timer.enabled = True
    self.avatar_product_3_timer.interval = 5  # Check every 5 seconds
    self.avatar_product_4_timer.enabled = True
    self.avatar_product_4_timer.interval = 5  # Check every 5 seconds
    self.avatar_product_5_timer.enabled = True
    self.avatar_product_5_timer.interval = 5  # Check every 5 seconds


    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Hide Panels of Products 2-5
    self.avatar_1_product_1_input_section.visible = False
    self.avatar_1_product_2_input_section.visible = False
    self.avatar_1_product_3_input_section.visible = False
    self.avatar_1_product_4_input_section.visible = False
    self.avatar_1_product_5_input_section.visible = False

    # HIDE BUTTONS:
    self.avatar_1_product_1_button.visible = False
    self.avatar_2_product_1_button.visible = False
    self.avatar_3_product_1_button.visible = False

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
          getattr(self, f'avatar_1_product_{i}_input_section').visible = True

        else:
          getattr(self, f'avatar_1_product_{i}_input_section').visible = False

        # Now, load the avatars associated with that product. There may be 1 avatar only, or there are 3. The cells might be empty!
        # Load the avatars associated with that product
        for j in range(1, 4):
          row_avatar_product_latest = user_table.get(variable=f'avatar_{j}_product_{i}_latest')

          # If the avatar cell exists
          if row_avatar_product_latest:
            avatar_product_latest = row_avatar_product_latest['variable_value']
            avatar_product_latest_name = row_avatar_product_latest['variable_title']

            # Check if the avatar cell is not empty
            if avatar_product_latest and avatar_product_latest.strip():
              getattr(self, f'avatar_{j}_product_{i}_input').text = avatar_product_latest
              getattr(self, f'avatar_{j}_product_{i}_name').text = avatar_product_latest_name
              getattr(self, f'avatar_{j}_product_{i}_input_section').visible = True
            else:
              # Make the section invisible if the avatar cell is empty
              getattr(self, f'avatar_{j}_product_{i}_input_section').visible = False

          else:
            # Make the section invisible if the avatar cell doesn't exist
            getattr(self, f'avatar_{j}_product_{i}_input_section').visible = False
            print(f"No row found for 'avatar_{j}_product_{i}_latest'")


    # Load the latest info for Avatars 1 to 5
    for i in range(1, 6):
      row_avatar_latest = user_table.search(variable=f'avatar_{i}_latest')
      row_avatar_name = user_table.search(variable=f'avatar{i}')

      if row_avatar_latest:
        avatar_latest = row_avatar_latest[0]['variable_value']
        getattr(self, f'avatar{i}_textbox').text = avatar_latest

      if row_avatar_name:
        avatar_name = row_avatar_name[0]['variable_title']
        getattr(self, f'avatar_{i}_name_input').text = avatar_name
      else:
        print(f"No row found for 'avatar_{i}_latest'")

    # Check if any of the final avatars are empty
    final_avatar_rows = [
        user_table.search(variable='avatar1')[0],
        user_table.search(variable='avatar2')[0],
        user_table.search(variable='avatar3')[0],
        user_table.search(variable='avatar4')[0],
        user_table.search(variable='avatar5')[0]
    ]

    # Check if any of the avatar descriptions are empty
    if any(not row['variable_value'] for row in final_avatar_rows if row and 'variable_value' in row):
      # If any of the avatar descriptions are empty, disable the button
      self.nav_button_avatars_to_brand_tone.enabled = False
    else:
      # If all avatar descriptions are saved, enable the button
      self.nav_button_avatars_to_brand_tone.enabled = True

# ADDING PRODUCTS / AVATAR PANELS

# Base Panel
  def add_avatar_2_product_1_click(self, **event_args):
    self.avatar_2_product_1_input_section.visible = True
    self.add_avatar_2_product_1.visible = False

  def add_avatar_3_product_1_click(self, **event_args):
    self.avatar_3_product_1_input_section.visible = True
    self.add_avatar_2_product_1.visible = False
    self.add_avatar_3_product_1.visible = False

  def add_product_2_panel_click(self, **event_args):
    self.product_2_panel.visible = True

# Panel 2 / Product 2
  def add_avatar_2_product_2_click(self, **event_args):
    self.avatar_2_product_2_input_section.visible = True
    self.add_avatar_2_product_2.visible = False

  def add_avatar_3_product_2_click(self, **event_args):
    self.avatar_3_product_2_input_section.visible = True
    self.add_avatar_2_product_2.visible = False
    self.add_avatar_3_product_2.visible = False

  def add_product_3_panel_click(self, **event_args):
    self.product_3_panel.visible = True

# Panel 3 / Product 3
  def add_avatar_2_product_3_click(self, **event_args):
    self.avatar_2_product_3_input_section.visible = True
    self.add_avatar_2_product_3.visible = False

  def add_avatar_3_product_3_click(self, **event_args):
    self.avatar_3_product_3_input_section.visible = True
    self.add_avatar_2_product_3.visible = False
    self.add_avatar_3_product_3.visible = False

  def add_product_4_panel_click(self, **event_args):
    self.product_4_panel.visible = True

# Panel 4 / Product 4
  def add_avatar_2_product_4_click(self, **event_args):
    self.avatar_2_product_4_input_section.visible = True
    self.add_avatar_2_product_4.visible = False
  def add_avatar_3_product_4_click(self, **event_args):
    self.avatar_3_product_4_input_section.visible = True
    self.add_avatar_2_product_4.visible = False
    self.add_avatar_3_product_4.visible = False
  def add_product_5_panel_click(self, **event_args):
    self.product_5_panel.visible = True

# Panel 5 / Product 5
  def add_avatar_2_product_5_click(self, **event_args):
    self.avatar_2_product_5_input_section.visible = True
    self.add_avatar_2_product_5.visible = False

  def add_avatar_3_product_5_click(self, **event_args):
    self.avatar_3_product_5_input_section.visible = True
    self.add_avatar_2_product_5.visible = False
    self.add_avatar_3_product_5.visible = False

#-- GENERATE THE AVATAR DEEP DIVES FOR EACH PRODUCT ------------#######################################################
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





      # # AVATAR PREVIEW
      # avatar_1_product_1_preview = self.avatar_1_product_1_input.text
      # avatar_1_product_1_preview_row = user_table.search(variable='avatar_1_product_1_preview')[0]
      # avatar_1_product_1_preview_row['variable_value'] = avatar_1_product_1_preview
      # # AVATAR NAME
      # avatar_1_product_1_name_preview = self.avatar_1_product_1_name.text
      # avatar_1_product_1_preview_row['variable_title'] = avatar_1_product_1_name_preview
      # avatar_1_product_1_preview_row.update()

      # # Save it it as the latest as well
      # avatar_1_product_1_latest_row = user_table.search(variable='avatar_1_product_1_latest')[0]
      # avatar_1_product_1_latest_row['variable_value'] = avatar_1_product_1_preview
      # avatar_1_product_1_latest_row['variable_title'] = avatar_1_product_1_name_preview
      # avatar_1_product_1_latest_row.update()

      # self.task_id = anvil.server.call('launch_deepdive_avatar_1_product_1_generator', product_1_name,product_1_profile,avatar_1_product_1_name_preview,avatar_1_product_1_preview)
      # print("Task ID:", self.task_id)

      # Loop to check the status of the background task
      #       while True:
      #         with anvil.server.no_loading_indicator:

      #           # Check if the background task is complete
      #           task_status = anvil.server.call('get_task_status', self.task_id)
      #           print("Task status:", task_status)

      #           if task_status is not None:
      #             if task_status == "completed":
      #               # Get the result of the background task
      #               avatar_generation = anvil.server.call('get_task_result', self.task_id)
      #               # Update the textbox with the result
      #               print("Avatars:", avatar_generation)
      #               self.avatar_1_product_1_input.text = avatar_generation
      #               self.indeterminate_10.visible = False

      #             # Save it it as the latest as well
      #               avatar_1_product_1_latest_row = user_table.search(variable='avatar_1_product_1_latest')[0]
      #               avatar_1_product_1_latest_row['variable_value'] = avatar_1_product_1_preview
      #               avatar_1_product_1_latest_row['variable_title'] = avatar_1_product_1_name_preview
      #               avatar_1_product_1_latest_row.update()

      #               break  # Exit the loop
      #             elif task_status == "failed":
      #               # Get the error message
      #               task_error = anvil.server.call('get_task_result', self.task_id)
      #               print("Task error:", task_error)
      #               self.indeterminate_10.visible = False
      #               break  # Exit the loop

      #           # Sleep for 1 second before checking again
      #           time.sleep(2)


#-- GENERATE THE 5 PREVIEWS ------------#######################################################################

  def all_avatars_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("All Avatars Generator button clicked")
      self.indeterminate_all_avatars.visible = True
      # Start the progress bar with a small value

      # Load stuff
      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      owner_company_profile = company_profile_row['variable_value']

      # PRODUCT PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      # product_profile_row = user_table.search(variable='product_profile_1')[0]
      # owner_product_profile = product_profile_row['variable_value']
      # avatars_grouped_row = user_table.get(variable='all_avatars_grouped')

      # Launch the background task
      self.task_id = anvil.server.call('launch_all_avatars_generator', owner_company_profile)
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
              all_avatars_json = anvil.server.call('get_task_result', self.task_id)
              # Convert the JSON string back to a dictionary
              all_avatars = json.loads(all_avatars_json)
              # Update the text boxes with the avatars
              self.avatar1_textbox.text = all_avatars['avatar_1']
              self.avatar2_textbox.text = all_avatars['avatar_2']
              self.avatar3_textbox.text = all_avatars['avatar_3']
              self.avatar4_textbox.text = all_avatars['avatar_4']
              self.avatar5_textbox.text = all_avatars['avatar_5']

              # Update the variable_table with the JSON string
              all_avatars_grouped_row = user_table.search(variable='all_avatars_grouped')[0]
              all_avatars_grouped_row['variable_value'] = all_avatars_json
              self.indeterminate_all_avatars.visible = False
              all_avatars_grouped_row.update()
              break  # Exit the loop

              for avatar_number in range(1, 6):
                # Save Latest
                avatar_latest_variable = f'avatar_{avatar_number}_latest'
                avatar_variable_value = all_avatars[f'avatar_{avatar_number}']
                avatar_latest_row = user_table.search(variable=avatar_latest_variable)[0]
                avatar_latest_row['variable_value'] = avatar_variable_value
                avatar_latest_row.update()

                # Save Preview
                avatar_preview_variable = f'avatar_{avatar_number}_preview'
                avatar_preview_value = all_avatars[f'avatar_{avatar_number}']
                avatar_preview_row = user_table.search(variable=avatar_preview_variable)[0]
                avatar_preview_row['variable_value'] = avatar_preview_value
                avatar_preview_row.update()

            elif task_status == "failed":
              # Handle the case where the background task failed
              print("Task failed")
              self.indeterminate_all_avatars.visible = False
              break  # Exit the loop

          # Sleep for 1 second before checking again
          time.sleep(1)

#-- FUNCTION TO GENERATE EACH GENERAL AVATAR ------------#######################################################################
  def generate_avatar1_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_1.visible = True

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      owner_company_profile = company_profile_row['variable_value']

      # AVATARS
      avatar_1_preview = self.avatar1_textbox.text
      avatar_1_preview_row = user_table.search(variable='avatar_1_preview')[0]
      avatar_1_preview_row['variable_value'] = avatar_1_preview
      avatar_1_preview_row.update()

      # Save it it as the latest as well
      avatar_1_latest = self.avatar1_textbox.text
      avatar_1_latest_row = user_table.search(variable='avatar_1_latest')[0]
      avatar_1_latest_row['variable_value'] = avatar_1_latest
      avatar_1_latest_row.update()

      self.task_id = anvil.server.call('launch_deepdive_avatar_1_generator', owner_company_profile,avatar_1_preview)
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
            avatar_generation = anvil.server.call('get_task_result', self.task_id)
            # Update the textbox with the result
            print("Avatars:", avatar_generation)
            self.avatar1_textbox.text = avatar_generation
            self.indeterminate_1.visible = False

          # Save it it as the latest as well
            avatar_1_latest_row = user_table.search(variable='avatar_1_latest')[0]
            avatar_1_latest_row['variable_value'] = avatar_generation
            avatar_1_latest_row.update()

            break  # Exit the loop
          elif task_status == "failed":
            # Get the error message
            task_error = anvil.server.call('get_task_result', self.task_id)
            print("Task error:", task_error)
            self.indeterminate_1.visible = False
            break  # Exit the loop

        # Sleep for 1 second before checking again
        time.sleep(2)

  def generate_avatar1_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_2.visible = True

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      owner_company_profile = company_profile_row['variable_value']

      # AVATARS
      avatar_2_preview = self.avatar2_textbox.text
      avatar_2_preview_row = user_table.search(variable='avatar_2_preview')[0]
      avatar_2_preview_row['variable_value'] = avatar_2_preview
      avatar_2_preview_row.update()

      # Save it it as the latest as well
      avatar_2_latest = self.avatar2_textbox.text
      avatar_2_latest_row = user_table.search(variable='avatar_2_latest')[0]
      avatar_2_latest_row['variable_value'] = avatar_2_latest
      avatar_2_latest_row.update()

      self.task_id = anvil.server.call('launch_deepdive_avatar_2_generator', owner_company_profile,avatar_2_preview)
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
            avatar_generation = anvil.server.call('get_task_result', self.task_id)
            # Update the textbox with the result
            print("Avatars:", avatar_generation)
            self.avatar2_textbox.text = avatar_generation
            self.indeterminate_2.visible = False

          # Save it it as the latest as well
            avatar_2_latest_row = user_table.search(variable='avatar_2_latest')[0]
            avatar_2_latest_row['variable_value'] = avatar_generation
            avatar_2_latest_row.update()

            break  # Exit the loop
          elif task_status == "failed":
            # Get the error message
            task_error = anvil.server.call('get_task_result', self.task_id)
            print("Task error:", task_error)
            self.indeterminate_2.visible = False
            break  # Exit the loop

        # Sleep for 1 second before checking again
        time.sleep(2)

  def generate_avatar3_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_3.visible = True

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      owner_company_profile = company_profile_row['variable_value']

      # AVATARS
      avatar_3_preview = self.avatar3_textbox.text
      avatar_3_preview_row = user_table.search(variable='avatar_3_preview')[0]
      avatar_3_preview_row['variable_value'] = avatar_3_preview
      avatar_3_preview_row.update()

      # Save it it as the latest as well
      avatar_3_latest = self.avatar3_textbox.text
      avatar_3_latest_row = user_table.search(variable='avatar_3_latest')[0]
      avatar_3_latest_row['variable_value'] = avatar_3_latest
      avatar_3_latest_row.update()

      self.task_id = anvil.server.call('launch_deepdive_avatar_4_generator', owner_company_profile,avatar_3_preview)
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
            avatar_generation = anvil.server.call('get_task_result', self.task_id)
            # Update the textbox with the result
            print("Avatars:", avatar_generation)
            self.avatar3_textbox.text = avatar_generation
            self.indeterminate_3.visible = False

          # Save it it as the latest as well
            avatar_3_latest_row = user_table.search(variable='avatar_3_latest')[0]
            avatar_3_latest_row['variable_value'] = avatar_generation
            avatar_3_latest_row.update()

            break  # Exit the loop
          elif task_status == "failed":
            # Get the error message
            task_error = anvil.server.call('get_task_result', self.task_id)
            print("Task error:", task_error)
            self.indeterminate_3.visible = False
            break  # Exit the loop

        # Sleep for 1 second before checking again
        time.sleep(2)

  def generate_avatar4_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_4.visible = True

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      owner_company_profile = company_profile_row['variable_value']

      # AVATARS
      avatar_4_preview = self.avatar4_textbox.text
      avatar_4_preview_row = user_table.search(variable='avatar_4_preview')[0]
      avatar_4_preview_row['variable_value'] = avatar_4_preview
      avatar_4_preview_row.update()

      # Save it it as the latest as well
      avatar_4_latest = self.avatar4_textbox.text
      avatar_4_latest_row = user_table.search(variable='avatar_4_latest')[0]
      avatar_4_latest_row['variable_value'] = avatar_4_latest
      avatar_4_latest_row.update()

      self.task_id = anvil.server.call('launch_deepdive_avatar_4_generator', owner_company_profile,avatar_4_preview)
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
            avatar_generation = anvil.server.call('get_task_result', self.task_id)
            # Update the textbox with the result
            print("Avatars:", avatar_generation)
            self.avatar4_textbox.text = avatar_generation
            self.indeterminate_4.visible = False

          # Save it it as the latest as well
            avatar_4_latest_row = user_table.search(variable='avatar_4_latest')[0]
            avatar_4_latest_row['variable_value'] = avatar_generation
            avatar_4_latest_row.update()

            break  # Exit the loop
          elif task_status == "failed":
            # Get the error message
            task_error = anvil.server.call('get_task_result', self.task_id)
            print("Task error:", task_error)
            self.indeterminate_4.visible = False
            break  # Exit the loop

        # Sleep for 1 second before checking again
        time.sleep(2)

  def generate_avatar5_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Deep Dive Avatar Generator Initiated")
      # Start the progress bar with a small value
      self.indeterminate_5.visible = True

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      # COMPANY PROFILE
      # Retrieve the row with 'variable' column containing 'company_profile'
      company_profile_row = user_table.search(variable='company_profile')[0]
      owner_company_profile = company_profile_row['variable_value']

      # AVATARS
      avatar_5_preview = self.avatar5_textbox.text
      avatar_5_preview_row = user_table.search(variable='avatar_5_preview')[0]
      avatar_5_preview_row['variable_value'] = avatar_5_preview
      avatar_5_preview_row.update()

      # Save it it as the latest as well
      avatar_5_latest = self.avatar5_textbox.text
      avatar_5_latest_row = user_table.search(variable='avatar_5_latest')[0]
      avatar_5_latest_row['variable_value'] = avatar_5_latest
      avatar_5_latest_row.update()

      self.task_id = anvil.server.call('launch_deepdive_avatar_5_generator', owner_company_profile,avatar_5_preview)
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
            avatar_generation = anvil.server.call('get_task_result', self.task_id)
            # Update the textbox with the result
            print("Avatars:", avatar_generation)
            self.avatar5_textbox.text = avatar_generation
            self.indeterminate_5.visible = False

          # Save it it as the latest as well
            avatar_5_latest_row = user_table.search(variable='avatar_5_latest')[0]
            avatar_5_latest_row['variable_value'] = avatar_generation
            avatar_5_latest_row.update()

            break  # Exit the loop
          elif task_status == "failed":
            # Get the error message
            task_error = anvil.server.call('get_task_result', self.task_id)
            print("Task error:", task_error)
            self.indeterminate_5.visible = False
            break  # Exit the loop

        # Sleep for 1 second before checking again
        time.sleep(2)

  # OLD VERSION
  # def generate_avatar5_button_click(self, **event_args):
  #   with anvil.server.no_loading_indicator:
  #     # This method should handle the UI logic
  #     print("Deep Dive Avatar Generator Initiated")
  #     self.indeterminate_5.visible = True

  #     current_user = anvil.users.get_user()
  #     # Get the email of the current user
  #     owner = current_user['email']
  #     # Get the row for the current user from the variable_table
  #     row = app_tables.variable_table.get(owner=owner)
  #     owner_company_profile = row['company_profile']
  #     owner_product_profile = row['product_profile']
  #     avatar_preview = self.avatar5_textbox.text

  #     self.task_id = anvil.server.call('launch_deepdive_avatar_generator', owner_company_profile,owner_product_profile,avatar_preview)
  #     print("Task ID:", self.task_id)

  #     # Loop to check the status of the background task
  #   while True:
  #     with anvil.server.no_loading_indicator:
  #       # Check if the background task is complete
  #       task_status = anvil.server.call('get_task_status', self.task_id)
  #       print("Task status:", task_status)

  #       if task_status is not None:
  #         if task_status == "completed":
  #           # Get the result of the background task
  #           avatar_generation = anvil.server.call('get_task_result', self.task_id)
  #           # Update the textbox with the result
  #           print("Avatars:", avatar_generation)
  #           self.avatar5_textbox.text = avatar_generation
  #           self.indeterminate_5.visible = False
  #           break  # Exit the loop
  #         elif task_status == "failed":
  #           # Get the error message
  #           task_error = anvil.server.call('get_task_result', self.task_id)
  #           print("Task error:", task_error)
  #           self.indeterminate_5.visible = False
  #           break  # Exit the loop

  #       # Sleep for 1 second before checking again
  #       time.sleep(2)

#-- SAVE / LOAD EACH AVATAR ------------#######################################################################

  def save_avatar1_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    avatar_number = "avatar1"
    avatar_row = user_table.get(variable=avatar_number)
    avatar = self.avatar1_textbox.text
    avatar_name = self.avatar_1_name_input.text

    if avatar_name and avatar:  # Check both fields are not empty
      avatar_row['variable_value'] = avatar
      avatar_row['variable_title'] = avatar_name
      avatar_row.update()
      self.nav_button_avatars_to_brand_tone.enabled = True
    else:
      # Prompt the user to enter the variable name/title
      anvil.js.window.alert("Avatar Name and Description cannot be empty.")

  def save_avatar2_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    avatar_number = "avatar2"
    avatar_row = user_table.get(variable=avatar_number)
    avatar = self.avatar2_textbox.text
    avatar_name = self.avatar_2_name_input.text

    if avatar_name and avatar:  # Check both fields are not empty
      avatar_row['variable_value'] = avatar
      avatar_row['variable_title'] = avatar_name
      avatar_row.update()
      self.nav_button_avatars_to_brand_tone.enabled = True
    else:
      # Prompt the user to enter the variable name/title
      anvil.js.window.alert("Avatar Name and Description cannot be empty.")

  def save_avatar3_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    avatar_number = "avatar3"
    avatar_row = user_table.get(variable=avatar_number)
    avatar = self.avatar3_textbox.text
    avatar_name = self.avatar_3_name_input.text

    if avatar_name and avatar:  # Check both fields are not empty
      avatar_row['variable_value'] = avatar
      avatar_row['variable_title'] = avatar_name
      avatar_row.update()
      self.nav_button_avatars_to_brand_tone.enabled = True
    else:
      # Prompt the user to enter the variable name/title
      anvil.js.window.alert("Avatar Name and Description cannot be empty.")

  def save_avatar4_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    avatar_number = "avatar4"
    avatar_row = user_table.get(variable=avatar_number)
    avatar = self.avatar4_textbox.text
    avatar_name = self.avatar_4_name_input.text

    if avatar_name and avatar:  # Check both fields are not empty
      avatar_row['variable_value'] = avatar
      avatar_row['variable_title'] = avatar_name
      avatar_row.update()
      self.nav_button_avatars_to_brand_tone.enabled = True
    else:
      # Prompt the user to enter the variable name/title
      anvil.js.window.alert("Avatar Name and Description cannot be empty.")

  def save_avatar5_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    user_table = getattr(app_tables, user_table_name)

    avatar_number = "avatar5"
    avatar_row = user_table.get(variable=avatar_number)
    avatar = self.avatar5_textbox.text
    avatar_name = self.avatar_5_name_input.text

    if avatar_name and avatar:  # Check both fields are not empty
      avatar_row['variable_value'] = avatar
      avatar_row['variable_title'] = avatar_name
      avatar_row.update()
      self.nav_button_avatars_to_brand_tone.enabled = True
    else:
      # Prompt the user to enter the variable name/title
      anvil.js.window.alert("Avatar Name and Description cannot be empty.")

### LOAD AVATARS ---------------#############################

  def load_avatar1_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    avatar1_row = user_table.get(variable='avatar1')
    avatar_1_preview_row = user_table.get(variable='avatar_1_preview')

    # Check if an avatar number is available
    if avatar1_row['variable_value']:
      avatar_loaded = avatar1_row['variable_value']
      print("Contents:", avatar_loaded)
      # Set the contents as the text of the rich text box
      avatar_name_loaded = avatar1_row['variable_title']
      self.avatar_1_name_input.text = avatar_name_loaded
      self.avatar1_textbox.text = avatar_loaded

    elif avatar_1_preview_row['variable_value']:
      # Handle case where the row does not exist for the current user
      avatar_preview_loaded = avatar_1_preview_row['variable_value']
      print("Contents:", avatar_preview_loaded)
      # Set the contents as the text of the rich text box
      self.avatar1_textbox.text = avatar_preview_loaded
    else:
      # Handle case where no avatar preview is available
      print("No avatar preview found")

  def load_avatar2_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    avatar2_row = user_table.get(variable='avatar2')
    avatar_2_preview_row = user_table.get(variable='avatar_2_preview')

    # Check if an avatar number is available
    if avatar2_row['variable_value']:
      avatar_loaded = avatar2_row['variable_value']
      print("Contents:", avatar_loaded)
      # Set the contents as the text of the rich text box
      self.avatar2_textbox.text = avatar_loaded

      avatar_name_loaded = avatar2_row['variable_title']
      self.avatar_2_name_input.text = avatar_name_loaded

    elif avatar_2_preview_row['variable_value']:
      # Handle case where the row does not exist for the current user
      avatar_preview_loaded = avatar_2_preview_row['variable_value']
      print("Contents:", avatar_preview_loaded)
      # Set the contents as the text of the rich text box
      self.avatar2_textbox.text = avatar_preview_loaded
    else:
      # Handle case where no avatar preview is available
      print("No avatar preview found")

  def load_avatar3_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    avatar3_row = user_table.get(variable='avatar3')
    avatar_3_preview_row = user_table.get(variable='avatar_3_preview')

    # Check if an avatar number is available
    if avatar3_row['variable_value']:
      avatar_loaded = avatar3_row['variable_value']
      print("Contents:", avatar_loaded)
      # Set the contents as the text of the rich text box
      self.avatar3_textbox.text = avatar_loaded

      avatar_name_loaded = avatar3_row['variable_title']
      self.avatar_3_name_input.text = avatar_name_loaded

    elif avatar_3_preview_row['variable_value']:
      # Handle case where the row does not exist for the current user
      avatar_preview_loaded = avatar_3_preview_row['variable_value']
      print("Contents:", avatar_preview_loaded)
      # Set the contents as the text of the rich text box
      self.avatar3_textbox.text = avatar_preview_loaded
    else:
      # Handle case where no avatar preview is available
      print("No avatar preview found")

  def load_avatar4_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    avatar4_row = user_table.get(variable='avatar4')
    avatar_4_preview_row = user_table.get(variable='avatar_4_preview')

    # Check if an avatar number is available
    if avatar4_row['variable_value']:
      avatar_loaded = avatar4_row['variable_value']
      print("Contents:", avatar_loaded)
      # Set the contents as the text of the rich text box
      self.avatar4_textbox.text = avatar_loaded

      avatar_name_loaded = avatar5_row['variable_title']
      self.avatar_5_name_input.text = avatar_name_loaded

    elif avatar_4_preview_row['variable_value']:
      # Handle case where the row does not exist for the current user
      avatar_preview_loaded = avatar_4_preview_row['variable_value']
      print("Contents:", avatar_preview_loaded)
      # Set the contents as the text of the rich text box
      self.avatar4_textbox.text = avatar_preview_loaded
    else:
      # Handle case where no avatar preview is available
      print("No avatar preview found")

  def load_avatar5_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']

    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    avatar5_row = user_table.get(variable='avatar5')
    avatar_5_preview_row = user_table.get(variable='avatar_5_preview')

    # Check if an avatar number is available
    if avatar5_row['variable_value']:
      avatar_loaded = avatar5_row['variable_value']
      print("Contents:", avatar_loaded)
      # Set the contents as the text of the rich text box
      self.avatar5_textbox.text = avatar_loaded

      avatar_name_loaded = avatar5_row['variable_title']
      self.avatar_5_name_input.text = avatar_name_loaded

    elif avatar_5_preview_row['variable_value']:
      # Handle case where the row does not exist for the current user
      avatar_preview_loaded = avatar_5_preview_row['variable_value']
      print("Contents:", avatar_preview_loaded)
      # Set the contents as the text of the rich text box
      self.avatar5_textbox.text = avatar_preview_loaded
    else:
      # Handle case where no avatar preview is available
      print("No avatar preview found")

###----------NAVIGATION---------------####

  def nav_button_avatars_to_brand_tone_click(self, **event_args):
    self.navigate_to_brand_tone()

  def navigate_to_brand_tone(self):
    brandtone = BrandTone()
    self.content_panel.clear()
    self.content_panel.add_component(brandtone)



####----------------------------OLD CODE------------------------##########

# Initial Load:
# self.avatars_dropdown.items = [(row['avatar'], row) for row in app_tables.stock_avatars.search()]
