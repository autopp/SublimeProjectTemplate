import sublime
import sublime_plugin


class ProjectTemplateCommand(sublime_plugin.WindowCommand):

    SETTINGS_FILE_NAME = 'ProjectTemplate.sublime-settings'
    TEMPLATES_KEY = 'templates'

    def run(self):
        # Check whether the folder is open only one in the current window.
        folders = self.window.folders()
        msg = None
        if len(folders) == 0:
            msg = "No floder opened in the current window."
        elif len(folders) > 1:
            msg = "Multiple folder opened in the current window."
        if msg:
            sublime.error_message(msg)
            return

        self.folder = folders[0]

        # Load settings
        settings = sublime.load_settings(self.SETTINGS_FILE_NAME)
        self.templates = settings.get(self.TEMPLATES_KEY, {})

        # Check the format of templates
        if type(self.templates) != dict:
            sublime.error_message("The templates should be an object.")
            return
        for name, template in self.templates.items():
            if type(template) != dict:
                msg = (
                    "Template '%s' is not a object.\n"
                    "Each of the template should be an object."
                ) % (name)
                sublime.error_message(msg)
                return

        # Show quick panel for selecting template
        self.template_names = list(self.templates.keys())
        self.window.show_quick_panel(self.template_names,
                                     self.on_selected)

    def on_selected(self, idx):
        if idx < 0:
            # No template selected
            return
        template_name = self.template_names[idx]
        print(template_name)
