from ._anvil_designer import Home_originalTemplate
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

#############################################

from ..Company import Company
from ..Product import Product
from ..BrandTone import BrandTone
from ..Avatars import Avatars
from ..VSL_Elements import VSL_Elements 
from ..VideoSalesLetter import VideoSalesLetter
from ..FinalProduct import FinalProduct
####################
# NAVIGATION
class Home_original(Home_originalTemplate):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      anvil.users.login_with_form()

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

    def save_company_info_component_click(self, **event_args):
      # Get the current user
      current_user = anvil.users.get_user()
      # Get the email of the current user
      owner = current_user['email']
      # Get the row for the current user from the variable_table
      row = app_tables.variable_table.get(owner=owner)  # Replace user_email with owner
      # Update the company_profile column for the current user
      if row:
          company_name = self.company_name_input.text
          company_url = self.company_url_input.text  # Get the company URL from the appropriate input field
          row.update(company_name=company_name, company_url=company_url)  # Update both columns at once

    def load_company_info_component_click(self, **event_args):
      # Get the current user
      current_user = anvil.users.get_user()
      
      # Get the email or username of the current user
      user_email = current_user['email']  # Change 'email' to 'username' if you are using usernames
      
    # Get the row for the current user from the variable_table
      row = app_tables.variable_table.get(owner=user_email)  # Change 'owner' to the appropriate column name if different
        
    # Get the company profile text for the current user
      if row:
          home_page_name = row['company_name']
          home_page_url = row['company_url']
          home_page_product = row['product_profile']
          home_page_avatar = row['avatar1']
          print("Contents:", home_page_name, home_page_url, home_page_product, home_page_avatar)
          # Set the contents as the text of the rich text box
          self.company_name_input.text = home_page_name
          self.company_url_input.text = home_page_url
          self.product_profile_input.text = home_page_product
          self.main_avatar_input.text = home_page_avatar
      else:
          # Handle case where the row does not exist for the current user
          print("No row found for the current user")

























