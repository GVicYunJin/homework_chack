from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import os
import json
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)
app.secret_key = '123456'

# 数据文件路径
data_file = "class_data.json"
history_file = "history.json"

# 加载班级数据
def load_class_data():
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

# 保存班级数据
def save_class_data(class_data):
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(class_data, f, ensure_ascii=False, indent=4)

# 加载历史记录
def load_history():
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

# 保存历史记录
def save_history(history):
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# 条码生成
def generate_barcode(student_id, student_name):
    barcode_dir = "static/barcodes"
    if not os.path.exists(barcode_dir):
        os.makedirs(barcode_dir)

    ean = barcode.get('code128', str(student_id), writer=ImageWriter())
    filename = f"{barcode_dir}/{student_name}_{student_id}"
    ean.save(filename)
    filename += ".png"
    return filename

# Flask 路由
@app.route('/')
def index():
    class_data = load_class_data()
    barcodes = {}
    if class_data:
        for student_id, student_name in class_data.items():
            barcode_path = f"barcodes/{student_name}_{student_id}.png"
            barcodes[student_id] = barcode_path
    history = load_history()
    return render_template('index.html', class_data=class_data, barcodes=barcodes, history=history)

@app.route('/register', methods=['POST'])
def register():
    student_names = request.form['student_names'].strip()
    if student_names:
        students = student_names.splitlines()
        class_data = {str(i+1): name for i, name in enumerate(students)}
        save_class_data(class_data)

        # 自动为所有学生生成条码
        for student_id, student_name in class_data.items():
            generate_barcode(student_id, student_name)

        flash("班级成员注册成功并生成条码！", "success")
    else:
        flash("请输入班级成员姓名！", "error")
    return redirect(url_for('index'))

@app.route('/unregister', methods=['POST'])
def unregister():
    if os.path.exists(data_file):
        os.remove(data_file)
    if os.path.exists(history_file):
        os.remove(history_file)
    flash("班级数据已删除。", "success")
    return redirect(url_for('index'))

@app.route('/check_homework', methods=['POST'])
def check_homework():
    file = request.files['barcode_image']
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # 解码条码图片
        img = Image.open(file_path)
        barcodes = decode(img)

        if not barcodes:
            flash("未检测到任何条码！", "error")
        else:
            class_data = load_class_data()
            submitted_ids = [int(barcode_obj.data.decode('utf-8')) for barcode_obj in barcodes if barcode_obj.type == 'CODE128']
            missing_students = [name for student_id, name in class_data.items() if int(student_id) not in submitted_ids]

            if missing_students:
                missing_list = "\n".join(missing_students)
                flash(f"未交作业的学生：\n{missing_list}", "info")

                # 更新历史记录
                history = load_history()
                for student_name in missing_students:
                    if student_name in history:
                        history[student_name] += 1
                    else:
                        history[student_name] = 1
                save_history(history)
            else:
                flash("所有学生都已提交作业。", "success")
    else:
        flash("请上传条码图片！", "error")

    return redirect(url_for('index'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    if os.path.exists(history_file):
        os.remove(history_file)
    flash("历史记录已清空。", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('static/barcodes'):
        os.makedirs('static/barcodes')
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0', port=44441)