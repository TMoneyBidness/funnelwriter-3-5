from ._anvil_designer import FinalProductTemplate
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


############################################################################################################
# LOADING

class FinalProduct(FinalProductTemplate):
 def __init__(self, **properties):
    # Call the parent class's __init__ method
    super().__init__(**properties)

    current_user = anvil.users.get_user()
    if current_user:
        user_table_name = current_user['user_id']
        user_table = getattr(app_tables, user_table_name)

        final_headline_rows = user_table.search(variable='chosen_final_headline')
        if final_headline_rows:
            self.main_headline_textbox.text = final_headline_rows[0]['variable_value']
        else:
            print("No row found for final_headline")

        final_subheadline_rows = user_table.search(variable='chosen_final_subheadline')
        if final_subheadline_rows:
            self.subheadline_textbox.text = final_subheadline_rows[0]['variable_value']
        else:
            print("No row found for final_subheadline")

        secondary_headline_rows = user_table.search(variable='chosen_final_secondary_headline')
        if secondary_headline_rows:
            self.secondary_headline_textbox.text = secondary_headline_rows[0]['variable_value']
        else:
            print("No row found for final_secondary_headline")

        vsl_script_rows = user_table.search(variable='vsl_script')
        if vsl_script_rows:
            self.vsl_script.text = vsl_script_rows[0]['variable_value']
        else:
            print("No row found for vsl_script")

        vsl_theme_1_rows = user_table.search(variable='vsl_theme_1')
        if vsl_theme_1_rows:
            self.vsl_theme_1_textbox.text = vsl_theme_1_rows[0]['variable_value']
        else:
            print("No row found for vsl_theme_1")

        vsl_theme_2_rows = user_table.search(variable='vsl_theme_2')
        if vsl_theme_2_rows:
            self.vsl_theme_2_textbox.text = vsl_theme_2_rows[0]['variable_value']
        else:
            print("No row found for vsl_theme_2")

        vsl_theme_3_rows = user_table.search(variable='vsl_theme_3')
        if vsl_theme_3_rows:
            self.vsl_theme_3_textbox.text = vsl_theme_3_rows[0]['variable_value']
        else:
            print("No row found for vsl_theme_3")

        vsl_theme_4_rows = user_table.search(variable='vsl_theme_4')
        if vsl_theme_4_rows:
            self.vsl_theme_4_textbox.text = vsl_theme_4_rows[0]['variable_value']
        else:
            print("No row found for vsl_theme_4")
    else:
        print("User not authenticated")

 def outlined_button_1_click(self, **event_args):
   anvil.open_form('VideoSalesLetter')
   pass

 def email_my_script_click(self, **event_args):
   anvil.js.window.alert("Check your inbox (TBD, but it's easily doable!")
   pass


