from flask import Flask, request, jsonify, render_template,session,abort, redirect
import cv2

"""para login"""
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
"""cierre"""