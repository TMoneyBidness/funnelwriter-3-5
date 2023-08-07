from ._anvil_designer import HomeTemplate
from anvil import *
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
from ..Product import Product
from ..BrandTone import BrandTone
from ..Avatars import Avatars
from ..VSL_Elements import VSL_Elements
from ..VideoSalesLetter import VideoSalesLetter
from ..FinalProduct import FinalProduct
####################


class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.users.login_with_form()
    self.indeterminate_1.visible = False
    self.free_navigate_label.visible = False
    self.status.text = 'Idle'
    self.youtube_intro_video.visible = False
    self.nav_button_company_to_products.visible = False

    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)
    
    # HIDE ALL PANELS OFF THE TOP
    # Hide Product 1, Avatars 2 and 3
    self.avatar_2_product_1_input_section.visible = False 
    self.avatar_3_product_1_input_section.visible = False
    
    # Hide Product 2, Avatars 2 and 3
    self.avatar_2_product_2_input_section.visible = False 
    self.avatar_3_product_2_input_section.visible = False
    
    # Hide Product 3, Avatars 2 and 3
    self.avatar_2_product_3_input_section.visible = False 
    self.avatar_3_product_3_input_section.visible = False
    
    # Hide Product 5, Avatars 2 and 3
    self.avatar_2_product_5_input_section.visible = False 
    self.avatar_3_product_5_input_section.visible = False

    # Hide Product 4, Avatars 2 and 3
    self.avatar_2_product_4_input_section.visible = False 
    self.avatar_3_product_4_input_section.visible = False
    
    # Hide Panels of Products 2-5
    self.product_2_panel.visible = False 
    self.product_3_panel.visible = False 
    self.product_4_panel.visible = False 
    self.product_5_panel.visible = False 
       

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
    self.avatar_3_product_34_input_section.visible = True
    self.add_avatar_2_product_4.visible = False
    self.add_avatar_3_product_4.visible = False 

  def add_product_3_panel_click(self, **event_args):
    self.product_3_panel.visible = True

# Panel 5 / Product 5
  def add_avatar_2_product_5_click(self, **event_args):
    self.avatar_2_product_5_input_section.visible = True
    self.add_avatar_2_product_5.visible = False
 
  def add_avatar_3_product_3_click(self, **event_args):
    self.avatar_3_product_5_input_section.visible = True
    self.add_avatar_2_product_5.visible = False
    self.add_avatar_3_product_5.visible = False 

