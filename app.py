import streamlit as st
from pdf2image import convert_from_path

import requests
import time
import json
import pandas as pd
import os

items = ['abn_number', 'account_number', 'bill_to_address', 'bill_to_name', 'bill_to_vat_number', 'card_number',
         'cashback', 'category', 'currency_code', 'date', 'delivery_date', 'discount', 'document_ref',
         'due_date','img_file_name', 'img_thumbnail', 'img_url', 'insurance', 'invoice_number', 'is_duplicate',
         'description', 'order', 'quantity', 'reference', 'section', 'sku', 'tax', 'tax_rate', 'total', 'type', 'unit_of_measure',
         'ocr_text', 'order_date', 'payment_disp', 'payment_terms', 'payment_type', 'phone_number', 'purchase_order', 'rounding',
         'service_end_date', 'service_start_date', 'ship_date', 'ship_to_address', 'ship_to_name', 'shipping', 'store_number', 'subtotal', 'tax_lines', 'tip', 'total_weight',
         'tracking_number','vat_number', 'address', 'email', 'fax_number', 'name', 'raw_name', 'vendor_logo', 'vendor_reg', 'vendor_type', 'web',
         'vendor_account', 'vendor_bank', 'vendor_bank_number', 'vendor_bank_swift', 'vendor_iban']
CLIENT_ID = "vrf3ZPfMXtt4vzaEtCYChFXtz4GemhUoNOXY4Xt"
ENVIRONMENT_URL = "api.veryfi.com"
username = "yassine.hamdaoui"
api_key = "005f364d189251026f4a514c30df16c9"
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
list_options = ['abn_number', 'account_number', 'bill_to_address', 'bill_to_name', 'bill_to_vat_number', 'card_number', 'cashback', 'category', 'created', 'currency_code', 'date', 'delivery_date', 'discount', 'document_reference_number', 'due_date', 'external_id', 'id', 'img_file_name', 'img_thumbnail_url', 'img_url', 'insurance', 'invoice_number', 'is_duplicate', 'line_items', 'ocr_text', 'order_date', 'payment_display_name', 'payment_terms', 'payment_type', 'phone_number', 'purchase_order_number', 'rounding', 'service_end_date', 'service_start_date', 'ship_date', 'ship_to_address', 'ship_to_name', 'shipping', 'store_number', 'subtotal', 'tax', 'tax_lines', 'tip', 'total', 'total_weight', 'tracking_number', 'updated', 'vat_number', 'vendor', 'vendor_account_number', 'vendor_bank_name', 'vendor_bank_number', 'vendor_bank_swift', 'vendor_iban']
st.title("NeuroData Extractor Demo")
st.subheader("")
c = st.beta_columns(9)
a = c[0].checkbox("select all")


st.markdown("---")
st.subheader("Select Items :")
st.subheader("")
cols= st.beta_columns(9)
for i in range(9):
    cols[i].checkbox(items[i],key=i,value=a)
cols= st.beta_columns(9)
for i in range(9,18):
    cols[i-9].checkbox(items[i],key=i,value=a)
cols= st.beta_columns(9)
for i in range(28,37):
    cols[i-28].checkbox(items[i],key=i,value=a)
cols= st.beta_columns(9)
for i in range(37,46):
    cols[i-37].checkbox(items[i],key=i,value=a)
cols= st.beta_columns(9)
for i in range(46,55):
    cols[i-46].checkbox(items[i],key=i,value=a)
cols= st.beta_columns(9)
for i in range(55,64):
    cols[i-55].checkbox(items[i],key=i,value=a)
cols= st.beta_columns(9)
for i in range(64,66):
    cols[i-64].checkbox(items[i],key=i,value=a)
st.markdown("---")





st.sidebar.image("images/logo.png",width=120)
st.sidebar.title("PDF Scraper For Businesses")
st.sidebar.image(r"images/extractor.gif")
st.sidebar.title("Reduce your manual data entry costs")
st.sidebar.image(r"images/ocr_illustration.gif")

img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg","pdf"])


tic = time.time()
if img_file_buffer is not None:
    file_details = {"FileName":img_file_buffer.name,"FileType":img_file_buffer.type}

    with open(os.path.join("tempDir", img_file_buffer.name), "wb") as f:
        f.write(img_file_buffer.getbuffer())
    st.success("Saved File")
    st.markdown("---")
    # Store Pdf with convert_from_path function
    pdf = convert_from_path("./tempDir/"+img_file_buffer.name)

    for i in range(len(pdf)):
        # Save pages as images in the pdf
        pdf[i].save('tempDir/'+img_file_buffer.name.split(".")[0]+ '.jpg', 'JPEG')

    image_path = "tempDir/"+img_file_buffer.name.split(".")[0]+ '.jpg'
    file_name = img_file_buffer.name.split(".")[0]+ '.jpg'

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
        for key,value in df.items():
            if key=="vendor":
                for k,v in df["vendor"].items():
                    dd[k]=v
            if key =="line_items":
                for k,v in df["line_items"][0].items():
                    dd[k]=v
            else:
                dd[key] = value

        st.json(dd)






