import sys
import struct
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
    QLineEdit, QVBoxLayout, QWidget, QMessageBox
)
import tifffile

class DNGWhiteBalanceEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DNG White Balance Editor v0.3')
        self.setGeometry(300, 300, 400, 220)
        self.dng_path = None
        self.as_shot_neutral = [1.0, 1.0, 1.0]

        # UI elements
        self.open_btn = QPushButton('Open DNG')
        self.save_btn = QPushButton('Save Copy')
        self.r_edit = QLineEdit()
        self.g_edit = QLineEdit()
        self.b_edit = QLineEdit()
        self.info_label = QLabel('No file loaded.')

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.open_btn)
        layout.addWidget(QLabel('R (AsShotNeutral):'))
        layout.addWidget(self.r_edit)
        layout.addWidget(QLabel('G (AsShotNeutral):'))
        layout.addWidget(self.g_edit)
        layout.addWidget(QLabel('B (AsShotNeutral):'))
        layout.addWidget(self.b_edit)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.info_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect buttons
        self.open_btn.clicked.connect(self.open_dng)
        self.save_btn.clicked.connect(self.save_copy)

    def open_dng(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open DNG File', '', 'DNG files (*.dng)')
        if path:
            self.dng_path = path
            try:
                with tifffile.TiffFile(path) as tif:
                    tags = {tag.name: tag for tag in tif.pages[0].tags.values()}
                    tag = tags.get('AsShotNeutral', None)
                    if tag:
                        values = tag.value
                        if len(values) >= 6:
                            r = values[0] / values[1]
                            g = values[2] / values[3]
                            b = values[4] / values[5]
                            self.as_shot_neutral = [r, g, b]
                            self.r_edit.setText(f'{r:.6f}')
                            self.g_edit.setText(f'{g:.6f}')
                            self.b_edit.setText(f'{b:.6f}')
                            self.info_label.setText('Loaded successfully.')
                        else:
                            self.info_label.setText('Invalid AsShotNeutral tag.')
                    else:
                        self.info_label.setText('AsShotNeutral not found.')
            except Exception as e:
                QMessageBox.critical(self, 'Error loading DNG', str(e))

    def save_copy(self):
        if not self.dng_path:
            QMessageBox.warning(self, 'Warning', 'No DNG loaded.')
            return
        
        try:
            # Read new values
            r = float(self.r_edit.text())
            g = float(self.g_edit.text())
            b = float(self.b_edit.text())

            denominator = 32768  # High precision denominator
            numerator_r = int(round(r * denominator))
            numerator_g = int(round(g * denominator))
            numerator_b = int(round(b * denominator))

            new_neutral = (
                numerator_r, denominator,
                numerator_g, denominator,
                numerator_b, denominator
            )

            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Edited DNG', '', 'DNG files (*.dng)')
            if save_path:
                with tifffile.TiffFile(self.dng_path) as tif:
                    page = tif.pages[0]
                    tag = page.tags.get('AsShotNeutral')

                    if not tag:
                        QMessageBox.warning(self, 'Warning', 'AsShotNeutral tag not found in file.')
                        return

                    offset = tag.valueoffset

                # Read entire file
                with open(self.dng_path, 'rb') as f:
                    data = bytearray(f.read())

                # Patch AsShotNeutral values at offset
                for i, val in enumerate(new_neutral):
                    struct.pack_into('<I', data, offset + i*4, val)


                # Save new file
                with open(save_path, 'wb') as f:
                    f.write(data)

                QMessageBox.information(self, 'Success', 'Edited DNG saved successfully.')

        except Exception as e:
            QMessageBox.critical(self, 'Error saving DNG', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = DNGWhiteBalanceEditor()
    editor.show()
    sys.exit(app.exec_())
