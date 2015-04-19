import mijet.mail.imap.attached.save

mail = mijet.mail.imap.attached.save.Build('{host}', '{username}', '{password}')
mail.mail_folder = '{mailbox-scanning}'
mail.mail_folder_copy_to = '{mailbox-move-mails-to-parsed-mailbox-folder}'
mail.mail_from = '{only-handle-from-this-email}'
mail.run()