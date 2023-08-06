from ._anvil_designer import Home_oldTemplate
from anvil import *
import plotly.graph_objects as go
import time
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

from ..Product import Product

############################################################################################################

PROMPT_TITLE = "FunnelWriter.AI needs a title to SAVE AS"

## LOADING
class Home_old(Home_oldTemplate):
  def __init__(self, **properties):
    # Call the parent class's __init__ method
    super().__init__(**properties)
    # Initialize task_id attribute
    self.task_id = None
    # Initialize counter
    anvil.users.login_with_form()
    self.indeterminate_1.visible = False
    self.free_navigate_label.visible = False
    self.status.text = 'Idle'
    self.youtube_intro_video.visible = False
    self.nav_button_company_to_products.visible = False
    self.add_another_product_panel_1.visible = False
    
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

  def go_get_all_assets_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Go Get All 1st Draft Assets")
    
      # Stop the function if any of the fields are empty
      if not self.company_name_input.text or not self.company_url_input.text or not self.product_1_name_input.text:
          anvil.js.window.alert("Please fill in all the required fields before generating the full description.")
          return

      else:
        self.indeterminate_1.visible = True
        self.free_navigate_label.visible = True
        self.status.text = 'Researching'

        # Load stuff        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
    
        # COMPANY NAME
        company_name = self.company_name_input.text
        # Save company name
        company_name_row = user_table.get(variable='company_name')
        company_name_row['variable_value'] = company_name
        company_name_row.update()
        
        # COMPANY URL
        company_url = self.company_url_input.text
        # Save company url
        company_url_row = user_table.get(variable='company_url')
        company_url_row['variable_value'] = company_url
        company_url_row.update()

        # PRODUCT 1 NAME
        product_1_name = self.product_1_name_input.text
        # Save product 1 name
        product_1_row = user_table.get(variable='product_1')
        product_1_row['variable_title'] = product_1_name
        product_1_row.update()

        # PRODUCT 1 URL
        product_1_url = self.product_1_url_input.text
        # Save product 1 url
        product_1_url_row = user_table.get(variable='product_1_url')
        product_1_url_row['variable_value'] = product_1_url
        product_1_url_row.update()

      # LAUNCH THE BACKGROUND TASKS
       # Launch the background task for company summary
        anvil.server.call('launch_draft_company_summary',user_table, company_name, company_url)
        print("Company Research Started")
       # Launch the background task for product research
        anvil.server.call('launch_draft_deepdive_product_1_generator',user_table,company_name,product_1_name,product_1_url)
        print("Deep Dive Product Research Started") 
      # Launch the background task for brand tone
        anvil.server.call('launch_draft_brand_tone_research', user_table,company_url)
        print("Brand Tone Research Started")

  
 ### Show Other Panels
  def add_another_product_panel_1_click(self, **event_args):
    self.add_another_product_panel_1.visible = True
    
    ### NAVIGATION
  def navigate_to_product(self, **event_args):
   product = Product()
   self.content_panel.clear()
   self.content_panel.add_component(product)
    # anvil.open_form('Product')

 ### Show Other Panels
  def add_another_product_panel_1_click(self, **event_args):
    self.add_another_product_panel_1.visible = True
    
  # def company_research(self, company_name,company_url):
  #   with anvil.server.no_loading_indicator:
  #       # This method should handle the UI logic
  #       print("Company Research Started")
  #       # Start the progress bar with a small value
  #       count_timer = 0
  #       self.youtube_intro_video.visible = True
  #       # print("Before setting status:", self.status.text)
  #       # self.status.text = 'Researching'
  #       # print("After setting status:", self.status.text)
  #       current_user = anvil.users.get_user()
  #       user_table_name = current_user['user_id']
  #       user_table = getattr(app_tables, user_table_name)
          
  #       # Launch the background task and store the task ID
  #       self.task_id = anvil.server.call('launch_company_summary', company_name, company_url)
  #       print("Task ID:", self.task_id)
      
  #       # Loop to check the status of the background task
  #       while True:
                    
  #           # Check if the background task is complete
  #           task_status = anvil.server.call('get_task_status', self.task_id)
  #           print("Task status:", task_status)
            
  #           if task_status is not None and task_status == "completed":
  #               # Get the result of the background task
  #               company_context = anvil.server.call('get_task_result', self.task_id)
                
  #               # Save this generated version as the latest version
  #               row_company_profile_latest = user_table.search(variable='company_profile_latest')
  #               row_company_profile_latest[0]['variable_value'] = company_context
  #               row_company_profile_latest[0].update()
  #               print("Company Research Complete")
  #               break  # Exit the loop
            
  #           # Sleep for 1 second before checking again
  #           time.sleep(2)
  
  # def brand_tone(self,company_url):
  #   with anvil.server.no_loading_indicator:
  #     # This method should handle the UI logic
  #     print("Brand Tone Research Started")
  #     # Start the progress bar
  #     self.indeterminate_brand_tone.visible = True
  #     brand_tone_url = company_url
      
  #     # Get the current user 
  #     current_user = anvil.users.get_user() 
  #     user_table_name = current_user['user_id']
  #     user_table = getattr(app_tables, user_table_name)
     
  #     # Save the brand tone URL
  #     brand_tone_url_latest_row = list(user_table.search(variable='brand_tone_url'))
      
  #     # Check if the row exists before updating it
  #     if brand_tone_url_latest_row:
  #         brand_tone_url_latest_row[0]['variable_value'] = brand_tone_url
  #         brand_tone_url_latest_row[0].update()
      
  #     self.task_id = anvil.server.call('launch_brand_tone_research', brand_tone_url)
  #     print("Task ID:", self.task_id)

  #    # Loop to check the status of the background task
  #   while True:
  #     with anvil.server.no_loading_indicator:
     
  #       # Check if the background task is complete
  #       task_status = anvil.server.call('get_task_status', self.task_id)
  #       print("Task status:", task_status)
  
  #       if task_status is not None:
  #         if task_status == "completed":
  #           # Get the result of the background task
  #           brand_tone_research = anvil.server.call('get_task_result', self.task_id)
  #           # Update the textbox with the result
  #           print("Brand Tone Research Complete")
  #           break  # Exit the loop
            
  #         elif task_status == "failed":
  #           # Get the error message
  #           task_error = anvil.server.call('get_task_result', self.task_id)
  #           print("Task error:", task_error)
  #           print("Brand Tone Research Error")
  #           break  # Exit the loop
  
  #       # Sleep for 1 second before checking again
  #       time.sleep(2)

  # def product_1_research(self,company_name, product_1_name, product_1_url):
  #   with anvil.server.no_loading_indicator:
  #     # This method should handle the UI logic
  #     print("Deep Product Researcher Initiated")
    
  #     # self.nav_button_products_to_avatars.enabled = False

  #     # Stop the Function if there's no product name
  #     if not self.product_1_name_input.text:
  #       anvil.js.window.alert("Please name your product before generating the full description.")
  #       return
  #     else:
  #       self.indeterminate_1.visible = True
  #       # Load stuff        
  #       current_user = anvil.users.get_user()
  #       user_table_name = current_user['user_id']
  #       # Get the table for the current user
  #       user_table = getattr(app_tables, user_table_name)
                  
  #       self.task_id = anvil.server.call('launch_deepdive_product_1_generator', company_name, product_1_name, product_1_url)
  #       print("Task ID:", self.task_id)
    
  #       # Loop to check the status of the background task
  #     while True:
  #       with anvil.server.no_loading_indicator:
    
  #       # Check if the background task is complete
  #         task_status = anvil.server.call('get_task_status', self.task_id)
  #         print("Task status:", task_status)
    
  #         if task_status is not None:
  #           if task_status == "completed":
  #         # Get the result of the background task
  #             product_1_generation = anvil.server.call('get_task_result', self.task_id)
              
  #             # # Update the textbox with the result
  #             # print("Product:", product_1_generation)
  #             # self.product_profile_1_textbox.text = product_1_generation
    
  #             # Save it in the table:
  #             product_1_latest_row = user_table.search(variable='product_1_latest')[0]
  #             product_1_latest_row['variable_value'] = product_1_generation
        
  #             break  # Exit the loop
              
  #           elif task_status == "failed":
  #             # Get the error message
  #             task_error = anvil.server.call('get_task_result', self.task_id)
  #             print("Task error:", task_error)
  #             # self.indeterminate_1.visible = False
  #             break  # Exit the loop
    
  #         # Sleep for 1 second before checking again
  #         time.sleep(2)


  # def form_show(self, **event_args):
  #   # Load the company profile on form show
  #   # self.company_profile_textbox.load_data()
  #   self.company_name_input.load_data()
  #   self.company_url_input.load_data()
    
  # def edit_company_profile_component_click(self, **event_args):
  #   self.company_profile_textbox.read_only = False
  
  # def save_company_profile_component_click(self, **event_args):
  #   # Get the current user
  #   current_user = anvil.users.get_user()
  #   user_table_name = current_user['user_id']

  #   # Get the table for the current user
  #   user_table = getattr(app_tables, user_table_name)

  #   # Check if the company profile textbox is not empty and doesn't have the placeholder text
  #   if self.company_profile_textbox.text.strip() and self.company_profile_textbox.text.strip() != "AI agents will populate your company profile here!":
  #       company_profile_row = user_table.get(variable='company_profile')
  #       company_profile_row['variable_value'] = self.company_profile_textbox.text
  #       company_profile_row.update()
  #       self.nav_button_company_to_products.enabled = True
  #       self.nav_button_company_to_products.background = "#6750A4"  # Set the background color to green
  #       self.nav_button_company_to_products.foreground = "#1E192B"

  #       # Save this generated version as the latest version
  #       # Save company name
  #       company_name_row = user_table.get(variable='company_name')
  #       company_name_row['variable_value'] = self.company_name_input.text
  #       company_name_row.update()
  #       company_name = self.company_name_input.text
        
  #       # Save company URL
  #       company_url_row = user_table.get(variable='company_url')
  #       company_url_row['variable_value'] = self.company_url_input.text
  #       company_url_row.update()
  #       company_url = self.company_url_input.text
      
  #       row_company_profile_latest = user_table.search(variable='company_profile_latest')
  #       row_company_profile_latest[0]['variable_value'] = self.company_profile_textbox.text
  #       row_company_profile_latest[0].update()
  #       self.nav_button_company_to_products.enabled = True
  #   else:
  #       # Handle case where no profile name is selected
  #       anvil.js.window.alert("Please build your company profile before proceeding")
  #       self.nav_button_company_to_products.enabled = False
  #       self.nav_button_company_to_products.background = "#EADDFF"

  # def load_company_profile_component_click(self, **event_args):
  #   # Get the current user
  #   current_user = anvil.users.get_user()
  #   user_table_name = current_user['user_id']

  #   # Get the table for the current user
  #   user_table = getattr(app_tables, user_table_name)

  #   company_profile_row = user_table.get(variable='company_profile')

  #   # Load the Company Profile from the profile row
  #   self.company_profile_textbox.text = company_profile_row['variable_value']

  #   # Load the Company Name and URL from the user_table
  #   company_name_row = user_table.get(variable='company_name')
  #   company_url_row = user_table.get(variable='company_url')


  

