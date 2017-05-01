#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Tristan Fischer (sphere@dersphere.de)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from xbmcswift2 import Plugin, xbmc, xbmcgui, xbmcaddon
import pyxbmct

STRINGS = {
    'compose': 30305,
    'new_message': 30306,
    'recipient': 30307,
    'subject': 30308,
    'body': 30309,
    'ok': 30310,
    'cancel': 30311
}

__language__ = xbmcaddon.Addon().getLocalizedString

def _(string_id):
    if string_id in STRINGS:
        return __language__(STRINGS[string_id])
    else:
        plugin.log.debug('String is missing: %s' % string_id)
        return string_id

class NewMailWindow(pyxbmct.AddonDialogWindow):
    def __init__(self, client, title=_('new_message'), recipient='', subject=''):
        super(NewMailWindow, self).__init__(title)
        self._client = client
        self._recipient = recipient
        self._subject = subject
        self.setGeometry(600, 480, 10, 2)
        self.set_controls()
        self.set_navigation()
        self.set_events()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        recipient_label = pyxbmct.Label(_('recipient'), alignment=pyxbmct.ALIGN_RIGHT)
        self.placeControl(recipient_label, 0, 0)
        self._recipient_ctl = pyxbmct.Edit('recipient')
        self.placeControl(self._recipient_ctl, 0, 1)
        self._recipient_ctl.setText(self._recipient)

        subject_label = pyxbmct.Label(_('subject'), alignment=pyxbmct.ALIGN_RIGHT)
        self.placeControl(subject_label, 1, 0)
        self._subject_ctl = pyxbmct.Edit('subject')
        self.placeControl(self._subject_ctl, 1, 1)
        self._subject_ctl.setText(self._subject)

        body_label = pyxbmct.Label(_('body'), alignment=pyxbmct.ALIGN_RIGHT)
        self.placeControl(body_label, 2, 0)
        self._body_ctl = pyxbmct.Edit('body')
        self.placeControl(self._body_ctl, 2, 1)

        self._view_body_ctl = pyxbmct.TextBox('view_body')
        self.placeControl(self._view_body_ctl, 3, 0, 6, 2)

        self._ok_button = pyxbmct.Button(_('ok'), alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self._ok_button, 9, 1)

        self._cancel_button = pyxbmct.Button(_('cancel'), alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self._cancel_button, 9, 0)

    def update_view(self):
        self._view_body_ctl.setText(self._body_ctl.getText())

    def set_navigation(self):
        self.setFocus(self._recipient_ctl)
        self._recipient_ctl.controlDown(self._subject_ctl)
        self._subject_ctl.controlDown(self._body_ctl)
        self._subject_ctl.controlUp(self._recipient_ctl)
        self._body_ctl.controlDown(self._ok_button)
        self._body_ctl.controlUp(self._subject_ctl)
        self._ok_button.controlLeft(self._cancel_button)
        self._cancel_button.controlRight(self._ok_button)
        self._cancel_button.controlUp(self._body_ctl)
        self._ok_button.controlUp(self._body_ctl)

    def set_events(self):
        self.connect(self._ok_button,self.send_mail)
        self.connect(self._cancel_button,self.close)

    def onAction(self, action):
        self.update_view()

    def send_mail(self):
        self._client.send_email(self._recipient_ctl.getText(),
                               self._subject_ctl.getText(),
                               self._body_ctl.getText())
        self.close()
        pass
