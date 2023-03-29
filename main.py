import requests
from bs4 import BeautifulSoup

def get_api_token(username, password, api_key):
    url = "https://api.enabiz.gov.tr/oauth/token"
    headers = {"Authorization": f"Basic {api_key}"}
    data = {"grant_type": "password", "username": username, "password": password}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("API girişi başarısız oldu.")

token = get_api_token("KULLANICI_ADI","GİRİLEN_ŞİFRE", "API_ANAHTARI")

def get_appointments(token):
    url = "https://api.enabiz.gov.tr/randevu/api/appointments"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Randevular alınamadı.")

appointments = get_appointments(token)

def check_dentist_appointments(appointments):
    dentist_appointments = []
    for appointment in appointments:
        if "Diş Hekimi" in appointment["Doctor"]["Profession"]:
            dentist_appointments.append(appointment)

    return dentist_appointments

dentist_appointments = check_dentist_appointments(appointments)

if dentist_appointments:
    print("Dişçi randevularınız:")
    for appointment in dentist_appointments:
        print(f"{appointment['AppointmentDate']} - {appointment['Doctor']['FullName']}")
else:
    print("Dişçi randevunuz bulunmamaktadır.")

