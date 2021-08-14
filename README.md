# Folder-Lock
Lock your folders with a password.

Deltaion's Edits:

I ported it to commandline only platforms.

- First, I removed all of the Tkinter-specific code in the project as well as operating system dependent functions and thread-based calling functions.
- Next, I merged the utility file into the main file to remove the requirement of multiple files linking. (This is a problem on my target platform, so that's an important part to note)
- Finally, I added a quick input system to grab a passkey and choose between locking and unlocking the files in the folder.

Remember, just like the original [Folder-Lock](https://github.com/MCMi460/Folder-Lock), this one requires all the target items to be in the `./STOARGE/` directory.

Thank you for reading!
