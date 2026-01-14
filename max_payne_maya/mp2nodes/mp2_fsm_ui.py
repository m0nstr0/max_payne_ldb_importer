import math

import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
import json


class MP2FSMEventDataModel:
    def __init__(self, name):
        self.name = name
        self.send_before = []
        self.send_after = []
        self.state_specific = {}

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
        self.events = [MP2FSMEventDataModel('OnStartTimer'), MP2FSMEventDataModel('OnEndTimer')]

    def getEventByName(self, name):
        for event in self.events:
            if event.name == name:
                return event
        return None


class MP2FSMDataModel:
    def __init__(self):
        self.states = []
        self.custom_events = []
        self.events = []
        self.timers = []
        self.default_state = None
        self.edit_event_delegate = []

    def getCustomEvents(self):
        return self.custom_events

    def getEvents(self):
        return self.events

    def getStates(self):
        return self.states

    def getTimers(self):
        return self.timers

    def renameCustomEvent(self, old_name, new_name):
        custom_event = self.getCustomEventByName(old_name)
        custom_event.name = new_name

        self.broadcastEditEvent(custom_event)

    def changeTimerLength(self, name, length):
        timer = self.getTimerByName(name)
        timer.length = length

    def toggleTimerType(self, name):
        timer = self.getTimerByName(name)
        timer.is_real_time = not timer.is_real_time

    def renameTimer(self, old_name, new_name):
        timer = self.getTimerByName(old_name)
        timer.name = new_name
        self.broadcastEditEvent(None)

    def renameState(self, old_name, new_name):
        state = self.getStateByName(old_name)
        state.name = new_name

        for i in self.states:
            i.renameState(old_name, new_name)

        if self.default_state.lower() == state.name.lower():
            default_state = new_name
            self.setDefaultState(default_state)
        self.broadcastEditEvent(state)

    def getEventByName(self, name):
        for i in self.events:
            if i.name.lower() == name:
                return i
        return None

    def getCustomEventByName(self, name):
        for i in self.custom_events:
            if i.name.lower() == name:
                return i
        return None

    def getTimerByName(self, name):
        for i in self.timers:
            if i.name.lower() == name:
                return i
        return None

    def getStateByName(self, name):
        for i in self.states:
            if i.name.lower() == name:
                return i
        return None

    def setDefaultState(self, name):
        self.default_state = name

    def removeState(self, name):
        state = self.getStateByName(name)
        self.states.remove(state)

        for i in self.states:
            i.removeState(name)

        if self.default_state.lower() == state.name.lower():
            default_state = None
            if len(self.states) > 0:
                default_state = self.states[0].name
            self.setDefaultState(default_state)

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

    @staticmethod
    def getNextName(prefix, data):
        index = len(data)
        next_name = "%s_%d" % (prefix, index)
        while True:
            found = False
            for i in data:
                if i.name.lower() == next_name:
                    found = True
                    break
            if found:
                index = index + 1
                next_name = "%s_%d" % (prefix, index)
            else:
                break
        return next_name

    def createCustomEvent(self):
        new_event = MP2FSMEventDataModel(self.getNextName('custom_event', self.custom_events))
        self.custom_events.append(new_event)
        return new_event

    def createTimer(self):
        new_timer = MP2FSMTimerDataModel(self.getNextName('timer', self.timers))
        self.timers.append(new_timer)
        return new_timer

    def createState(self):
        new_state = MP2FSMEventDataModel(self.getNextName('state', self.states))
        self.states.append(new_state)
        return new_state

    def subscribeToEditEvent(self, callback):
        self.edit_event_delegate.append(callback)

    def broadcastEditEvent(self, event):
        for i in self.edit_event_delegate:
            i(event)

    def removeCustomEvent(self, name):
        event = self.getCustomEventByName(name)
        self.custom_events.remove(event)

    def removeTimer(self, name):
        timer = self.getTimerByName(name)
        self.timers.remove(timer)

# QItemDelegate
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
            super(MP2FSMTreeItemDelegate, self).paint(painter, option, index)
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

        state = self.data_model.getStateByName(name)

        style = opt.widget.style() if opt.widget else QtWidgets.QApplication.style()

        name_font = QtGui.QFont(opt.font)
        if state.name.lower() == self.data_model.default_state.lower():
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


