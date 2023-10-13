from ._anvil_designer import VideoSalesLetter_workspacesTemplate
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

############################################################################################################
# LOADING
class VideoSalesLetter_workspaces(VideoSalesLetter_workspacesTemplate):
  def __init__(self, **properties):
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

    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    # Initialize counter
    self.counter = 0
    self.indeterminate_progress_main_headlines.visible = False
    self.indeterminate_progress_subheadlines.visible = False
    self.indeterminate_progress_vsl.visible = False
    self.indeterminate_progress_vsl_themes.visible = False

    # Load stuff
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)


    # COMPANY NAME
    # Retrieve the row with 'variable' column containing 'company_profile'
    company_name_row = user_table.search(variable='company_name')[0]

    # Access the value of the 'company_name' column from the retrieved row
    self.company_name_input.text = company_name_row['variable_value']

    # Get the rows for company profiles
    company_profile_rows = [
    user_table.search(variable='company_profile_1')[0],
    user_table.search(variable='company_profile_2')[0],
    user_table.search(variable='company_profile_3')[0]
    ]
    # Extract the values from the rows
    company_profiles = [row['variable_title'] for row in company_profile_rows]
    # Assign the values to the company_profile_dropdown
    self.company_profile_dropdown.items = company_profiles

    # PRODUCT NAME
    product_name_rows = [
    user_table.search(variable='product_profile_1')[0],
    user_table.search(variable='product_profile_2')[0],
    user_table.search(variable='product_profile_3')[0],
    user_table.search(variable='product_profile_4')[0],
    user_table.search(variable='product_profile_5')[0]
    ]
    # Extract the values from the rows
    product_names = [row['variable_title'] for row in product_name_rows]
    # Assign the values to the company_profile_dropdown
    self.product_name_dropdown.items = product_names

    # PRODUCT PROFILE
    product_profile_rows = [
    user_table.search(variable='product_profile_1')[0],
    user_table.search(variable='product_profile_2')[0],
    user_table.search(variable='product_profile_3')[0],
    user_table.search(variable='product_profile_4')[0],
    user_table.search(variable='product_profile_5')[0]
    ]
    # Extract the values from the rows
    product_profiles = [row['variable_title'] for row in product_profile_rows]
    # Assign the values to the company_profile_dropdown
    self.product_profile_dropdown.items = product_profiles

    # AVATARS
    avatar_rows_custom = [
        user_table.search(variable='avatar1')[0],
        user_table.search(variable='avatar2')[0],
        user_table.search(variable='avatar3')[0],
        user_table.search(variable='avatar4')[0],
        user_table.search(variable='avatar5')[0]
    ]
    avatars_custom = [row['variable_title'] for row in avatar_rows_custom]
    avatar_rows_stock = [row for row in app_tables.stock_avatars.search() if row['avatar']]
    # Create a list of tuples for the avatar_dropdown items
    avatar_dropdown_items = [(row['avatar'], row['avatar']) for row in avatar_rows_stock] + [(avatar, avatar) for avatar in avatars_custom]
    # Assign the values to the avatar_dropdown
    self.avatar_dropdown.items = avatar_dropdown_items

    # BRAND TONE
    brand_tone_urls = user_table.search(variable='brand_tone')
    brand_tone_extracted = [row['variable_title'] for row in brand_tone_urls]
    brand_tone_stock = [row['tone'] for row in app_tables.stock_tones.search() if row['tone']]

    # Create a list of tuples for the brand_tone_dropdown items
    brand_tone_dropdown_items = [(tone, tone) for tone in brand_tone_stock] + [(title, title) for title in brand_tone_extracted]

    # Assign the values to the brand_tone_dropdown
    self.brand_tone_dropdown.items = brand_tone_dropdown_items

   # SCRIPT FORMAT
    self.script_format_dropdown.items = ['Who, What, Where, How', 'Star, Story, Solution']
    rows = app_tables.example_scripts.search()
    script_format_items = []
    for row in rows:
      if row['script'] == 'wwwh_1' or row['script'] == 'wwwh_2':
        script_format_items.append((row['script'], row['script_contents']))
    self.script_format_dropdown.items = script_format_items

