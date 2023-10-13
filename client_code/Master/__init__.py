from ._anvil_designer import MasterTemplate
from anvil import *
import stripe.checkout
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

from ..Product import Product
from ..BrandTone import BrandTone
from ..Avatars import Avatars
from ..VSL_Elements import VSL_Elements
from ..VideoSalesLetter import VideoSalesLetter
from ..FinalProduct import FinalProduct
####################

class Master(MasterTemplate):
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

    # Hide Product 4, Avatars 2 and 3
    self.avatar_2_product_4_input_section.visible = False
    self.avatar_3_product_4_input_section.visible = False

    # Hide Product 5, Avatars 2 and 3
    self.avatar_2_product_5_input_section.visible = False
    self.avatar_3_product_5_input_section.visible = False

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
        self.youtube_intro_video.visible = True
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

        # LAUNCH THE TASKS
        task_ids = []  # List to store all task IDs

        # Launch the background tasks concurrently
        # COMPANY SUMMARY // BRAND TONE
        task_id_company_summary = anvil.server.call('launch_draft_company_summary', user_table, company_name, company_url)
        print("Company Summary Launch function called")
        task_ids.append(task_id_company_summary)
        task_id_brand_tone = anvil.server.call('launch_draft_brand_tone_research', user_table, company_url)
        print("Brand Tone Launch function called")
        task_ids.append(task_id_brand_tone)

        tasks_product_research = []
        tasks_avatar = []

        for i in range(1, 6):
          # Get the product name and url from the textboxes
          product_name_input = getattr(self, f"product_{i}_name_input").text
          product_url_input = getattr(self, f"product_{i}_url_input").text

          # Check if the product name is not empty and save it to the user table
          if product_name_input:
            product_name_row = user_table.get(variable=f"product_{i}_latest")
            product_name_row['variable_title'] = product_name_input
            product_name_row.update()

            product_url_row = user_table.get(variable=f"product_{i}_url")
            product_url_row['variable_title'] = product_url_input
            product_url_row.update()

            # Launch the background task for product research
            if product_name_input:
              task_product_research = anvil.server.call(f"launch_draft_deepdive_product_{i}_generator", user_table, company_name, product_name_input, product_url_input)
              print(f"product_{i} analysis initiated")
              tasks_product_research.append((i, task_product_research))
              task_ids.append(task_product_research)

        # CHECK THE AVATARS FOR EACH PRODUCT
        for i in range(1, 6):
          # Loop through avatars 1 to 3 for each product
          for j in range(1, 4):
            # Get the avatar description from the textbox
            avatar_input = getattr(self, f"avatar_{j}_product_{i}_input").text

            # Check if the avatar description is not empty and save it to the user table
            if avatar_input:
              # Launch the background task for Avatar
              task_id_avatar = anvil.server.call(f"launch_draft_deepdive_avatar_{j}_product_{i}_generator", user_table, company_name, getattr(self, f"product_{i}_name_input").text, avatar_input)
              print("Deep Dive Draft Avatar Research Started")

              # Save it as the preview
              avatar_preview_row = user_table.search(variable=f"avatar_{j}_product_{i}_preview")[0]
              avatar_preview_row['variable_value'] = avatar_input
              avatar_preview_row.update()

              # Save it as the latest
              avatar_latest_row = user_table.search(variable=f"avatar_{j}_product_{i}_latest")[0]
              avatar_latest_row['variable_value'] = avatar_input
              avatar_latest_row.update()
             # CHECK THE STATUS OF THE TASKS
        # self.check_all_task_status(task_ids)

 # # CHECK THE STATUS OF THE TASKS
 #  def check_all_task_status(self, task_ids):
 #      all_tasks_completed = False
 #      while not all_tasks_completed:
 #          # Check the status of each task
 #          completed_tasks = 0
 #          for task_id in task_ids:
 #              task_status = anvil.server.call('get_status_function', task_id)
 #              if task_status == 'completed':
 #                  completed_tasks += 1
 #              elif task_status == 'failed':
 #                  print(f"Task {task_id} failed.")
 #                  # Handle the failure gracefully, e.g., inform the user or retry the task

 #          # Check if all tasks are completed
 #          if completed_tasks == len(task_ids):
 #              all_tasks_completed = True
 #               # All tasks are completed
 #              print("All tasks are completed!")
 #          else:
 #              # Wait for a short interval before checking again
 #              time.sleep(1)  # Adjust the interval as needed


  # NAVIGATION

  def navigate_to_form(self, form_class):
        content_form = form_class()
        self.content_panel.clear()
        self.content_panel.add_component(content_form)

  def company_asset_link_click(self, **event_args):
      self.navigate_to_form(Company_new)

  def product_asset_link_click(self, **event_args):
      self.navigate_to_form(Product)

  def brand_tone_asset_link_click(self, **event_args):
      self.navigate_to_form(BrandTone)
      
  def home_asset_link_copy_click(self, **event_args):
    open_form("Home")

  def product_asset_link_click(self, **event_args):
    product=Product()
    self.content_panel.clear()
    self.content_panel.add_component(product)

  def company_asset_link_click(self, **event_args):
    from ..Company_new import Company_new
    company_form = Company_new()
    self.content_panel.clear()
    self.content_panel.add_component(company_form)

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









              # # Wait for product research tasks to complete
              # for i, task_id_product_research in tasks_product_research:
              #     task_status_product_research = anvil.server.wait_for_task(task_id_product_research)
              #     print("Product Research Task Status:", task_status_product_research)
              #     if task_status_product_research == "completed":
              #         # Background task completed successfully
              #         product_research_result = anvil.server.get_task_result(task_id_product_research)
              #         print("Product Research Result:", product_research_result)
              #         # Update the user table with the result
              #         product_research_row = user_table.get(variable=f"product_{i}_latest")
              #         product_research_row['variable_value'] = product_research_result
              #         product_research_row.update()



        # # Wait for avatar task to complete
        # task_status_avatar = anvil.server.wait_for_task(task_id_avatar)
        # print("Avatar Task Status:", task_status_avatar)
        # if task_status_avatar == "completed":
        #     # Background task completed successfully
        #     avatar_result = anvil.server.get_task_result(task_id_avatar)
        #     print("Avatar Research Result:", avatar_result)
        #     # Update the user table with the result
        #     avatar_row = user_table.get(variable=f"avatar_{j}_product_{i}_latest")
        #     avatar_row['variable_value'] = avatar_result
        #     avatar_row.update()

        #   # Wait for brand tone task to complete
        #   task_status_brand_tone = anvil.server.wait_for_task(task_id_brand_tone)
        #   print("Brand Tone Task Status:", task_status_brand_tone)
        #   if task_status_brand_tone == "completed":
        #       # Background task completed successfully
        #       brand_tone_result = anvil.server.get_task_result(task_id_brand_tone)
        #       print("Brand Tone Research Result:", brand_tone_result)
        #       # Update the user table with the result
        #       brand_tone_row = user_table.get(variable='brand_tone')
        #       brand_tone_row['variable_value'] = brand_tone_result
        #       brand_tone_row.update()

      # # Launch the background task for COMPANY SUMMARY
      # task_id_company_summary = anvil.server.call('launch_draft_company_summary', user_table, company_name, company_url)
      # print("Company Research Started")
      # # Check the status of the background task for company summary
      # while True:
      #     task_status_company_summary = anvil.server.call('get_task_status', task_id_company_summary)
      #     print("Company Summary Task Status:", task_status_company_summary)
      #     if task_status_company_summary == "completed":
      #         # Background task completed successfully
      #         company_summary_result = anvil.server.call('get_task_result', task_id_company_summary)
      #         print("Company Summary Result:", company_summary_result)
      #         # Update the user table with the result
      #         company_profile_row = user_table.get(variable='company_profile')
      #         company_profile_row['variable_value'] = company_summary_result
      #         company_profile_row.update()
      #         break
      #     elif task_status_company_summary == "failed":
      #         # Background task encountered an error
      #         print("Company Profile Failed")
      #         break
      #     # Sleep for a few seconds before checking again
      #     time.sleep(2)

      # # Launch the background task for BRAND TONE
      # task_id_brand_tone = anvil.server.call('launch_draft_brand_tone_research', user_table, company_url)
      # print("Brand Tone Research Started")

      # # Check the status of the background task for brand tone
      # while True:
      #     task_status_brand_tone = anvil.server.call('get_task_status', task_id_brand_tone)
      #     print("Brand Tone Task Status:", task_status_brand_tone)
      #     if task_status_brand_tone == "completed":
      #         # Background task completed successfully
      #         brand_tone_result = anvil.server.call('get_task_result', task_id_brand_tone)
      #         print("Brand Tone Research Result:", brand_tone_result)
      #         # Update the user table with the result
      #         brand_tone_row = user_table.get(variable='brand_tone')
      #         brand_tone_row['variable_value'] = brand_tone_result
      #         brand_tone_row.update()
      #         break
      #     elif task_status_brand_tone == "failed":
      #         # Background task encountered an error
      #         print("Brand Tone Research Failed")
      #         break
      #     # Sleep for a few seconds before checking again
      #     time.sleep(2)

      # # Loop through products 1 to 5
      # for i in range(1, 6):
      #     # Get the product name and url from the textboxes
      #     product_name_input = getattr(self, f"product_{i}_name_input").text
      #     product_url_input = getattr(self, f"product_{i}_url_input").text

      #     # Check if the product name is not empty and save it to the user table
      #     if product_name_input:
      #         product_name_row = user_table.get(variable=f"product_{i}")
      #         product_name_row['variable_title'] = product_name_input
      #         product_name_row.update()

      #         # Launch the background task for product research
      #         task_id_product_research = anvil.server.call(f'launch_draft_deepdive_product_{i}_generator', user_table, company_name, product_name_input, product_url_input)
      #         print(f"Deep Dive Product {i} Research Called")

      #         # Check the status of the background task for product research
      #         while True:
      #             task_status_product_research = anvil.server.call('get_task_status', task_id_product_research)
      #             print("Product Research Task Status:", task_status_product_research)
      #             if task_status_product_research == "completed":
      #                 # Background task completed successfully
      #                 product_research_result = anvil.server.call('get_task_result', task_id_product_research)
      #                 print("Product Research Result:", product_research_result)
      #                 # Update the user table with the result
      #                 product_research_row = user_table.get(variable=f"product_{i}_research")
      #                 product_research_row['variable_value'] = product_research_result
      #                 product_research_row.update()
      #                 break
      #             elif task_status_product_research == "failed":
      #                 # Background task encountered an error
      #                 print("Product Research Failed")
      #                 break
      #             # Sleep for a few seconds before checking again
      #             time.sleep(2)

      #     # Check if the product url is not empty and save it to the user table
      #     if product_url_input:
      #         product_url_row = user_table.get(variable=f"product_{i}_url")
      #         product_url_row['variable_value'] = product_url_input
      #         product_url_row.update()

      # # CHECK THE AVATARS FOR EACH PRODUCT
      # # Loop through products 1 to 5
      # for i in range(1, 6):
      #     # Loop through avatars 1 to 3 for each product
      #     for j in range(1, 4):
      #         # Get the avatar description from the textbox
      #         avatar_input = getattr(self, f"avatar_{j}_product_{i}_input").text

      #         # Check if the avatar description is not empty and save it to the user table
      #         if avatar_input:
      #             # Launch the background task for Avatar
      #             task_id_avatar = anvil.server.call(f'launch_draft_deepdive_avatar_{j}_generator', user_table, company_name, getattr(self, f"product_{i}_name_input").text, avatar_input)
      #             print("Deep Dive Draft Avatar Research Started")

      #           # Save it as the preview
      #             avatar_preview_row = user_table.search(variable=f"avatar_{j}_product_{i}_preview")[0]
      #             avatar_preview_row['variable_value'] = avatar_input
      #             avatar_preview_row.update()

      #             # Save it as the latest
      #             avatar_latest_row = user_table.search(variable=f"avatar_{j}_product_{i}_latest")[0]
      #             avatar_latest_row['variable_value'] = avatar_input
      #             avatar_latest_row.update()

      #           # Check the status of the background task for Avatar
      #             while True:
      #                 task_status_avatar = anvil.server.call('get_task_status', task_id_avatar)
      #                 print("Avatar Task Status:", task_status_avatar)
      #                 if task_status_avatar == "completed":
      #                     # Background task completed successfully
      #                     avatar_result = anvil.server.call('get_task_result', task_id_avatar)
      #                     print("Avatar Research Result:", avatar_result)
      #                   # Update the user table with the result
      #                     avatar_row = user_table.get(variable=f"avatar_{j}_latest")
      #                     avatar_row['variable_value'] = avatar_result
      #                     avatar_row.update()
      #                     break
      #                 elif task_status_avatar == "failed":
      #                     # Background task encountered an error
      #                     print("Avatar Research Failed")
      #                     break
      #                 # Sleep for a few seconds before checking again
      #                 time.sleep(2)

  ### END OF THE TRIAL

      # # Loop through products 1 to 5
      # for i in range(1, 6):
      #     # Get the product name and url from the textboxes
      #     product_name_input = getattr(self, f"product_{i}_name_input").text
      #     product_url_input = getattr(self, f"product_{i}_url_input").text

      #     # Check if the product name is not empty and save it to the user table
      #     if product_name_input:
      #         product_name_row = user_table.get(variable=f"product_{i}")
      #         product_name_row['variable_title'] = product_name_input
      #         product_name_row.update()

      #         # Launch the background task for product research
      #         task_id_product_research = anvil.server.call(f'launch_draft_deepdive_product_{i}_generator', user_table, company_name, product_name_input, product_url_input)
      #         print(f"Deep Dive Product {i} Research Called")

      #     # Check if the product url is not empty and save it to the user table
      #     if product_url_input:
      #         product_url_row = user_table.get(variable=f"product_{i}_url")
      #         product_url_row['variable_value'] = product_url_input
      #         product_url_row.update()

      #    # Check the status of the background task for product research
      # while True:
      #     task_status_product_research = anvil.server.call('get_task_status', task_id_product_research)
      #     print("Product Research Task Status:", task_status_product_research)
      #     if task_status_product_research == "completed":
      #         # Background task completed successfully
      #         product_research_result = anvil.server.call('get_task_result', task_id_product_research)
      #         print("Product Research Result:", product_research_result)
      #         # Update the user table with the result
      #         product_research_row = user_table.get(variable='product_research')
      #         product_research_row['variable_value'] = product_research_result
      #         product_research_row.update()
      #         break
      #     elif task_status_product_research == "failed":
      #         # Background task encountered an error
      #         print("Product Research Failed")
      #         break
      #     # Sleep for a few seconds before checking again
      #     time.sleep(2)


      # # SAVE PRODUCT 1
      # # PRODUCT 1 NAME
      # product_1_name = self.product_1_name_input.text
      # # Save product 1 name
      # product_1_row = user_table.get(variable='product_1')
      # product_1_row['variable_title'] = product_1_name
      # product_1_row.update()

      # # PRODUCT 1 URL
      # product_1_url = self.product_1_url_input.text
      # # Save product 1 url
      # product_1_url_row = user_table.get(variable='product_1_url')
      # product_1_url_row['variable_value'] = product_1_url
      # product_1_url_row.update()

      # # PRODUCT 1, AVATAR 1 DESCRIPTION
      # # Save it as the preview
      # avatar_1_product_1_preview = self.avatar_1_product_1_input.text
      # avatar_1_product_1_preview_row = user_table.search(variable='avatar_1_product_1_preview')[0]
      # avatar_1_product_1_preview_row['variable_value'] = avatar_1_product_1_preview
      # avatar_1_product_1_preview_row.update()
      # # Save it as the latest
      # avatar_1_product_1_latest = self.avatar_1_product_1_input.text
      # avatar_1_product_1_latest_row = user_table.search(variable='avatar_1_product_1_latest')[0]
      # avatar_1_product_1_latest_row['variable_value'] = avatar_1_product_1_latest
      # avatar_1_product_1_latest_row.update()


      # # Launch the background task for product research
      # task_id_product_research = anvil.server.call('launch_draft_deepdive_product_1_generator', user_table, company_name, product_1_name, product_1_url)
      # print("Deep Dive Product Research Started")

      # # Launch the background task for Avatar
      # task_id_avatar = anvil.server.call('launch_draft_deepdive_avatar_1_generator', user_table, company_name, product_1_name, avatar_1_preview)
      # print("Deep Dive Draft Avatar Research Started")


      # # Check the status of the background task for Avatar
      # while True:
      #     task_status_avatar = anvil.server.call('get_task_status', task_id_avatar)
      #     print("Avatar Task Status:", task_status_avatar)
      #     if task_status_avatar == "completed":
      #         # Background task completed successfully
      #         avatar_result = anvil.server.call('get_task_result', task_id_avatar)
      #         print("Avatar Research Result:", avatar_result)
      #         # Update the user table with the result
      #         avatar_row = user_table.get(variable='avatar_1_latest')
      #         avatar_row['variable_value'] = avatar_result
      #         avatar_row.update()
      #         break
      #     elif task_status_avatar == "failed":
      #         # Background task encountered an error
      #         print("Avatar Research Failed")
      #         break
      #     # Sleep for a few seconds before checking again
      #     time.sleep(2)
