import sublime
import sublime_plugin


class ProjectTemplateCommand(sublime_plugin.WindowCommand):

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

        folder = folders[0]
        print(folder)
