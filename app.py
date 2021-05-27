import streamlit as st
from pdf2image import convert_from_path

import requests
import time
import json
import pandas as pd
import os

from collections import namedtuple
import warnings

analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')

items = ['abn_number', 'account_number', 'bill_to_address', 'bill_to_name', 'bill_to_vat_number', 'card_number',
         'cashback', 'category', 'currency_code', 'date', 'delivery_date', 'discount', 'document_ref',
         'due_date', 'img_file_name', 'img_thumbnail', 'img_url', 'insurance', 'invoice_number', 'is_duplicate',
         'description', 'order', 'quantity', 'reference', 'section', 'sku', 'tax', 'tax_rate', 'total', 'type',
         'unit_of_measure',
         'ocr_text', 'order_date', 'payment_disp', 'payment_terms', 'payment_type', 'phone_number', 'purchase_order',
         'rounding',
         'service_end_date', 'service_start_date', 'ship_date', 'ship_to_address', 'ship_to_name', 'shipping',
         'store_number', 'subtotal', 'tax_lines', 'tip', 'total_weight',
         'tracking_number', 'vat_number', 'address', 'email', 'fax_number', 'name', 'raw_name', 'vendor_logo',
         'vendor_reg', 'vendor_type', 'web',
         'vendor_account', 'vendor_bank', 'vendor_bank_number', 'vendor_bank_swift', 'vendor_iban']
CLIENT_ID = "vrfncE0Py8CCX8fzP5CoClKhOvVhngBcsvncwfh"
ENVIRONMENT_URL = "api.veryfi.com"
username = "contact.neurodata"
api_key = "501237936122316437457a0df27a20e9"
process_file_url = 'https://{0}/api/v7/partner/documents/'.format(ENVIRONMENT_URL)
headers = {
    "Accept": "application/json",
    "CLIENT-ID": CLIENT_ID,
    "AUTHORIZATION": "apikey {0}:{1}".format(username, api_key)
}

url = 'https://app.nanonets.com/api/v2/OCR/Model/54ead1ca-698f-4e41-92c2-7cbde54f7e3b/LabelFile/'

st.set_page_config(
    page_title="NeuroData Extractor Demo", layout="wide", page_icon="./images/logo.png"
)

st.title("NeuroData Extractor Demo")
st.subheader("")
c = st.beta_columns(9)
a = c[0].checkbox("select all")

st.markdown("---")


st.sidebar.image("images/logo.png", width=120)
st.sidebar.title("PDF Scraper For Businesses")
st.sidebar.image(r"images/extractor.gif")
st.sidebar.title("Reduce your manual data entry costs")
st.sidebar.image(r"images/ocr_illustration.gif")

img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "pdf"])

tic = time.time()
if img_file_buffer is not None:
    file_details = {"FileName": img_file_buffer.name, "FileType": img_file_buffer.type}

    with open(os.path.join("tempDir", img_file_buffer.name), "wb") as f:
        f.write(img_file_buffer.getbuffer())
    st.success("Saved File")
    st.markdown("---")
    # Store Pdf with convert_from_path function
    fn = "./tempDir/" + img_file_buffer.name

    os.system('convert ' +
              '-density 300 ' +
              '%s ' % fn +
              '-quality 100 ' +
              '-flatten ' +
              '%s' % fn.replace('.pdf', '.jpg'))
    

    image_path = "tempDir/" + img_file_buffer.name.split(".")[0] + '.jpg'
    file_name = img_file_buffer.name.split(".")[0] + '.jpg'

    if st.button("Process Your Invoices"):
        # You can send the list of categories that is relevant to your case
        # Veryfi will try to choose the best one that fits this document
        categories = ["Office Expense", "Meals & Entertainment", "Utilities", "Automobile"]
        payload = {
            'file_name': file_name,
            'categories': categories
        }
        files = {'file': ('file', open(image_path, 'rb'), "image/jpeg")}
        response = requests.post(url=process_file_url, headers=headers, data=payload, files=files)

        df = response.json()
        dd = {}
        for key, value in df.items():
            if key == "vendor":
                for k, v in df["vendor"].items():
                    dd[k] = v
            if key == "line_items":
                for k, v in df["line_items"][0].items():
                    dd[k] = v
            else:
                dd[key] = value

        st.json(dd)