# LOCK IT ALL IN

  def save_funnel_settings_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # COMPANY NAME
    self.chosen_company_name = self.company_name_input.text

    # COMPANY PROFILE
    selected_company_profile_value = self.company_profile_dropdown.selected_value
    self.chosen_company_profile = anvil.server.call('get_chosen_variable_value', user_table, selected_company_profile_value)
    print('chosen_company_profile:', self.chosen_company_profile)

    # PRODUCT NAME
    selected_product_name_value = self.product_name_dropdown.selected_value
    self.chosen_product_name = anvil.server.call('get_chosen_variable_value', user_table, selected_product_name_value)
    print('chosen_product_name:', self.chosen_product_name)

    # PRODUCT RESEARCH
    selected_product_profile_value = self.product_profile_dropdown.selected_value
    self.chosen_product_research = anvil.server.call('get_chosen_variable_value', user_table, selected_product_profile_value )
    print('self.chosen_product_research:', self.chosen_product_research)

    # AVATARS
    selected_avatar_value = self.avatar_dropdown.selected_value
    # Check if the selected avatar value is from the stock avatars table
    stock_avatar_rows = app_tables.stock_avatars.search(avatar=selected_avatar_value)
    if stock_avatar_rows and len(stock_avatar_rows) > 0:
      self.chosen_avatar = stock_avatar_rows[0]['value']
      print('Stock Avatar:', self.chosen_avatar)
    else:
      print('No Stock Avatar Found')
      # Check if the selected avatar value is from the custom avatars table
      self.chosen_avatar = anvil.server.call('get_chosen_variable_value', user_table, selected_avatar_value)
      print('Custom Avatar:', self.chosen_avatar)

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
      self.chosen_tone = anvil.server.call('get_chosen_variable_value', user_table, selected_tone_value)
      print('Custom Tone:', self.chosen_tone)

    # SCRIPT
    self.chosen_script = self.script_format_dropdown.selected_value

  #Use the saved values in other functions
  def generate_main_headlines_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.indeterminate_progress_main_headlines.visible = True

      print("Generate Main Headlines button clicked")
      # Use the saved values from the dropdowns
      print("Company Name:", self.chosen_company_name)
      print("Company Profile:", self.chosen_company_profile)
      print("Product Name:", self.chosen_product_name)
      print("Product Research:", self.chosen_product_research)
      print("Avatar:", self.chosen_avatar)
      print("Brand Tone:", self.chosen_tone)
      print("Script Format:", self.chosen_script)

      self.task_id = anvil.server.call('launch_generate_main_headlines', self.chosen_product_name, self.chosen_company_profile, self.chosen_product_research, self.chosen_tone)
      print("Task ID:", self.task_id)
      # Launch the background task


      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      row = user_table.get(variable='main_headlines')

      # Loop to check the status of the background task
      while True:
        with anvil.server.no_loading_indicator:
          # Check if the background task is complete
          task_status = anvil.server.call('get_task_status', self.task_id)
          print("Task status:", task_status)

          if task_status is not None:
            if task_status == "completed":
              # Get the result of the background task
              all_main_headlines_json = anvil.server.call('get_task_result', self.task_id)
              self.indeterminate_progress_main_headlines.visible = False


              if all_main_headlines_json is not None:
                # Convert the JSON string back to a list
                all_headlines = json.loads(all_main_headlines_json)
                # Update the text boxes with the headlines
                self.main_headline_1.text = all_headlines[0]
                self.main_headline_2.text = all_headlines[1]
                self.main_headline_3.text = all_headlines[2]
                self.main_headline_4.text = all_headlines[3]
                self.main_headline_5.text = all_headlines[4]
                self.main_headline_6.text = all_headlines[5]
                self.main_headline_7.text = all_headlines[6]
                self.main_headline_8.text = all_headlines[7]
                self.main_headline_9.text = all_headlines[8]
                self.main_headline_10.text = all_headlines[9]

              if row:
                # Update the 'variable_value' column of the row
                row['variable_value'] = all_main_headlines_json
                row.update()
              else:
                print("Error: Row not found in user_table")

              # Hide the progress bar
              self.indeterminate_progress_main_headlines.visible = False

              break  # Exit the loop

            elif task_status == "failed":
              # Handle the case where the background task failed
              print("Task failed")
              break  # Exit the loop

          # Sleep for 1 second before checking again
          time.sleep(1)


