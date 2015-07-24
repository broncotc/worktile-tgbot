# encoding: UTF-8
from __future__ import unicode_literals
from flask import Flask, request
from commandParser import *
import requests
import pickledb
import commandHandler
import apiCommander

global token
token = "96054818:AAFiPFHafymEzsJx67ftJ0XFKe5pwlRKF3E"
app = Flask(__name__)
db = pickledb.load("worktilebot.db", True)


@app.before_first_request
def setWebhook():
	requests.get(
		"https://api.telegram.org/bot" + token + "/setWebhook?url=https://broncotc.com:8443/bot/webhook" + token)


@app.route('/bot/webhook' + token, methods=["POST"])
def telegramWebhookHandler():
	if request.method == "POST":
		incoming = request.get_json()
		print incoming
		chat_id = incoming['message']['chat']['id']
		msg = incoming['message']['text']
		user_id = incoming['message']['from']['id']
		commandContent = commandParser(msg)
		apiCommander.commandRouter(commandContent, user_id, chat_id)
		return '{"status":"ok"}'


@app.route('/bot/worktileOauth')
def oauthHandler():
	user_id = request.args["state"]
	oauthToken = request.args["code"]
	db.set(str(user_id) + "_worktileToken", oauthToken)
	return '<h3>您已成功授权此Bot访问您的Worktile账户</h3>'


if __name__ == '__main__':
	sslcontext = ('all.crt', 'all.key')
	app.run(host="0.0.0.0", port=8443, ssl_context=sslcontext)
