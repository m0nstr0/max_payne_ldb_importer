import math
import sys

# import maya.OpenMayaUI as omui
from PySide6 import QtCore, QtGui, QtWidgets
from shiboken6 import wrapInstance
import maya.api.OpenMaya as OpenMaya
import json


class MP2FSMEventDataModel:
    def __init__(self, name, use_states=True):
        self.name = name
        self.events = []
        self.event_specific = {}
        self.use_states = use_states
        self.state_specific = {}

    def addEvent(self, name):
        self.events.append(name)
        self.event_specific[name] = []

    def getEventsNames(self):
        return self.events

    def getEventSpecific(self, name):
        for k in self.event_specific:
            if k.lower() == name.lower():
                return self.event_specific[k]
        return []

    def setEventSpecific(self, name, messages):
        for k in self.event_specific:
            if k.lower() == name.lower():
                self.event_specific[k] = messages
                return

    def setStateSpecific(self, name, messages):
        for k in self.state_specific:
            if k.lower() == name.lower():
                self.state_specific[k] = messages
                return
        self.state_specific[name] = messages

    def getStateMessages(self, name):
        for k in self.state_specific:
            if k.lower() == name.lower():
                return self.state_specific[k]
        return []

    def removeState(self, name):
        found_key = None
        for key in self.state_specific:
            if key.lower() == name.lower():
                found_key = key
                break

        if found_key is None:
            return

        self.state_specific.pop(found_key, None)

    def renameState(self, old_name, new_name):
        found_key = None
        for key in self.state_specific:
            if key.lower() == old_name.lower():
                found_key = key
                break

        if found_key is None:
            return

        data = self.state_specific[found_key]
        self.state_specific.pop(found_key, None)
        self.state_specific[new_name] = data


class MP2FSMTimerDataModel:
    def __init__(self, name):
        self.name = name
        self.is_real_time = False
        self.length = 3.0

        on_start_timer = MP2FSMEventDataModel(f"OnStartTimer({name})")
        on_start_timer.addEvent('Send Always Before')
        on_start_timer.addEvent('Send Always After')
        on_start_timer.use_states = True

        on_end_timer = MP2FSMEventDataModel(f"OnEndTimer({name})")
        on_end_timer.addEvent('Send Always Before')
        on_end_timer.addEvent('Send Always After')
        on_end_timer.use_states = True

        self.events = {'OnStartTimer': on_start_timer, 'OnEndTimer': on_end_timer}

    def rename(self, new_name):
        self.name = new_name
        self.events['OnStartTimer'].name = f"OnStartTimer({new_name})"
        self.events['OnEndTimer'].name = f"OnEndTimer({new_name})"

    def renameState(self, old_name, new_name):
        for i in self.events:
            self.events[i].renameState(old_name, new_name)

    def removeState(self, name):
        for i in self.events:
            self.events[i].removeState(name)

    def getEventByName(self, name):
        return self.events[name]


