from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from decouple import config
import firebase_admin
from firebase_admin import db
import json

asklepius_obj = firebase_admin.credentials.Certificate(config('CERTIFICATE'))
default_app = firebase_admin.initialize_app(asklepius_obj, {
	'databaseURL' : config('DATABASE_URL')
})

ref = db.reference('users')

def home(request, limit = -1):
	snapshot = ref.get()
	patient_data = dict()
	total_entries = 0
	result_found = False
	username = request.user.username

	if (request.method == 'POST'):
		for patient, patient_details in snapshot.items():
			if patient_details['regID'] == request.POST(['id']):
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


def rejected(rejected, id, limit):
	if ref.child(id + '/status').get() == 'Pending':
		ref.child(id).update({'status' : 'Rejected'})
	return HttpResponseRedirect(reverse('limiter', args = [limit]))