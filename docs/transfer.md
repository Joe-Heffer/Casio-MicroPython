# Copying programs to the calculator

The fx-CG100 connects to a computer over USB and appears as a USB drive. This guide follows Casio’s fx-CG100 user’s guide. Links to the relevant pages are at the end.

## Steps

1. Connect the calculator to the computer with a USB data cable.
2. The calculator shows a **Select Connection Mode** dialogue. Choose **USB Flash** and confirm.
3. The calculator’s storage memory appears on the computer as a drive.
4. Copy the program’s `.py` file (for example `programs/mandelbrot/mandelbrot.py`) onto the drive. Only the `.py` file is needed. The README and screenshots stay on your computer.
5. Eject the drive in your operating system before you unplug the cable.
6. On the calculator, open the **Python** app. The file appears in its file list. Select it and run it.

## Things to watch for

* **Copying can be slow to start.** Casio’s guide says that copying to the calculator can take several minutes to begin while storage memory is optimised.
* **Sleep and standby.** The connection can drop if the computer goes to sleep or standby during a transfer.
* **ASCII only.** The Python app cannot show files saved with characters outside ASCII. Such a file opens as blank or garbled text. `tools/check_programs.py` checks for this.
* **Line endings.** Casio’s guide advises changing newline codes to suit the target environment when moving `.py` files between the calculator and a computer. If a file looks wrong in a desktop editor after you copy it back, convert its line endings.
* **Exam Mode.** If the calculator is in Exam Mode, the connection dialogue offers **USB Flash / Unlock Exam Mode** instead. Ending that connection restarts the calculator.

## Testing without a calculator

Casio offers a PC emulator of the fx-CG100. I have not confirmed how it loads `.py` files, so check the emulator’s own help. For quick checks on a laptop, use the desktop stand-in described in the [README](../README.md#development-quick-start).

## Sources

* Casio, fx-CG100 user’s guide: [Connecting the Calculator to a Computer](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYeiiehand.html)
* Casio, fx-CG100 user’s guide: [Python App](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYlkjdoxxc.html)
* Casio, fx-CG100 user’s guide: [Exam Mode App](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYaooxarfm.html)

These pages were read through search-engine extracts. The Casio site could not be opened directly when this guide was written, so check the wording against the pages themselves.
