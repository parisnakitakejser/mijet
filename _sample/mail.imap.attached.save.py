import mijet.mail.imap.attached.save

mail = mijet.mail.imap.attached.save.build('{host}', '{username}', '{password}')
mail.mailFolder = '{mailbox-scanning}'
mail.mailFolderCopyTo = '{mailbox-move-mails-to-parsed-mailbox-folder}'
mail.mailFrom = '{only-handle-from-this-email}'
mail.run()