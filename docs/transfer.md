# Copying programs to the calculator

The fx-CG100 connects to a computer over USB and appears as a USB drive. This guide follows Casio’s fx-CG100 user’s guide, with a few points from community write-ups that are marked as such. Links to the sources are at the end.

## Before you start

* A USB data cable. Casio recommends its own cable; a charge-only cable will not work.
* The program’s `.py` file, for example `programs/mandelbrot/mandelbrot.py`. Run `python tools/check_programs.py` first to confirm it is within the 300-line limit and uses ASCII only.
* Check the file extension on your computer. Some systems hide extensions, and a file you think is `time.py` can really be `time.py.txt`. A community report describes exactly this failure: the file arrived on the calculator with the wrong name and type.

## Steps

1. Connect the calculator to the computer with the cable.
2. The calculator shows a **Select Connection Mode** dialogue. Choose **USB Flash** and confirm.
3. The calculator’s storage memory appears on the computer as a drive.
4. Copy the `.py` file onto the drive. Only the `.py` file is needed. The README and screenshots stay on your computer.
5. Eject the drive in your operating system before you unplug the cable. Unplugging without ejecting can corrupt the calculator’s storage memory.
6. On the calculator, open the **Python** app. Open the file from the app’s file list and run it.

### Running a program in the Python app

* Press **Tools** and use **File > Open** to load a saved script.
* Run it from the **Run** option, or with the arrow key shortcut the manual describes.
* If a script has unsaved changes, the app asks whether to save first, run without saving, or go back to the editor.
* Files you create on the calculator are saved with the `.py` extension in storage memory. The **Memory** app lists them under the Storage Memory tab as Python script files.

### Backing up before a large transfer

USB Flash mode lets you copy files off the calculator as well. Copy the contents of the drive to your computer before a large transfer or an operating system update.

## Things to watch for

* **Copying can be slow to start.** Casio’s guide says that copying to the calculator can take several minutes to begin while storage memory is optimised.
* **Sleep and standby.** The connection can drop if the computer goes to sleep or standby during a transfer.
* **ASCII only.** The Python app cannot show files saved with characters outside ASCII. Such a file opens as blank or garbled text. `tools/check_programs.py` checks for this.
* **Line endings.** Casio’s guide advises changing newline codes to suit the target environment when moving `.py` files between the calculator and a computer. If a file looks wrong in a desktop editor after you copy it back, convert its line endings.
* **File names.** Exam Mode limits file names to five characters. The manual does not state the normal limit that I could find, so short lowercase names are the safe choice.
* **Where the files are stored.** Casio’s pages disagree. The Python App page says storage memory, and the Exam Mode page says main memory. The Memory app lists `.py` files under Storage Memory, so copy to the USB drive and not to a folder you create.
* **Exam Mode.** If the calculator is in Exam Mode, the connection dialogue offers **USB Flash / Unlock Exam Mode** instead. Ending that connection restarts the calculator.

## Other transfer options

* **FA-124 (Casio’s PC link software).** Its documentation lists older models such as the fx-9860G series and does not list the fx-CG100. Use USB Flash mode instead.
* **PythonExtra.** A third-party MicroPython build for the fx-CG50 that is installed by copying a `.g3a` add-in to the calculator. I found no evidence that it supports the fx-CG100, and these programs target Casio’s built-in Python app. Treat it as out of scope.

## Testing without a calculator

Casio offers a PC emulator of the fx-CG100. I have not confirmed how it loads `.py` files, so check the emulator’s own help. For quick checks on a laptop, use the desktop stand-in described in the [README](../README.md#development-quick-start).

## Sources

* Casio, fx-CG100 user’s guide: [Connecting the Calculator to a Computer](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYeiiehand.html)
* Casio, fx-CG100 user’s guide: [Python App](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYlkjdoxxc.html)
* Casio, fx-CG100 user’s guide: [Memory App](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYacwdbyyk.html)
* Casio, fx-CG100 user’s guide: [Exam Mode App](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYaooxarfm.html)
* Casio Education, [FA-124 user’s guide](https://edu.casio.com/education/support_software/dl/PC_links/FA-124_E.pdf)
* HP Museum forum, [Python comes to the Casio fx-CG 50](https://www.hpmuseum.org/forum/post-106324.html) (community reports on USB mass storage, hidden file extensions and PythonExtra)

The Casio pages were read through search-engine extracts. The Casio site could not be opened directly from the environment this guide was written in, so check the wording against the pages themselves.
