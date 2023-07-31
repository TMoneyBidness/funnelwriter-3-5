from ._anvil_designer import VideoSalesLetter_copyTemplate
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


############################################################################################################
# LOADING
class VideoSalesLetter_copy(VideoSalesLetter_copyTemplate):
  def __init__(self, **properties):

    self.chosen_company_profile = None
    self.chosen_product_name = None
    self.chosen_product_research = None
    self.chosen_avatar = None
    self.chosen_tone = None
    self.chosen_script = None

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
    # Get the email or username of the current user
    owner = current_user['email']
    # Get the row for the current user from the variable_table
    row = app_tables.variable_table.get(owner=owner)

    # COMPANY NAME
    self.company_name_input.text = row['company_name']

    # COMPANY RESEARCH
    self.company_profile_dropdown.items = [(row['company_profile'], row['company_profile'])]

    # PRODUCT
    self.product_name_dropdown.items = [(row['product_name'], row['product_name'])]
    self.product_profile_dropdown.items = [(row['product_profile'], row['product_profile'])]

    # AVATAR
    self.avatar_dropdown.items = [
    (row['avatar1'], row['avatar1']) for row['avatar1'] in [row['avatar1']] if row['avatar1']
    ] + [(row['avatar2'], row['avatar2']) for row['avatar2'] in [row['avatar2']] if row['avatar2']
    ] + [(row['avatar3'], row['avatar3']) for row['avatar3'] in [row['avatar3']] if row['avatar3']
    ] + [(row['avatar4'], row['avatar4']) for row['avatar4'] in [row['avatar4']] if row['avatar4']
    ] + [(row['avatar5'], row['avatar5']) for row['avatar5'] in [row['avatar5']] if row['avatar5']
    ] + [(row['saved_stock_avatar'], row['saved_stock_avatar']) for row['saved_stock_avatar'] in [row['saved_stock_avatar']] if row['saved_stock_avatar']
    ] + [(row['avatar'], row) for row in app_tables.stock_avatars.search()]

    #BRAND TONE
    final_stock_tones = [(row['tone'], row) for row in app_tables.stock_tones.search() if row['tone']]
    final_saved_tones = [(row['brand_tone'], row) for row in app_tables.variable_table.search() if row['brand_tone']]
    self.brand_tone_dropdown.items = final_stock_tones + final_saved_tones

   # SCRIPT FORMAT
    self.script_format_dropdown.items = ['Who, What, Where, How', 'Star, Story, Solution']
    # rows = app_tables.example_scripts.search()
    # script_format_items = []
    # for row in rows:
    #   if row['script'] == 'wwwh_1' or row['script'] == 'wwwh_2':
    #     script_format_items.append((row['script'], row['script_contents']))
    # self.script_format_dropdown.items = script_format_items

  def form_show(self, **event_args):
    # Load the company profile on form show
    self.load_company_profile()


  def save_funnel_settings_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    owner = current_user['email']
    row = app_tables.variable_table.get(owner=owner)  # Replace user_email with owner

    # Finalize the variables for the funnel
    self.chosen_company_name = self.company_name_input.text
    self.chosen_company_profile = self.company_profile_dropdown.selected_value
    self.chosen_product_name = self.product_name_dropdown.selected_value
    self.chosen_product_research = self.product_profile_dropdown.selected_value
    self.chosen_avatar = self.avatar_dropdown.selected_value
    self.chosen_tone = self.brand_tone_dropdown.selected_value
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

      # Get the row from the variable_table based on the owner
      current_user = anvil.users.get_user()
      owner = current_user['email']
      row = app_tables.variable_table.get(owner=owner)
      # Loop to check the status of the background task

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

                # Update the variable_table with the JSON string
                row['main_headlines'] = all_main_headlines_json
                row.update()
              else:
                print("Error: JSON string is None")

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

  #### ----- SUB HEADLINES------------#########################################################################################################
  def generate_subheadlines_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.indeterminate_progress_subheadlines.visible = True

      self.chosen_final_headline = self.main_headline_textbox.text
      self.chosen_company_name = self.company_name_input.text
      self.chosen_company_profile = self.company_profile_dropdown.selected_value
      self.chosen_product_name = self.product_name_dropdown.selected_value
      self.chosen_product_research = self.product_profile_dropdown.selected_value
      self.chosen_avatar = self.avatar_dropdown.selected_value
      self.chosen_tone = self.brand_tone_dropdown.selected_value
      self.chosen_script = self.script_format_dropdown.selected_value

      self.task_id = anvil.server.call('launch_generate_subheadlines', self.chosen_final_headline, self.chosen_product_name, self.chosen_company_profile, self.chosen_product_research, self.chosen_tone)
      print("Task ID:", self.task_id)
      # Launch the background task

      # Get the row from the variable_table based on the owner
      current_user = anvil.users.get_user()
      owner = current_user['email']
      row = app_tables.variable_table.get(owner=owner)
      # Loop to check the status of the background task

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

                # Update the variable_table with the JSON string
                row['subheadlines'] = all_subheadlines_json
                row.update()
              else:
                print("Error: JSON string is None")

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

      self.chosen_final_headline = self.main_headline_textbox.text
      self.chosen_final_subheadline = self.subheadline_textbox.text
      self.chosen_company_name = self.company_name_input.text
      self.chosen_company_profile = self.company_profile_dropdown.selected_value
      self.chosen_product_name = self.product_name_dropdown.selected_value
      self.chosen_product_research = self.product_profile_dropdown.selected_value
      self.chosen_avatar = self.avatar_dropdown.selected_value
      self.chosen_tone = self.brand_tone_dropdown.selected_value

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

      # Get the row from the variable_table based on the owner
      current_user = anvil.users.get_user()
      owner = current_user['email']
      row = app_tables.variable_table.get(owner=owner)
      # Loop to check the status of the background task

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
              row['vsl_script'] = vsl_script
              row.update()

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

