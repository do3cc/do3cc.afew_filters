#!/usr/bin/env python
# coding = utf-8


from setuptools import setup, find_packages

setup(
    version='0.0.1',
    name='do3cc.afew_filters',
    packages=find_packages(),
    test_suite='do3cc.afew_filters.tests',
    description="A collection for afew filters",
    long_description=open("README.md").read() + '\n' +
    open('CHANGES.md').read(),
    entry_points={
        'afew.filter': [
            'SaveMailAttachments = do3cc.afew_filters.mail_attachments:SaveAttachmentsFilter']
    },
    license='BSD',
    install_requires=[
        'afew',
        'requests',
        'easywebdav',
    ],
)