#### ----- HEADLINE HANDLERS------------######
  # Event handler for the click event of the radio buttons
  def main_headline_button_click(self, **event_args):
      # Get the clicked radio button
    clicked_radio_button = event_args['sender']

    # Get the text of the clicked radio button
    selected_headline = clicked_radio_button.text

    # Set the text of the textbox
    self.main_headline_textbox.text = selected_headline

  def secondary_headline_1_clicked(self, **event_args):
    # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_1.text

  def secondary_headline_2_clicked(self, **event_args):
    # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_2.text

  def secondary_headline_3_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_3.text

  def secondary_headline_4_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_4.text

  def secondary_headline_5_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_5.text

  def secondary_headline_6_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_6.text

  def secondary_headline_7_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_7.text

  def secondary_headline_8_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_8.text

  def secondary_headline_9_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_9.text

  def secondary_headline_10_clicked(self, **event_args):
  # Set the text of radiobutton2 to the text of radiobutton1
    self.secondary_headline_textbox.text = self.main_headline_10.text

  def check_task_status(self, task_id):
    task_status = anvil.server.call('get_task_status', task_id)
    if task_status is not None:
      if task_status == "completed":
        generated_headlines = anvil.server.call('get_task_result', task_id)
        self.handle_generated_headlines(generated_headlines)
      elif task_status == "failed":
        # Handle the case where the task failed
        print("Task failed")

      # Repeat the check after a delay
      anvil.timer.call_after(1, self.check_task_status, task_id)

#   #### ----- SUB HEADLINES------------#########################################################################################################
  def generate_subheadlines_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.indeterminate_progress_subheadlines.visible = True

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      row = user_table.get(variable='subheadlines')

      self.task_id = anvil.server.call('launch_generate_subheadlines', self.chosen_final_headline, self.chosen_product_name, self.chosen_company_profile, self.chosen_product_research, self.chosen_tone)
      print("Task ID:", self.task_id)
      # Launch the background task

      # Loop to check the status of the background task
      while True:
        with anvil.server.no_loading_indicator:
          # Check if the background task is complete
          task_status = anvil.server.call('get_task_status', self.task_id)
          print("Task status:", task_status)

          if task_status is not None:
            if task_status == "completed":
              # Get the result of the background task
              all_subheadlines_json = anvil.server.call('get_task_result', self.task_id)

              if all_subheadlines_json is not None:
                # Convert the JSON string back to a list
                all_subheadlines = json.loads(all_subheadlines_json)
                # Update the text boxes with the headlines
                self.subheadline_1.text = all_subheadlines[0]
                self.subheadline_2.text = all_subheadlines[1]
                self.subheadline_3.text = all_subheadlines[2]
                self.subheadline_4.text = all_subheadlines[3]
                self.subheadline_5.text = all_subheadlines[4]
                self.subheadline_6.text = all_subheadlines[5]
                self.subheadline_7.text = all_subheadlines[6]
                self.subheadline_8.text = all_subheadlines[7]
                self.subheadline_9.text = all_subheadlines[8]
                self.subheadline_10.text = all_subheadlines[9]

              if row:
                # Update the 'variable_value' column of the row
                row['variable_value'] = all_subheadlines_json
                row.update()
              else:
                print("Error: Row not found in user_table")

              self.indeterminate_progress_subheadlines.visible = False
              break  # Exit the loop

            elif task_status == "failed":
              # Handle the case where the background task failed
              print("Task failed")
              break  # Exit the loop

          # Sleep for 1 second before checking again
          time.sleep(1)

  #### ----- SUBHEADLINE HANDLERS------------######
  # Event handler for the click event of the radio buttons
  def subheadline_button_click(self, **event_args):
    # Get the clicked radio button
    clicked_radio_button = event_args['sender']

    # Get the text of the clicked radio button
    selected_subheadline = clicked_radio_button.text

    # Set the text of the textbox
    self.subheadline_textbox.text = selected_subheadline


####### --------VIDEO SALES LETTER SCRIPT --------###################################################

  def generate_vsl_script_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.indeterminate_progress_vsl.visible = True

      print("Generate Video Sales Letter Script button clicked")
      # Use the saved values from the dropdowns

      # Find the example script
      if self.chosen_script == 'Who, What, Where, How':
        example_wwwh_1_row = app_tables.example_scripts.get(script='wwwh_1')
        example_script = example_wwwh_1_row['script_contents']
      elif self.chosen_script == 'Star, Story, Solution':
        example_sss_row = app_tables.example_scripts.get(script='sss')
        example_script = example_sss_row['script_contents']
      else:
        # Handle the case where the selected value is not recognized or doesn't require a specific example
        example_script = ""  # Set a default value or leave it empty based on your requirement

      self.task_id = anvil.server.call('launch_generate_vsl_script', self.chosen_product_name, self.chosen_final_headline,self.chosen_final_subheadline, self.chosen_company_profile, self.chosen_product_research,self.chosen_avatar, self.chosen_tone, example_script)
      print("Task ID:", self.task_id)
      # Launch the background task

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      vsl_row = user_table.get(variable='vsl_script')

      # Loop to check the status of the background task
      while True:
        with anvil.server.no_loading_indicator:
          # Check if the background task icomplete
          task_status = anvil.server.call('get_task_status', self.task_id)
          print("Task status:", task_status)

          if task_status is not None:
            if task_status == "completed":
              # Get the result of the background task
              vsl_script = anvil.server.call('get_task_result', self.task_id)

              # Update the variable_table with the JSON string
              vsl_row['variable_value'] = vsl_script
              vsl_row.update()

              # Populate the textbox with the generated script
              self.video_sales_script_textbox.text = vsl_script

              # Hide the progress bar
              self.indeterminate_progress_vsl.visible = False
              break  # Exit the loop

            elif task_status == "failed":
              # Handle the case where the background task failed
              print("Task failed")
              break  # Exit the loop

          # Sleep for 1 second before checking again
          time.sleep(1)