####### --------VIDEO SALES LETTER THEMES --------###################################################
  def generate_vsl_themes_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.indeterminate_progress_vsl_themes.visible = True

      self.chosen_final_headline = self.main_headline_textbox.text
      self.chosen_final_subheadline = self.subheadline_textbox.text
      self.chosen_company_name = self.company_name_input.text
      self.chosen_company_profile = self.company_profile_dropdown.selected_value
      self.chosen_product_name = self.product_name_dropdown.selected_value
      self.chosen_product_research = self.product_profile_dropdown.selected_value
      self.chosen_avatar = self.avatar_dropdown.selected_value
      self.chosen_tone = self.brand_tone_dropdown.selected_value
      self.chosen_script = self.script_format_dropdown.selected_value
      self.vsl_script = self.video_sales_script_textbox.text

      current_user = anvil.users.get_user()
      owner = current_user['email']

      self.task_id = anvil.server.call('launch_generate_vsl_themes', self.chosen_final_headline, self.chosen_final_subheadline, self.chosen_product_name, self.chosen_product_research, self.chosen_tone,self.vsl_script,owner)
      print("Task ID:", self.task_id)
      # Launch the background task

      # Get the row from the variable_table based on the owner
      row = app_tables.variable_table.get(owner=owner)
      # Loop to check the status of the background task

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

                # Update the variable_table with the JSON string
                row['vsl_themes'] = all_vsl_themes_json
                row.update()
              else:
                print("Error: JSON string is None")

              self.indeterminate_progress_vsl_themes.visible = False
              break  # Exit the loop

            elif task_status == "failed":
              # Handle the case where the background task failed
              print("Task failed")
              break  # Exit the loop

          # Sleep for 1 second before checking again
          time.sleep(1)