class MP2FSMDataModel:
    def __init__(self):
        self.states_names = []
        self.states_events = []
        self.custom_events_names = []
        self.custom_events = []
        self.timers = []
        self.default_state = None
        self.edit_event_delegate = []

        self.events = []

    def getEvents(self):
        return self.events

    @staticmethod
    def getNextName(prefix, data):
        index = len(data)
        next_name = "%s_%d" % (prefix, index)
        while True:
            found = False
            for name in data:
                if name.lower() == next_name:
                    found = True
                    break
            if found:
                index = index + 1
                next_name = "%s_%d" % (prefix, index)
            else:
                break
        return next_name

    def getNextTimerName(self):
        index = len(self.timers)
        next_name = "timer_%d" % index
        while True:
            found = False
            for timer in self.timers:
                if timer.name.lower() == next_name:
                    found = True
                    break
            if found:
                index = index + 1
                next_name = "timer_%d" % index
            else:
                break
        return next_name

    def getStatesNames(self):
        return self.states_names

    def getStatesEvents(self):
        return self.states_events

    def getStateEventByName(self, name):
        for i in self.states_events:
            if i.name.lower() == f"fsm_switch(%s)" % name.lower():
                return i
        return None

    def renameState(self, old_name, new_name):
        for i in range(len(self.states_names)):
            if self.states_names[i].lower() == old_name.lower():
                self.states_names[i] = new_name
                break

        state = self.getStateEventByName(old_name)
        state.name = f"FSM_Switch({new_name})"

        for i in self.states_events:
            i.renameState(old_name, new_name)

        for i in self.custom_events:
            i.renameState(old_name, new_name)

        for i in self.timers:
            i.renameState(old_name, new_name)

        if self.default_state.lower() == old_name.lower():
            default_state = new_name
            self.setDefaultState(default_state)

        self.broadcastEditEvent(state)

    def setDefaultState(self, name):
        self.default_state = name

    def createState(self):
        new_state_name = self.getNextName('state', self.states_names)
        self.states_names.append(new_state_name)

        new_state = MP2FSMEventDataModel(f"FSM_Switch({new_state_name})")
        new_state.addEvent('Send Always Before')
        new_state.addEvent('Send Always After')
        new_state.use_states = True
        self.states_events.append(new_state)

        if len(self.states_names) == 1:
            self.setDefaultState(new_state_name)

        return new_state_name

    def removeState(self, name):
        for i in range(len(self.states_names)):
            if self.states_names[i].lower() == name.lower():
                self.states_names.remove(self.states_names[i])
                break

        state = self.getStateEventByName(name)
        self.states_events.remove(state)

        for i in self.states_events:
            i.removeState(name)

        for i in self.custom_events:
            i.removeState(name)

        for i in self.timers:
            i.removeState(name)

        if self.default_state.lower() == name.lower():
            default_state = None
            if len(self.states_names) > 0:
                default_state = self.states_names[0]
            self.setDefaultState(default_state)

    def getCustomEventsNames(self):
        return self.custom_events_names

    def getCustomEvents(self):
        return self.custom_events

    def createCustomEvent(self):
        new_custom_event_name = self.getNextName('custom_event', self.custom_events_names)
        self.custom_events_names.append(new_custom_event_name)

        new_state = MP2FSMEventDataModel(f"FSM_Send({new_custom_event_name})")
        new_state.addEvent('Send Always Before')
        new_state.addEvent('Send Always After')
        new_state.use_states = True
        self.custom_events.append(new_state)

        return new_custom_event_name

    def getCustomEventByName(self, name):
        for i in self.custom_events:
            if i.name.lower() == f"fsm_send(%s)" % name.lower():
                return i
        return None

    def renameCustomEvent(self, old_name, new_name):
        for i in range(len(self.custom_events_names)):
            if self.custom_events_names[i].lower() == old_name.lower():
                self.custom_events_names[i] = new_name
                break

        custom_event = self.getCustomEventByName(old_name)
        custom_event.name = f"FSM_Send({new_name})"

        self.broadcastEditEvent(custom_event)

    def removeCustomEvent(self, name):
        for i in range(len(self.custom_events_names)):
            if self.custom_events_names[i].lower() == name.lower():
                self.custom_events_names.remove(self.custom_events_names[i])
                break
        event = self.getCustomEventByName(name)
        self.custom_events.remove(event)

    def getTimerByName(self, name):
        for i in self.timers:
            if i.name.lower() == name:
                return i
        return None

    def getTimers(self):
        return self.timers

    def renameTimer(self, old_name, new_name):
        timer = self.getTimerByName(old_name)
        timer.rename(new_name)
        self.broadcastEditEvent(None)

    def createTimer(self):
        new_timer = MP2FSMTimerDataModel(self.getNextTimerName())
        self.timers.append(new_timer)
        return new_timer

    def removeTimer(self, name):
        timer = self.getTimerByName(name)
        self.timers.remove(timer)

    def subscribeToEditEvent(self, callback):
        self.edit_event_delegate.append(callback)

    def broadcastEditEvent(self, event):
        for i in self.edit_event_delegate:
            i(event)

    def changeTimerLength(self, name, length):
        timer = self.getTimerByName(name)
        timer.length = length

    def toggleTimerType(self, name):
        timer = self.getTimerByName(name)
        timer.is_real_time = not timer.is_real_time

    def getEventByName(self, name):
        for i in self.events:
            if i.name.lower() == name:
                return i
        return None

    def getEventsDict(self, events):
        events_list = []
        for event in events:
            event_dict = {
                'name': event.name,
                'send_before': event.send_before,
                'send_after': event.send_after,
                'state_specific': event.state_specific
            }
            events_list.append(event_dict)
        return events_list

    def createEventsFromDict(self, events_dict):
        model = MP2FSMEventDataModel(events_dict['name'])
        model.send_before = events_dict['send_before']
        model.send_after = events_dict['send_after']
        model.state_specific = events_dict['state_specific']

    def toJson(self):
        timers = []
        for timer in self.timers:
            timers.append({'name': timer.name,
                           'events': self.getEventsDict(timer.events),
                           'is_real_time': timer.is_real_time,
                           'length': timer.length})

        json_dict = {
            'states': self.getEventsDict(self.states),
            'custom_events': self.getEventsDict(self.custom_events),
            'default_state': self.default_state,
            'events': self.getEventsDict(self.events),
            'timers': timers,
        }

        return json.dumps(json_dict)

    def fromJson(self, data):
        self.states = []
        self.events = []
        self.custom_events = []
        self.timers = []

        json_dict = json.loads(data)
        for state in json_dict['states']:
            self.states.append(self.createEventsFromDict(state))
        for event in json_dict['custom_events']:
            self.custom_events.append(self.createEventsFromDict(event))
        for event in json_dict['events']:
            self.events.append(self.createEventsFromDict(event))
        for timer in json_dict['timers']:
            _timer = MP2FSMTimerDataModel(timer['name'])
            _timer.is_real_time = timer['is_real_time']
            _timer.length = timer['length']
            for event in timer['events']:
                _timer.events.append(self.createEventsFromDict(event))
            self.timers.append(_timer)

        self.default_state = json_dict['default_state']