class MP2FSMTreeComponent(QtWidgets.QWidget):
    def __init__(self, main_window, parent, data_model: MP2FSMDataModel):
        super(MP2FSMTreeComponent, self).__init__(parent)
        self.toggle_timer_type_action = None
        self.main_window = main_window
        self.data_model = data_model
        self.tree_widget = None
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

        top_v_layout = QtWidgets.QVBoxLayout(self)
        top_v_layout.setContentsMargins(0, 0, 0, 0)
        top_v_layout.addWidget(self.createTreeWidget())

        self.createTreeItems()
        self.createContextMenu()

    def createTreeItems(self):
        self.custom_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.custom_events_item.setText(0, "Custom Events (FSM_Send)")
        self.custom_events_item.setData(0, QtCore.Qt.UserRole, 'custom_events')

        self.states_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.states_events_item.setText(0, "States (FSM_Switch)")
        self.states_events_item.setData(0, QtCore.Qt.UserRole, 'states')

        self.timers_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.timers_events_item.setText(0, "Timers")
        self.timers_events_item.setData(0, QtCore.Qt.UserRole, 'timers')

        self.do_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.do_events_item.setText(0, "DO")
        self.do_events_item.setData(0, QtCore.Qt.UserRole, 'do')

        self.ai_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.ai_events_item.setText(0, "AI")
        self.ai_events_item.setData(0, QtCore.Qt.UserRole, 'ai')

        self.trigger_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.trigger_events_item.setText(0, "Trigger")
        self.trigger_events_item.setData(0, QtCore.Qt.UserRole, 'trigger')

        self.generic_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.generic_events_item.setText(0, "Generic")
        self.generic_events_item.setData(0, QtCore.Qt.UserRole, 'generic')

        self.animation_events_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
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

        item = self.tree_widget.itemAt(pos)
        self.updateContextMenu(item)

        global_pos = self.tree_widget.mapToGlobal(pos)
        selected_action = self.context_menu.exec_(global_pos)

        if selected_action == self.add_custom_state_action:
            self.createNewState()
        elif selected_action == self.add_custom_event_action:
            self.createNewCustomEvent()
        elif selected_action == self.set_default_state_action:
            if self.data_model is not None:
                self.data_model.setDefaultState(item.text(0))
        elif selected_action == self.rename_action:
            self.tree_widget.editItem(item, 0)
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
        self.tree_widget.setCurrentItem(parent)
        self.data_model.broadcastEditEvent(None)

    def createNewState(self):
        new_state = self.data_model.createState()

        self.states_events_item.setExpanded(True)
        new_state_item = QtWidgets.QTreeWidgetItem(self.states_events_item)
        new_state_item.setText(0, new_state.name)
        new_state_item.setData(0, QtCore.Qt.UserRole, 'state')
        new_state_item.setFlags(new_state_item.flags() | QtCore.Qt.ItemIsEditable)

        if len(self.data_model.getStates()) == 1:
            self.data_model.setDefaultState(new_state.name)

        self.tree_widget.setCurrentItem(new_state_item, 0)
        self.tree_widget.editItem(new_state_item, 0)

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

        self.tree_widget.setCurrentItem(new_timer_item, 0)
        self.tree_widget.editItem(new_timer_item, 0)

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
        new_event = self.data_model.createCustomEvent()

        self.custom_events_item.setExpanded(True)
        new_event_item = QtWidgets.QTreeWidgetItem(self.custom_events_item)
        new_event_item.setText(0, new_event.name)
        new_event_item.setData(0, QtCore.Qt.UserRole, 'custom_event')
        new_event_item.setFlags(new_event_item.flags() | QtCore.Qt.ItemIsEditable)

        self.tree_widget.setCurrentItem(new_event_item, 0)
        self.tree_widget.editItem(new_event_item, 0)

    def itemSelectionChanged(self, current, previous):
        if not current:
            self.data_model.broadcastEditEvent(None)
            return

        event_model = None
        item_type = current.data(0, QtCore.Qt.UserRole)
        if item_type == 'state':
            event_model = self.data_model.getStateByName(current.text(0))

        if item_type == 'custom_event':
            event_model = self.data_model.getCustomEventByName(current.text(0))

        if item_type == 'timer_event':
            timer = self.data_model.getTimerByName(current.parent().text(0))
            event_model = timer.getEventByName(current.text(0))

        if item_type == 'event':
            event_model = self.data_mode.getEventByName(current.text(0))

        self.data_model.broadcastEditEvent(event_model)

    def createTreeWidget(self):
        self.tree_widget = QtWidgets.QTreeWidget(self)
        self.tree_widget.setColumnCount(1)
        tree_header_item = QtWidgets.QTreeWidgetItem()
        tree_header_item.setText(0, 'FSM')
        self.tree_widget.setHeaderItem(tree_header_item)
        self.tree_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.tree_widget.setItemDelegate(MP2FSMTreeItemDelegate(self.tree_widget, self.data_model))

        self.tree_widget.customContextMenuRequested.connect(self.showContextMenu)
        self.tree_widget.currentItemChanged.connect(self.itemSelectionChanged)

        return self.tree_widget