#### ----- SAVING AND LOADING------------#########################################################################################################

  def edit_company_profile_component_click(self, **event_args):
    self.company_profile_textbox.read_only = False

  def save_company_profile_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()

    # Check if a user is signed in
    if current_user:
    # Get the email of the current user
      owner = current_user['email']

      # Get the row for the current user from the variable_table
      row = app_tables.variable_table.get(owner=owner)  # Replace user_email with owner

      # Update the company_profile column for the current user
      if row:
        text = self.company_profile_textbox.text
        row['company_profile'] = text
        row.update()
      else:
        # Handle case where the row does not exist for the current user
        print("No row found for the current user")
    else:
      # Handle case where no user is signed in
      print("No user is signed in")

  def save_vsl_script_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    # Get the email of the current user
    owner = current_user['email']

    # Get the row for the current user from the variable_table
    row = app_tables.variable_table.get(owner=owner)  # Replace user_email with owner
    # Update the company_profile column for the current user
    if row:
      text = self.video_sales_script_textbox.text
      row['vsl_script'] = text
      row.update()
    else:
      # Handle case where the row does not exist for the current user
      print("No row found for the current user")

  def save_vsl_themes_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    # Get the email of the current user
    owner = current_user['email']

    # Get the row for the current user from the variable_table
    row = app_tables.variable_table.get(owner=owner)  # Replace user_email with owner
    # Update the company_profile column for the current user
    if row:
      row['vsl_theme_1'] = self.vsl_theme_1.text
      row['vsl_theme_2'] = self.vsl_theme_2.text
      row['vsl_theme_3'] = self.vsl_theme_3.text
      row['vsl_theme_4'] = self.vsl_theme_4.text
      row.update()
    else:
      # Handle case where the row does not exist for the current user
      print("No row found for the current user")

  def load_vsl_themes_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    user_email = current_user['email']  # Change 'email' to 'username' if you are using usernames
    # Get the row for the current user from the variable_table
    row = app_tables.variable_table.get(owner=user_email)  # Change 'owner' to the appropriate column name if different

    # Get the vsl script contents for the current user
    if row:
      self.vsl_theme_1.text = row['vsl_theme_1']
      self.vsl_theme_2.text = row['vsl_theme_2']
      self.vsl_theme_3.text = row['vsl_theme_3']
      self.vsl_theme_4.text = row['vsl_theme_4']
    else:
      # Handle case where the row does not exist for the current user
      print("No row found for the current user")

  def save_chosen_headlines_button_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()
    # Get the email of the current user
    owner = current_user['email']

    # Get the row for the current user from the variable_table
    row = app_tables.variable_table.get(owner=owner)

    # Update the headlines in the row
    if row:
      row['final_headline'] = self.main_headline_textbox.text
      row['final_subheadline'] = self.subheadline_textbox.text
      row['final_secondary_headline'] = self.secondary_headline_textbox.text
      row.update()
    else:
      # Handle case where the row does not exist for the current user
      print("No row found for the current user")

  ############################################################################################################
  # NAVIGATION

  def load_vsl_script_component_click(self, **event_args):
    # Get the current user
    current_user = anvil.users.get_user()

    user_email = current_user['email']  # Change 'email' to 'username' if you are using usernames

    # Get the row for the current user from the variable_table
    row = app_tables.variable_table.get(owner=user_email)  # Change 'owner' to the appropriate column name if different

    # Get the company profile text for the current user
    if row:
      contents = row['vsl_script']
      print("Contents:", contents)
      # Set the contents as the text of the rich text box
      self.video_sales_script_textbox.text = contents
    else:
      # Handle case where the row does not exist for the current user
      print("No row found for the current user")


  def product_asset_link_click(self, **event_args):
    product=Product()
    self.content_panel.clear()
    self.content_panel.add_component(product)

  def finalproduct_page_link_click(self, **event_args):
    finalproduct=FinalProduct()
    self.content_panel.clear()
    self.content_panel.add_component(finalproduct)
