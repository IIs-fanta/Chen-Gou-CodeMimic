import sys
import time
import random
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox, 
    QSpinBox, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, 
    QProgressBar, QTextEdit, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextCharFormat

class LogGenerator(QThread):
    new_log = pyqtSignal(str, str)  # (text, color: 'normal', 'error', 'success', 'progress')
    module_change = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, duration):
        super().__init__()
        self.duration = duration  # seconds
        self.running = True
        self.start_time = None
    
    def run(self):
        self.start_time = time.time()
        
        # 预定义的代码和日志片段
        code_snippets = {
            'compilation': [
                'gcc -O2 -c main.c',
                'In file included from main.c:5:',
                'header.h:12: warning: implicit declaration of function',
                'Linking object files...',
                'Creating executable: output.exe',
                'ld: warning: -z relro reduced flexibility',
                '[=====>                      ] 28% Compiling core modules...',
                '[===========>                ] 45% Optimizing memory access...'
            ],
            'model_training': [
                'Epoch 1/100',
                '500/500 [==============================] - 15s 30ms/step - loss: 0.4523 - accuracy: 0.8234',
                'Epoch 2/100',
                '500/500 [==============================] - 14s 28ms/step - loss: 0.3215 - accuracy: 0.8765',
                'Optimizer: Adam learning rate: 0.001',
                'Layers: 4 Hidden units: 256, 128, 64, 32',
                'Processing... █████░░░░░ 32% - Batch normalization applied',
                'Checkpoint saved at epoch 5'
            ],
            'data_mining': [
                'Loading dataset: 1,234,567 records',
                'Extracting features from raw data...',
                'Applying dimensionality reduction (PCA)...',
                'Clustering with K-means: K=8',
                'Calculating information entropy...',
                'Correlation matrix computed: 0.879',
                '[=================>          ] 65% - Pattern recognition in progress',
                'Found 15 anomalies in the dataset'
            ],
            'system_optimization': [
                'Scanning system files...',
                'Defragmenting memory allocation tables',
                'Optimizing kernel parameters...',
                'Adjusting CPU scheduling priorities',
                'Updating system cache policies',
                'Benchmark results: 12754 IOPS',
                'Performance improved by 15.3%',
                '[============================> ] 92% - Finalizing system configurations'
            ],
            'model_initialization': [
                'Importing TensorFlow/PyTorch modules',
                'Defining model architecture...',
                'Setting up loss functions and metrics',
                'Configuring callbacks: EarlyStopping, ModelCheckpoint',
                'Preparing dataset for training',
                'Initializing weights with Xavier uniform distribution',
                'Building computation graph...',
                'Model summary: 2,567,890 parameters'
            ],
            'flux_model_repair': [
                'Self-check protocol initiated',
                'Scanning model components...',
                'Error detected in attention mechanism',
                'Initiating auto-repair sequence',
                'Reconstructing model layers 3-7',
                'Validating model integrity...',
                'Repair progress: █████████░░ 75%',
                'Attention mechanism restored successfully'
            ],
            'errors': [
                'ERROR: Memory allocation failed in layer 4',
                'WARNING: Training loss increased unexpectedly',
                'CRITICAL: Connection timeout with data server',
                'ERROR: CUDA out of memory. Trying to reduce batch size...',
                'WARNING: NAN values detected in gradient',
                'ERROR: File not found: weights.h5'
            ],
            'fixes': [
                'Applying workaround: Memory fragmentation reduced',
                'Solution: Adjusting learning rate scheduler',
                'Retrying connection with backup server...',
                'Successfully reduced batch size to 16',
                'Gradient clipping applied to prevent NAN values',
                'Loading weights from backup file: weights_bak.h5',
                'Fix applied successfully!',
                'System recovered from critical error'
            ],
            'progress': [
                '[=                     ] 5%',
                '[====                  ] 20%',
                '[==========            ] 40%',
                '[==============        ] 60%',
                '[====================  ] 85%',
                '[======================] 100%',
                'Processing... ██░░░░░░░░░░░ 15%',
                'Processing... ██████░░░░░░░ 35%',
                'Processing... ██████████░░░ 65%',
                'Processing... █████████████ 100%'
            ]
        }
        
        modules = [
            'Neural Network Optimization',
            'Data Preprocessing Pipeline',
            'Feature Engineering',
            'Hyperparameter Tuning',
            'Cross-Validation',
            'Model Ensemble',
            'Performance Benchmarking',
            'System Integration'
        ]
        
        # 根据当前模式选择主要的日志类型
        current_time = time.time()
        while self.running and (current_time - self.start_time) < self.duration:
            current_time = time.time()
            
            # 随机决定当前的行动
            action = random.random()
            
            if action < 0.03:  # 3% 概率切换模块
                module = random.choice(modules)
                self.module_change.emit(module)
                time.sleep(0.5)
            elif action < 0.08:  # 5% 概率显示错误
                error = random.choice(code_snippets['errors'])
                self.new_log.emit(error, 'error')
                # 通常错误后会有修复
                time.sleep(random.uniform(0.5, 1.5))
                fix = random.choice(code_snippets['fixes'])
                self.new_log.emit(fix, 'success')
            elif action < 0.15:  # 7% 概率显示进度
                progress = random.choice(code_snippets['progress'])
                self.new_log.emit(progress, 'progress')
            else:  # 80% 概率显示正常日志
                log_type = random.choice(['compilation', 'model_training', 'data_mining', 
                                        'system_optimization', 'model_initialization', 'flux_model_repair'])
                log = random.choice(code_snippets[log_type])
                self.new_log.emit(log, 'normal')
            
            # 随机的滚动速度
            sleep_time = random.choice([
                0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0
            ])
            time.sleep(sleep_time)
            
        self.finished.emit()
    
    def stop(self):
        self.running = False
        self.wait()