###-----------GO GET ALL ASSETS--------------##
  
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

        # AVATAR 1 DESCRIPTION
        avatar_1_preview = self.avatar_1_name_input.text
        avatar_1_preview_row = user_table.search(variable='avatar_1_preview')[0]
        avatar_1_preview_row['variable_value'] = avatar_1_preview
        avatar_1_preview_row.update()

        # LAUNCH THE BACKGROUND TASKS
        # Launch the background task for company summary
        task_id_company_summary = anvil.server.call('launch_draft_company_summary', user_table, company_name, company_url)
        print("Company Research Started")
        
        # Launch the background task for product research
        task_id_product_research = anvil.server.call('launch_draft_deepdive_product_1_generator', user_table, company_name, product_1_name, product_1_url)
        print("Deep Dive Product Research Started")
        
        # Launch the background task for Avatar
        task_id_avatar = anvil.server.call('launch_draft_deepdive_avatar_1_generator', user_table, company_name, product_1_name, avatar_1_preview)
        print("Deep Dive Draft Avatar Research Started") 
        
        # Launch the background task for brand tone
        task_id_brand_tone = anvil.server.call('launch_draft_brand_tone_research', user_table, company_url)
        print("Brand Tone Research Started")
        
        # Check the status of the background task for Avatar
        while True:
            task_status_avatar = anvil.server.call('get_task_status', task_id_avatar)
            print("Avatar Task Status:", task_status_avatar)
            if task_status_avatar == "completed":
                # Background task completed successfully
                avatar_result = anvil.server.call('get_task_result', task_id_avatar)
                print("Avatar Research Result:", avatar_result)
                # Update the user table with the result
                avatar_row = user_table.get(variable='avatar_1_latest')
                avatar_row['variable_value'] = avatar_result
                avatar_row.update()
                break
            elif task_status_avatar == "failed":
                # Background task encountered an error
                print("Avatar Research Failed")
                break
            # Sleep for a few seconds before checking again
            time.sleep(2)
        
        # Check the status of the background task for brand tone
        while True:
            task_status_brand_tone = anvil.server.call('get_task_status', task_id_brand_tone)
            print("Brand Tone Task Status:", task_status_brand_tone)
            if task_status_brand_tone == "completed":
                # Background task completed successfully
                brand_tone_result = anvil.server.call('get_task_result', task_id_brand_tone)
                print("Brand Tone Research Result:", brand_tone_result)
                # Update the user table with the result
                brand_tone_row = user_table.get(variable='brand_tone')
                brand_tone_row['variable_value'] = brand_tone_result
                brand_tone_row.update()
                break
            elif task_status_brand_tone == "failed":
                # Background task encountered an error
                print("Brand Tone Research Failed")
                break
            # Sleep for a few seconds before checking again
            time.sleep(2)
          
        # Check the status of the background task for company summary
        while True:
            task_status_company_summary = anvil.server.call('get_task_status', task_id_company_summary)
            print("Company Summary Task Status:", task_status_company_summary)
            if task_status_company_summary == "completed":
                # Background task completed successfully
                company_summary_result = anvil.server.call('get_task_result', task_id_company_summary)
                print("Company Summary Result:", company_summary_result)
                # Update the user table with the result
                company_profile_row = user_table.get(variable='company_profile')
                company_profile_row['variable_value'] = company_summary_result
                company_profile_row.update()
                break
            elif task_status_company_summary == "failed":
                # Background task encountered an error
                print("Company Profile Failed")
                break
            # Sleep for a few seconds before checking again
            time.sleep(2)
        
        # Check the status of the background task for product research
        while True:
            task_status_product_research = anvil.server.call('get_task_status', task_id_product_research)
            print("Product Research Task Status:", task_status_product_research)
            if task_status_product_research == "completed":
                # Background task completed successfully
                product_research_result = anvil.server.call('get_task_result', task_id_product_research)
                print("Product Research Result:", product_research_result)
                # Update the user table with the result
                product_research_row = user_table.get(variable='product_research')
                product_research_row['variable_value'] = product_research_result
                product_research_row.update()
                break
            elif task_status_product_research == "failed":
                # Background task encountered an error
                print("Product Research Failed")
                break
            # Sleep for a few seconds before checking again
            time.sleep(2)
        
  # NAVIGATION
  
  def home_asset_link_copy_click(self, **event_args):
    open_form("Home")

  def product_asset_link_click(self, **event_args):
    product=Product()
    self.content_panel.clear()
    self.content_panel.add_component(product)

  def company_asset_link_click(self, **event_args):
    company=Company()
    self.content_panel.clear()
    self.content_panel.add_component(company)

  def brand_tone_asset_link_click(self, **event_args):
    brandtone=BrandTone()
    self.content_panel.clear()
    self.content_panel.add_component(brandtone)

  def avatars_asset_link_click(self, **event_args):
    avatars=Avatars()
    self.content_panel.clear()
    self.content_panel.add_component(avatars)

  def finalproduct_page_link_click(self, **event_args):
    finalproduct=FinalProduct()
    self.content_panel.clear()
    self.content_panel.add_component(finalproduct)

  def nav_button_to_company_click(self, **event_args):
    company = Company()
    self.content_panel.clear()
    self.content_panel.add_component(company)


## FUNNELS
  def VSL_page_link_click(self, **event_args):
    vsl_elements = VSL_Elements()
    self.content_panel.clear()
    self.content_panel.add_component(vsl_elements)



 
