import os
from os import path
import sys
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor
from drivers import drivers, prefixes
from encoders import encoders
from util import calc_sha1, size_string, read_in_chunk, block_offset

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from UI import Ui_MainWindow

encoder = None
api = None
lock = threading.Lock()


def load_api_by_prefix(s):
    global api
    global encoder

    prefix = s.split('://')[0]
    if prefix not in prefixes:
        return False
    site = prefixes[prefix]
    api = drivers[site]
    encoder = encoders[site]
    return True


def fetch_meta(s):
    url = api.meta2real(s)
    if not url:
        return None
    full_meta = api.image_download(url)
    if not full_meta:
        return None
    meta_dict = json.loads(encoder.decode(full_meta).decode("utf-8"))
    return meta_dict


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    t = None
    push_message_signal = pyqtSignal(str)
    download_done_signal = pyqtSignal()

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()
        self.thread = 8
        self.force = True

    def set_download_path(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择下载路径", os.getcwd())
        self.lineEdit.setText(directory)

    def download_handle(self):
        self.progressBar.setValue(0)
        links = self.plainTextEdit.toPlainText()
        links = links.replace('\r\n', '\n').strip().split('\n')
        self.downloadStartButton.setEnabled(False)
        self.t = threading.Thread(target=self.download_handle_inner, args=(links,))
        self.t.start()

    def download_handle_inner(self, links):
        all = len(links)
        for i, link in enumerate(links):
            self.download_single_handle(link)
            self.progressBar.setValue((i+1)/all*100)
        self.download_done_signal.emit()

    def download_done(self):
        self.downloadStartButton.setEnabled(True)
        self.t = None

    def log(self, message):
        self.logText.appendPlainText(message)

    def ask_overwrite(self):
        answer = QtWidgets.QMessageBox.question(self, '确认', '文件已存在, 是否覆盖?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        return answer == QtWidgets.QMessageBox.Yes

    def tr_download(self, i, block_dict, f, offset):
        url = block_dict['url']
        for j in range(10):
            block = api.image_download(url)
            if not block:
                self.push_message_signal.emit(f"分块{i + 1}/{self.nblocks}第{j + 1}次下载失败")
                continue
            block = encoder.decode(block)
            if calc_sha1(block) == block_dict['sha1']:
                with lock:
                    f.seek(offset)
                    f.write(block)
                self.push_message_signal.emit(f"分块{i + 1}/{self.nblocks}下载完毕")
                return
            else:
                self.push_message_signal.emit(f"分块{i + 1}/{self.nblocks}校验未通过")
        self.succ = False

    def download_single_handle(self, meta):

        if not load_api_by_prefix(meta):
            self.push_message_signal.emit("元数据解析失败")
            return
        start_time = time.time()
        meta_dict = fetch_meta(meta)
        if not meta_dict:
            self.push_message_signal.emit("元数据解析失败")
            return

        file_name = path.join(self.lineEdit.text(), meta_dict['filename'])
        self.push_message_signal.emit(f"下载: {path.basename(file_name)} ({size_string(meta_dict['size'])}), 共有{len(meta_dict['block'])}个分块, 上传于{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(meta_dict['time']))}")

        if path.exists(file_name):
            if path.getsize(file_name) == meta_dict['size'] and calc_sha1(read_in_chunk(file_name)) == meta_dict['sha1']:
                self.push_message_signal.emit("文件已存在, 且与服务器端内容一致")
                return file_name
            if not self.force and not self.ask_overwrite():
                return

        self.push_message_signal.emit(f"线程数: {self.thread}")
        self.succ = True
        self.nblocks = len(meta_dict['block'])
        trpool = ThreadPoolExecutor(self.thread)
        hdls = []

        mode = "r+b" if path.exists(file_name) else "wb"
        with open(file_name, mode) as f:
            for i, block_dict in enumerate(meta_dict['block']):
                offset = block_offset(meta_dict, i)
                hdl = trpool.submit(self.tr_download, i, block_dict, f, offset)
                hdls.append(hdl)
            for h in hdls:
                h.result()
            if not self.succ:
                return
            f.truncate(meta_dict['size'])

        self.push_message_signal.emit(f"{path.basename(file_name)} ({size_string(meta_dict['size'])}) 下载完毕, 用时{time.time() - start_time:.1f}秒, 平均速度{size_string(meta_dict['size'] / (time.time() - start_time))}/s")
        sha1 = calc_sha1(read_in_chunk(file_name))
        if sha1 == meta_dict['sha1']:
            self.push_message_signal.emit("文件校验通过")
            return file_name
        else:
            self.push_message_signal.emit("文件校验未通过")
            return

    def initUI(self):
        self.lineEdit.setReadOnly(True)
        self.logText.setReadOnly(True)
        self.selectDirectoryButton.clicked.connect(self.set_download_path)
        self.downloadStartButton.clicked.connect(self.download_handle)
        self.clearInputButton.clicked.connect(self.plainTextEdit.clear)
        self.push_message_signal.connect(self.log)
        self.download_done_signal.connect(self.download_done)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
