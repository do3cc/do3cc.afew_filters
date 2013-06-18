# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import easywebdav
import os

from tempfile import NamedTemporaryFile

from afew.filters import BaseFilter


class SaveAttachmentsFilter(BaseFilter):
    message = 'Saving attachments'
    query = 'tag:save_attachments'
    folder = "attachments"
    basepath = 'files/webdav.php'

    host = ''
    username = ''
    password = ''
    protocol = 'https'

    def __init__(self, database, client=None, **kwargs):
        super(SaveAttachmentsFilter, self).__init__(database, **kwargs)
        if not client:
            self.client = easywebdav.connect(self.host, username=self.username,
                                             password=self.password,
                                             protocol=self.protocol)
        else:
            self.client = client

    def handle_message(self, message):
        for part in message.get_message_parts():
            if part.get_content_type() != 'application/pdf':
                continue
            filename = part.get_filename()
            body = part.get_payload(decode=1)
            remote_path = os.path.join(self.basepath, self.folder, filename)
            try:
                self.client.ls(remote_path)
            except easywebdav.OperationFailed as e:
                if e.actual_code != 404:
                    raise
            else:
                continue
            with NamedTemporaryFile() as tmpfile:
                tmpfile.write(body)
                tmpfile.flush()
                self.dav.upload(tmpfile.name, remote_path)
                self.remove_tags(message, 'unread', 'save_attachments')
