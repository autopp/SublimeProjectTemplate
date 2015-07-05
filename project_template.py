import sublime
import sublime_plugin
import os.path


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
        # Store selected template
        self.template = self.templates[self.template_names[idx]]
        folder = os.path.basename(self.folder_path())

        self.window.show_input_panel("Project name:", folder,
                                     self.on_input, None, None)

    def on_input(self, project_name):
        project_file_path = os.path.join(self.folder_path(),
                                         project_name + ".sublime-project")

        # Check whether the project file exists
        if os.path.exists(project_file_path):
            if os.path.isfile(project_file_path):
                msg = (
                    "Are you sure you want to "
                    "override the existing project file?"
                )
                if sublime.ok_cancel_dialog(msg):
                    self.create_project_file(project_file_path)
                else:
                    return
            else:
                msg = "%s exists and is not a file." % project_file_path
                sublime.error_message(msg)
                return
        else:
            self.create_project_file(project_file_path)

    def folder_path(self):
        return self.window.folders()[0]

    def create_project_file(self, path):
        print("called with " + path)
