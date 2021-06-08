from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from decouple import config
import firebase_admin
from firebase_admin import db
import json

asklepius_obj = firebase_admin.credentials.Certificate({
  "type": config('TYPE'),
  "project_id": config('PROJECT_ID'),
  "private_key_id": config('PROJECT_KEY_ID'),
  "private_key": config('PRIVATE_KEY').replace("\\n","\n"),
  "client_email": config('CLIENT_EMAIL'),
  "client_id": config('CLIENT_ID'),
  "auth_uri": config('AUTH_URI'),
  "token_uri": config('TOKEN_URI'),
  "auth_provider_x509_cert_url": config('AUTH_PROVIDER_URL'),
  "client_x509_cert_url": config('CLIENT_URL')
	})

default_app = firebase_admin.initialize_app(asklepius_obj, {
	'databaseURL' : config('DATABASE_URL')
})

ref = db.reference('users')

@login_required
def home(request, limit = -1):
	snapshot = ref.get()
	patient_data = dict()
	total_entries = 0
	result_found = False
	username = request.user.username

	if (request.method == 'POST'):
		for patient, patient_details in snapshot.items():
			if patient_details['regID'] == request.POST['id'] and patient_details['status'] == 'Pending':
				patient_data[patient] = patient_details
				result_found = True
			if patient_details['status'] == 'Pending':
				total_entries += 1
		limit = 1 if result_found else 0
	
	else:
		for patient, patient_details in snapshot.items():
			if patient_details['status'] == 'Pending':
				patient_data[patient] = patient_details
				total_entries += 1
		if limit == -1 or limit > total_entries:
			limit = total_entries
	return render(request, 'dashboard/home.html', {
			'patients_data' : patient_data,
			'username' : username,
			'total_entries' : total_entries,
			'limit' : limit
	})


def accepted(request, id, limit):
	if ref.child(id + '/status').get() == 'Pending':
		ref.child(id).update({'status' : 'Verified'})
	return HttpResponseRedirect(reverse('limiter', args = [limit]))


def rejected(request, id, limit):
	if ref.child(id + '/status').get() == 'Pending':
		ref.child(id).update({'status' : 'Rejected', 'rejectionReason' : request.POST['msg']})
	return HttpResponseRedirect(reverse('limiter', args = [limit]))