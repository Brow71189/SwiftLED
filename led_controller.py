# standard libraries
import subprocess

ssh_path = 'C:/cygwin64/bin/ssh.exe'
raspiname = 'raspi7'

class LEDPanelDelegate(object):
    
    
    def __init__(self, api):
        self.__api = api
        self.panel_id = 'LED-Panel'
        self.panel_name = 'LED controller'
        self.panel_positions = ['left', 'right']
        self.panel_position = 'right'
    
    def create_panel_widget(self, ui, document_controller):
        def toggle_led_button_clicked():
            if toggle_led_button.text == 'ON':
                value = '1' 
                toggle_led_button.text = 'OFF'
            else:
                value = '0'
                toggle_led_button.text = 'ON'
                
            current_gpio = selection_combo_box.current_item
            
            res = subprocess.run([ssh_path, raspiname, 'echo', value, '>',
                                  '/sys/class/gpio/gpio' + current_gpio + '/value'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(res)
            
        
        def selection_combo_box_changed(current_item):
            res = subprocess.run([ssh_path, raspiname, 'echo', current_item, '>', '/sys/class/gpio/export'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            res = subprocess.run([ssh_path, raspiname, 'echo', 'out', '>', '/sys/class/gpio/gpio' + current_item + '/direction'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
        column = ui.create_column_widget()
        
        description = ui.create_label_widget('Control a led attached to a raspi gpio port')
        
        selection_combo_box = ui.create_combo_box_widget()
        selection_combo_box.items = ['17', '27']
        selection_combo_box.on_current_item_changed = selection_combo_box_changed
        
        selection_combo_box_changed('17')
        
        toggle_led_button = ui.create_push_button_widget('ON')
        toggle_led_button.on_clicked = toggle_led_button_clicked
        
        column.add(description)
        column.add_spacing(10)
        column.add(selection_combo_box)
        column.add_spacing(10)
        column.add(toggle_led_button)
        column.add_stretch()

        return column
        
class LEDExtension(object):
    extension_id = 'univie.ledcontroller'
    
    def __init__(self, api_broker):
        api = api_broker.get_api(version='1', ui_version='1')
        self.__panel_ref = api.create_panel(LEDPanelDelegate(api))
    
    def close(self):
        self.__panel_ref.close()
        self.__panel_ref = None