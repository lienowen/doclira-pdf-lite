import sys
from pathlib import Path

import fitz
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from .pdf_ops import add_basic_watermark, delete_page, merge_pdfs, rotate_page, split_pdf


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.document = None
        self.setWindowTitle("Doclira PDF Lite")
        self.resize(1240, 800)
        self._build_toolbar()
        self._build_content()
        self.statusBar().showMessage("Open a PDF to preview and organize pages locally.")

    def _build_toolbar(self):
        toolbar = self.addToolBar("Document")
        toolbar.setMovable(False)
        for label, handler in [
            ("Open PDF", self.open_pdf),
            ("Merge", self.merge_files),
            ("Split", self.split_pages),
            ("Rotate Page", self.rotate_current),
            ("Delete Page", self.delete_current),
        ]:
            action = QAction(label, self)
            action.triggered.connect(handler)
            toolbar.addAction(action)

    def _build_content(self):
        splitter = QSplitter()
        self.pages = QListWidget()
        self.pages.setMinimumWidth(170)
        self.pages.currentRowChanged.connect(self.render_page)
        splitter.addWidget(self.pages)

        self.preview = QLabel("Open a PDF to begin", alignment=Qt.AlignCenter)
        self.preview.setStyleSheet("background: #eef2f6; color: #60728b; padding: 24px;")
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setWidget(self.preview)
        splitter.addWidget(self.preview_scroll)

        tools = QWidget()
        tools.setMinimumWidth(280)
        panel = QVBoxLayout(tools)
        title = QLabel("Basic Watermark")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        panel.addWidget(title)
        form = QFormLayout()
        self.watermark = QLineEdit("CONFIDENTIAL")
        self.opacity = QSlider(Qt.Horizontal)
        self.opacity.setRange(8, 65)
        self.opacity.setValue(22)
        form.addRow("Text", self.watermark)
        form.addRow("Opacity", self.opacity)
        panel.addLayout(form)
        apply_button = QPushButton("Save Watermarked Copy")
        apply_button.clicked.connect(self.watermark_copy)
        panel.addWidget(apply_button)
        notice = QLabel(
            "Lite includes a simple footer watermark for one PDF. "
            "Batch, tiled and logo watermarks are available in Doclira PDF Pro."
        )
        notice.setWordWrap(True)
        notice.setStyleSheet("color: #60728b; padding-top: 16px;")
        panel.addWidget(notice)
        website = QLabel('<a href="https://www.doclira.com/">Get Doclira PDF Pro</a>')
        website.setOpenExternalLinks(True)
        panel.addWidget(website)
        panel.addStretch()
        splitter.addWidget(tools)
        splitter.setSizes([180, 780, 300])
        self.setCentralWidget(splitter)

    def closeEvent(self, event):
        if self.document:
            self.document.close()
        event.accept()

    def require_document(self):
        if not self.path:
            QMessageBox.information(self, "Open PDF", "Please open a PDF first.")
            return False
        return True

    def open_pdf(self, path=None):
        if path is None or isinstance(path, bool):
            path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF files (*.pdf)")
        if not path:
            return
        if self.document:
            self.document.close()
        self.path = Path(path)
        self.document = fitz.open(self.path)
        self.pages.clear()
        self.pages.addItems([f"Page {number + 1}" for number in range(self.document.page_count)])
        self.pages.setCurrentRow(0)
        self.statusBar().showMessage(f"Opened {self.path.name} - {self.document.page_count} page(s)")

    def render_page(self, row):
        if not self.document or row < 0:
            return
        pixmap = self.document[row].get_pixmap(matrix=fitz.Matrix(1.45, 1.45), alpha=False)
        image = QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            QImage.Format_RGB888,
        ).copy()
        self.preview.setPixmap(QPixmap.fromImage(image))
        self.preview.adjustSize()

    def choose_output(self, suffix):
        suggested = self.path.with_name(f"{self.path.stem}_{suffix}.pdf")
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", str(suggested), "PDF files (*.pdf)")
        return path

    def merge_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Merge PDF Files", "", "PDF files (*.pdf)")
        if len(paths) < 2:
            return
        output, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "merged.pdf", "PDF files (*.pdf)")
        if output:
            self._run(lambda: merge_pdfs(paths, output), output, "PDF files merged.")

    def split_pages(self):
        if not self.require_document():
            return
        output_dir = QFileDialog.getExistingDirectory(self, "Choose Folder for Split Pages")
        if output_dir:
            try:
                outputs = split_pdf(self.path, output_dir)
                self.statusBar().showMessage(f"Created {len(outputs)} page PDF files.")
                QMessageBox.information(self, "Split Complete", f"Created {len(outputs)} PDF files.")
            except Exception as error:
                QMessageBox.critical(self, "Split Failed", str(error))

    def rotate_current(self):
        if not self.require_document():
            return
        output = self.choose_output("rotated")
        if output:
            row = self.pages.currentRow()
            self._run(lambda: rotate_page(self.path, output, row), output, "Rotated page saved.")

    def delete_current(self):
        if not self.require_document():
            return
        output = self.choose_output("page_removed")
        if output:
            row = self.pages.currentRow()
            self._run(lambda: delete_page(self.path, output, row), output, "Page removed in saved copy.")

    def watermark_copy(self):
        if not self.require_document():
            return
        output = self.choose_output("watermarked")
        if output:
            opacity = self.opacity.value() / 100
            self._run(
                lambda: add_basic_watermark(self.path, output, self.watermark.text(), opacity),
                output,
                "Watermarked copy saved.",
            )

    def _run(self, operation, output, success_message):
        try:
            operation()
            self.open_pdf(output)
            self.statusBar().showMessage(success_message)
        except Exception as error:
            QMessageBox.critical(self, "Operation Failed", str(error))


def main():
    application = QApplication(sys.argv)
    application.setApplicationName("Doclira PDF Lite")
    window = MainWindow()
    window.show()
    sys.exit(application.exec())

