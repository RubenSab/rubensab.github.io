# How to Build and Publish a Simple Linux Command-Line Tool with Python on GitHub: a Guided Example

Let’s find out about it!

Going from coding that tiny random python script which makes your life just a bit easier by solving that very specific problem you had, to packaging and porting it worldwide on Github could seem a daunting task for the unitiated; but I promise, it really isn’t.

With just a few tools in your belt you’ll be able to publish your own portable CLI tool that end users will be able to install and run as an ordinary command with no trouble.

During the **four steps** or this example ([https://github.com/RubenSab/dlmv](https://github.com/RubenSab/dlmv)) we are going to use:

- the [**argparse](https://docs.python.org/3/howto/argparse.html)** python library to process CLI arguments according to the [GNU Coding Standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html);

- a [**bash script](https://www.geeksforgeeks.org/bash-scripting-introduction-to-bash-and-bash-scripting/) **or a [**Makefile](https://makefiletutorial.com/)** as an alternative to automate the installation of our project for the end user;

- a [**tar.gz archive](https://www.geeksforgeeks.org/how-to-compress-and-extract-files-using-the-tar-command-on-linux/)** to package everything**;**

- [**Github](http://github.com)** to publish our project and its releases.

> You’ll need a personal access token to use Github from the terminal. click [**here](https://docs.catalyst.zoho.com/en/tutorials/githubbot/java/generate-personal-access-token/)** to learn how to get it if you don’t know how.

Enough talking, let’s start building:

## 1. Our goal

Let’s say we need to code a handy script that takes the n-th most recent files in the Downloads folder and moves them automatically to whatever folder we are currently in inside our terminal.

We’ll call it dlmv.py; and for now, if we want to stick to that simple goal and no more, the only input required from the user is the *number of files *they want to move.

### The arguments syntax

What CLI argument syntax would be the fastest and most efficient to achieve this?

Of course dlmv n with n being the (optional) number of files to move (with default being 1 file).

Other than this, we need to take in account two other arguments in order to respect the GNU Coding Standards, namely --help and its shorthand -h , but **argparse** is going to take care of this automatically.

### The code (you can skip to the packaging part)

``` Python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "files_number", 
    type=int, # Obviously our argument needs to be an integer.
    nargs='?', # The argument is optional
    default=1, # because the default is 1 file.
    # this handles --help and -h
    help="The number of most recent files to move from the Downloads folder to the current directory (default: 1)"
)
args = parser.parse_args()
```

This code created the variable `args.files_number`, now we need to find the user’s Downloads folder path, list it and cap the number of files desired to the number of files that can be taken from Downloads.

``` Python
downloads_path = os.path.expanduser('~/Downloads')
paths = [f'{downloads_path}/{path}' for path in os.listdir(downloads_path)]
if len(paths) < args.files_number:
    files_number = len(paths)
else:
    files_number = int(args.files_number)
```

Then, we need to take into account if the downloads folder is empty or if the user inputted an invalid number.

If this is not the case, then we proceed normally, sorting files from new to old using os.path.getmtime(path) and selecting the needed ones by list slicing paths[:files_number] .

Finally we get the current working directory with os.getcwd() and we move them into it one by one with shutil.move after the user consents.

```
if args.files_number > 0 and len(paths) > 0:

    # selects the paths of specified files
    paths.sort(key=lambda path: os.path.getmtime(path), reverse = True)
    selected = paths[:files_number]

    # prints the confirmation and moves the file if positive
    current_dir = os.getcwd()
    confirmation = input(f'Do you want to move:\n* {"\n* ".join(selected)}\nto {os.getcwd()}? [y/n]: ').lower()
    if confirmation == 'y':
        for path in selected:
            shutil.move(path, current_dir)
        print(f'{files_number} file{"s"*(files_number>1)} moved.')


elif len(paths) == 0:
    print(f'The Downloads folder is empty.')


else:
    print(f'{files_number} is an invalid number of files to move.')
```

Finally ensure your script is ready to be executed with the right python interpreter adding a Shebang right before the code:

```
#!/usr/bin/env python3
```

## 2. Create an install.sh

**PROS**: More universal across platforms (even Windows!), simple for non-developers and clickable.

**CONS**: Less structured than Makefile , harder to manage dependencies, no automatic clean up after installation and less scalable as your project grows.

If you want a clickable tar.gz file or you want to automate installation on Windows or environments that don’t support Make , create a file named install.sh with the following content:

```
#!/bin/bash

echo "Starting installation of dlmv..."

# Ensure the script is executable
chmod +x dlmv.py

# Copy the script to /usr/local/bin, where you can launch it with 'dlmv'
sudo cp dlmv.py /usr/local/bin/dlmv

echo "Installation complete! You can now run 'dlmv' from the terminal."
```

> The end user will need to install our script using ./install.sh in its directory.

## 2. (Alternative) Create the Makefile

**PROS**: Widely used for development, extensible, allow install , uninstall and clean commands.

**CONS**: Requires make , not familiar to non-developers or not techy people.

Make a new file named Makefile with the following content:

``` bash
SCRIPT_NAME=dlmv.py
INSTALL_DIR=/usr/local/bin
TARGET=$(INSTALL_DIR)/dlmv

# Default action
all:
 @echo "Run 'make install' to install $(SCRIPT_NAME)."

# Install the script
install:
 @echo "Installing $(SCRIPT_NAME) to $(INSTALL_DIR)..."
 chmod +x $(SCRIPT_NAME)
 sudo cp $(SCRIPT_NAME) $(TARGET)
 @echo "Installation complete! You can now use 'dlmv' as a command."

# Uninstall the script
uninstall:
 @echo "Removing $(TARGET)..."
 sudo rm -f $(TARGET)
 @echo "Uninstallation complete."
```

> The end user will need to install our script using make install in its directory.

## 3. Package everything into a tar.gz (or zip on Windows)

Open the terminal and write:
```
tar -czvf dlmv_installer.tar.gz dlmv.py Makefile install.sh
```
or
```
zip -r dlmv_installer.zip dlmv.py Makefile install.sh
```

## 4. Create a release on Github

### Push your Code

Go on [Github](http://github.com), create a new repository with a name of your choice, then click on the green button on the top-right corner and copy the link shown, then open the terminal and clone the repo:

```
git clone YOUR_LINK_HERE
```

Move every file you made before in the new folder and push:

```
git add .
git commit -m "Prepare for release"
git push origin main
```

### **Create a Tag**

You need a **Git tag** for the release, create it and push it to the main branch:

```
git tag v1.0.0
git push origin v1.0.0
```

### Create the Release

* Go to your GitHub repository.

* Click on **Releases** in the right sidebar.

* Click **Draft a new release**.

* Select the tag you just created (e.g., v1.0.0).

* Add a release title (e.g., Initial Release) and description (optional).

* Attach your .tar.gz or .zip file by dragging it into the release page.

* Click **Publish Release**.

## Conclusion

See? That wasn’t so hard!

With just a few simple steps, we’ve taken your idea from concept to production, making it available for the world to install and use.

![[https://github.com/RubenSab/dlmv](https://github.com/RubenSab/dlmv)](https://cdn-images-1.medium.com/max/2578/1*ZvqpteyTF9eCJJsw8JDoJQ.png)*[https://github.com/RubenSab/dlmv](https://github.com/RubenSab/dlmv)*
q