# THIS IS THE CODE IF WE CONTINUED TO DO LOAD / SAVE SLOTS:

# THIS IS THE SLOT LOADING OPTION AS SOON AS WE OPEN THE PAGE

    # # Get the variable_title values for the specific profiles
    # variable_titles_company_profiles = []

    # # Search for the rows with company_profile_1
    # rows_company_profile_1 = user_table.search(variable='company_profile_1')
    # if rows_company_profile_1:
    #     variable_titles_company_profiles.append(rows_company_profile_1[0]['variable_title'])

    # # Search for the rows with company_profile_2
    # rows_company_profile_2 = user_table.search(variable='company_profile_2')
    # if rows_company_profile_2:
    #     variable_titles_company_profiles.append(rows_company_profile_2[0]['variable_title'])

    # # Search for the rows with company_profile_3
    # rows_company_profile_3 = user_table.search(variable='company_profile_3')
    # if rows_company_profile_3:
    #     variable_titles_company_profiles.append(rows_company_profile_3[0]['variable_title'])

    # # Update the dropdown items with the variable_titles
    # self.company_profile_dropdown.items = variable_titles_company_profiles
    # self.load_company_profile_dropdown.items = variable_titles_company_profiles


 # def save_company_profile_component_click(self, **event_args):
 #    # Get the current user
 #    current_user = anvil.users.get_user()
 #    user_table_name = current_user['user_id']

 #    # Get the table for the current user
 #    user_table = getattr(app_tables, user_table_name)

 #    # Prompt the user to select a profile name from the dropdown
 #    selected_profile_name = self.company_profile_dropdown.selected_value

 #    # Check if a profile name is selected
 #    if selected_profile_name:
 #        # Get the row from the user_table based on the selected profile name
 #        profile_row = user_table.get(variable_title=selected_profile_name)

 #        # Update the variable_value column in the profile row
 #        profile_row['variable_value'] = self.company_profile_textbox.text

 #        # Prompt the user to enter the variable name/title
 #        variable_title = anvil.js.window.prompt("What would you like to call this profile?")

 #        # Check if the user entered a variable name/title
 #        if variable_title is not None:
 #            # Update the variable_title column in the profile row
 #            profile_row['variable_title'] = variable_title

 #            # Save the Company Name and URL
 #            company_name_row = user_table.get(variable='company_name')
 #            company_url_row = user_table.get(variable='company_url')

 #            # Check if company_name_row and company_url_row exist
 #            if company_name_row and company_url_row:
 #                company_name_row['variable_value'] = self.company_name_input.text
 #                company_url_row['variable_value'] = self.company_url_input.text
 #                # Update the rows in the user_table
 #                company_name_row.update()
 #                company_url_row.update()
 #            else:
 #                # Handle case where company_name_row or company_url_row is missing
 #                print("Company name or URL not found")
 #        else:
 #            # Handle case where the user cancelled the variable name/title prompt
 #            print("Variable name/title input cancelled by the user")
 #    else:
 #        # Handle case where no profile name is selected
 #        print("No profile name selected")
 


  # def load_company_profile_component_click(self, **event_args):
  #   # Get the current user
  #   current_user = anvil.users.get_user()
  #   user_table_name = current_user['user_id']

  #   # Get the table for the current user
  #   user_table = getattr(app_tables, user_table_name)

  #   # Prompt the user to select a profile name from the dropdown
  #   selected_profile_name = self.load_company_profile_dropdown.selected_value

  #   # Check if a profile name is selected
  #   if selected_profile_name:
  #       # Get the row from the user_table based on the selected profile name
  #       profile_row = user_table.get(variable_title=selected_profile_name)

  #       # Load the Company Profile from the profile row
  #       self.company_profile_textbox.text = profile_row['variable_value']

  #       # Load the Company Name and URL from the user_table
  #       company_name_row = user_table.get(variable='company_name')
  #       company_url_row = user_table.get(variable='company_url')

  #       # Check if company_name_row and company_url_row exist
  #       if company_name_row and company_url_row:
  #           self.company_name_input.text = company_name_row['variable_value']
  #           self.company_url_input.text = company_url_row['variable_value']
  #       else:
  #           # Handle case where company_name_row or company_url_row is missing
  #           print("Company name or URL not found")
  #   else:
  #       # Handle case where no profile name is selected
  #       print("No profile name selected")


