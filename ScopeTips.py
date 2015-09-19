import sublime, sublime_plugin

class IndentTipsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.showTips(self.view, True)

	def showTips(self, view, showInputPanel):
		sel_a = view.sel()[0].a
		sel_b = view.sel()[0].b
		line_a = view.line(view.sel()[0]).a
		line_b = view.line(view.sel()[0]).b
		line_str = view.substr(view.line(view.sel()[0]))

		# return if selection is not empty
		if sel_a != sel_b :
			return

		# return if current line does not have indent
		indent = view.find(r'^(	| )+', line_a)
		if indent.a > line_b or indent.a == -1 :
			return

		# handle vaild location
		if sel_a >= indent.a and sel_a < indent.b :
			offset = sel_a - indent.a
			indent_str = line_str[0:offset]
			indent_str_2 = line_str[0:offset+1]
			thisLine = view.line(line_a)
			while thisLine.a > 0 :
				thisLine = view.line(thisLine.a-1)

				# skip empty line
				if view.find(r'[^	 \n]', thisLine.a).a > thisLine.b :
					continue

				if indent_str == view.substr(sublime.Region(thisLine.a,thisLine.a+offset)) and indent_str_2 != view.substr(sublime.Region(thisLine.a,thisLine.a+offset+1)) :
					if showInputPanel :
						sublime.Window.show_quick_panel(sublime.active_window(), [view.substr(thisLine)] , sublime.status_message(view.substr(thisLine)))
					sublime.status_message(view.substr(thisLine))
					return

class IndentTipsListener(sublime_plugin.EventListener):
	def on_selection_modified(self, view):
		IndentTipsCommand.showTips(self, view, False)