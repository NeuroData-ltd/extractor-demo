import streamlit as st
from pdf2image import convert_from_path
import base64
from io import BytesIO
import requests
import time
import json
import pandas as pd
import os

from collections import namedtuple
import warnings

analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')


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



st.title("NeuroData Extractor Demo")
st.subheader("")


st.markdown("---")




img_file_buffer = st.file_uploader("Upload Your Invoice", type=["png", "jpg", "jpeg", "pdf"])

tic = time.time()
if img_file_buffer is not None:
    file_details = {"FileName": img_file_buffer.name, "FileType": img_file_buffer.type}

    with open(os.path.join("tempDir", img_file_buffer.name.split(".")[0].split(" ")[0]+".pdf"), "wb") as f:
        f.write(img_file_buffer.getbuffer())
    st.success("Saved File")
    st.markdown("---")
    # Store Pdf with convert_from_path function
    fn = "./tempDir/" + img_file_buffer.name.split(".")[0].split(" ")[0]+".pdf"
    print(fn)

    os.system('convert ' +
              '-density 300 ' +
              '%s ' % fn +
              '-quality 100 ' +
              '-flatten ' +
              '%s' % fn.replace('.pdf', '.jpg'))


    image_path = "tempDir/" + img_file_buffer.name.split(".")[0].split()[0] + '.jpg'
    file_name = img_file_buffer.name.split(".")[0] + '.jpg'
    c =st.beta_columns(10)
    if c[4].button("Process Your Invoices"):
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
        attributes = ["bill_to_address","bill_to_name","currency_code","invoice_number","description","quantity","tax","tax_rate","total","type","subtotal","vendor_reg_number"]
        values = [dd[k] for k in attributes]
        df = pd.DataFrame([values], columns=attributes)
        st.dataframe(df, width=4000)


        def tto_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            processed_data = output.getvalue()
            return processed_data


        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            val = tto_excel(df)
            b64 = base64.b64encode(val)  # val looks like b'...'
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Data.xlsx">Download Excel file</a>'


        c = st.beta_columns(10)
        c[4].markdown(get_table_download_link(df), unsafe_allow_html=True)
