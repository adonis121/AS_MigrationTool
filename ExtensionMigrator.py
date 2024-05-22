import os
import json
import requests
import ssl
import tempfile
from OpenSSL import crypto
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

def invoke_cm2cloud_extensions(config_file=None, user_map_file=None, qlik_client=None):
    base_dir = os.getcwd()

    if config_file is None:
        config_file = Path(base_dir) / 'Config.json'

    if qlik_client is None:
        # Get the Qlik Client Certificate from the CurrentUser\My store
        x509_current_user = get_certificates(store_name="CurrentUser")
        x509_local_machine = get_certificates(store_name="LocalMachine")

        qlik_client_certificates = x509_current_user + x509_local_machine

        connected = False
        for cert in qlik_client_certificates:
            if not connected:
                try:
                    connect_qlik_sense(cert)
                    connected = True
                    qlik_client = cert
                except Exception as e:
                    pass

        if qlik_client is None:
            print('Error: Qlik Client Certificate must be accessible in CurrentUser Store, or provided when calling "invoke_cm2cloud_extensions"')
            return None

    # Connect to Qlik Sense SaaS
    config = import_cm2cloud_config_file(config_file)
    if config:
        tenant_admin_key = config.get('TenantAdminKey')
        tenant = config.get('Tenant')

    if not tenant_admin_key or not tenant:
        print('Warning: Provide a Tenant Config File or run: New-CM2CloudConfig')
        return None

    saas_session = new_qcloud_session(tenant, tenant_admin_key)

    # Connect to Qlik Sense CM
    try:
        qrs_client = connect_qlik_sense(qlik_client, return_client=True)
        wes = determine_wes_url(qrs_client)
    except Exception as e:
        print('Error: Unable to Connect to Qlik Sense CM')
        return None

    extensions = get_extensions(wes, qrs_client)
    wes_extensions = select_wes_extensions(extensions)
    selected_extensions = select_extensions_to_migrate(wes_extensions)

    for extension in selected_extensions:
        temp_file = Path(os.path.join(tempfile.gettempdir(), f"{extension['Name']}.zip"))
        download_extension(wes, extension['Name'], temp_file, qrs_client)
        publish_qcloud_extensions(saas_session, temp_file, extension['Name'])
        temp_file.unlink()

def get_certificates(store_name):
    # Implementation to get certificates from Windows Certificate Store
    pass

def connect_qlik_sense(cert, return_client=False):
    # Implementation to connect to Qlik Sense
    pass

def import_cm2cloud_config_file(config_file_path):
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)

def new_qcloud_session(tenant, tenant_admin_key):
    # Implementation to create a new Qlik Cloud session
    pass

def determine_wes_url(qrs_client):
    if qrs_client['URLQRS'].rindex(':') > 5:
        return f"https://{qrs_client['HostName']}:9080/v1/"
    else:
        return qrs_client['URLQRS'].rstrip('qrs') + 'api/wes/v1/'

def get_extensions(wes, qrs_client):
    response = requests.get(f"{wes}extensions/", verify=False, cert=(qrs_client['cert'], qrs_client['key']))
    return response.json()

def select_wes_extensions(extensions):
    wes_extensions = []
    for extension in extensions['data']:
        wes_extensions.append({
            'Display Name': extension.get('name'),
            'Version': extension.get('version'),
            'Type': extension.get('type'),
            'Name': extension.get('name')
        })
    return wes_extensions

def select_extensions_to_migrate(wes_extensions):
    # Create the Tkinter GUI
    root = tk.Tk()
    root.title("Select Extensions to Migrate")

    tree = ttk.Treeview(root, columns=("Display Name", "Version", "Type", "Name"), show='headings')
    tree.heading("Display Name", text="Display Name")
    tree.heading("Version", text="Version")
    tree.heading("Type", text="Type")
    tree.heading("Name", text="Name")
    tree.pack(fill=tk.BOTH, expand=True)

    for ext in wes_extensions:
        tree.insert("", "end", values=(ext["Display Name"], ext["Version"], ext["Type"], ext["Name"]))

    def on_select():
        selected_items = tree.selection()
        selected_extensions = []
        for item in selected_items:
            ext = tree.item(item, "values")
            selected_extensions.append({
                "Display Name": ext[0],
                "Version": ext[1],
                "Type": ext[2],
                "Name": ext[3]
            })
        root.destroy()
        return selected_extensions

    select_button = ttk.Button(root, text="Select", command=on_select)
    select_button.pack()

    root.mainloop()
    return on_select()

def download_extension(wes, extension_name, temp_file, qrs_client):
    url = f"{wes}extensions/export/{extension_name}"
    with requests.get(url, stream=True, verify=False, cert=(qrs_client['cert'], qrs_client['key'])) as r:
        r.raise_for_status()
        with open(temp_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def publish_qcloud_extensions(session, temp_file, name):
    # Implementation to publish Qlik Cloud extensions
    pass

# Sample usage
invoke_cm2cloud_extensions()
