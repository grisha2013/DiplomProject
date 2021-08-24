

from flask import Flask, render_template, request
import paramiko
import time
import socket

app = Flask(__name__)

@app.route("/", methods=("GET","POST"))
def Router():
    if request.method == 'POST':
        if request.form.get("status") == 'Обновить статус':
            send_get_command("\r\n")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("index.html", texttohtml=texttohtml)
        elif request.form.get("status#") == 'Обновить статус':
            send_get_command("\n")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("enable.html", texttohtml=texttohtml)
        elif request.form.get("status_terminal") == 'Обновить статус':
            send_get_command("\n")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("Terminal.html", texttohtml=texttohtml)
        elif request.form.get("console_str") != None:
            command = request.form.get("console_str")
            text = send_get_command(command)
            text += send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("index.html", texttohtml=texttohtml)
        elif request.form.get("console_str#") != None:
            command = request.form.get("console_str#")
            text = send_get_command(command)
            text += send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("enable.html", texttohtml=texttohtml)
        elif request.form.get("console_str_terminal") != None:
            command = request.form.get("console_str_terminal")
            text = send_get_command(command)
            text += send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("Terminal.html", texttohtml=texttohtml)
        elif request.form.get("show") == 'Показ информации':
            return render_template("Show.html")
        elif request.form.get("show_run") == 'Текущая конфигурация':
            text = send_get_command("show run\n")
            for i in range(0, 6):
                text += send_get_command(" \n")
            texttohtml = text.split("\n")
            return render_template("enable.html", texttohtml=texttohtml)
        elif request.form.get("cancel_show") == 'Отмена':
            texttohtml = send_get_command("\n")
            texttohtml = texttohtml.split("\n")
            return render_template("enable.html", texttohtml=texttohtml)
        elif request.form.get("enable") == 'Вход в #':
            send_get_command("en")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("enable.html", texttohtml=texttohtml)
        elif request.form.get("copy_from_tftp") == "Загрузка конфига с TFTP сервера":
            send_get_command("copy tftp: st\n")
            return render_template("configfromtftp.html")
        elif request.form.get("apply") == "Отправить":
            ip = request.form.get("ip")
            file_name = request.form.get("file_name")
            send_get_command(ip + "\n")
            texttohtml = send_get_command(file_name + "\n")
            return render_template("enable.html", texttohtml=texttohtml)
        elif request.form.get("cancel") == "Отмена":
            texttohtml = send_get_command("\n")
            texttohtml = texttohtml.split("\n")
            return render_template("enable.html", texttohtml=texttohtml)
        elif request.form.get("exit") == 'Выход из #':
            send_get_command("exit\n")
            ssh.send("\r\n")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("index.html", texttohtml=texttohtml)
        elif request.form.get("terminal") == 'Терминал':
            send_get_command("conf t")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("Terminal.html", texttohtml=texttohtml)
        elif request.form.get("exit") == 'Выход из терминала':
            send_get_command("exit")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("enable.html", texttohtml=texttohtml)
        else:
            print ("Всё сломалось")
            text = send_get_command("\n")
            texttohtml = text.split("\n")
            return render_template("index.html", texttohtml=texttohtml)
    elif request.method == 'GET':
        text = ssh.recv(60000).decode("utf-8")
        texttohtml = text.split("\n")
        return render_template("index.html", texttohtml=texttohtml)
    else: return "Всё сломалось 2"

def send_get_command(
        command = '',
        pause = 1
):
    if command == "\r\n": ssh.send("\r\n")
    if command == " \n": command = ' '

    ssh.send(command)
    ssh.settimeout(pause)
    part = ""
    while True:
        try:
            inpart = ssh.recv(60000).decode("utf-8")
            part += inpart
        except socket.timeout:
            break
    command = command.replace('\n', '', 1)
    part = part.replace(command, '', 1)
    print(part, end='')
    return part

#main

cl = paramiko.SSHClient()
cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cl.connect(
    hostname="192.168.30.163",
    username="cisco",
    password="cisco",
    port=2502,
    look_for_keys=False,
    allow_agent=False
)
with cl.invoke_shell() as ssh:
    ssh.send("\r\n")
    time.sleep(1)
    app.run(debug=True)