class ProgressManager(QThread):
    progress_update = pyqtSignal(int, int, int)  # (main_progress, secondary1_progress, secondary2_progress)
    time_update = pyqtSignal(str, str)  # (elapsed_time, remaining_time)
    finished = pyqtSignal()
    
    def __init__(self, duration):
        super().__init__()
        self.duration = duration  # seconds
        self.running = True
        self.start_time = None
        # 随机生成其他两个进度条的目标时间（在0.5T到1.5T之间）
        self.secondary1_time = duration * random.uniform(0.5, 1.5)
        self.secondary2_time = duration * random.uniform(0.5, 1.5)
    
    def run(self):
        self.start_time = time.time()
        
        # 随机生成一些卡顿点
        slowdown_points1 = sorted([random.uniform(0.1, 0.9) for _ in range(3)])
        slowdown_points2 = sorted([random.uniform(0.1, 0.9) for _ in range(3)])
        
        current_time = time.time()
        while self.running and (current_time - self.start_time) < self.duration:
            current_time = time.time()
            elapsed = current_time - self.start_time
            
            # 计算主进度（线性的）
            main_progress = min(100, int((elapsed / self.duration) * 100))
            
            # 计算次要进度1（有卡顿效果）
            secondary1_elapsed = elapsed
            # 模拟卡顿效果
            for point in slowdown_points1:
                if main_progress > point * 100:
                    slowdown_factor = random.uniform(0.1, 0.3)
                    secondary1_elapsed += slowdown_factor * self.duration * 0.1
            secondary1_progress = min(100, int((secondary1_elapsed / self.secondary1_time) * 100))
            
            # 计算次要进度2（有卡顿效果）
            secondary2_elapsed = elapsed
            for point in slowdown_points2:
                if main_progress > point * 100:
                    slowdown_factor = random.uniform(0.1, 0.3)
                    secondary2_elapsed += slowdown_factor * self.duration * 0.1
            secondary2_progress = min(100, int((secondary2_elapsed / self.secondary2_time) * 100))
            
            # 模拟卡在99%的效果
            if main_progress == 99 and secondary1_progress == 99:
                secondary1_progress = 99
            elif main_progress == 99 and secondary2_progress == 99:
                secondary2_progress = 99
            
            # 更新进度
            self.progress_update.emit(main_progress, secondary1_progress, secondary2_progress)
            
            # 计算时间
            elapsed_time = self.format_time(elapsed)
            remaining = max(0, self.duration - elapsed)
            remaining_time = self.format_time(remaining)
            self.time_update.emit(elapsed_time, remaining_time)
            
            time.sleep(0.1)  # 更新频率
            current_time = time.time()
        
        # 确保最终都到达100%
        self.progress_update.emit(100, 100, 100)
        elapsed = time.time() - self.start_time
        elapsed_time = self.format_time(elapsed)
        self.time_update.emit(elapsed_time, '00:00:00')
        self.finished.emit()
    
    def format_time(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    
    def stop(self):
        self.running = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self, mode, duration, show_time_in_progress, show_status_bar):
        super().__init__()
        self.mode = mode
        self.duration = duration
        self.show_time_in_progress = show_time_in_progress
        self.show_status_bar = show_status_bar
        self.elapsed_time = '00:00:00'
        self.remaining_time = self.format_time(duration)
        self.expected_completion = ''
        
        # 如果模式包含时间占位符，替换为预计完成时间
        if '预计XX:XX:XX完成' in mode:
            completion_time = time.time() + duration
            self.expected_completion = time.strftime('%H:%M:%S', time.localtime(completion_time))
            self.mode = mode.replace('XX:XX:XX', self.expected_completion)
        
        self.init_ui()
        self.start_simulation()
    
    def init_ui(self):
        # 设置窗口属性 - 添加最大化最小化按钮
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('陈狗模型检测代码执行器')
        self.setGeometry(300, 300, 800, 600)
        
        # 设置黑色主题
        self.setStyleSheet('background-color: #000000;')
        
        # 主布局
        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: #000000;')
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # 模式标题
        self.mode_label = QLabel(self.mode)
        self.mode_label.setFont(QFont('SimHei', 16, QFont.Bold))
        self.mode_label.setStyleSheet('color: #FF4500; background-color: #000000; padding: 10px;')
        self.mode_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.mode_label)
        
        # 代码显示区域
        self.code_text = QTextEdit()
        self.code_text.setReadOnly(True)
        self.code_text.setStyleSheet('background-color: #000000; color: #00FF00; font-family: Consolas, Courier New; font-size: 10pt;')
        main_layout.addWidget(self.code_text)
        
        # 进度条区域
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(10, 10, 10, 10)
        
        # 进度条1（主进度条）
        self.main_progress = QProgressBar()
        self.main_progress.setRange(0, 100)
        self.main_progress.setValue(0)
        # 设置进度条样式 - 黑色背景下更明显
        self.main_progress.setStyleSheet(
            "QProgressBar { " 
            "    border: 2px solid #333333; " 
            "    border-radius: 5px; " 
            "    background-color: #000000; " 
            "    text-align: center; " 
            "    color: #FFFFFF; " 
            " } " 
            "QProgressBar::chunk { " 
            "    background-color: #00FF00; " 
            "    border-radius: 3px; " 
            " }"
        )
        self.main_progress_label = QLabel('模型训练进度')
        self.main_progress_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        self.main_progress_layout = QHBoxLayout()
        self.main_progress_layout.addWidget(self.main_progress_label, 1)
        if self.show_time_in_progress:
            self.main_progress_time = QLabel(f'剩余: {self.remaining_time}')
            self.main_progress_time.setStyleSheet('color: #FFFFFF; background-color: #000000;')
            self.main_progress_layout.addWidget(self.main_progress_time)
        self.main_progress_layout.addWidget(self.main_progress, 3)
        progress_layout.addLayout(self.main_progress_layout)
        
        # 进度条2
        self.secondary1_progress = QProgressBar()
        self.secondary1_progress.setRange(0, 100)
        self.secondary1_progress.setValue(0)
        # 设置进度条样式
        self.secondary1_progress.setStyleSheet(
            "QProgressBar { " 
            "    border: 2px solid #333333; " 
            "    border-radius: 5px; " 
            "    background-color: #000000; " 
            "    text-align: center; " 
            "    color: #FFFFFF; " 
            " } " 
            "QProgressBar::chunk { " 
            "    background-color: #0099FF; " 
            "    border-radius: 3px; " 
            " }"
        )
        self.secondary1_label = QLabel('数据加载进度')
        self.secondary1_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        self.secondary1_layout = QHBoxLayout()
        self.secondary1_layout.addWidget(self.secondary1_label, 1)
        self.secondary1_layout.addWidget(self.secondary1_progress, 3)
        progress_layout.addLayout(self.secondary1_layout)
        
        # 进度条3
        self.secondary2_progress = QProgressBar()
        self.secondary2_progress.setRange(0, 100)
        self.secondary2_progress.setValue(0)
        # 设置进度条样式
        self.secondary2_progress.setStyleSheet(
            "QProgressBar { " 
            "    border: 2px solid #333333; " 
            "    border-radius: 5px; " 
            "    background-color: #000000; " 
            "    text-align: center; " 
            "    color: #FFFFFF; " 
            " } " 
            "QProgressBar::chunk { " 
            "    background-color: #FF00FF; " 
            "    border-radius: 3px; " 
            " }"
        )
        self.secondary2_label = QLabel('内存分配进度')
        self.secondary2_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        self.secondary2_layout = QHBoxLayout()
        self.secondary2_layout.addWidget(self.secondary2_label, 1)
        self.secondary2_layout.addWidget(self.secondary2_progress, 3)
        progress_layout.addLayout(self.secondary2_layout)
        
        main_layout.addLayout(progress_layout)
        
        # 状态栏
        if self.show_status_bar:
            self.status_label = QLabel(f'已运行: {self.elapsed_time} / 剩余: {self.remaining_time} / 预计完成: {self.expected_completion}')
            self.status_label.setStyleSheet('background-color: #000000; color: #CCCCCC; padding: 5px;')
            main_layout.addWidget(self.status_label)
    
    def start_simulation(self):
        # 启动日志生成线程
        self.log_generator = LogGenerator(self.duration)
        self.log_generator.new_log.connect(self.append_log)
        self.log_generator.module_change.connect(self.change_module)
        self.log_generator.finished.connect(self.simulation_finished)
        self.log_generator.start()
        
        # 启动进度管理线程
        self.progress_manager = ProgressManager(self.duration)
        self.progress_manager.progress_update.connect(self.update_progress)
        self.progress_manager.time_update.connect(self.update_time)
        self.progress_manager.finished.connect(self.simulation_finished)
        self.progress_manager.start()
    
    def append_log(self, text, color_type):
        # 设置文本颜色
        format = QTextCharFormat()
        if color_type == 'error':
            format.setForeground(QColor('#FF0000'))
        elif color_type == 'success':
            format.setForeground(QColor('#00FF00'))
        elif color_type == 'progress':
            format.setForeground(QColor('#FFFF00'))
        else:
            format.setForeground(QColor('#00FF00'))
        
        # 追加文本
        cursor = self.code_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text + '\n', format)
        self.code_text.setTextCursor(cursor)
        self.code_text.ensureCursorVisible()
    
    def change_module(self, module_name):
        # 插入模块分隔符
        separator = f'\n----- Starting Module: {module_name} -----\n'
        format = QTextCharFormat()
        format.setForeground(QColor('#00FFFF'))
        format.setFontWeight(QFont.Bold)
        
        cursor = self.code_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(separator, format)
        self.code_text.setTextCursor(cursor)
        self.code_text.ensureCursorVisible()
    
    def update_progress(self, main_val, secondary1_val, secondary2_val):
        self.main_progress.setValue(main_val)
        self.secondary1_progress.setValue(secondary1_val)
        self.secondary2_progress.setValue(secondary2_val)
        
        # 随机更新进度条标签
        if random.random() < 0.01:  # 1%概率更新标签
            labels = ['编译进度', '模型收敛度', '数据加载', '内存分配', '校验和计算']
            self.main_progress_label.setText(random.choice(labels))
            self.secondary1_label.setText(random.choice(labels))
            self.secondary2_label.setText(random.choice(labels))
    
    def update_time(self, elapsed, remaining):
        self.elapsed_time = elapsed
        self.remaining_time = remaining
        
        # 更新进度条上的时间
        if self.show_time_in_progress:
            self.main_progress_time.setText(f'剩余: {remaining}')
        
        # 更新状态栏
        if self.show_status_bar:
            self.status_label.setText(f'已运行: {elapsed} / 剩余: {remaining} / 预计完成: {self.expected_completion}')
        
        # 更新模式标题中的时间
        if '预计' in self.mode and ':' in self.mode:
            # 重新计算预计完成时间
            completion_time = time.time() + int(self.duration)
            self.expected_completion = time.strftime('%H:%M:%S', time.localtime(completion_time))
            # 假设模式字符串格式是固定的，我们需要重新构建它
            parts = self.mode.split('预计')
            if len(parts) > 1:
                time_part = parts[1].split('完成')[0]
                new_mode = self.mode.replace(f'预计{time_part}完成', f'预计{self.expected_completion}完成')
                self.mode_label.setText(new_mode)
    
    def simulation_finished(self):
        # 任务完成后，更改标题并显示完成消息
        self.mode_label.setText('任务执行完毕！')
        self.mode_label.setStyleSheet('color: #00FF00; background-color: #1E1E1E; padding: 10px;')
        
        # 追加完成日志
        self.append_log('\n========================================', 'progress')
        self.append_log('任务执行完毕！系统已恢复正常状态。', 'success')
        self.append_log('所有模块已成功完成。', 'success')
        self.append_log('========================================\n', 'progress')
        
        # 3秒后自动关闭窗口
        QTimer.singleShot(3000, self.close)
    
    def format_time(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    
    def closeEvent(self, event):
        # 停止线程
        if hasattr(self, 'log_generator') and self.log_generator.isRunning():
            self.log_generator.stop()
        if hasattr(self, 'progress_manager') and self.progress_manager.isRunning():
            self.progress_manager.stop()
        event.accept()

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle('陈狗模型检测代码执行器')
        self.setGeometry(400, 300, 500, 400)
        
        # 设置黑色主题
        self.setStyleSheet('background-color: #000000;')
        
        # 主布局
        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: #000000;')
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setCentralWidget(central_widget)
        
        # 模式选择
        mode_label = QLabel('选择执行模式：')
        mode_label.setFont(QFont('SimHei', 12))
        mode_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        main_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            '正在编译中，请勿关闭窗口',
            '正在训练模型，预计XX:XX:XX完成',
            '深度数据挖掘中，请勿触碰输入设备',
            '系统内核优化进行时，避免移动鼠标',
            '模型定义构建初始化中...',
            '检测到FLUX大模型损坏，自检协议运行中..请勿触碰输入设备。'
        ])
        self.mode_combo.setFont(QFont('SimHei', 10))
        self.mode_combo.setStyleSheet(
            "QComboBox {" 
            "    background-color: #000000;" 
            "    color: #FFFFFF;" 
            "    border: 2px solid #333333;" 
            "    border-radius: 5px;" 
            "    padding: 5px;" 
            "}" 
            "QComboBox::drop-down {" 
            "    border-left: 2px solid #333333;" 
            "    background-color: #111111;" 
            "}" 
            "QComboBox QAbstractItemView {" 
            "    background-color: #000000;" 
            "    color: #FFFFFF;" 
            "    border: 2px solid #333333;" 
            "}"
        )
        main_layout.addWidget(self.mode_combo)
        
        # 持续时间设置
        time_label = QLabel('执行时间（分钟）：')
        time_label.setFont(QFont('SimHei', 12))
        time_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        main_layout.addWidget(time_label)
        
        time_layout = QHBoxLayout()
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(1, 60)
        self.minutes_spin.setValue(5)
        self.minutes_spin.setFont(QFont('SimHei', 10))
        self.minutes_spin.setStyleSheet(
            "QSpinBox {" 
            "    background-color: #000000;" 
            "    color: #FFFFFF;" 
            "    border: 2px solid #333333;" 
            "    border-radius: 5px;" 
            "    padding: 5px;" 
            "}"
        )
        minutes_label = QLabel('分钟')
        minutes_label.setFont(QFont('SimHei', 10))
        minutes_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        self.seconds_spin.setValue(0)
        self.seconds_spin.setFont(QFont('SimHei', 10))
        self.seconds_spin.setStyleSheet(
            "QSpinBox {" 
            "    background-color: #000000;" 
            "    color: #FFFFFF;" 
            "    border: 2px solid #333333;" 
            "    border-radius: 5px;" 
            "    padding: 5px;" 
            "}"
        )
        seconds_label = QLabel('秒')
        seconds_label.setFont(QFont('SimHei', 10))
        seconds_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        
        time_layout.addWidget(self.minutes_spin)
        time_layout.addWidget(minutes_label)
        time_layout.addWidget(self.seconds_spin)
        time_layout.addWidget(seconds_label)
        main_layout.addLayout(time_layout)
        
        # 时间显示选项
        options_label = QLabel('时间显示选项：')
        options_label.setFont(QFont('SimHei', 12))
        options_label.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        main_layout.addWidget(options_label)
        
        self.show_time_in_progress = QCheckBox('在进度条上显示剩余时间')
        self.show_time_in_progress.setChecked(True)
        self.show_time_in_progress.setFont(QFont('SimHei', 10))
        self.show_time_in_progress.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        main_layout.addWidget(self.show_time_in_progress)
        
        self.show_status_bar = QCheckBox('在状态栏显示详细时间信息')
        self.show_status_bar.setChecked(True)
        self.show_status_bar.setFont(QFont('SimHei', 10))
        self.show_status_bar.setStyleSheet('color: #FFFFFF; background-color: #000000;')
        main_layout.addWidget(self.show_status_bar)
        
        # 执行按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton('开始执行')
        self.start_button.setFont(QFont('SimHei', 14, QFont.Bold))
        self.start_button.setStyleSheet(
            "QPushButton {" 
            "    background-color: #4CAF50;" 
            "    color: white;" 
            "    padding: 10px;" 
            "    border-radius: 5px;" 
            "    border: none;" 
            "}" 
            "QPushButton:hover {" 
            "    background-color: #45a049;" 
            "}" 
            "QPushButton:pressed {" 
            "    background-color: #3d8b40;" 
            "}"
        )
        self.start_button.clicked.connect(self.start_execution)
        button_layout.addWidget(self.start_button)
        main_layout.addLayout(button_layout)
    
    def start_execution(self):
        # 获取用户选择的选项
        mode = self.mode_combo.currentText()
        minutes = self.minutes_spin.value()
        seconds = self.seconds_spin.value()
        duration = minutes * 60 + seconds
        show_time_in_progress = self.show_time_in_progress.isChecked()
        show_status_bar = self.show_status_bar.isChecked()
        
        # 隐藏配置窗口并显示执行窗口
        self.hide()
        
        # 创建并显示主执行窗口
        self.main_window = MainWindow(mode, duration, show_time_in_progress, show_status_bar)
        self.main_window.show()
        self.main_window.closeEvent = self.on_main_window_closed
    
    def on_main_window_closed(self, event):
        # 当主窗口关闭时，重新显示配置窗口
        self.show()
        event.accept()

if __name__ == '__main__':
    # 确保中文显示正常
    import os
    os.environ['QT_FONT_DPI'] = '96'
    
    app = QApplication(sys.argv)
    config_window = ConfigWindow()
    config_window.show()
    sys.exit(app.exec_())