class MP2FSMTextEditHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent.document())

    def highlightBlock(self, text):
        block_number = self.currentBlock().blockNumber()

        if "§§ " in text:
            fmt = QtGui.QTextCharFormat()
            fmt.setFontWeight(QtGui.QFont.Bold)
            self.setFormat(0, len(text), fmt)


class MP2FSMTextEditWidget(QtWidgets.QPlainTextEdit):
    TAG = "§§ %s:\n"

    def __init__(self, parent, model: MP2FSMDataModel):
        super().__init__(parent)
        self.cursor_range_id = None
        self.prev_cur_pos = None
        self.current_event_model = None
        self.states_cached = []
        self.events_cached = []
        self.data_model = model
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.setAcceptDrops(False)
        self.highlighter = MP2FSMTextEditHighlighter(self)
        self.data_model.subscribeToEditEvent(self.updateCode)
        self.updateCode(None)

    def dragEnterEvent(self, event):
        event.ignore()

    def dragMoveEvent(self, event):
        event.ignore()

    def dropEvent(self, event):
        event.ignore()

    def contextMenuEvent(self, e) -> None:
        pass

    def getTagRanges(self):
        extra_selections = self.extraSelections()
        extra_selections_len = len(extra_selections)

        ranges = []
        for i in range(extra_selections_len):
            if i == 0:
                continue
            a = extra_selections[i].cursor.blockNumber()
            b = self.blockCount()
            if i + 1 < extra_selections_len:
                b = extra_selections[i + 1].cursor.blockNumber()
            ranges.append([a, b])

        return ranges

    def isDeleteAllowed(self, key):
        ranges = self.getTagRanges()
        block = self.textCursor().blockNumber()
        for i in ranges:
            if block == i[
                0] + 1 and self.textCursor().atBlockStart() and key == QtCore.Qt.Key_Backspace and not self.textCursor().hasSelection():
                return False
            if block == i[
                1] - 1 and self.textCursor().atBlockEnd() and key == QtCore.Qt.Key_Delete and not self.textCursor().hasSelection():
                return False

        return True

    def keyPressEvent(self, event) -> None:
        # navigation is ok
        if event.key() in (
                QtCore.Qt.Key_Left, QtCore.Qt.Key_Right,
                QtCore.Qt.Key_Up, QtCore.Qt.Key_Down,
                QtCore.Qt.Key_Home, QtCore.Qt.Key_End,
                QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown
        ):
            super().keyPressEvent(event)
            return

        if event.key() in (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete):
            if not self.isDeleteAllowed(event.key()):
                event.ignore()
                return

        if not self.isSelectionInEditableRange():
            event.ignore()
            return

        super().keyPressEvent(event)

    def isSelectionInEditableRange(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return self.isCursorInEditableRange(cursor.blockNumber())

        doc = self.document()
        start_block = doc.findBlock(cursor.selectionStart()).blockNumber()
        end_block = doc.findBlock(cursor.selectionEnd()).blockNumber()

        ranges = self.getTagRanges()
        for i in ranges:
            if start_block > i[0] and end_block < i[1]:
                return True

        return False

    def isCursorInEditableRange(self, blockNumber=None):
        if blockNumber is None:
            pos = self.textCursor().blockNumber()
        else:
            pos = blockNumber
        for selection in self.extraSelections():
            if pos == selection.cursor.blockNumber():
                return False
        return True

    def saveCode(self, event_model: MP2FSMEventDataModel = None):
        if event_model is None:
            return

        extra_selections = self.extraSelections()
        extra_selections_len = len(extra_selections)

        ranges = []
        for i in range(extra_selections_len):
            if i == 0:
                continue
            a = extra_selections[i].cursor.blockNumber() + 1
            b = self.blockCount()
            if i + 1 < extra_selections_len:
                b = extra_selections[i + 1].cursor.blockNumber()
            ranges.append([a, b])

        document = self.document()
        event = 0
        state = 0
        for i in ranges:
            a = i[0]
            b = i[1]
            messages = []
            while a < b:
                block = document.findBlockByNumber(a)
                a = a + 1
                if not block.isValid():
                    continue
                text = block.text().strip()
                if text != '':
                    messages.append(text)
            if event_model.use_states and event > 0 and state < len(self.states_cached):
                event_model.setStateSpecific(self.states_cached[state], messages)
                state = state + 1
            elif event < len(self.events_cached):
                event_model.setEventSpecific(self.events_cached[event], messages)
                event = event + 1

    def updateCode(self, event_model=None) -> None:
        self.saveCode(self.current_event_model)
        self.current_event_model = event_model

        self.clear()
        self.setEnabled(False)

        if not event_model:
            return

        self.setEnabled(True)
        self.fillWithCode(event_model)

    def fillWithCode(self, event_model: MP2FSMEventDataModel):
        tag_lines = {0: "#C0C0C0"}

        self.events_cached = event_model.getEventsNames()
        self.states_cached = self.data_model.getStatesNames()

        states_added = False
        line_no = 1

        code_text = MP2FSMTextEditWidget.TAG % ('Upon Receiving: ' + event_model.name)
        for event_name in self.events_cached:
            messages = event_model.getEventSpecific(event_name)
            code_text = code_text + (MP2FSMTextEditWidget.TAG % event_name)
            tag_lines[line_no] = "#C0E080"
            line_no = line_no + 1

            for message in messages:
                code_text = code_text + message + "\n"
                line_no = line_no + 1
            code_text = code_text + "\n"
            line_no = line_no + 1

            if event_model.use_states and not states_added:
                for state_name in self.states_cached:
                    code_text = code_text + (MP2FSMTextEditWidget.TAG % state_name)
                    state_messages = event_model.getStateMessages(state_name)
                    tag_lines[line_no] = "#FFFFA0"
                    line_no = line_no + 1

                    if len(state_messages) > 0:
                        for message in state_messages:
                            code_text = code_text + message + "\n"
                            line_no = line_no + 1
                    code_text = code_text + "\n"
                    line_no = line_no + 1
                states_added = True

        self.setPlainText(code_text)
        self.highlightMarkerLines(tag_lines)
        block = self.document().findBlockByLineNumber(2)
        self.textCursor().setPosition(block.position())

    def highlightMarkerLine(self, line, color):
        block = self.document().findBlockByLineNumber(line)

        if block.isValid():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.cursor = QtGui.QTextCursor(block)
            fmt = QtGui.QTextCharFormat()
            fmt.setBackground(QtGui.QColor(color))
            fmt.setForeground(QtCore.Qt.black)
            fmt.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.format = fmt
            selection.cursor.clearSelection()
            return selection

        return None

    def highlightMarkerLines(self, lines):
        extra_selections = []

        for line in lines:
            extra_selections.append(self.highlightMarkerLine(line, lines[line]))

        self.setExtraSelections(extra_selections)


class MP2FSMTreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent, data_model):
        self.data_model = data_model
        super(MP2FSMTreeItemDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        return editor

    def setModelData(self, editor, model, index):
        new_name = editor.text().strip()
        old_name = index.data(QtCore.Qt.DisplayRole)

        if not new_name:
            QtWidgets.QMessageBox.warning(
                editor,
                "Rename error",
                "Name cannot be empty"
            )
            return

        parent_index = index.parent()
        row_count = model.rowCount(parent_index)

        for row in range(row_count):
            sibling = model.index(row, index.column(), parent_index)
            if sibling != index and sibling.data(QtCore.Qt.DisplayRole).lower() == new_name.lower():
                QtWidgets.QMessageBox.warning(
                    editor,
                    "Rename error",
                    "Duplicate name"
                )
                return

        model.setData(index, new_name, QtCore.Qt.EditRole)

        user_role = index.data(QtCore.Qt.UserRole)

        if user_role == 'state':
            self.data_model.renameState(old_name, new_name)

        if user_role == 'custom_event':
            self.data_model.renameCustomEvent(old_name, new_name)

        if user_role == 'timer':
            self.data_model.renameTimer(old_name, new_name)

    def sizeHint(self, option, index):
        return super().sizeHint(option, index)

    def paint(self, painter, option, index):

        user_role = index.data(QtCore.Qt.UserRole)

        if user_role != 'timer' and user_role != 'state':
            super().paint(painter, option, index)
            return

        painter.save()

        if user_role == 'timer':
            self.paintTimer(index, option, painter)

        if user_role == 'state':
            self.paintState(index, option, painter)

        painter.restore()

    def paintState(self, index, option, painter):
        opt = option
        self.initStyleOption(opt, index)
        name = index.data(QtCore.Qt.EditRole)

        style = opt.widget.style() if opt.widget else QtWidgets.QApplication.style()

        name_font = QtGui.QFont(opt.font)
        if name.lower() == self.data_model.default_state.lower():
            name_font.setBold(True)
        else:
            name_font.setBold(False)
        opt.font = name_font

        style.drawControl(
            QtWidgets.QStyle.CE_ItemViewItem,
            opt,
            painter,
            opt.widget
        )

    def paintTimer(self, index, option, painter):
        opt = option
        self.initStyleOption(opt, index)
        opt.text = ''
        style = opt.widget.style() if opt.widget else QtWidgets.QApplication.style()
        style.drawControl(
            QtWidgets.QStyle.CE_ItemViewItem,
            opt,
            painter,
            opt.widget
        )
        name = index.data(QtCore.Qt.EditRole)
        timer = self.data_model.getTimerByName(name)
        is_real_time = timer.is_real_time
        length = timer.length
        name_font = QtGui.QFont(opt.font)
        if is_real_time:
            name_font.setBold(True)
        else:
            name_font.setBold(False)
        painter.setFont(name_font)
        painter.setPen(
            opt.palette.highlightedText().color()
            if opt.state & QtWidgets.QStyle.State_Selected
            else opt.palette.text().color()
        )
        rect = opt.rect.adjusted(4, 0, -4, 0)
        x = rect.left()
        metrics = painter.fontMetrics()
        name_width = metrics.horizontalAdvance(name)
        text_y = rect.top() + rect.height() // 2 + metrics.ascent() // 2
        painter.drawText(x, text_y, name)
        x += name_width + 6
        sub_font = QtGui.QFont(opt.font)
        sub_font.setPointSize(sub_font.pointSize() - 1)
        painter.setFont(sub_font)
        painter.setPen(
            opt.palette.highlightedText().color()
            if opt.state & QtWidgets.QStyle.State_Selected
            else QtGui.QColor("gray")
        )
        painter.drawText(x, text_y, f"- {length:.2f}s")


class MP2FSMTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, main_window, parent, data_model: MP2FSMDataModel):
        super().__init__(parent)

        self.toggle_timer_type_action = None
        self.main_window = main_window
        self.data_model = data_model
        self.custom_events_item = None
        self.states_events_item = None
        self.timers_events_item = None
        self.do_events_item = None
        self.ai_events_item = None
        self.trigger_events_item = None
        self.generic_events_item = None
        self.animation_events_item = None

        self.context_menu = None
        self.add_custom_event_action = None
        self.add_custom_state_action = None
        self.set_default_state_action = None
        self.add_timer_action = None
        self.change_timer_length_action = None
        self.rename_action = None
        self.delete_action = None

        self.setColumnCount(1)
        tree_header_item = QtWidgets.QTreeWidgetItem()
        tree_header_item.setText(0, 'FSM')
        self.setHeaderItem(tree_header_item)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setItemDelegate(MP2FSMTreeItemDelegate(self, self.data_model))
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.currentItemChanged.connect(self.itemSelectionChanged)

        self.createTreeItems()
        self.createContextMenu()

    def createTreeItems(self):
        self.custom_events_item = QtWidgets.QTreeWidgetItem(self)
        self.custom_events_item.setText(0, "Custom Events (FSM_Send)")
        self.custom_events_item.setData(0, QtCore.Qt.UserRole, 'custom_events')

        self.states_events_item = QtWidgets.QTreeWidgetItem(self)
        self.states_events_item.setText(0, "States (FSM_Switch)")
        self.states_events_item.setData(0, QtCore.Qt.UserRole, 'states')

        self.timers_events_item = QtWidgets.QTreeWidgetItem(self)
        self.timers_events_item.setText(0, "Timers")
        self.timers_events_item.setData(0, QtCore.Qt.UserRole, 'timers')

        self.do_events_item = QtWidgets.QTreeWidgetItem(self)
        self.do_events_item.setText(0, "DO")
        self.do_events_item.setData(0, QtCore.Qt.UserRole, 'do')

        self.ai_events_item = QtWidgets.QTreeWidgetItem(self)
        self.ai_events_item.setText(0, "AI")
        self.ai_events_item.setData(0, QtCore.Qt.UserRole, 'ai')

        self.trigger_events_item = QtWidgets.QTreeWidgetItem(self)
        self.trigger_events_item.setText(0, "Trigger")
        self.trigger_events_item.setData(0, QtCore.Qt.UserRole, 'trigger')

        self.generic_events_item = QtWidgets.QTreeWidgetItem(self)
        self.generic_events_item.setText(0, "Generic")
        self.generic_events_item.setData(0, QtCore.Qt.UserRole, 'generic')

        self.animation_events_item = QtWidgets.QTreeWidgetItem(self)
        self.animation_events_item.setText(0, "Animation")
        self.animation_events_item.setData(0, QtCore.Qt.UserRole, 'animation')

    def updateContextMenu(self, item):
        self.add_custom_event_action.setEnabled(False)
        self.add_custom_state_action.setEnabled(False)
        self.set_default_state_action.setEnabled(False)
        self.add_timer_action.setEnabled(False)
        self.change_timer_length_action.setEnabled(False)
        self.rename_action.setEnabled(False)
        self.delete_action.setEnabled(False)
        self.toggle_timer_type_action.setEnabled(False)

        if item is None:
            self.add_custom_event_action.setEnabled(True)
            self.add_custom_state_action.setEnabled(True)
            self.add_timer_action.setEnabled(True)
        else:
            item_type = item.data(0, QtCore.Qt.UserRole)

            if item_type == 'custom_events':
                self.add_custom_event_action.setEnabled(True)
            elif item_type == 'custom_event':
                self.add_custom_event_action.setEnabled(True)
                self.rename_action.setEnabled(True)
                self.delete_action.setEnabled(True)
            elif item_type == 'states':
                self.add_custom_state_action.setEnabled(True)
            elif item_type == 'state':
                self.add_custom_state_action.setEnabled(True)
                self.set_default_state_action.setEnabled(True)
                self.rename_action.setEnabled(True)
                self.delete_action.setEnabled(True)
            elif item_type == 'timers':
                self.add_timer_action.setEnabled(True)
            elif item_type == 'timer':
                self.add_timer_action.setEnabled(True)
                self.change_timer_length_action.setEnabled(True)
                self.rename_action.setEnabled(True)
                self.delete_action.setEnabled(True)
                self.toggle_timer_type_action.setEnabled(True)

    def createContextMenu(self):
        self.context_menu = QtWidgets.QMenu(self)
        self.add_custom_event_action = self.context_menu.addAction('Add Custom Event')
        self.context_menu.addSeparator()
        self.add_custom_state_action = self.context_menu.addAction('Add Custom State')
        self.set_default_state_action = self.context_menu.addAction('Set As Default State')
        self.context_menu.addSeparator()
        self.add_timer_action = self.context_menu.addAction('Add Timer')
        self.change_timer_length_action = self.context_menu.addAction('Change Timer Length')
        self.toggle_timer_type_action = self.context_menu.addAction('Toggle Timer Type (game/real-time(BOLD))')
        self.context_menu.addSeparator()
        self.rename_action = self.context_menu.addAction('Rename')
        self.context_menu.addSeparator()
        self.delete_action = self.context_menu.addAction('Delete')

    def showContextMenu(self, pos):

        item = self.itemAt(pos)
        self.updateContextMenu(item)

        global_pos = self.mapToGlobal(pos)
        selected_action = self.context_menu.exec_(global_pos)

        if selected_action == self.add_custom_state_action:
            self.createNewState()
        elif selected_action == self.add_custom_event_action:
            self.createNewCustomEvent()
        elif selected_action == self.set_default_state_action:
            if self.data_model is not None:
                self.data_model.setDefaultState(item.text(0))
        elif selected_action == self.rename_action:
            self.editItem(item, 0)
        elif selected_action == self.add_timer_action:
            self.createNewTimer()
        elif selected_action == self.toggle_timer_type_action:
            self.toggleTimerType(item)
        elif selected_action == self.change_timer_length_action:
            if not self.changeTimerLength(item):
                QtWidgets.QMessageBox.warning(
                    self.main_window,
                    "Error",
                    "The entered value is not valid"
                )
        elif selected_action == self.delete_action:
            self.deleteItem(item)

    def deleteItem(self, item):
        reply = QtWidgets.QMessageBox.question(
            self.main_window,
            "Delete",
            "Delete %s?" % item.text(0),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply != QtWidgets.QMessageBox.Yes:
            return

        item_type = item.data(0, QtCore.Qt.UserRole)

        parent = item.parent()
        if item_type == 'state':
            self.data_model.removeState(item.text(0))
        if item_type == 'custom_event':
            self.data_model.removeCustomEvent(item.text(0))
        if item_type == 'timer':
            self.data_model.removeTimer(item.text(0))

        parent.removeChild(item)
        self.setCurrentItem(parent)
        self.data_model.broadcastEditEvent(None)

    def createNewState(self):
        new_state_name = self.data_model.createState()

        self.states_events_item.setExpanded(True)
        new_state_item = QtWidgets.QTreeWidgetItem(self.states_events_item)
        new_state_item.setText(0, new_state_name)
        new_state_item.setData(0, QtCore.Qt.UserRole, 'state')
        new_state_item.setFlags(new_state_item.flags() | QtCore.Qt.ItemIsEditable)

        self.setCurrentItem(new_state_item, 0)
        self.editItem(new_state_item, 0)

    def createNewTimer(self):
        new_timer = self.data_model.createTimer()

        self.timers_events_item.setExpanded(True)
        new_timer_item = QtWidgets.QTreeWidgetItem(self.timers_events_item)
        new_timer_item.setText(0, new_timer.name)
        new_timer_item.setData(0, QtCore.Qt.UserRole, 'timer')
        new_timer_item.setFlags(new_timer_item.flags() | QtCore.Qt.ItemIsEditable)

        new_timer_item.setExpanded(True)
        new_timer_on_start_timer = QtWidgets.QTreeWidgetItem(new_timer_item)
        new_timer_on_start_timer.setText(0, 'OnStartTimer')
        new_timer_on_start_timer.setData(0, QtCore.Qt.UserRole, 'timer_event')

        new_timer_on_end_timer = QtWidgets.QTreeWidgetItem(new_timer_item)
        new_timer_on_end_timer.setText(0, 'OnEndTimer')
        new_timer_on_end_timer.setData(0, QtCore.Qt.UserRole, 'timer_event')

        self.setCurrentItem(new_timer_item, 0)
        self.editItem(new_timer_item, 0)

    def changeTimerLength(self, item):
        timer = self.data_model.getTimerByName(item.text(0))

        text, ok = QtWidgets.QInputDialog.getText(
            self.main_window,
            'Change Timer Length',
            'Enter a floating-point value greater than 0:',
            QtWidgets.QLineEdit.Normal,
            str(timer.length)
        )

        if not ok:
            return False

        if not text:
            return False

        length_text = text.strip()
        if length_text == '':
            return False

        try:
            length = float(length_text)
        except (ValueError, TypeError):
            return False

        is_float = isinstance(length, float) and not math.isnan(length) and not math.isinf(length)

        if not is_float:
            return False

        if length < 0.0 or math.isclose(length, 0.0, abs_tol=1e-9):
            return False

        self.data_model.changeTimerLength(item.text(0), length)

        return True

    def toggleTimerType(self, item):
        self.data_model.toggleTimerType(item.text(0))

    def createNewCustomEvent(self):
        new_event_name = self.data_model.createCustomEvent()

        self.custom_events_item.setExpanded(True)
        new_event_item = QtWidgets.QTreeWidgetItem(self.custom_events_item)
        new_event_item.setText(0, new_event_name)
        new_event_item.setData(0, QtCore.Qt.UserRole, 'custom_event')
        new_event_item.setFlags(new_event_item.flags() | QtCore.Qt.ItemIsEditable)

        self.setCurrentItem(new_event_item, 0)
        self.editItem(new_event_item, 0)

    def itemSelectionChanged(self, current, previous):
        if not current:
            self.data_model.broadcastEditEvent(None)
            return

        event_model = None
        item_type = current.data(0, QtCore.Qt.UserRole)
        if item_type == 'state':
            event_model = self.data_model.getStateEventByName(current.text(0))

        if item_type == 'custom_event':
            event_model = self.data_model.getCustomEventByName(current.text(0))

        if item_type == 'timer_event':
            timer = self.data_model.getTimerByName(current.parent().text(0))
            event_model = timer.getEventByName(current.text(0))

        if item_type == 'event':
            event_model = self.data_mode.getEventByName(current.text(0))

        self.data_model.broadcastEditEvent(event_model)


class MP2FSMDialog(QtWidgets.QDialog):
    def __init__(self, node_to_edit, attr_to_edit):
        super().__init__(None)
        self.dialog_buttons = None
        self.data = MP2FSMDataModel()
        self.code_widget = None
        self.tree_widget = None

        self.node_to_edit = node_to_edit
        self.attr_to_edit = attr_to_edit

        # maya_window_ptr = omui.MQtUtil.mainWindow()
        # parent = wrapInstance(int(maya_window_ptr), QtWidgets.QWidget)
        parent = None
        # super(MP2FSMDialog, self).__init__(parent)
        self.setWindowTitle("Max Payne 2 FSM Editor")
        self.resize(1280, 720)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
        self.setLayout(self.mainLayout)
        self.configureUI()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setModal(True)

    def keyPressEvent(self, event):
        key = event.key()

        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            event.ignore()
            return

        if key == QtCore.Qt.Key_Escape:
            return

        super().keyPressEvent(event)

    def createDialogButtons(self):
        self.dialog_buttons = QtWidgets.QDialogButtonBox()
        self.dialog_buttons.setStandardButtons(
            QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Save)

        self.dialog_buttons.clicked.connect(self.onDialogButtonClicked)
        self.mainLayout.addWidget(self.dialog_buttons)

    def onDialogButtonClicked(self, button):
        role = self.dialog_buttons.buttonRole(button)

        if role == QtWidgets.QDialogButtonBox.ApplyRole:
            self.apply()

        elif role == QtWidgets.QDialogButtonBox.AcceptRole:
            self.save()

        elif role == QtWidgets.QDialogButtonBox.RejectRole:
            self.close()

    def close(self):
        self.reject()

    def save(self):
        self.apply()
        self.accept()

    def apply(self):
        self.writeToAttr(self.data.toJson())

    def readFromAttr(self):
        if not self.node_to_edit:
            return
        plug = self.node_to_edit.findPlug(self.attr_to_edit, False)
        if not plug:
            return
        return plug.asString()

    def writeToAttr(self, data):
        print(data)

        if not self.node_to_edit:
            return
        plug = self.node_to_edit.findPlug(self.attr_to_edit, False)
        if not plug:
            return
        plug.setString(data)

    def configureUI(self):
        self.createSplitter()
        self.createDialogButtons()

    def createSplitter(self):
        splitter_widget = QtWidgets.QSplitter()
        splitter_widget.setOrientation(QtCore.Qt.Horizontal)
        splitter_widget.setChildrenCollapsible(False)

        self.tree_widget = MP2FSMTreeWidget(self, splitter_widget, self.data)
        self.code_widget = MP2FSMTextEditWidget(splitter_widget, self.data)

        splitter_widget.addWidget(self.tree_widget)
        splitter_widget.addWidget(self.code_widget)
        self.mainLayout.addWidget(splitter_widget)

# 'DO_BulletCollides'
# 'DO_MovedToInvalidPosition'
# 'DO_MovedToInvalidPositionEnds'
# 'DO_OnDeath'
# 'Animation'
# 'FSM_Send'
# 'FSM_Switch'
# 'OnStartTimer'
# 'OnEndTimer'

def perform_edit_fsm_action(node_name):
    print(node_name)

    node_only = node_name.split('.')[0]
    try:
        sel = OpenMaya.MSelectionList()
        sel.add(node_only)
        node = sel.getDependNode(0)
    except:
        return

    my_node = OpenMaya.MFnDependencyNode(node)
    if my_node:
        fsm_edit_widow = MP2FSMDialog(my_node, "na_fsm")
        fsm_edit_widow.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = MP2FSMDialog(None, "2")
    dialog.show()
    sys.exit(app.exec_())

