#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from flask import Flask, request, render_template, url_for, redirect, jsonify
from search.web.run_server import app
from search.web.app.admin.models import *


