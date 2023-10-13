from ._anvil_designer import VideoSalesLetterTemplate
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

from ..FinalProduct import FinalProduct
############################################################################################################
# LOADING
class VideoSalesLetter(VideoSalesLetterTemplate):
  def __init__(self, **properties):
    anvil.users.login_with_form()

    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    # Initialize counter
    self.counter = 0
    self.indeterminate_progress_vsl.visible = False
    self.indeterminate_progress_vsl_themes.visible = False
    self.nav_button_vsl_to_final_product.enabled = True

    self.chosen_company_name = None
    self.chosen_product_name = None
    self.chosen_product_research = None
    self.chosen_avatar = None
    self.chosen_tone = None
    self.chosen_final_headline = None
    self.chosen_final_subheadline = None
    self.chosen_final_secondary_headline = None

    # Load stuff
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

    # COMPANY NAME
    chosen_company_name_row = user_table.search(variable='chosen_company_name')[0]
    self.chosen_company_name = chosen_company_name_row['variable_value']

    # COMPANY PROFILE
    chosen_company_profile_row = user_table.search(variable='chosen_company_profile')[0]
    self.chosen_company_profile = chosen_company_profile_row['variable_value']
    
    # PRODUCT NAME
    chosen_product_name_row = user_table.search(variable='chosen_product_name')[0]
    self.chosen_product_name = chosen_product_name_row['variable_value']

    # PRODUCT PROFILE
    chosen_product_research_row = user_table.search(variable='chosen_product_research')[0]
    self.chosen_product_research = chosen_product_research_row['variable_value']

    # AVATARS
    chosen_avatar_row = user_table.search(variable='chosen_avatar')[0]
    self.chosen_avatar = chosen_avatar_row['variable_value']

    # BRAND TONE
    chosen_tone_row = user_table.search(variable='chosen_tone')[0]
    self.chosen_tone = chosen_tone_row['variable_value']

    # SCRIPT FORMAT
    chosen_script_row = user_table.search(variable='chosen_script')[0]
    self.chosen_script = chosen_script_row['variable_value']

    # FINAL HEADLINE
    chosen_final_headline_row = user_table.search(variable='chosen_final_headline')[0]
    self.chosen_final_headline = chosen_final_headline_row['variable_value']

    # FINAL SUBHEADLINE
    chosen_final_subheadline_row = user_table.search(variable='chosen_final_subheadline')[0]
    self.chosen_final_subheadline = chosen_final_subheadline_row['variable_value']

    # FINAL SECONDARY HEADLINE
    chosen_final_secondary_headline_row = user_table.search(variable='chosen_final_secondary_headline')[0]
    self.chosen_final_secondary_headline = chosen_final_secondary_headline_row['variable_value']
    

    # Call set_saved_values to store the retrieved values in class-level variables
    self.set_saved_values(
        self.chosen_company_name,
        self.chosen_company_profile,
        self.chosen_product_name,
        self.chosen_product_research,
        self.chosen_tone,
        self.chosen_avatar,
        self.chosen_script,
        self.chosen_final_headline,
        self.chosen_final_subheadline,
        self.chosen_final_secondary_headline
    )

  def set_saved_values(self, chosen_company_name, chosen_company_profile, chosen_product_name, chosen_product_research, chosen_tone, chosen_avatar, chosen_script, chosen_final_headline, chosen_final_subheadline,chosen_final_secondary_headline):
      self.chosen_company_name = chosen_company_name
      self.chosen_company_profile = chosen_company_profile
      self.chosen_product_name = chosen_product_name
      self.chosen_product_research = chosen_product_research
      self.chosen_tone = chosen_tone
      self.chosen_avatar = chosen_avatar
      self.chosen_script = chosen_script
      self.chosen_final_headline = chosen_final_headline
      self.chosen_final_subheadline = chosen_final_subheadline
      self.chosen_final_secondary_headline = chosen_final_secondary_headline


####### --------VIDEO SALES LETTER SCRIPT --------###################################################

  def generate_vsl_script_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      self.indeterminate_progress_vsl.visible = True

      print("Generate Video Sales Letter Script button clicked")
      # Use the saved values from the dropdowns

      current_user = anvil.users.get_user()
      user_table_name = current_user['user_id']
      # Get the table for the current user
      user_table = getattr(app_tables, user_table_name)
      vsl_row = user_table.get(variable='vsl_script')
      
      # Find the example script
      row_chosen_script = user_table.search(variable='chosen_script')
      
      if row_chosen_script and row_chosen_script[0]['variable_title'] == 'Who, What, Where, How - 1':
          example_wwwh_1_row = app_tables.example_scripts.get(script='wwwh_1')
          example_script = example_wwwh_1_row['script_contents']
      elif row_chosen_script and row_chosen_script[0]['variable_title'] == 'Who, What, Where, How - 2':
          example_wwwh_2_row = app_tables.example_scripts.get(script='wwwh_2')
          example_script = example_wwwh_2_row['script_contents']
      elif self.chosen_script == 'Star, Story, Solution':
          example_sss_row = app_tables.example_scripts.get(script='sss')
          example_script = example_sss_row['script_contents']
      
      self.task_id = anvil.server.call('launch_generate_vsl_script', self.chosen_product_name, self.chosen_final_headline,self.chosen_final_subheadline, self.chosen_company_profile, self.chosen_product_research,self.chosen_avatar, self.chosen_tone, example_script)
      print("Task ID:", self.task_id)
      # Launch the background task

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
      # Check if the video sales script textbox is empty
      if not self.video_sales_script_textbox.text:
          anvil.js.window.alert("Please Create a Video Sales Script Before Generating your themes.")
          return      
      else:
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
    row = user_table.get(variable='vsl_script')

    # Update the video sales column for the current user
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


  def nav_button_vsl_to_final_product_click(self, **event_args):
          # Check if any of the textboxes are empty
    if not self.vsl_theme_1.text or not self.vsl_theme_2.text or not self.vsl_theme_3.text or not self.vsl_theme_4.text:
        # If any of the vsl_theme textboxes are empty, show an alert
        anvil.js.window.alert("Please enter all 4 main theme excerpts before proceeding")
        return
    else:      
     anvil.open_form('FinalProduct')
      
# NAVIGATION

# # Define the function to navigate to the 'Company' form
#   def navigate_to_headlines(self, **event_args):
#     anvil.open_form('Company')

  # def finalproduct_page_link_click(self, **event_args):
  #   finalproduct=FinalProduct()
  #   self.content_panel.clear()
  #   self.content_panel.add_component(finalproduct)


#INTRO

    # # Get the rows for company profiles
    # company_profile_rows = [
    # user_table.search(variable='company_profile_1')[0],
    # user_table.search(variable='company_profile_2')[0],
    # user_table.search(variable='company_profile_3')[0]
    # ]
    # # Extract the values from the rows
    # company_profiles = [row['variable_title'] for row in company_profile_rows]
    # # Assign the values to the company_profile_dropdown
    # self.company_profile_dropdown.items = company_profiles

      

  # def nav_button_VSL_Elements_to_headline(self, **event_args):
  #       headlines = Headlines()
  #       self.content_panel.clear()
  #       self.content_panel.add_component(headlines)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def nav_back_to_headlines(self, **event_args):
   anvil.open_form('Headlines')
    