# ####### --------VIDEO SALES LETTER THEMES --------###################################################
  def generate_vsl_themes_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.indeterminate_progress_vsl_themes.visible = True

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)

      row = user_table.get(variable='vsl_themes')
      vsl_theme_1_row = user_table.get(variable='vsl_theme_1')
      vsl_theme_2_row = user_table.get(variable='vsl_theme_2')
      vsl_theme_3_row = user_table.get(variable='vsl_theme_3')
      vsl_theme_4_row = user_table.get(variable='vsl_theme_4')

      self.task_id = anvil.server.call('launch_generate_vsl_themes', self.chosen_final_headline, self.chosen_final_subheadline, self.chosen_product_name, self.chosen_product_research, self.chosen_tone,self.video_sales_script_textbox,row)
      print("Task ID:", self.task_id)
      # Launch the background task

      # Loop to check the status of the background task
      while True:
        with anvil.server.no_loading_indicator:
          # Check if the background task is complete
          task_status = anvil.server.call('get_task_status', self.task_id)
          print("Task status:", task_status)

          if task_status is not None:
            if task_status == "completed":
              # Get the result of the background task
              all_vsl_themes_json = anvil.server.call('get_task_result', self.task_id)

              if all_vsl_themes_json is not None:
                # Convert the JSON string back to a list
                all_vsl_themes = json.loads(all_vsl_themes_json)
                # Update the text boxes with the headlines
                self.vsl_theme_1.text = all_vsl_themes[0]
                self.vsl_theme_2.text = all_vsl_themes[1]
                self.vsl_theme_3.text = all_vsl_themes[2]
                self.vsl_theme_4.text = all_vsl_themes[3]

                # Update the rows in the 'variable' column of the 'mdia' table
                vsl_theme_1_row['variable_value'] = all_vsl_themes[0]
                vsl_theme_2_row['variable_value'] = all_vsl_themes[1]
                vsl_theme_3_row['variable_value'] = all_vsl_themes[2]
                vsl_theme_4_row['variable_value'] = all_vsl_themes[3]

                vsl_theme_1_row.update()
                vsl_theme_2_row.update()
                vsl_theme_3_row.update()
                vsl_theme_4_row.update()

                # Update the variable_table with the JSON string
                row['variable_value'] = all_vsl_themes_json
                row.update()
              else:
                print("Error: Row not found in user_table")

              self.indeterminate_progress_vsl_themes.visible = False
              break  # Exit the loop

            elif task_status == "failed":
              # Handle the case where the background task failed
              print("Task failed")
              break  # Exit the loop

          # Sleep for 1 second before checking again
          time.sleep(1)

