#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from flask import Flask, request, render_template, url_for, redirect, jsonify
from search.web.app import app
from search.web.apps.admin.models import *


