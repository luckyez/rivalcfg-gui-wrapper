import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

# define the base command
base_command = "rivalcfg"

# define a list of polling rate options
polling_rate_options = ["125", "250", "500", "1000"]

# define a GTK window to display the GUI
class MouseSettingsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Mouse Settings")
        self.set_default_size(400, 300)

        # create a Gtk.Grid container
        grid = Gtk.Grid()
        self.add(grid)

        # label for battery level
        self.battery_label = Gtk.Label(label="Battery Level: N/A")
        grid.attach(self.battery_label, left=0, top=0, width=2, height=1)

        # sensitivity field
        sensitivity_label = Gtk.Label(label="Sensitivity (DPI):")
        self.sensitivity_entry = Gtk.Entry()
        grid.attach(sensitivity_label, left=0, top=1, width=1, height=1)
        grid.attach(self.sensitivity_entry, left=1, top=1, width=1, height=1)

        # polling rate dropdown
        polling_rate_label = Gtk.Label(label="Polling Rate (Hz):")
        self.polling_rate_combo = Gtk.ComboBoxText()
        for option in polling_rate_options:
            self.polling_rate_combo.append_text(option)
        self.polling_rate_combo.set_active(3)  # Set the default value to 1000 Hz
        grid.attach(polling_rate_label, left=0, top=2, width=1, height=1)
        grid.attach(self.polling_rate_combo, left=1, top=2, width=1, height=1)

        # sleep timer input field
        sleep_timer_label = Gtk.Label(label="Sleep Timer (minutes):")
        self.sleep_timer_entry = Gtk.Entry()
        grid.attach(sleep_timer_label, left=0, top=3, width=1, height=1)
        grid.attach(self.sleep_timer_entry, left=1, top=3, width=1, height=1)

        # dim timer input field
        dim_timer_label = Gtk.Label(label="Dim Timer (seconds):")
        self.dim_timer_entry = Gtk.Entry()
        grid.attach(dim_timer_label, left=0, top=4, width=1, height=1)
        grid.attach(self.dim_timer_entry, left=1, top=4, width=1, height=1)

        # create a "Reset Settings" button
        reset_button = Gtk.Button(label="Reset Settings")
        reset_button.connect("clicked", self.reset_settings)
        grid.attach(reset_button, left=0, top=5, width=2, height=1)

        # schedule the command execution every 5 seconds
        GLib.timeout_add_seconds(5, self.run_command)

    def run_command(self):
        # build the command based on user input
        command = base_command

        sensitivity = self.sensitivity_entry.get_text()
        if sensitivity:
            command += f" --sensitivity {sensitivity}"

        polling_rate = self.polling_rate_combo.get_active_text()
        if polling_rate:
            command += f" --polling-rate {polling_rate}"

        sleep_timer = self.sleep_timer_entry.get_text()
        if sleep_timer:
            command += f" --sleep-timer {sleep_timer}"

        dim_timer = self.dim_timer_entry.get_text()
        if dim_timer:
            command += f" --dim-timer {dim_timer}"

        try:
            # run the rivalcfg --battery-level to get the battery level
            battery_output = subprocess.check_output(f"{base_command} --battery-level", shell=True, text=True)
            self.battery_label.set_text(f"Battery Level: {battery_output.strip()}")

            # run the command to update mouse settings
            subprocess.check_output(command, shell=True, text=True)
        except subprocess.CalledProcessError as e:
            # display an error message in the console
            print(f"Error running the command: {e}")

        # return true to continue scheduling the function
        return True

    def reset_settings(self, button):
        # reset all settings to their factory default
        try:
            output = subprocess.check_output(f"{base_command} -r", shell=True, text=True)
            # Display the reset message in the console
            print(output)
        except subprocess.CalledProcessError as e:
            # display an error message in the terminal
            print(f"Error resetting settings: {e}")

win = MouseSettingsWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()

Gtk.main()