# #### ----- SAVING AND LOADING------------#########################################################################################################

  def edit_company_profile_component_click(self, **event_args):
    self.company_profile_textbox.read_only = False

  def save_vsl_script_component_click(self, **event_args):
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
    row = user_table.get(variable='subheadlines')

    # Update the company_profile column for the current user
    if row:
      text = self.video_sales_script_textbox.text
      row['variable_value'] = text
      row.update()
    else:
      # Handle case where the row does not exist for the current user
      print("No row found for the current user")

  def save_vsl_themes_component_click(self, **event_args):
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Update vsl_theme_1
    vsl_theme_1_rows = user_table.search(variable='vsl_theme_1')
    if vsl_theme_1_rows:
      vsl_theme_1_row = vsl_theme_1_rows[0]
      vsl_theme_1_row['variable_value'] = self.vsl_theme_1.text
      vsl_theme_1_row.update()
    else:
      # Handle case where no rows are found for vsl_theme_1
      print("No row found for vsl_theme_1")

    # Update vsl_theme_2
    vsl_theme_2_rows = user_table.search(variable='vsl_theme_2')
    if vsl_theme_2_rows:
      vsl_theme_2_row = vsl_theme_2_rows[0]
      vsl_theme_2_row['variable_value'] = self.vsl_theme_2.text
      vsl_theme_2_row.update()
    else:
      # Handle case where no rows are found for vsl_theme_2
      print("No row found for vsl_theme_2")

    # Update vsl_theme_3
    vsl_theme_3_rows = user_table.search(variable='vsl_theme_3')
    if vsl_theme_3_rows:
      vsl_theme_3_row = vsl_theme_3_rows[0]
      vsl_theme_3_row['variable_value'] = self.vsl_theme_3.text
      vsl_theme_3_row.update()
    else:
      # Handle case where no rows are found for vsl_theme_3
      print("No row found for vsl_theme_3")

    # Update vsl_theme_4
    vsl_theme_4_rows = user_table.search(variable='vsl_theme_4')
    if vsl_theme_4_rows:
      vsl_theme_4_row = vsl_theme_4_rows[0]
      vsl_theme_4_row['variable_value'] = self.vsl_theme_4.text
      vsl_theme_4_row.update()
    else:
      # Handle case where no rows are found for vsl_theme_4
      print("No row found for vsl_theme_4")


  def load_vsl_themes_component_click(self, **event_args):
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # Load vsl_theme_1
    vsl_theme_1_rows = user_table.search(variable='vsl_theme_1')
    if vsl_theme_1_rows:
      vsl_theme_1_row = vsl_theme_1_rows[0]
      self.vsl_theme_1.text = vsl_theme_1_row['variable_value']
    else:
      # Handle case where no rows are found for vsl_theme_1
      print("No row found for vsl_theme_1")

    # Load vsl_theme_2
    vsl_theme_2_rows = user_table.search(variable='vsl_theme_2')
    if vsl_theme_2_rows:
      vsl_theme_2_row = vsl_theme_2_rows[0]
      self.vsl_theme_2.text = vsl_theme_2_row['variable_value']
    else:
      # Handle case where no rows are found for vsl_theme_2
      print("No row found for vsl_theme_2")

    # Load vsl_theme_3
    vsl_theme_3_rows = user_table.search(variable='vsl_theme_3')
    if vsl_theme_3_rows:
      vsl_theme_3_row = vsl_theme_3_rows[0]
      self.vsl_theme_3.text = vsl_theme_3_row['variable_value']
    else:
      # Handle case where no rows are found for vsl_theme_3
      print("No row found for vsl_theme_3")

    # Load vsl_theme_4
    vsl_theme_4_rows = user_table.search(variable='vsl_theme_4')
    if vsl_theme_4_rows:
      vsl_theme_4_row = vsl_theme_4_rows[0]
      self.vsl_theme_4.text = vsl_theme_4_row['variable_value']
    else:
      # Handle case where no rows are found for vsl_theme_4
      print("No row found for vsl_theme_4")


  def save_chosen_headlines_button_click(self, **event_args):
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    final_headline_rows = user_table.search(variable='final_headline')
    if final_headline_rows:
      final_headline_row = final_headline_rows[0]
      final_headline_row['variable_value'] = self.main_headline_textbox.text
      final_headline_row.update()
    else:
      # Handle case where no rows are found for final_headline
      print("No row found for final_headline")

    final_subheadline_rows = user_table.search(variable='final_subheadline')
    if final_subheadline_rows:
      final_subheadline_row = final_subheadline_rows[0]
      final_subheadline_row['variable_value'] = self.subheadline_textbox.text
      final_subheadline_row.update()
    else:
      # Handle case where no rows are found for final_subheadline
      print("No row found for final_subheadline")

    final_secondary_headline_rows = user_table.search(variable='final_secondary_headline')
    if final_secondary_headline_rows:
      final_secondary_headline_row = final_secondary_headline_rows[0]
      final_secondary_headline_row['variable_value'] = self.secondary_headline_textbox.text
      final_secondary_headline_row.update()
    else:
      # Handle case where no rows are found for final_secondary_headline
      print("No row found for final_secondary_headline")

  def load_vsl_script_component_click(self, **event_args):
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    load_vsl_rows = user_table.search(variable='vsl_script')
    if load_vsl_rows:
      loaded_vsl_script = load_vsl_rows[0]['variable_value']
      self.video_sales_script_textbox.text = loaded_vsl_script
      print("Contents:", loaded_vsl_script)
    else:
      # Handle case where no rows are found for vsl_script
      print("No row found for vsl_script")

#   ############################################################################################################
#   # NAVIGATION

  # def finalproduct_page_link_click(self, **event_args):
  #   finalproduct=FinalProduct()
  #   self.content_panel.clear()
  #   self.content_panel.add_component(finalproduct)
