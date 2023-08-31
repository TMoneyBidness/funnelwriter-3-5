from ._anvil_designer import HeadlinesTemplate
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

from ..VideoSalesLetter import VideoSalesLetter


############################################################################################################

PROMPT_TITLE = "FunnelWriter.AI needs a title to SAVE AS"

## LOADING
class Headlines(HeadlinesTemplate):
  def __init__(self, **properties):
    # Find the example script
    anvil.users.login_with_form()
  
    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    # Initialize counter
    self.counter = 0
    self.indeterminate_progress_main_headlines.visible = False
    self.indeterminate_progress_subheadlines.visible = False
    self.indeterminate_progress_vsl_themes.visible = False
    self.indeterminate_progress_vsl_themes_rewrites.visible = False
    self.generate_headlines_vsl_button.enabled = True
    self.generate_vsl_themes_button.visible = False
    self.indeterminate_progress_vsl_excerpts.visible = False
    self.indeterminate_progress_vsl_script.visible = False
    self.rewrite_box.visible = False
     
    
    self.chosen_company_name = None
    self.chosen_product_name = None
    self.chosen_product_research = None
    self.chosen_avatar = None
    self.chosen_tone = None
    self.chosen_script = None

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

    # Call set_saved_values to store the retrieved values in class-level variables
    self.set_saved_values(
        self.chosen_company_name,
        self.chosen_company_profile,
        self.chosen_product_name,
        self.chosen_product_research,
        self.chosen_tone,
        self.chosen_avatar,
        self.chosen_script
    )

    # Find the example script
    row_chosen_script = user_table.search(variable='chosen_script')

    for component in self.get_components():
        # Check if the component is a Timer
        if isinstance(component, anvil.Timer):
            # Stop the timer by setting its interval to None
            component.interval = None
          
    if row_chosen_script and row_chosen_script[0]['variable_title'] == 'Who, What, Where, How':
        example_wwwh_1_row = app_tables.example_scripts.get(script='wwwh_1')
        example_script = example_wwwh_1_row['script_contents']
        self.example_script = example_script
    # elif row_chosen_script and row_chosen_script[0]['variable_title'] == 'Who, What, Where, How - 2':
    #     example_wwwh_2_row = app_tables.example_scripts.get(script='wwwh_2')
    #     example_script = example_wwwh_2_row['script_contents']
    #     self.example_script = example_script
    elif self.chosen_script == 'Star, Story, Solution':
        example_sss_row = app_tables.example_scripts.get(script='sss')
        example_script = example_sss_row['script_contents']
        self.example_script = example_script

    # Stop all Timers
    # self.task_check_timer_headlines.enabled = False
    # self.task_check_timer_headlines.interval = 0
  
    # self.task_check_timer_subheadlines.enabled = False
    # self.task_check_timer_subheadlines.interval = 0  # Check every 2seconds

    # self.task_check_timer_vsl_script.enabled = False
    # self.task_check_timer_vsl_script.interval = 0 # Check every 2seconds
      
    self.task_ids = []  # List to store all task IDs
    
  def generate_headlines_vsl_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        self.indeterminate_progress_main_headlines.visible = True
        self.indeterminate_progress_subheadlines.visible = True

      # Delete whatever is in the table with existing headlines.
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        
      # Delete all the existing boxes and start fresh
        headline_row = user_table.get(variable='main_headlines')
        headline_row['variable_value'] = None
        headline_row.update()
        
        subheadline_row = user_table.get(variable='subheadlines')
        subheadline_row['variable_value'] = None
        subheadline_row.update()
        
        vsl_script_row = user_table.get(variable='vsl_script')
        vsl_script_row['variable_value'] = None
        vsl_script_row.update()
        
       # Launch the background tasks concurrently
        # MAIN HEADLINES 
        task_id_main_headlines = anvil.server.call('launch_generate_main_headlines', self.chosen_product_name,self.chosen_company_profile,self.chosen_product_research, self.chosen_tone)
        print("Main Headlines Launch function called")
        self.indeterminate_progress_main_headlines.visible = True

      # SUBHEADLINES 
        task_id_subheadlines = anvil.server.call('launch_generate_subheadlines', self.chosen_product_name,self.chosen_company_profile,self.chosen_product_research, self.chosen_tone)
        print("Subheadlines Launch function called")
        self.indeterminate_progress_subheadlines.visible = True
     
        self.task_id_vsl_script = anvil.server.call('launch_generate_vsl_script', self.chosen_product_name, self.chosen_company_profile, self.chosen_product_research,self.chosen_avatar, self.chosen_tone, self.example_script)
        print("Video Sales Script function called")
        self.indeterminate_progress_main_headlines.visible = True
        self.indeterminate_progress_vsl_themes.visible = True

        self.task_check_timer_headlines.enabled = True
        self.task_check_timer_headlines.interval = 3  # Check every 2seconds
      
        self.task_check_timer_subheadlines.enabled = True
        self.task_check_timer_subheadlines.interval = 3  # Check every 2seconds

        self.task_check_timer_vsl_script.enabled = True
        self.task_check_timer_vsl_script.interval = 3  # Check every 2seconds
  
  def generate_vsl_themes_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        self.indeterminate_progress_vsl_excerpts.visible = True
        # Check if all of the textboxes are populated
        if not self.main_headline_textbox.text or not self.subheadline_textbox.text or not self.video_sales_script_textbox.text:
            anvil.js.window.alert("Please Populate All Fields Before Generating your themes.")
            return
        else:
            current_user = anvil.users.get_user()
            user_table_name = current_user['user_id']
            # Get the table for the current user
            user_table = getattr(app_tables, user_table_name)

            #Define and save the final headlines and subheadlines
            self.chosen_final_headline = self.main_headline_textbox.text
            self.chosen_final_subheadline = self.subheadline_textbox.text
            self.chosen_final_secondary_headline = self.secondary_headline_textbox.text
          
            chosen_final_headline_row = user_table.search(variable='chosen_final_headline')[0]
            chosen_final_subheadline_row = user_table.search(variable='chosen_final_subheadline')[0]
            chosen_final_secondary_headline_row = user_table.search(variable='chosen_final_secondary_headline')[0]
          
            chosen_final_headline_row['variable_value'] = self.chosen_final_headline
            chosen_final_subheadline_row['variable_value'] = self.chosen_final_subheadline
            chosen_final_secondary_headline_row['variable_value'] = self.chosen_final_secondary_headline
            chosen_final_headline_row.update()
            chosen_final_secondary_headline_row.update()
            
            row = user_table.get(variable='vsl_themes')
            vsl_theme_1_row = user_table.get(variable='vsl_theme_1')
            vsl_theme_2_row = user_table.get(variable='vsl_theme_2')
            vsl_theme_3_row = user_table.get(variable='vsl_theme_3')
            vsl_theme_4_row = user_table.get(variable='vsl_theme_4')
      
            self.task_id = anvil.server.call('launch_generate_vsl_themes', self.chosen_final_headline, self.chosen_final_subheadline, self.chosen_product_name, self.chosen_product_research, self.chosen_tone,self.video_sales_script_textbox,row)
    
            self.task_check_timer_vsl_themes.enabled = True
            self.task_check_timer_vsl_themes.interval = 3
        
  def check_task_status_headlines(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete

        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='main_headlines')

        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Headlines!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Main Headlines Generated!")
            self.task_check_timer_headlines.enabled = False
            self.task_check_timer_headlines.interval = 0
            self.indeterminate_progress_main_headlines.visible = False
                
            # Convert the JSON string back to a list
            all_main_headlines_json = row['variable_value'] 
          
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

            # Update the 'variable_value' column of the row
            row['variable_value'] = all_main_headlines_json
            row.update()

  def check_task_status_subheadlines(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete

        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        subheadlines_row = user_table.get(variable='subheadlines')

        if subheadlines_row['variable_value'] is None or subheadlines_row['variable_value'] == '':
            print("Still working on Subheadlines!")
        elif subheadlines_row['variable_value'] is not None and subheadlines_row['variable_value'] != '':
            print("Subheadlines Generated!")
            self.task_check_timer_headlines.enabled = False
            self.task_check_timer_headlines.interval = 0
            self.indeterminate_progress_subheadlines.visible = False

           # Convert the JSON string back to a list
            all_subheadlines_json = subheadlines_row['variable_value'] 
          
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

          # Update the 'variable_value' column of the row
            subheadlines_row['variable_value'] = all_subheadlines_json
            subheadlines_row.update()
   
  def check_task_status_vsl_script(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete

        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='vsl_script')

        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Video Sales Script Generated!")
                                      
            # Update the 'variable_value' column of the row
            vsl_script = row['variable_value']
            row.update()
          
            # Populate the textbox with the generated script
            self.video_sales_script_textbox.text = vsl_script
            self.task_check_timer_vsl_script.enabled = False
            self.task_check_timer_vsl_script.interval = 0
            self.generate_vsl_themes_button.visible = True
            self.indeterminate_progress_vsl_themes.visible = False

  def check_task_status_vsl_themes(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete

        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='vsl_themes')

        vsl_theme_1_row = user_table.get(variable='vsl_theme_1')
        vsl_theme_2_row = user_table.get(variable='vsl_theme_2')
        vsl_theme_3_row = user_table.get(variable='vsl_theme_3')
        vsl_theme_4_row = user_table.get(variable='vsl_theme_4')

        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on the Video Sales Script!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("VSL Themes Extracted!")
                                        
            # Populate the textbox with the generated script
            self.task_check_timer_vsl_script.enabled = False
            self.task_check_timer_vsl_script.interval = 0
            self.generate_vsl_themes_button.visible = False
            self.indeterminate_progress_vsl_excerpts.visible = False

            # Convert the JSON string back to a list
            all_vsl_themes_json = row['variable_value'] 
          
            all_vsl_themes = json.loads(all_vsl_themes_json)
            # Update the text boxes with the headlines
            self.excerpt_textbox_1.text = all_vsl_themes[0]
            self.excerpt_textbox_2.text = all_vsl_themes[1]
            self.excerpt_textbox_3.text = all_vsl_themes[2]
            self.excerpt_textbox_4.text = all_vsl_themes[3]

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

# REGENERATE STUFF    
  def regenerate_main_headlines_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        self.indeterminate_progress_main_headlines.visible = True
      
      # Delete whatever is in the table with existing headlines.
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        
      # Delete all the existing boxes and start fresh
        headline_row = user_table.get(variable='main_headlines')
        headline_row['variable_value'] = None
        headline_row.update()

        # MAIN HEADLINES 
        task_id_main_headlines = anvil.server.call('launch_generate_main_headlines', self.chosen_product_name,self.chosen_company_profile,self.chosen_product_research, self.chosen_tone)
        print("Main Headlines Launch function called")
        self.indeterminate_progress_main_headlines.visible = True

        self.task_check_timer_headlines.enabled = True
        self.task_check_timer_headlines.interval = 3  # Check every 2seconds
      
  def check_task_status_regenerate_headlines(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete

        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='main_headlines')
        row['variable_value'] = None
        row.update()
      
        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working on Headlines!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Main Headlines Generated!")
            self.task_check_timer_headlines.enabled = False
            self.task_check_timer_headlines.interval = 0
            self.indeterminate_progress_main_headlines.visible = False
                
            # Convert the JSON string back to a list
            all_main_headlines_json = row['variable_value'] 
          
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

            # Update the 'variable_value' column of the row
            row['variable_value'] = all_main_headlines_json
            row.update()

  def regenerate_subheadlines_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        self.indeterminate_progress_subheadlines.visible = True

      # Delete whatever is in the table with existing headlines.
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
              
        subheadline_row = user_table.get(variable='subheadlines')
        subheadline_row['variable_value'] = None
        subheadline_row.update()
        
       # Launch the background tasks concurrently
        # SUBHEADLINES 
        task_id_subheadlines = anvil.server.call('launch_generate_subheadlines', self.chosen_product_name,self.chosen_company_profile,self.chosen_product_research, self.chosen_tone)
        print("Subheadlines Launch function called")
        self.indeterminate_progress_subheadlines.visible = True
     
        self.task_check_timer_subheadlines.enabled = True
        self.task_check_timer_subheadlines.interval = 3  # Check every 2seconds

  def check_task_status_regenerate_subheadlines(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
      
        subheadlines_row = user_table.get(variable='subheadlines')
        subheadlines_row['variable_value'] = None
        subheadlines_row.update()

        if subheadlines_row['variable_value'] is None or subheadlines_row['variable_value'] == '':
            print("Still working on Subheadlines!")
        elif subheadlines_row['variable_value'] is not None and subheadlines_row['variable_value'] != '':
            print("Subheadlines Generated!")
            self.task_check_timer_headlines.enabled = False
            self.task_check_timer_headlines.interval = 0
            self.indeterminate_progress_subheadlines.visible = False

           # Convert the JSON string back to a list
            all_subheadlines_json = subheadlines_row['variable_value'] 
          
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

          # Update the 'variable_value' column of the row
            subheadlines_row['variable_value'] = all_subheadlines_json
            subheadlines_row.update()

  def regenerate_vsl_button_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        self.indeterminate_progress_vsl_script.visible = True

      # Delete whatever is in the table with existing headlines.
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        
        vsl_script_row = user_table.get(variable='vsl_script')
        vsl_script_row['variable_value'] = None
        vsl_script_row.update()
        
       # Launch the background tasks concurrently
      # REGENERATE VSL SCRIPT     
        self.task_id_vsl_script = anvil.server.call('launch_generate_vsl_script', self.chosen_product_name, self.chosen_company_profile, self.chosen_product_research,self.chosen_avatar, self.chosen_tone, self.example_script)
        print("Video Sales Script function called")
    
        self.task_check_timer_regenerate_vsl_script.enabled = True
        self.task_check_timer_regenerate_vsl_script.interval = 3  # Check every 2seconds

  def check_task_status_regenerate_vsl_script(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete

        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='vsl_script')

        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Video Sales Script Generated!")
                                      
            # Update the 'variable_value' column of the row
            vsl_script = row['variable_value']
            row.update()
          
            # Populate the textbox with the generated script
            self.video_sales_script_textbox.text = vsl_script
            self.task_check_timer_vsl_script.enabled = False
            self.task_check_timer_vsl_script.interval = 0
            self.indeterminate_progress_vsl_script.visible = False
            self.generate_vsl_themes_button.visible = True
            return

  def regenerate_vsl_button_with_edits_click(self, **event_args):
    with anvil.server.no_loading_indicator:
        self.indeterminate_progress_vsl_themes_rewrites.visible = True
        vsl_script_feedback = self.feedback_box.text
      
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        
        vsl_script_row = user_table.get(variable='vsl_script')
        vsl_script_row['variable_value'] = None
        vsl_script_row.update()
        
       # Launch the background tasks concurrently
      # REGENERATE VSL SCRIPT     
        self.task_id_vsl_script_feedback = anvil.server.call('launch_generate_vsl_script_with_feedback', self.chosen_product_name, self.chosen_product_research,vsl_script_feedback)
        print("Video Sales Script For Feedback function called")
    
        self.task_check_timer_regenerate_vsl_script_with_feedback.enabled = True
        self.task_check_timer_regenerate_vsl_script_with_feedback.interval = 3  # Check every 2seconds


  def check_task_status_regenerate_vsl_script_with_feedback(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete

        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='vsl_script')

        if row['variable_value'] is None or row['variable_value'] == '':
            print("Still working!")
        elif row['variable_value'] is not None and row['variable_value'] != '':
            print("Video Sales Script Generated!")
                                      
            # Update the 'variable_value' column of the row
            vsl_script = row['variable_value']
            row.update()
          
            # Populate the textbox with the generated script
            self.video_sales_script_textbox.text = vsl_script
            self.task_check_timer_regenerate_vsl_script_with_feedback.enabled = False
            self.task_check_timer_regenerate_vsl_script_with_feedback.interval = 0
            self.indeterminate_progress_vsl_themes_rewrites.visible = False
            self.generate_vsl_themes_button.visible = True
            return
          
###---- GENERATE HEADLINES--------#########################################################################################################
  #Use the saved values in other functions
  # def generate_main_headlines_button_click(self, **event_args):
  #   with anvil.server.no_loading_indicator:
  #       print("Main Headlines Launch function was received!")

  #       current_user = anvil.users.get_user()
  #       user_table_name = current_user['user_id']
  #       # Get the table for the current user
  #       user_table = getattr(app_tables, user_table_name)
  #       row = user_table.get(variable='main_headlines')

  #       # Start the timer immediately
  #       self.task_check_timer_headlines.enabled = True
  #       self.task_check_timer_headlines.interval = 5  # Check every 5 seconds

            
    #       #Define and save the final headlines and subheadlines
      # self.chosen_final_headline = self.main_headline_textbox.text
      # self.chosen_final_secondary_headline = self.secondary_headline_textbox.text
      # chosen_final_headline_row = user_table.search(variable='chosen_final_headline')[0]
    #   chosen_final_secondary_headline_row = user_table.search(variable='chosen_final_secondary_headline')[0]

    #   chosen_final_headline_row['variable_value'] = self.chosen_final_headline
    #   chosen_final_secondary_headline_row['variable_value'] = self.chosen_final_secondary_headline
    #   chosen_final_headline_row.update()
    #   chosen_final_secondary_headline_row.update()
    
  
              
  def check_task_status(self, sender=None, **event_args):
    with anvil.server.no_loading_indicator:
        # Check if the background task is complete
        task_status = anvil.server.call('get_task_status', self.task_id)
        print("Task status:", task_status)
      
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
        row = user_table.get(variable='main_headlines')
      
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

                # Stop the timer
                self.task_check_timer_headlines.enabled = False

            elif task_status == "failed":
                # Handle the case where the background task failed
                print("Task failed")
                # Stop the timer
                self.task_check_timer_headlines.enabled = False

          

          
# NAVIGATION

# Define the function to navigate to the 'Company' form
  def navigate_to_headlines(self, **event_args):
    anvil.open_form('Company')

#### ----- SAVE VARIABLES------------######
  def set_saved_values(self, chosen_company_name, chosen_company_profile, chosen_product_name, chosen_product_research, chosen_tone, chosen_avatar, chosen_script):
      self.chosen_company_name = chosen_company_name
      self.chosen_company_profile = chosen_company_profile
      self.chosen_product_name = chosen_product_name
      self.chosen_product_research = chosen_product_research
      self.chosen_tone = chosen_tone
      self.chosen_avatar = chosen_avatar
      self.chosen_script = chosen_script
    
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

  ###### ----- SUBHEADLINE HANDLERS------------######
  # Event handler for the click event of the radio buttons
  def subheadline_button_click(self, **event_args):
    # Get the clicked radio button
    clicked_radio_button = event_args['sender']

    # Get the text of the clicked radio button
    selected_subheadline = clicked_radio_button.text

    # Set the text of the textbox
    self.subheadline_textbox.text = selected_subheadline

    # Turn on the button
    # self.nav_button_headlines_to_vsl.enabled = True

  # Lock everything in, and navigate away
  def nav_button_headlines_to_vsl_click(self, **event_args):
    
    # SAVE THE CHOSEN HEADLINES
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

      # Check if any of the textboxes are empty
    if not self.main_headline_textbox.text or not self.subheadline_textbox.text or not self.secondary_headline_textbox.text:
        # If any of the textboxes are empty, show an alert
        anvil.js.window.alert("Please choose your headline, subheadline, and secondary headline before proceeding")
        return
    else:
      self.chosen_final_headline = self.main_headline_textbox.text
      self.chosen_final_subheadline = self.subheadline_textbox.text
      self.chosen_final_secondary_headline = self.secondary_headline_textbox.text
      
      chosen_final_headline_row = user_table.search(variable='chosen_final_headline')[0]
      chosen_final_subheadline_row = user_table.search(variable='chosen_final_subheadline')[0]
      chosen_final_secondary_headline_row = user_table.search(variable='chosen_final_secondary_headline')[0]
        
      chosen_final_headline_row['variable_value'] = self.chosen_final_headline
      chosen_final_subheadline_row['variable_value'] = self.chosen_final_subheadline
      chosen_final_secondary_headline_row['variable_value'] = self.chosen_final_secondary_headline
      chosen_final_headline_row.update()
      chosen_final_subheadline_row.update()
      chosen_final_secondary_headline_row.update()
    
      #Navigate away
      anvil.open_form('VideoSalesLetter')

  def email_my_script_click(self, **event_args):
   anvil.js.window.alert("Check your inbox (TBD, but it's easily doable!")
   pass

  def provide_feedback_button_click(self, **event_args):
    self.rewrite_box.visible = True
    