# Launch the Brand Tone and Save it!

  # def extract_my_brand_tone(self, **event_args):
  #   with anvil.server.no_loading_indicator:

  #     brand_tone_url = self.company_url_input.text
  #     brand_tone_title = self.company_name_input.text
      
  #     # Get the current user 
  #     current_user = anvil.users.get_user() 
  #     user_table_name = current_user['user_id']
  #     user_table = getattr(app_tables, user_table_name)
     
  #     brand_tone_url_latest_row = list(user_table.search(variable='brand_tone_url'))
  #     brand_tone_title_row = user_table.get(variable='brand_tone')
      
  #     # Check if the row exists before updating it
  #     if brand_tone_url_latest_row:
  #         brand_tone_url_latest_row[0]['variable_value'] = brand_tone_url
  #         brand_tone_url_latest_row[0].update()
      
  #     if brand_tone_title_row is not None:
  #         brand_tone_title_row['variable_title'] = brand_tone_title 
  #         brand_tone_title_row.update()


  #     self.task_id = anvil.server.call('launch_brand_tone_research', brand_tone_url)
  #     print("Task ID:", self.task_id)

  #    # Loop to check the status of the background task
  #   while True:
  #     with anvil.server.no_loading_indicator:
     
  #       # Check if the background task is complete
  #       task_status = anvil.server.call('get_task_status', self.task_id)
  #       print("Task status:", task_status)
  
  #       if task_status is not None:
  #         if task_status == "completed":
  #           # Get the result of the background task
  #           brand_tone_research = anvil.server.call('get_task_result', self.task_id)
  #           # Update the textbox with the result
  #           print("Brand Tone:", brand_tone_research  )
  #           brand_tone_title_row[0]['variable_value'] = brand_tone_research
  #           brand_tone_title_row.update()
  #           break  # Exit the loop
  #         elif task_status == "failed":
  #           # Get the error message
  #           task_error = anvil.server.call('get_task_result', self.task_id)
  #           print("Task error:", task_error)
           
  #           break  # Exit the loop
  
  #       # Sleep for 1 second before checking again
  #       time.sleep(2)


       # self.task_id = anvil.server.call('launch_go_get_all_assets', company_name, company_url, product_1_name, product_1_url)
        # print("Task ID:", self.task_id)

        # # Start monitoring the task status
        # while True:
        #     task_status = anvil.server.call('get_background_task_status', self.task_id)
        #     print("Task status:", task_status)

        #     if task_status == "completed":
        #         # Get the result of the background task
        #         company_context = anvil.server.get_background_task_result(self.task_id)
        #         # Update the textbox with the result
        #         print("Company Context:", company_context)
        #         self.company_profile_textbox.text = company_context

        #         # Save this generated version as the latest version
        #         row_company_profile_latest = user_table.search(variable='company_profile_latest')
        #         row_company_profile_latest[0]['variable_value'] = company_context
        #         row_company_profile_latest[0].update()

        #         self.status.text = 'Complete'
        #         self.indeterminate_company_research.visible = False
        #         self.free_navigate_label.visible = False
        #         break  # Exit the loop

        #     elif task_status == "failed":
        #         # Get the error message
        #         task_error = anvil.server.get_background_task_result(self.task_id)
        #         print("Task error:", task_error)
        #         break  # Exit the loop

            # Sleep for 1 second before checking again
            # time.sleep(2)

        # while True:                       
        #         # Check if the background task is complete
        #         task_status = anvil.server.call('get_task_status', self.task_id)
        #         print("Task status:", task_status)
                
        #         if task_status is not None and task_status == "completed":
          
        #             self.status.text = 'Complete'
        #             self.indeterminate_1.visible = False
        #             self.free_navigate_label.visible = False
        #             break  # Exit the loop
                
        #         # Sleep for 1 second before checking again
        #         time.sleep(2)
    
        # # PRODUCT 2 NAME
        # product_name_2 = self.product_2_name_input.text
        # product_2_row = user_table.get(variable='product_2')
        # product_2_row['variable_title'] = product_name_2
        # product_2_row.update()

        # # # PRODUCT 1 URL
        # # product_url_2 = self.product_2_url_input.text
        # # product_url_2_row = user_table.get(variable='product_url_2')
        # # product_url_2_row['variable_value'] = product_url_1
        # # product_url_2_row.update()
        
        # # Launch the background task and store the task ID
        # self.task_id = anvil.server.call('launch_go_get_all_assets', company_name, company_url)
        # print("Task ID:", self.task_id)
        
        # # Save it it as the latest as well
        # product_1_latest_row = user_table.search(variable='product_1_latest')[0]
        # product_1_latest_row['variable_value'] = product_1_latest
        # product_1_latest_row.update()
        
        # # COMPANY PROFILE
        # # Retrieve the row with 'variable' column containing 'company_profile'
        # company_profile_row = user_table.search(variable='company_profile')[0]
        # company_profile = company_profile_row['variable_value']
    
        # # COMPANY URL
        # # Retrieve the row with 'variable' column containing 'company_profile'
        # company_url_row = user_table.search(variable='company_url')[0]
        # company_url = company_url_row['variable_value']
    
        # # PRODUCT NAME
        # product_1_name = self.product_1_name_input.text
        # product_1_name_row = user_table.search(variable='product_1_name_latest')[0]
        # product_1_name_row['variable_value'] = product_1_name
    
        # # PRODUCT EXCERPT / PREVIEW
        # product_1_preview = self.product_profile_1_textbox.text
        # product_1_latest = self.product_profile_1_textbox.text
        # product_1_preview_row = user_table.search(variable='product_1_preview')[0]
        # product_1_preview_row['variable_value'] = product_1_preview
        # product_1_preview_row.update()
        # # Save it it as the latest as well
        # product_1_latest_row = user_table.search(variable='product_1_latest')[0]
        # product_1_latest_row['variable_value'] = product_1_latest
        # product_1_latest_row.update()
              
        # self.task_id = anvil.server.call('launch_go_get_all_assets', company_name,company_url,product_1_name,product_1_url)
        # print("Task ID:", self.task_id)

    
    # # Load the latest company profile
    # row_company_profile_latest = user_table.search(variable='company_profile_latest')
    # if row_company_profile_latest:
    #     company_profile_latest = row_company_profile_latest[0]['variable_value']
    #     self.company_profile_textbox.text = company_profile_latest
    # else:
    #     # Handle case where the row does not exist for the current user
    #     print("No row found for 'company_profile_latest'")

    # # Load the latest company name  
    # row_company_name = user_table.search(variable='company_name')
    # if row_company_name:
    #     company_name = row_company_name[0]['variable_value']
    #     self.company_name_input.text = company_name

    # # Load the latest company name
    # row_company_url = user_table.search(variable='company_url')
    # if row_company_url:
    #     company_url = row_company_url[0]['variable_value']
    #     self.company_url_input.text = company_url

    # # Check if any of the final company profile is empty
    # row_company_profile = user_table.search(variable='company_profile')
    # if not row_company_profile:
    #     # If any of the company profiles are empty, disable the button
    #     self.nav_button_company_to_products.enabled = False
    # else:
    #     # If all company profiles are saved, enable the button and navigate to the 'Products' form
    #     self.nav_button_company_to_products.enabled = True