class MP2FSMCodeComponent(QtWidgets.QWidget):
    def __init__(self, main_window, parent, data_model: MP2FSMDataModel):
        super(MP2FSMCodeComponent, self).__init__(parent)
        self.is_updating = True
        self.main_window = main_window
        self.data_model = data_model
        self.current_event_model = None
        self.before_add_button_widget = None
        self.before_messages_widget = None
        self.state_add_button_widget = None
        self.state_list_widget = None
        self.state_messages_widget = None
        self.after_messages_widget = None
        self.after_add_button_widget = None
        self.current_state = ''

        top_v_layout = QtWidgets.QVBoxLayout(self)
        top_v_layout.setContentsMargins(0, 0, 0, 0)
        top_v_layout.addWidget(self.createSendAlwaysBefore())
        top_v_layout.addWidget(self.createStateSpecific())
        top_v_layout.addWidget(self.createSendAlwaysAfter())

        self.update()

        self.data_model.subscribeToEditEvent(self.update)

    def createSendAlwaysBefore(self):
        self.before_add_button_widget = QtWidgets.QPushButton('Add', self)
        self.before_messages_widget = QtWidgets.QListWidget(self)

        before_v_layout = QtWidgets.QVBoxLayout(self)
        before_add_button_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        before_add_button_size_policy.setHorizontalStretch(0)
        before_add_button_size_policy.setVerticalStretch(0)
        before_add_button_size_policy.setHeightForWidth(self.before_add_button_widget.sizePolicy().hasHeightForWidth())
        self.before_add_button_widget.setSizePolicy(before_add_button_size_policy)
        self.before_add_button_widget.clicked.connect(self.addSendAlwaysBeforeMessage)

        before_v_layout.addWidget(self.before_add_button_widget)
        before_v_layout.addWidget(self.before_messages_widget)

        before_group_widget = QtWidgets.QGroupBox("Send Always Before", self)
        before_group_widget.setLayout(before_v_layout)

        return before_group_widget

    def createSendAlwaysAfter(self):
        self.after_messages_widget = QtWidgets.QListWidget(self)
        self.after_add_button_widget = QtWidgets.QPushButton('Add', self)

        after_v_layout = QtWidgets.QVBoxLayout(self)

        after_add_button_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        after_add_button_size_policy.setHorizontalStretch(0)
        after_add_button_size_policy.setVerticalStretch(0)
        after_add_button_size_policy.setHeightForWidth(self.after_add_button_widget.sizePolicy().hasHeightForWidth())
        self.after_add_button_widget.setSizePolicy(after_add_button_size_policy)
        self.after_add_button_widget.clicked.connect(self.addSendAlwaysAfterMessage)

        after_v_layout.addWidget(self.after_add_button_widget)
        after_v_layout.addWidget(self.after_messages_widget)

        after_group_widget = QtWidgets.QGroupBox("Send Always After", self)
        after_group_widget.setLayout(after_v_layout)

        return after_group_widget

    def createStateSpecific(self):
        self.state_add_button_widget = QtWidgets.QPushButton('Add', self)
        self.state_list_widget = QtWidgets.QComboBox(self)
        self.state_list_widget.currentIndexChanged.connect(self.onStateSelected)
        self.state_messages_widget = QtWidgets.QListWidget(self)

        state_v_layout = QtWidgets.QVBoxLayout(self)
        state_h_layout = QtWidgets.QHBoxLayout(self)

        state_add_button_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        state_add_button_size_policy.setHorizontalStretch(0)
        state_add_button_size_policy.setVerticalStretch(0)
        state_add_button_size_policy.setHeightForWidth(self.state_add_button_widget.sizePolicy().hasHeightForWidth())
        self.state_add_button_widget.setSizePolicy(state_add_button_size_policy)
        self.state_add_button_widget.clicked.connect(self.addStateSpecificMessage)

        state_h_layout.addWidget(self.state_add_button_widget)
        state_h_layout.addWidget(self.state_list_widget)

        state_v_layout.addLayout(state_h_layout)
        state_v_layout.addWidget(self.state_messages_widget)

        state_group_widget = QtWidgets.QGroupBox("State Specific", self)
        state_group_widget.setLayout(state_v_layout)

        return state_group_widget

    def getNewMessage(self, title):
        text, ok = QtWidgets.QInputDialog.getText(self.main_window, title, "Enter message:")
        if not ok:
            return ''

        if not text:
            return ''

        item_text = text.strip()
        if item_text == '':
            return ''

        return item_text

    def addNewMessage(self, parent, title):
        item_text = self.getNewMessage(title)
        if item_text == '':
            return
        item = QtWidgets.QListWidgetItem(parent)
        item.setText(item_text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        parent.setCurrentItem(item)
        parent.scrollToItem(item)

    def addSendAlwaysBeforeMessage(self, checked):
        self.addNewMessage(self.before_messages_widget, 'Send Always Before Message')

    def addSendAlwaysAfterMessage(self, checked):
        self.addNewMessage(self.after_messages_widget, 'Send Always After Message')

    def addStateSpecificMessage(self, checked):
        self.addNewMessage(self.state_messages_widget, 'State Specific Message')

    def onStateSelected(self, index):
        if self.is_updating and index != -3:
            return

        if index != -3 and self.current_state.lower() != self.state_list_widget.currentText().lower():
            self.saveStateSpecificMessages()

        self.state_messages_widget.clear()

        if index == -1:
            return

        if self.current_event_model is None:
            return

        state_name = self.state_list_widget.currentText()
        self.current_state = state_name

        found_key = ''
        for key in self.current_event_model.state_specific:
            if key.lower() == state_name.lower():
                found_key = key

        if found_key == '':
            return

        for message in self.current_event_model.state_specific[found_key]:
            item = QtWidgets.QListWidgetItem(self.state_messages_widget)
            item.setText(message)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def saveSendBeforeMessages(self):
        if self.current_event_model is None:
            return

        num_messages = self.before_messages_widget.count()
        messages = []
        for i in range(num_messages):
            messages.append(self.before_messages_widget.item(i).text())
        if self.current_event_model is not None:
            self.current_event_model.send_before = messages

    def saveSendAfterMessages(self):
        if self.current_event_model is None:
            return

        num_messages = self.after_messages_widget.count()
        messages = []
        for i in range(num_messages):
            messages.append(self.after_messages_widget.item(i).text())
        if self.current_event_model is not None:
            self.current_event_model.send_after = messages

    def saveStateSpecificMessages(self):
        if self.current_event_model is None:
            return

        num_messages = self.state_messages_widget.count()
        messages = []
        for i in range(num_messages):
            messages.append(self.state_messages_widget.item(i).text())

        state_name = self.current_state

        found_key = ''
        for key in self.current_event_model.state_specific:
            if key.lower() == state_name.lower():
                found_key = key

        if found_key == '':
            found_key = state_name

        if self.current_event_model is not None:
            self.current_event_model.state_specific[found_key] = messages

    def save(self):
        self.saveSendBeforeMessages()
        self.saveStateSpecificMessages()
        self.saveSendAfterMessages()

    def update(self, event_model=None):
        self.is_updating = True
        if self.current_event_model is not None:
            self.save()
        self.current_event_model = event_model
        self.before_add_button_widget.setEnabled(False)
        self.before_messages_widget.setEnabled(False)
        self.before_messages_widget.clear()
        self.state_add_button_widget.setEnabled(False)
        self.state_list_widget.setEnabled(False)
        self.state_list_widget.clear()
        self.state_messages_widget.setEnabled(False)
        self.state_messages_widget.clear()
        self.after_messages_widget.setEnabled(False)
        self.after_messages_widget.clear()
        self.after_add_button_widget.setEnabled(False)

        if not event_model:
            self.is_updating = False
            return

        for message in event_model.send_before:
            item = QtWidgets.QListWidgetItem(self.before_messages_widget)
            item.setText(message)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

        for message in event_model.send_after:
            item = QtWidgets.QListWidgetItem(self.after_messages_widget)
            item.setText(message)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

        for state in self.data_model.getStates():
            self.state_list_widget.addItem(state.name)

        self.current_state = self.state_list_widget.currentText()

        self.before_add_button_widget.setEnabled(True)
        self.before_messages_widget.setEnabled(True)

        if len(self.data_model.getStates()) > 0:
            self.state_add_button_widget.setEnabled(True)
            self.state_list_widget.setEnabled(True)
            self.state_messages_widget.setEnabled(True)
            self.onStateSelected(-3)

        self.after_messages_widget.setEnabled(True)
        self.after_add_button_widget.setEnabled(True)
        self.is_updating = False


class MP2FSMDialog(QtWidgets.QDialog):
    def __init__(self, node_to_edit, attr_to_edit):
        self.dialog_buttons = None
        self.data = MP2FSMDataModel()
        self.code_widget = None
        self.tree_widget = None

        self.node_to_edit = node_to_edit
        self.attr_to_edit = attr_to_edit

        maya_window_ptr = omui.MQtUtil.mainWindow()
        parent = wrapInstance(int(maya_window_ptr), QtWidgets.QWidget)
        super(MP2FSMDialog, self).__init__(parent)
        self.setWindowTitle("Max Payne 2 FSM Editor")
        self.resize(800, 600)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
        self.setLayout(self.mainLayout)
        self.configureUI()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setModal(True)

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

        self.tree_widget = MP2FSMTreeComponent(self, splitter_widget, self.data)
        self.code_widget = MP2FSMCodeComponent(self, splitter_widget, self.data)

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

dialog = MP2FSMDialog(None, "2")
dialog.show()
