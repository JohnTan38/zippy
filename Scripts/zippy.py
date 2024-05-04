import streamlit as st
from zipfile import ZipFile
from pathlib import Path
import glob
import timeit
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

st.set_page_config('COSCO MNR', page_icon="🏟️", layout='wide')

def title_main(url):
    st.markdown(f'<h1 style="color:#230c6e;font-size:42px;border-radius:2%;"><br>{url}</h1>', unsafe_allow_html=True)

def success_df(html_str):
    html_str = f"""
        <p style='background-color:#baffc9;
        color: #313131;
        font-size: 15px;
        border-radius:5px;
        padding-left: 12px;
        padding-top: 10px;
        padding-bottom: 12px;
        line-height: 18px;
        border-color: #03396c;
        text-align: left;'>
        {html_str}</style>
        <br></p>"""
    st.markdown(html_str, unsafe_allow_html=True)

title_main('COSCO MNR Containers Photos Upload 🚛 🚢')

st.divider()

def z(pathZip, path_mnr):
        import glob
        import timeit
        from zipfile import ZipFile
        from pathlib import Path
        fldrs = glob.glob(pathZip+'*.zip') #fldrs = [pathlib.Path().glob('C:/Users/john.tan/Downloads/*.zip')]
        for f_zip in fldrs:
            file_name = Path(f_zip).name #stem
            file_stem = Path(f_zip).stem
            with ZipFile(pathZip+file_name, 'r') as zipObj:
                zipObj.extractall(path=path_mnr+file_stem)
#from __main__ import z  
def linear_time():
        SETUP_CODE = '''
from __main__ import z     
from zipfile import ZipFile
import pathlib, glob
from pathlib import Path'''

        TEST_CODE = '''
pathZip = "C:/Users/john.tan/Downloads/"
path_mnr = "C:/Users/john.tan/OneDrive - Cogent Holdings Pte. Ltd/Documents/DMS/MNR/"
z(pathZip, path_mnr)
        '''
        #timeit.repeat statement
        times = timeit.repeat(setup=SETUP_CODE,stmt=TEST_CODE,repeat=1,number=1)

        # printing minimum exec. time
        print('unzip time: {}'.format(min(times)))
        st.write('Unzip time (s): {}'.format(min(times)))
        #success_df('all files unzipped. '+'unzip time: {}'.format(min(times)))
    #if __name__ == '__main__':
        #linear_time()

def filter_rows_noClip(df):
    df_filtered = df[df['Column-1 Src'].str.contains('shadow_total')] # Filter rows where 'Column-1 src' contains 'shadow_total'
    
    # Select only 'Column-1 src' and 'Column-4' columns and rename them
    df_filtered = df_filtered[['Column-1 Src', 'Column-4']].rename(columns={'Column-1 Src': 'src', 'Column-4': 'CONTAINER'})
    return df_filtered

usr_name = st.multiselect("Select Your UserName",['john.tan', 'abu.zaar', 'yuxiang.zhang'], placeholder='john.tan') #select user name
mnr_upload = st.file_uploader("Upload MNR file", type=["xlsx"])
if st.button("Get Download List"):
    path_mnr = "C:/Users/"+usr_name[0]+"/OneDrive - Cogent Holdings Pte. Ltd/Documents/DMS/MNR/"
    if mnr_upload is not None:
        mnr = pd.read_excel(mnr_upload, sheet_name='MNR', engine='openpyxl')
        df_noClip = filter_rows_noClip(mnr)
        df_noClip = df_noClip.dropna(subset=['CONTAINER'])
        df_noClip = df_noClip[['CONTAINER']]
        st.dataframe(df_noClip)
        with pd.ExcelWriter(path_mnr+ r"toDownload.xlsx", mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer_download:
            df_noClip.to_excel(writer_download, sheet_name='CONTAINER', index=False)
            success_df("saved to local folder.")
    else:
        st.write('Please upload MNR file.')
st.divider()

if st.button("Unzip Folders"):
    pathZip = "C:/Users/"+usr_name[0]+"/Downloads/"
    path_mnr = "C:/Users/"+usr_name[0]+"/OneDrive - Cogent Holdings Pte. Ltd/Documents/DMS/MNR/"
    z(pathZip,path_mnr)
    success_df('all folders unzipped.')
    if __name__ == '__main__':
        linear_time()

footer_html = """
    <div class="footer">
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f0f2f6;
            padding: 10px 20px;
            text-align: center;
        }
        .footer a {
            color: #4a4a4a;
            text-decoration: none;
        }
        .footer a:hover {
            color: #3d3d3d;
            text-decoration: underline;
        }
    </style>
        All rights reserved @2024. Cogent Holdings IT Solutions.      
    </div>
"""
st.markdown(footer_html,unsafe_allow_html=True)        