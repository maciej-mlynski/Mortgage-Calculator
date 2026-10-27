import streamlit as st
import pandas as pd
from KredytNormalnie import Parametry_kredytu
import numpy_financial as nf
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import date, timedelta, datetime
import streamlit as st
import pickle as pkle
import os.path
import toml
import streamlit.components.v1 as components

import base64
import matplotlib.ticker as mtick
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

# Dane do bazy są w zmiennych środowiskowych: lokalnie z pliku .env, na Heroku z Config Vars
load_dotenv()

def get_db_config():
    return {
        'host': os.environ['MYSQL_HOST'],
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
        'database': os.environ['MYSQL_DATABASE'],
        'user': os.environ['MYSQL_USER'],
        'password': os.environ['MYSQL_PASSWORD'],
    }



#style.css
def local_css(): 
        st.markdown(
       f"""
       <style>
       @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');
    body {{
        font-family: 'Montserrat';
        font-weight: 300;
        color: white;
    }}
    .p, p {{
        font-family: 'Montserrat';
        font-weight: 300;
        color: white;
    }}
    .h1, h1 {{
        font-family: 'Montserrat';
        font-weight: 800;
        line-height: 154%;
        font-size: 30px;
        color: white;
    }}
    .h2, h2 {{
        font-family: 'Montserrat';
        font-size: 14px;
        font-weight: 500;
        line-height: 154%;
        color: white;
        
    }}
    .css-glyadz {{
        color: rgb(255 255 255);
    }}
    .nazwyParametrow{{
        font-family: 'Montserrat';
        font-weight: 700;
        text-align: center; 
        color: white; 
        font-size:25px
    }}
    .instrukcja-kroki{{
        background-color: rgba(255,255,255, 0.1);
        color:#fffff;
        font-size: 15px;
        font-weight: 400;
        border-radius: 0px 0px 20px 20px;
        text-align:center;
        padding: 0px 15px 27.5px 15px;
        

    }}
    .parametry-contenery {{
        background-color:rgba(225, 225, 255, 0.2);
        color:#fffff;
        font-family: Montserrat;
        font-size:17px;
        border-radius:5px;
        text-align:center;
        padding-top: 15px;
        padding-bottom: 15px;
    }}
    .padding-dlatego {{
        padding-top: 150px;
    }}
    .padding-dlatego2 {{
        padding-top: 170px;
    }}
    .stopy-twoje{{
        background-color:rgba(56, 217, 217, 0.2);
        color:#fffff;
        font-family: Montserrat;
        font-size:17px;
        border-radius:5px;
        text-align:center;
        padding-top:5px; 
        padding-bottom:5px;
    }}
    .stopy-optymistyczny{{
        background-color:rgba(136, 217, 56, 0.2);
        color:#fffff;
        font-family: Montserrat;
        font-size:17px;
        border-radius:5px;
        text-align:center;
        padding-top:5px; 
        padding-bottom:5px;
    }}
    .stopy-bazowy{{
        background-color:rgba(214, 217, 56, 0.2);
        color:#fffff;
        font-family: Montserrat;
        font-size:17px;
        border-radius:5px;
        text-align:center;
        padding-top:5px; 
        padding-bottom:5px;
    }}
    .stopy-pesymistyczny{{
        background-color:rgba(98, 56, 217, 0.2);
        color:#fffff;
        font-size:17px;
        font-family: Montserrat;
        border-radius:5px;
        text-align:center;
        padding-top:5px; 
        padding-bottom:5px;
    }}
    .nadplaty-contenery{{
        background-color:rgba(0, 178, 255, 0.15);
        color:#fffff;
        font-family: Montserrat;
        font-size:17px;
        border-radius:5px;
        text-align:center;
        padding-top: 15px;
        padding-bottom: 15px;
    }}
    .bilansowanie-contenery{{
        background-color:rgba(0, 225, 117, 0.15);
        color:#fffff;
        font-family: Montserrat;
        font-size:17px;
        border-radius:5px;
        text-align:center;
        padding-top: 15px;
        padding-bottom: 15px;
    }}
    .bilansowanie-left_cont{{
        background-color:rgba(0, 178, 255, 0.15);
        color:#fffff;
        font-family: Montserrat;
        font-size:16px;
        border-radius:20px;
        text-align:left;
        padding: 27.5px 15px 27.5px 35px;
    }}
    .sam-contenery{{
        background-color:rgba(0, 225, 117, 0.15);
        color:#fffff;
        font-family: Montserrat;
        font-size:17px;
        border-radius:5px;
        text-align:center; 
        padding-top: 15px;
        padding-bottom: 15px;
    }}
    .first_last-coment {{
        font-family: Montserrat; 
        font-size: 35px; 
        font-weight:800; 
        text-align: center;
    }}
    .down-coment{{
        text-align: center; 
        color: white;
        font-size:22px;
        font-weight:700; 
        letter-spacing: 0.05em; 
        line-height: 154%;
    }}
    .btn-primary {{
        text-decoration: none;
        background-color: #31333f;
        border-radius: 5px;
        padding: 10px 12px;
        border: 2px solid;
        border-color: #31333f;
    }}
    .btn-primary2 {{
        text-decoration: none;
        background-color: #31333f;
        border-radius: 5px;
        padding: 10px 12px;
        border: 2px solid;
        border-color: #31333f;
    }}
    .css-c8vtvv a {{
        font-family: 'Monserrat';
        font-size: 16px;
        font-weight: 300;
        color: #ffffff;
        letter-spacing: 0.05em;
    }}

    .css-fjj0yo {{
        height: 49px;
        display: flex;
        flex-direction: row;
        width: 50px;
    }}


    .btn-primary:hover {{
        border-color: #7792E3;
        transform: scale(1.1);
        transform-origin: center;
        transition: 0.3s cubic-bezier(0.75, 0.12, 0.065, 1);
        text-decoration:none;
        color: #7792E3; 
    }}
    .btn-primary2:hover {{
        border-color: red;
        transform: scale(1.1);
        transform-origin: center;
        transition: 0.3s cubic-bezier(0.75, 0.12, 0.065, 1);
        text-decoration:none;
        color: red; 
    }}
    .css-11b04td {{
        color: rgba(250, 250, 250, 0);
    }}
    .css-11b04td a {{
        color: rgba(250, 250, 250, 0);
    }}
    
    .css-1gez77v {{
        background-color: rgba(4, 9, 22, 0.8) !important;
    }}
    .css-euz70k {{
        width: 35px;
        background-color: rgba(4, 9, 22, 0.8) !important;
    }}

    .css-1d81imo {{
        padding-top: 28px;
        padding-bottom: 13px;
        font-family: 'Montserrat';
        font-weight: 600;
        justify-content: center;
        font-size: 14px;
    }}

    .st-br, .st-bs {{
        background: rgba(123, 124, 131, 1);
    }}
    .css-1v0mbdj {{
        align-items: center;
        width: 100%;
    }}

    # robi co chce..
    # .st-bs:actve {{
    #     border-color: rgb(255, 255, 255);
    # }}
    
    # .st-bs:hover {{
    #     border-color: rgb(255, 255, 255);
    # }}
    
    # .st-ei:active {{
    #     border-color: rgb(255, 255, 255);
    # }}

    # .st-ei:hover {{
    #     border-color: rgb(255, 255, 255);
    # }}


    @media only screen and (max-width:1220px) {{
        .bilansowanie-contenery {{
            margin-top: 10px;
        }}
    }}
    
    @media only screen and (max-width:1020px) {{
        .nadplaty-contenery {{
            margin-top: 12px;
        }}
        .bilansowanie-contenery {{
            margin-top: 15px;
        }}
    }}

    @media only screen and (max-width:760px) {{
        
        .block-container{{
            max-width: 100vw;
            min-height: 100vh;
            position: static;
            overflow: hidden;
            overflow-y: auto;
            max-width: 100vw;
        }}
    
        .h2, h2 {{
            font-size: 14px;
        }}
        .down-coment {{
            font-size: 17px;
            font-weight: 600;
        }}
        .first_last-coment {{
            font-size:25px;
            padding-top: 10px;
        }}
        .instrukcja-kroki{{
            font-size: 14px;
        }}
        .padding-dlatego {{
            padding-top: 0px;
        }}
        .padding-dlatego2 {{
            padding-top: 0px;
        }}
        .nadplaty-contenery {{
            margin-top: 21px;
        }}
        .css-18j7ggn {{
            min-width: 98%;
        }}
        .css-1othchw {{
            min-width: 98%;
        }}
        .css-1d81imo{{
            margin-bottom: 10px;
        }}
        .stTooltipIcon {{
            transform: scale(1.5);
            margin-right: 15px;
        }}
        .css-2rzj6y e1tzin5v2 {{
            min-width: 98%;
        }}
        .bilansowanie-contenery {{
            margin-top: 15px;
        }}
        .css-2rzj6y {{
            min-width: 98%;
        }}
        .css-rncmk8 {{
            max-width: 103%;
        }}
        
    }}
    @media only screen and (max-width:640px) {{
        .css-ns35eg {{
            width: 100%;
            flex: auto;
        }}

        .first_last-coment {{
            font-size:20px;
        }}
        .h2, h2 {{
            font-size: 13px;
            padding-right: 15px !important;
            padding-left: 15px !important;
        }}
        .instrukcja-kroki{{
            font-size: 13px;
        }}
        .css-4a1i5u {{
            min-width: 100%;
        }}
        .down-coment {{
            font-size: 15px;
            font-weight: 600;
        }}
        .css-o8xcvx {{
            min-width: max(47.619%, 290.762px);
        }}

    }}
    
    @media only screen and (max-width:375px) {{
        .parametry-text {{
            font-size: 15px;
        }}
        .parametry-contenery {{
            font-size: 15px;
        }}
        .css-1wer3zp {{
            width: 340px;
        }}
    }}

    @media only screen and (max-width:320px) {{
        .instrukcja-kroki{{
            font-size: 12px;
        }}
        .css-c8vtvv a {{
            font-size: 12px;
        }}
        .css-hi6a2p {{
            padding: 3rem 1rem 10rem;
        }}
        .h1, h1 {{
            font-size:20px;
        }}
        .css-2rzj6y {{
            min-width: max(25% - 1.5rem, 100px);
        }}
        .first_last-coment {{
            font-size: 20px;
            padding-top: 25px;
        }}
        .down-coment {{
            font-size: 16px;
            font-weight: 600;
        }} 
        .bilansowanie-contenery {{
            margin-top: 19px;
            
        }}
        .down-coment {{
            font-size: 14px;
            font-weight: 600;
        }}
        .css-2rzj6y {{
            min-width: 100%;
        }}
    }}
    
    
    </style>
        """,
            unsafe_allow_html=True,
)


#Ustawienia z config.toml
st.get_option("theme.primaryColor") 

# # Initialize connection.
# # Uses st.cache to only run once.
# @st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
# def init_connection():
#     # return mysql.connector.custom_error_exception()
#     return mysql.connector.connect(**get_db_config())

# conn = init_connection()

# # Perform query.
# # Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()


# df = pd.read_sql_query("SELECT * from users;",conn, index_col = None)

#st.write(df)


#1 Sidebar
#2 kolor strony
#3 szerokość
main_bg = "images/pic80black.png"
main_bg_ext = "png"
st.markdown(
    f"""
    <style>
    .css-hby737 {{
        background: linear-gradient(180deg, rgba(49, 51, 63, 0.8) 0%, rgba(49, 51, 63, 0.7) 100%);
        opacity: 0.95;
        padding-left: 40px;
        padding-right: 40px;
        width: 280px;
        position: absolute;
        backdrop-filter: blur(10px);
        height: 100%;
        padding-top: 3rem;
        
    }}
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
        background-repeat: no-repeat;
        background-size: cover;
        background-position-x: center;

    }}
    .reportview-container .main .block-container{{
        max-width: 1000px;
    }} 

    @media only screen and (min-width: 1260px) {{
        .css-hby737 {{
            position: relative;
        }}
    }}

    @media only screen and (max-width: 440px) {{
        .css-hby737 {{
            width: 100%;
        }}
    }}

    </style>""",
    unsafe_allow_html=True)


def main():
    
    lister = []
    def get_data():
        return lister
    
    local_css()
    Tabela = pd.DataFrame(lister)
    lister = get_data() 
    aktualny_wibor = 3.17
    get_data().append({'wielkosc': 0,'okres': 0, 'marza' :0.0, 'wibor': aktualny_wibor,'nadplata':0,'kiedynad':0,'indn':0.0,'skladka':0,'procent': 0.0,'inds':0.0,'kiedyskl':0,'procentdyw':0.0})
        
        
    Tabela = pd.DataFrame(lister)
    

    # Initialize connection.
    # Uses st.cache to only run once.

        
    st.sidebar.image("images/logo_fm.png")
    
    st.sidebar.markdown(f'<p style="font-weight: 800;font-size: 16px;  margin-bottom: 10px; text-align: center; font-family: "Montserrat">\
                            kalkulator kredytowy\
                            </p>\
                            ', unsafe_allow_html=True)
    topics = ['Logowanie', 'Rejestracja']
    lns = st.sidebar.selectbox("Start", topics)
    if lns == 'Rejestracja':
        
        link = "https://financialmill.pl/premium/index.php"
        st.sidebar.markdown(f'<div style="text-align: center; margin-top:20px;"> <a role="button" class="btn-primary" target="_blank" style="font-family: "Montserrat" href={link}>Zapisz się!</a></div>', unsafe_allow_html=True)  
    
    elif lns == 'Logowanie':
        
        email = st.sidebar.text_input("Kod aktywacyjny")   
        approve = st.sidebar.checkbox('Zaloguj', email)
    
        if approve:
            
            # df = pd.read_sql_query("SELECT * from users;",conn, index_col = None)
        
            if email == 'FinancialMill2022':
                
                new_choice = ['Zacznij tutaj', 'Parametry kredytu','Stopy procentowe vs rata','Nadpłacanie kredytu','Bilansowanie kredytu','Kredyt spłaca sie sam?']
                choice = st.sidebar.selectbox("Wybierz temat", new_choice)

                
                st.sidebar.markdown(f'<div style="margin-top: 50px; display: flex; justify-content: center;">         \
                                                <p style=" font-weight: 700; font-size: 14px;  margin-bottom: 10px; font-family: "Montserrat";">           \
                                                    Masz jakieś pytania?                                                    \
                                                </p> \
                                            </div>                                                                            \
                                            <div style = "background-color: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 5px; justify-content: center; text-align: center; margin-bottom: 21px;"> \
                                                financialmill@kredyty.pl   \
                                        </div>            \
                                            ', unsafe_allow_html=True)
                col1, col2, col3 = st.sidebar.beta_columns([1,1,1])
                with col1:
                    st.image("images/twitter.png")
                with col2:
                    st.image("images/instagram.png")
                with col3:
                    st.image("images/facebook.png")
                
                

                #-----------------------------------------------SEKCJA nr.1 Instrukcja------------------------------------------------
                if choice == 'Zacznij tutaj':

                    link = "https://financialmill.pl/posts/readpageKredytyHipoteczneWstep/readpage.html"
                    st.markdown(f'<a role="button" class="btn-primary" target="_blank" href={link}>Lekcja nr.1 WSTĘP</a>', unsafe_allow_html=True)

                    st.markdown(f'<p class="first_last-coment">{"Witaj w kalkulatorze kredytowym!"}</p>', unsafe_allow_html=True)
                    
                    up = "Kredyt hipoteczny to jedna z kluczowych decyzji jakie podejmujemy w życiu. Warto zatem poświęcić chwile na zdobycie fundamentalnej wiedzy. Przeprowadzimy Cię przez ten proces odpowiednio tylko wtedy, gdy Ty sam podejdziesz do tego profesjonalnie. Przejdź przez każdy etap z należytą uwagą, poczynając od poniższej instrukcji!"
                    st.markdown(f'<h2 style="background-color:rgba(255,255,255, 0.1);\
                                                        color:#fffff;\
                                                        border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 25px 30px 25px 30px;\
                                                        ">{up}</h2>', unsafe_allow_html=True)
                    st.write("")
                    st.write("")

                    st.write("")
                    st.write("")
                    st.write("")

                    left_top = "W każdej zakładce znajdziesz odnośnik do artykułu, który dokładnie wyjaśni Ci poszczególne kwestie związane z kredytem. "
                    left_mid = "Jeśli potrzebujesz pomocy z kredytem lub wyborem formy optymalizacji wystarczy, że do nas napiszesz na financialmill@kredyty.com"
                    left_bottom = "Dane dotyczące WIBOR 3M i wariantów oprocentowania aktualizowane będą na koniec każdego miesiąca."
                    right_top = "Przy każdym oknie do wypełnienia znajduje się krótka instrukcja wyjaśniająca znaczenie oraz odpowiednią formę parametru."
                    right_mid = 'W naszych wyliczeniach nie uwzględniliśmy kosztów okołokredytowych, ponieważ zależą one od indywidualnej oferty banku.'

                    
                    right_bottom = "Pola do wypełniania oznaczone gwiazdką* to pola obowiązkowe, bez których kalkulator nie wykona obliczeń."
                    

                    ok = "images/tooltip.png"
                    
                    
                    col1, col2, col3 = st.beta_columns([1,0.1,1])
                    with col1:
                        st.markdown(f'<p style="font-size:130px; font-weight:900; text-align: center; background-color: rgba(255,255,255, 0.1); margin-bottom: -16px; border-radius: 20px 20px 0px 0px;">{"1"}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class ="instrukcja-kroki" style="background:rgba(255,255,255, 0.1);">{left_top}</p>', unsafe_allow_html=True)
                        st.write("")
                        st.write("")
                        st.write("")
                        
                    with col2:
                        st.write("")
                        st.write("")  
                    with col3:
                        st.markdown(f'<p style="font-size:130px; font-weight:900; text-align: center; background-color: rgba(255,255,255, 0.1); margin-bottom: -16px; border-radius: 20px 20px 0px 0px;">{"2"}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="instrukcja-kroki" >{right_top}\
                        <img src="data:image/png;base64,{base64.b64encode(open(ok, "rb").read()).decode()}">\
                        </p>', unsafe_allow_html=True)
                        st.write("")
                        st.write("")
                        st.write("")
                        
                    col1, col2, col3 = st.beta_columns([1,0.1,1])

                    with col1:
                        st.markdown(f'<p style="font-size:130px; font-weight:900; text-align: center; background-color: rgba(255,255,255, 0.1); margin-bottom: -16px; border-radius: 20px 20px 0px 0px;">{"3"}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="instrukcja-kroki" >{left_mid}</p>', unsafe_allow_html=True)
                        st.write("")
                        st.write("")
                        st.write("")
                    with col2:
                        st.write("")
                        st.write("") 
                    with col3:
                        st.markdown(f'<p style="font-size:130px; font-weight:900; text-align: center; background-color: rgba(255,255,255, 0.1); margin-bottom: -16px; border-radius: 20px 20px 0px 0px;">{"4"}</p>', unsafe_allow_html=True)
                        st.markdown(f"""<p class="instrukcja-kroki">{right_mid}
                        </p>""", unsafe_allow_html=True)
                        st.write("")
                        st.write("")
                        st.write("")

                    col1, col2, col3 = st.beta_columns([1,0.1,1])

                    with col1:
                        st.markdown(f'<p style="font-size:130px; font-weight:900; text-align: center; background-color: rgba(255,255,255, 0.1); margin-bottom: -16px; border-radius: 20px 20px 0px 0px;">{"5"}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="instrukcja-kroki" >{left_bottom}</p>', unsafe_allow_html=True)
                    with col2:
                        st.write("")
                        st.write("") 
                    with col3:
                        st.markdown(f'<p style="font-size:130px; font-weight:900; text-align: center; background-color: rgba(255,255,255, 0.1); margin-bottom: -16px; border-radius: 20px 20px 0px 0px;">{"6"}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="instrukcja-kroki">{right_bottom}</p>', unsafe_allow_html=True)






                #------------------------------------------------------------Sekcja nr.2 Parametry kedytu----------------------------------------------

                elif choice == 'Parametry kredytu':

                    link = "https://financialmill.pl/posts/readpageKredytyHipoteczneKonstrukcja/readpage.html"
                    st.markdown(f'<a role="button" class="btn-primary" target="_blank" href={link}>Lekcja nr. 2 KONSTRUKCJA KREDYTU</a>', unsafe_allow_html=True)
                
                    up = "Wpisz parametry swojego kredytu i przekonaj się ile prowizji<br>zapłacisz za jego udzielenie przez cały okres."
                    st.markdown(f'<h2 style= "background-color:rgba(255, 255, 255, 0.1);\
                            color:#fffff; margin-top: 30px;\
                            border-radius:5px;\
                            text-align:center;\
                            padding:20px 20px 20px 20px; ">{up}</h2>', unsafe_allow_html=True) 

                    st.markdown(f'<p class="nazwyParametrow">{"Parametry kredytu"}</p>', unsafe_allow_html=True)
                    st.write("")

                    col1, col2, col3, col4, col5 =  st.beta_columns([1.2,0.9,0.8,0.9,0.9])

                    with col1:
                        wielkosc = st.number_input('Kwota kredytu*', key = "", min_value=0, step=50000, value = Tabela['wielkosc'][len(Tabela)-1], help='Podaj kwotę kredytu, o którą chciałbyś wnioskować (wnioskowałeś). Chodzi o część pożyczoną z banku, nie uwzględniaj wkładu własnego.')
                        
                    with col2: 
                        okres = st.number_input('Na ile lat?*', min_value=0, step=10, max_value=30,value = Tabela['okres'][len(Tabela)-1], help = 'Określ czas trwania kredytu, wyrażony w latach.')
                    with col3:
                        kiedy = st.date_input('Kiedy kredyt?', min_value=datetime.today(), help='Nie zdecydowałeś się jeszcze na zaciągnięcie kredytu? Podaj szcunkową datę jego startu. Jeśli już jesteś kredytobiorcą, wybierz dzisiejszą datę. W polu "Kwota kredytu" wpisz kapitał pozostały do spłaty, a w "Na ile lat?" wpisz ile lat pozostało Ci do spłaty.')
                    with col4:
                        marza = st.number_input('Marża banku*', min_value=0.00, format="%.2f", step=0.5,value = Tabela['marza'][len(Tabela)-1], help="Podaj marżę banku wyrażoną w procentach. Przykład: Marza = 2,5% wpisz do kalkulatora 2.5")
                    with col5:
                        wibor = st.number_input('WIBOR 3M', min_value=0.1, format="%.2f",value = aktualny_wibor, help="Domyślnie ustawiony jest aktualny poziom WIBOR 3M. Pamiętaj, że możesz go zmienić według własnych potrzeb.")

                    if st.button("Oblicz"):
                        get_data().append({'wielkosc': wielkosc,'okres': okres, 'marza' :marza, 'wibor' :wibor, 'kiedy': kiedy,'nadplata':Tabela['nadplata'][len(Tabela)-1],'kiedynad':Tabela['kiedynad'][len(Tabela)-1],'indn':Tabela['indn'][len(Tabela)-1],'skladka':Tabela['skladka'][len(Tabela)-1],'procent': Tabela['procent'][len(Tabela)-1],'inds':Tabela['inds'][len(Tabela)-1],'kiedyskl':Tabela['kiedyskl'][len(Tabela)-1],'procentdyw':Tabela['procentdyw'][len(Tabela)-1]})     
                    
                        lister = get_data()
                        Tabela = pd.DataFrame(lister)
                        
                        #Wykres
                    
                        if Tabela["wielkosc"][len(Tabela)-1]>0 and Tabela["okres"][len(Tabela)-1]>0 and Tabela["marza"][len(Tabela)-1]>0:
                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")
                                
                            st.markdown(f'<p style= "text-align:center; font-weight:600; font-size:18px;">{"Wykres ilustruje kapitał pozostały do spłaty"}</p>', unsafe_allow_html=True)
                                
                            kredyt1 = Parametry_kredytu(Tabela["wielkosc"][len(Tabela)-1],Tabela["kiedy"][len(Tabela)-1], Tabela["okres"][len(Tabela)-1], Tabela["wibor"][len(Tabela)-1], Tabela["marza"][len(Tabela)-1],Tabela["nadplata"][len(Tabela)-1],Tabela["indn"][len(Tabela)-1],Tabela["kiedynad"][len(Tabela)-1],Tabela["skladka"][len(Tabela)-1],Tabela["procent"][len(Tabela)-1],Tabela["inds"][len(Tabela)-1],Tabela["kiedyskl"][len(Tabela)-1], Tabela["procentdyw"][len(Tabela)-1])
                            fig, ax = plt.subplots()
                            fig.patch.set_facecolor('#0E1117')
                            fig.patch.set_alpha(0)
                                
                            x = kredyt1.Kapital_do_splaty_daty()
                            y = kredyt1.Kapital_do_splaty()
                            line = ax.plot(x, y, color = 'white', linewidth=0.5)
                                
                            ax.set_facecolor('#0E1117')
                            ax.patch.set_alpha(0)
                            ax.spines['top'].set_alpha(0)
                            ax.spines['right'].set_alpha(0)
                            ax.spines['bottom'].set_color('white')
                            ax.spines['left'].set_color('white')
                            ax.tick_params(colors='white', which='both')
                            ax.grid(axis='y',linestyle='--',linewidth=0.3)

                            y_value=['{:,.0f}'.format(x).replace(",", " ") + 'PLN' for x in ax.get_yticks()]
                            ax.set_yticklabels(y_value)

                            plt.xticks(fontsize=5)
                            plt.yticks(fontsize=5)

                            line = plt.fill_between(x, y, 0, color= 'white', alpha=0.08)
                            st.pyplot(plt)

                            st.write("")
                            st.write("")
                            st.write("")
                            

                                #Tabelka
                            x = "Koszt kredytu"
                            x1 = "Rata kredytu"

                            y = "Dzień spłaty"
                            y1 = "Oprocentowanie"

                            col1, col2,  = st.beta_columns([1,1])
                                
                            
                            with col1:
                                    st.markdown(f'<p class="parametry-contenery"><b>{x}</b> <br>{kredyt1.Koszt_kredytu()}</p>', unsafe_allow_html=True)
                                    st.markdown(f'<p class="parametry-contenery"><b>{x1}</b> <br>{kredyt1.Rata_kredytu()}</p>', unsafe_allow_html=True)  
                            with col2:
                                    st.markdown(f'<p class="parametry-contenery"><b>{y}</b> <br>{kredyt1.Dzien_splaty_normalnie()}</p>', unsafe_allow_html=True)
                                    st.markdown(f'<p class="parametry-contenery"><b>{y1}</b> <br>{kredyt1.Oprocentowanie()}</p>', unsafe_allow_html=True)
                                

                            st.write("")
                            st.write("")
                            st.write("")

                            down = "Raty Twojego kredytu zależą od poziomu stóp procentowych ustalanych przez Radę Polityki Pieniężnej"
                            st.markdown(f'<h2 style= "background-color:rgba(225, 225, 255, 0.1);\
                                color:#fffff;\
                                font-weight: 400;\
                                border-radius:5px;\
                                text-align:center;\
                                padding:20px 20px 20px 20px; ">{down}</h2>', unsafe_allow_html=True) 
                                
                            st.write("")
                            st.write("")
                            st.markdown('<p class="down-coment">Przejdź do następnego krotku i przekonaj się, jak decyzje RPP mogą wpłynąć na ratę i koszt Twojego kredytu.</p>', unsafe_allow_html=True)

                        


                #-------------------------------------SEKCJA nr.2 Stopy procentowe vs. rata---------------------------------------------------
                elif choice == 'Stopy procentowe vs rata':

                    link = "https://financialmill.pl/posts/readpageKredytyHipoteczneWibor/readpage.html"
                    st.markdown(f'<a role="button" class="btn-primary" target="_blank" href={link}>Lekcja nr. 3 WIBOR 3M</a>', unsafe_allow_html=True)
                    
                    up = "Dwa podstawowe koszty kredytu to <b>marża</b>, która jest ustalana w momencie podpisania umowy oraz <b>WIBOR 3M</b>, który w czasie kredytu może ulegać zmianie. Sprawdź jak zmienność WIBOR 3M wpłynie na kosz i ratę Twojego kredytu"
                    st.markdown(f'<h2 style= "background-color:rgba(225, 225, 255, 0.1);\
                                color:#fffff;\
                                border-radius:5px;\
                                text-align:center;\
                                padding:20px 20px 20px 20px; ">{up}</h2>', unsafe_allow_html=True) 
                    
                    st.markdown(f'<p class="nazwyParametrow">{"Parametry kredytu"}</p>', unsafe_allow_html=True)
                    st.write("")
                    col1, col2, col3, col4, col5 =  st.beta_columns([1.2,0.9,0.8,0.9,0.9])

                    with col1:
                        wielkosc = st.number_input('Kwota kredytu*', min_value=0, step=50000,value = Tabela['wielkosc'][len(Tabela)-1], help='Podaj kwotę kredytu, o którą chciałbyś wnioskować (wnioskowałeś). Chodzi o część pożyczoną z banku, nie uwzględniaj wkładu własnego.')
                    with col2:
                        okres = st.number_input('Na ile lat?', min_value=0, step=10, max_value=30,value = Tabela['okres'][len(Tabela)-1], help = 'Określ czas trwania kredytu, wyrażony w latach.')
                    with col3:
                        kiedy = st.date_input('Kiedy kredyt?', min_value=datetime.today(), help='Nie zdecydowałeś się jeszcze na zaciągnięcie kredytu? Podaj szcunkową datę jego startu. Jeśli już jesteś kredytobiorcą, wybierz dzisiejszą datę. W polu "Kwota kredytu" wpisz kapitał pozostały do spłaty, a w "Na ile lat?" wpisz ile lat pozostało Ci do spłaty.')
                    with col4:
                        marza = st.number_input('Marża banku', min_value=0.00, format="%.2f", step=0.5,value = Tabela['marza'][len(Tabela)-1], help="Podaj marżę banku wyrażoną w procentach. Przykład: Marza = 2,5% wpisz do kalkulatora 2.5")
                    with col5:
                        wibor = st.number_input('WIBOR 3M', min_value=0.1, format="%.2f",value = Tabela['wibor'][len(Tabela)-1], help="Domyślnie ustawiony jest aktualny poziom WIBOR 3M. Pamiętaj, że możesz go zmienić według własnych potrzeb.")
                    
                    if st.button("Oblicz"): 
                        get_data().append({'wielkosc': wielkosc,'okres': okres, 'marza' :marza, 'wibor' :wibor, "kiedy": kiedy,'nadplata':Tabela['nadplata'][len(Tabela)-1],'kiedynad':Tabela['kiedynad'][len(Tabela)-1],'indn':Tabela['indn'][len(Tabela)-1],'skladka':Tabela['skladka'][len(Tabela)-1],'procent': Tabela['procent'][len(Tabela)-1],'inds':Tabela['inds'][len(Tabela)-1],'kiedyskl':Tabela['kiedyskl'][len(Tabela)-1],'procentdyw':Tabela['procentdyw'][len(Tabela)-1]})     
                    
                        lister = get_data()
                        Tabela = pd.DataFrame(lister)
                        
                        kredyt1 = Parametry_kredytu(Tabela["wielkosc"][len(Tabela)-1],Tabela["kiedy"][len(Tabela)-1], Tabela["okres"][len(Tabela)-1], Tabela["wibor"][len(Tabela)-1], Tabela["marza"][len(Tabela)-1],Tabela["nadplata"][len(Tabela)-1],Tabela["indn"][len(Tabela)-1],Tabela["kiedynad"][len(Tabela)-1],Tabela["skladka"][len(Tabela)-1],Tabela["procent"][len(Tabela)-1],Tabela["inds"][len(Tabela)-1],Tabela["kiedyskl"][len(Tabela)-1], Tabela["procentdyw"][len(Tabela)-1])

                        #------------------------------Wykres stopy procentowe-------------------------------------------
                        st.markdown(f'<p style= "text-align:center; font-weight:600; font-size:18px;">{"WIBOR 3M na przestrzenia XXI wieku"}</p>', unsafe_allow_html=True)
                            
                        fig, ax = plt.subplots(figsize=(5,3))
                        fig.patch.set_facecolor('white')
                        fig.patch.set_alpha(0)
                        
                        ax.set_facecolor('white')
                        ax.patch.set_alpha(0)
                        ax.spines['top'].set_alpha(0)
                        ax.spines['right'].set_alpha(0)
                        ax.spines['bottom'].set_color('white')
                        ax.spines['left'].set_color('white')
                        dfS = kredyt1.wykres_wibor()
                        x = dfS.idx
                        y = dfS.Zamkniecie*100
                        ax.grid(axis='y',linestyle='--',linewidth=0.3)
                        fmt = '%.0f%%' 
                        yticks = mtick.FormatStrFormatter(fmt)
                        ax.yaxis.set_major_formatter(yticks)
                        ax.plot(x,y, color='white', linestyle='--', linewidth=0.5)
                        line = plt.fill_between(x, y, 0, color='WHITE', alpha=0.1)
                        ax.tick_params(colors='white', which='both')
                        plt.xticks(fontsize=5)
                        plt.yticks(fontsize=5)
                        
                        st.pyplot(plt)


                        
                        kom = "Historycznie najniższy poziom WIBOR 3M przypada na lata 2020/2021. Nie możemy jendak zapomnieć o początku XXI wieku, kiedy oprocentowanie sięgało nawet 20 procent. Bądź sprytniejszy i przygotuj się wcześniej."

                        st.markdown(f'<p style= "background-color:rgba(225, 225, 255, 0.1);\
                                color:#fffff;\
                                font-size:16px;\
                                font-weight: 400;\
                                border-radius:5px;\
                                text-align:center;\
                                padding:20px 20px 20px 20px; ">{kom}</p>', unsafe_allow_html=True) 
                        
                        st.write("")
                        st.write("")
                        


                        left = "<b>Marża banku jest stała</b>, jednak w momencie <b>podwyższenia WIBOR 3M</b> przez RPP istnieje możliwość <b>renegocjowania warunków kredytu</b> do bieżacych stawek rynkowych."
                        right = "Przygotowaliśmy dla was scenariusze kredytu w <b>różnych wariantach WIBOR 3M</b> skorygowane o <b>średnie marże</b> banków za ostatnie <b>15 lat</b>."
                        
                        col1, col2, col3 = st.beta_columns([1.1,0.8,1.1])
                        with col1:
                            st.markdown(f'<p style="background-color:rgba(225, 225, 255, 0.1);\
                                                        color:#fffff;font-size:17px;border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 15px 30px 15px 30px;\
                                                            ">{left}</p>', unsafe_allow_html=True)

                        with col2:
                            st.markdown(f'<p class="padding-dlatego">{""}</p>', unsafe_allow_html=True)
                            st.image('images/dlatego.png')

                        with col3:
                            st.markdown(f'<p class="padding-dlatego2">{""}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="background-color:rgba(225, 225, 255, 0.1);\
                                                        color:#fffff;font-size:17px;border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 15px 30px 15px 30px;\
                                                            ">{right}</p>', unsafe_allow_html=True)

                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")


                        #------------------------------Wykres warianty rat-------------------------------------------
                        
                        st.markdown(f'<p style= "text-align:center; font-weight:600; font-size:18px;">{"Jak zmieniają się koszty i rata kredytu względem różnych poziomów WIBOR 3M"}</p>', unsafe_allow_html=True)
                        df = kredyt1.Warianty_rat_i_kosztow_kredytowych_wykres()
                        
                        fig = plt.figure(figsize=(15,8))

                        x = np.arange(4)
                        ax1 = plt.subplot(1,1,1)
                        w = 0.2
                        fig.patch.set_facecolor('#010024')
                        fig.patch.set_alpha(0.2)

                        ax = fig.add_subplot(1, 1, 1)
                        ax.patch.set_alpha(0)
                        ax.spines['top'].set_alpha(0)
                        ax.spines['right'].set_alpha(0)
                        ax.spines['bottom'].set_color('white')
                        ax.spines['left'].set_color('white')
                        ax.grid(axis='y',linestyle='--',linewidth=0.3)
                        ax1.tick_params(colors='white', which='both')
                        
                        plt.xticks(x, [], rotation=0.45)
                    
                        ax1.bar(x, df, width=0.2,  align='center', color= ['#38D9D9', '#88D938', '#D6D938', '#6238D9'] , alpha=0.3,linewidth=2)

                        y_value=['{:,.0f}'.format(x).replace(",", " ") + 'PLN' for x in ax.get_yticks()]
                        ax.set_yticklabels(y_value)
                        
                        plt.show()
                        st.pyplot(plt)
                        #------------------------------------------------------------------------------------------------------

                        #---------------------------tabela z wariantami rat i kosztów-----------------------------------------
                        dfkoszty = kredyt1.Warianty_rat_i_kosztow_kredytowych_tabela()

                        x = "%"
                        x1 = "Rata"
                        x2 = "Koszt"

                        col1, col2, col3, col4, col5 = st.beta_columns([0.2,1,1,1,1])
                        with col1:
                            st.markdown(f'<p style= "color: #FFFFFF; opacity: 0;">{"PUSTE"}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style=";color:#fffff;font-size:17px;text-align:right;  padding-top:10px;">{x}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style=";color:#fffff;font-size:17px;text-align:right;  padding-top:10px;">{x1}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style=";color:#fffff;font-size:17px;text-align:right;  padding-top:10px;">{x2}</p>', unsafe_allow_html=True)

                        with col2: 
                            st.markdown(f'<p style= "text-align:center;">{"Twoje parametry"}</p>', unsafe_allow_html=True)
                            a = "{:,.2f} %".format(dfkoszty.iloc[0,0]*100)
                            st.markdown(f'<p class ="stopy-twoje">{a}</p>', unsafe_allow_html=True)
                            b = "{:,.2f} PLN".format(dfkoszty.iloc[0,1]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-twoje"">{b}</p>', unsafe_allow_html=True)
                            c = "{:,.2f} PLN".format(dfkoszty.iloc[0,2]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-twoje">{c}</p>', unsafe_allow_html=True)
                            
                        with col3:
                            st.markdown(f'<p style= "text-align:center;">{"Optymistyczny"}</p>', unsafe_allow_html=True)
                            d = dfkoszty.iloc[1,0]
                            st.markdown(f'<p class ="stopy-optymistyczny">{d}</p>', unsafe_allow_html=True)
                            e = "{:,.2f} PLN".format(dfkoszty.iloc[1,1]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-optymistyczny">{e}</p>', unsafe_allow_html=True)
                            f = "{:,.2f} PLN".format(dfkoszty.iloc[1,2]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-optymistyczny">{f}</p>', unsafe_allow_html=True)
                            
                        with col4:
                            st.markdown(f'<p style= "text-align:center;">{"Bazowyy"}</p>', unsafe_allow_html=True)
                            g = dfkoszty.iloc[2,0]
                            st.markdown(f'<p class ="stopy-bazowy">{g}</p>', unsafe_allow_html=True)
                            h = "{:,.2f} PLN".format(dfkoszty.iloc[2,1]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-bazowy">{h}</p>', unsafe_allow_html=True)
                            i = "{:,.2f} PLN".format(dfkoszty.iloc[2,2]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-bazowy">{i}</p>', unsafe_allow_html=True)
                            
                        with col5:
                            st.markdown(f'<p style= "text-align:center;">{"Pesymistyczny"}</p>', unsafe_allow_html=True)
                            j = dfkoszty.iloc[3,0]
                            st.markdown(f'<p class ="stopy-pesymistyczny">{j}</p>', unsafe_allow_html=True)
                            k = "{:,.2f} PLN".format(dfkoszty.iloc[3,1]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-pesymistyczny">{k}</p>', unsafe_allow_html=True)
                            l = "{:,.2f} PLN".format(dfkoszty.iloc[3,2]).replace(",", " ")
                            st.markdown(f'<p class ="stopy-pesymistyczny">{l}</p>', unsafe_allow_html=True)
                                    

                        st.write("")
                        down = "Ciesz się gdy rata jest niska, bądź gotowy na wariant pesymistyczny, jednak <b>kalkulacje odnośnie kosztów i optymalizacji</b> powinieneś opierać o <b>wariant bazowy</b>."
                        st.markdown(f'<p style= "background-color:rgba(225, 225, 255, 0.1);\
                                color:#fffff;\
                                font-size:17px;\
                                font-weight: 400;\
                                border-radius:5px;\
                                text-align:center;\
                                padding:20px 20px 20px 20px; ">{down}</p>', unsafe_allow_html=True) 
                        


                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.markdown(f'<p class="down-coment" style="padding-bottom:50px;">Nie unikaj ryzyka!<br> Staraj się je ograniczyć wybierając właściwy wariant</p>', unsafe_allow_html=True)


                        link = "https://financialmill.pl/posts/readpageKredytyHipoteczneKredytNaMiare/readpage.html"
                        st.markdown(f'<a role="button" class="btn-primary" target="_blank" href={link}>Lekcja nr. 4 KREDYT SZYTY NA MIARĘ </a>', unsafe_allow_html=True)


                #-------------------------------------------------------Sekcja nr.3 Nadpłaty--------------------------------------------------------------------------
                elif choice == 'Nadpłacanie kredytu':
                    
                    link = "https://financialmill.pl/posts/readpageKredytyHipoteczneNadplaty/readpage.html"
                    st.markdown(f'<a role="button" class="btn-primary" href={link}>Lekcja nr. 4 NADPŁACANIE KREDYTU</a>', unsafe_allow_html=True)
                    
                    up = "Jednym ze sposobów na zmniejszenie kosztów kredytu są nadpłaty.<br>Sprawdź ile możesz dzięki nim zaoszczędzić."
                    st.markdown(f'<h2 style= "background-color:rgba(0, 178, 255, 0.15);\
                                color:#fffff;\
                                border-radius:5px;\
                                text-align:center;\
                                padding:20px 20px 20px 20px; ">{up}</h2>', unsafe_allow_html=True) 
                    
                    st.markdown(f'<p class="nazwyParametrow">{"Parametry kredytu"}</p>', unsafe_allow_html=True)
                    st.write("")

                    col1, col2, col3, col4, col5 =  st.beta_columns([1.2,0.9,0.8,0.9,0.9])

                    with col1:
                        wielkosc = st.number_input('Kwota kredytu*', min_value=0, step=50000,value = Tabela['wielkosc'][len(Tabela)-1], help='Podaj kwotę kredytu, o którą chciałbyś wnioskować (wnioskowałeś). Chodzi o część pożyczoną z banku, nie uwzględniaj wkładu własnego.')
                    with col2:
                        okres = st.number_input('Na ile lat?*', min_value=0, step=10, max_value=30,value = Tabela['okres'][len(Tabela)-1], help = 'Określ czas trwania kredytu, wyrażony w latach.')
                    with col3:
                        kiedy = st.date_input('Kiedy kredyt?', min_value=datetime.today(), help='Nie zdecydowałeś się jeszcze na zaciągnięcie kredytu? Podaj szcunkową datę jego startu. Jeśli już jesteś kredytobiorcą, wybierz dzisiejszą datę. W polu "Kwota kredytu" wpisz kapitał pozostały do spłaty, a w "Na ile lat?" wpisz ile lat pozostało Ci do spłaty.')
                    with col4:
                        marza = st.number_input('Marża banku*', min_value=0.00, format="%.2f", step=0.5,value = Tabela['marza'][len(Tabela)-1], help="Podaj marżę banku wyrażoną w procentach. Przykład: Marza = 2,5% wpisz do kalkulatora 2.5")
                    with col5:
                        wibor = st.number_input('WIBOR 3M*', min_value=0.1, format="%.2f",value = Tabela['wibor'][len(Tabela)-1], help="Domyślnie ustawiony jest aktualny poziom WIBOR 3M. Pamiętaj, że możesz go zmienić według własnych potrzeb.")
                    
                    
                    st.write("")
                    st.markdown(f'<p class="nazwyParametrow">{"Parametry nadpłat"}</p>', unsafe_allow_html=True)
                    st.write("")
                    col1, col2, col3 =  st.beta_columns(3)
                    with col1:
                        nadplata = st.number_input('Nadpłata*', min_value=0, step=50,value = int(Tabela['nadplata'][len(Tabela)-1]), help="Podaj ile szacunkowo jesteś w stanie nadpłacać swój kredyt każdego miesiąca.")
                    with col2:
                        kiedynad = st.number_input('Od którego roku?', min_value=0, step=1,value = int(Tabela['kiedynad'][len(Tabela)-1]), help="Zdecyduj od kiedy zaczniesz nadpłątę. 0 - od początku kredytu, 1 - po roku, 2 - po 2 latach itd.")
                    with col3:
                        indn = st.number_input('Indeksacja', min_value=0.00, format="%.2f", step=0.5,value = Tabela['indn'][len(Tabela)-1], help="Indeksacja to coroczny, procentowy wzrost nadpłat. Zazwyczaj zależy on od wysokości pensji. Polacy średniorocznie zwiększają swoje przychody o 6%. Każdy przypadek jest jednak nieco inny.  Zalecamy przyjąc poziom indeksacji między 4%, a 8%. ")
                    
                    if st.button("Oblicz"):
                        get_data().append({'wielkosc': wielkosc,'okres':okres,'marza':marza,'wibor':wibor,"kiedy": kiedy,'nadplata':nadplata,'kiedynad':kiedynad,'indn':indn,'skladka':Tabela['skladka'][len(Tabela)-1],'procent': Tabela['procent'][len(Tabela)-1],'inds':Tabela['inds'][len(Tabela)-1],'kiedyskl':Tabela['kiedyskl'][len(Tabela)-1],'procentdyw':Tabela['procentdyw'][len(Tabela)-1]})     
                    
                        lister = get_data()
                        Tabela = pd.DataFrame(lister)

                        if Tabela['nadplata'][len(Tabela)-1]>0 :

                            st.markdown(f'<p style= "text-align:center; font-weight:600; font-size:18px;">{"Wykres zestawia kredyt spłacany normalnie oraz kredyt z nadpłatami"}</p>', unsafe_allow_html=True)
                            
                            
                            kredyt1 = Parametry_kredytu(Tabela["wielkosc"][len(Tabela)-1],Tabela["kiedy"][len(Tabela)-1], Tabela["okres"][len(Tabela)-1], Tabela["wibor"][len(Tabela)-1], Tabela["marza"][len(Tabela)-1],Tabela["nadplata"][len(Tabela)-1],Tabela["indn"][len(Tabela)-1],Tabela["kiedynad"][len(Tabela)-1],Tabela["skladka"][len(Tabela)-1],Tabela["procent"][len(Tabela)-1],Tabela["inds"][len(Tabela)-1],Tabela["kiedyskl"][len(Tabela)-1], Tabela["procentdyw"][len(Tabela)-1])

                            #------------------------------NAdpłaty wykres-------------------------------------------------

                            b = kredyt1.Oszczednosc_nadplaty_wykres()

                            fig, ax = plt.subplots()
                            fig.patch.set_facecolor('#0E1117')
                            fig.patch.set_alpha(0)
                            
                            x = b.DataKalendarzowa
                            y = b.KapitałDoSpłaty
                            y1 = b.KapitałDoSpłatyNormalnie
                            line = ax.plot(x, y, color = '#00B2FF', linewidth=0.5)
                            ax.plot(x,y1, color = 'white', linewidth=0.5)
                            
                            ax.set_facecolor('#0E1117')
                            ax.patch.set_alpha(0)
                            ax.spines['top'].set_alpha(0)
                            ax.spines['right'].set_alpha(0)
                            ax.spines['bottom'].set_color('white')
                            ax.spines['left'].set_color('white')
                            ax.tick_params(colors='white', which='both')
                            ax.grid(axis='y',linestyle='--',linewidth=0.3)

                            y_value=['{:,.0f}'.format(x).replace(",", " ") + 'PLN' for x in ax.get_yticks()]
                            ax.set_yticklabels(y_value)

                            plt.xticks(fontsize=5)
                            plt.yticks(fontsize=5)

                            line = plt.fill_between(x, y, 0, color='#00B2FF', alpha=0.07)
                            st.pyplot(plt)

                            st.write("")
                            st.write("")
                            
                            #------------------------------------------OUTPUT nadpłacanie kredytu----------------------------------------------------
                            
                            dfNd = kredyt1.Oszczednosc_nadplaty_dane()
                            st.write("")
                            st.write("")
                            st.write("")

                            x = "Koszt kredyt normalnie"
                            x1 = "Koszt nadpłacanego kredytu"
                            x2 = "Oszczędność razem"

                            y = "Dzień spłaty normalnie"
                            y1 = "Dzień spłaty z nadpłatami"
                            y2 = "Oszczędność czasu"

                            col1, col2 = st.beta_columns([1,1])
                            
                            with col1:      
                                a = "{:,.2f} PLN".format(dfNd.iloc[0,0]).replace(",", " ")
                                st.markdown(f'<p class = "nadplaty-contenery"><b>{x}</b> <br>{a}</p>', unsafe_allow_html=True)
                                c = "{:,.2f} PLN".format(dfNd.iloc[1,0]).replace(",", " ")
                                st.markdown(f'<p class = "nadplaty-contenery"><b>{x1}</b> <br>{c}</p>', unsafe_allow_html=True)
                                e = "{:,.2f} PLN".format(dfNd.iloc[2,0]).replace(",", " ")
                                st.markdown(f'<p class = "nadplaty-contenery"><b>{x2}</b> <br>{e}</p>', unsafe_allow_html=True)
                            
                                
                            with col2:    
                                b = dfNd.iloc[0,1].strftime('%d-%m-%Y')
                                st.markdown(f'<p class = "nadplaty-contenery"><b>{y}</b> <br>{b}</p>', unsafe_allow_html=True)
                                d = dfNd.iloc[1,1].strftime('%d-%m-%Y')
                                st.markdown(f'<p class = "nadplaty-contenery"><b>{y1}</b> <br>{d}</p>', unsafe_allow_html=True)
                                f = dfNd.iloc[2,1]
                                g = dfNd.iloc[2,2] 
                                st.markdown(f'<p class = "nadplaty-contenery"><b>{y2}</b> <br>{f} lat i {g} ms.</p>', unsafe_allow_html=True)
                                
                    
                            st.write("")
                            st.write("")
                            st.write("")
                        
                            down = "<b>Nadpłacanie kredytu</b> to tak jakby wziąć kredyt na <b>krótszy okres</b>. Pozostawiamy sobie jendak pewną elastyczność, ponieważ gdy <b>rata kredytu wzrośnie</b> w najgorszym przypadku <b>nie dokonamy nadpłaty</b>."
                            st.markdown(f'<p style="background-color:rgba(225, 225, 225, 0.15);\
                                                        color:#fffff;font-size:16px;border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 15px 30px 15px 30px;\
                                                            ">{down}</p>', unsafe_allow_html=True)

                            st.write("")
                            st.markdown('<p class="down-coment">Nadpłaty to całkiem niezłe, lecz nie jedyne rozwiązanie.</br> Przejdź do następnego kroku i sprawdź jak jeszcze możesz zaoszczędzić!</p>', unsafe_allow_html=True)



                #--------------------------------------------Sekcja nr. 4 bilansowanie kredytu-----------------------------------------------------------
                elif choice == 'Bilansowanie kredytu':

                    link = "https://financialmill.pl/posts/readpageKredytyHipoteczneBilansowanie/readpage.html"
                    st.markdown(f'<a role="button" class="btn-primary" href={link}>Lekcja nr. 5 BILANSOWANIE KREDYTU</a>', unsafe_allow_html=True)

                    up = "Kolejnym sposobem na optymalizację kosztów kredytu jest bilansowanie.<br>Polego ona na regularnym inwestowaniu środków w celu jednorazowej spłaty kapitału"
                    st.markdown(f'<h2 style="background-color:rgba(0, 225, 117, 0.15);\
                                                        color:#fffff;\
                                                        border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 20px 20px 10px 20px;\
                                                            ">{up}</p>', unsafe_allow_html=True) 
                    
                    st.markdown(f'<p class="nazwyParametrow">{"Parametry kredytu"}</p>', unsafe_allow_html=True)
                    col1, col2, col3, col4, col5 =  st.beta_columns([1.2,0.9,0.8,0.9,0.9])

                    with col1:
                        wielkosc = st.number_input('Kwota kredytu*', min_value=0, step=50000,value = Tabela['wielkosc'][len(Tabela)-1], help='Podaj kwotę kredytu, o którą chciałbyś wnioskować (wnioskowałeś). Chodzi o część pożyczoną z banku, nie uwzględniaj wkładu własnego.')
                    with col2:
                        okres = st.number_input('Na ile lat?*', min_value=0, step=10, max_value=30,value = Tabela['okres'][len(Tabela)-1], help = 'Określ czas trwania kredytu, wyrażony w latach.')
                    with col3:
                        kiedy = st.date_input('Kiedy kredyt?', min_value=datetime.today(), help='Nie zdecydowałeś się jeszcze na zaciągnięcie kredytu? Podaj szcunkową datę jego startu. Jeśli już jesteś kredytobiorcą, wybierz dzisiejszą datę. W polu "Kwota kredytu" wpisz kapitał pozostały do spłaty, a w "Na ile lat?" wpisz ile lat pozostało Ci do spłaty.')
                    with col4:
                        marza = st.number_input('Marża banku*', min_value=0.00, format="%.2f", step=0.5,value = Tabela['marza'][len(Tabela)-1], help="Podaj marżę banku wyrażoną w procentach. Przykład: Marza = 2,5% wpisz do kalkulatora 2.5")
                    with col5:
                        wibor = st.number_input('WIBOR 3M', min_value=0.1, format="%.2f",value = Tabela['wibor'][len(Tabela)-1], help="Domyślnie ustawiony jest aktualny poziom WIBOR 3M. Pamiętaj, że możesz go zmienić według własnych potrzeb.")
                    
                    st.write("")
                    st.markdown(f'<p class="nazwyParametrow">Parametry systematycznego inwestowania</p>', unsafe_allow_html=True)
                    col1, col2, col3, col4 =  st.beta_columns(4)

                    with col1:
                        skladka = st.number_input('Składka*',min_value=0, step=50,value = Tabela['skladka'][len(Tabela)-1], help="Wpisz ile złotych jesteś w stanie odłożyc miesięcznie w celu oszczędzania długoterminowego (10-30lat)")
                    with col2:
                        kiedyskl = st.number_input('Od kiedy?',min_value=0, step=1,value = Tabela['kiedyskl'][len(Tabela)-1], help='Zdecyduj od kiedy zaczniesz bilansowanie. 0 - od teraz, 1 - za rok, 2 - za 2 lata itd.')      
                    with col3:
                        procent = st.number_input('Oprocentowanie składki*',min_value=0.00,value = Tabela['procent'][len(Tabela)-1], step=0.5, help="Podaj średnie oprocentowanie netto twoich oszczędności. Pamiętaj, że zależy ono od wielu czynników, m.in. akcpetowalnego poziomu ryzyka, horyzontu czasowego czy posiadanych instrumentów finansowych. Aby bilansowanie mogło być efektywne powinieneś przyjąć oprocentowanie składek na poziomie zbliżonym do oprocentowania kredytu (WIBOR 3M + marża).")    
                    with col4:
                        inds = st.number_input('Indeksacja',min_value=0.00, step=0.5,value = Tabela['inds'][len(Tabela)-1], help="Indeksacja to coroczny, procentowy wzrost nadpłat. Zazwyczaj zależy on od wysokości pensji. Polacy średniorocznie zwiększają swoje przychody o 6%. Każdy przypadek jest jednak nieco inny.  Zalecamy przyjąc poziom indeksacji między 4%, a 8%.")
                    
                    if st.button("Oblicz"):
                        get_data().append({'wielkosc': wielkosc,'okres': okres, 'marza' :marza, 'wibor' :wibor, "kiedy": kiedy,'nadplata':Tabela['nadplata'][len(Tabela)-1],'kiedynad':Tabela['kiedynad'][len(Tabela)-1],'indn':Tabela['indn'][len(Tabela)-1],'skladka':skladka,'kiedyskl':kiedyskl,'procent':procent,'inds':inds,'procentdyw':Tabela['procentdyw'][len(Tabela)-1]})     
                    
                        lister = get_data()
                        Tabela = pd.DataFrame(lister)

                        if Tabela['skladka'][len(Tabela)-1]>0 and Tabela['procent'][len(Tabela)-1]>0.000:
                            
                            kredyt1 = Parametry_kredytu(Tabela["wielkosc"][len(Tabela)-1],Tabela["kiedy"][len(Tabela)-1], Tabela["okres"][len(Tabela)-1], Tabela["wibor"][len(Tabela)-1], Tabela["marza"][len(Tabela)-1],Tabela["nadplata"][len(Tabela)-1],Tabela["indn"][len(Tabela)-1],Tabela["kiedynad"][len(Tabela)-1],Tabela["skladka"][len(Tabela)-1],Tabela["procent"][len(Tabela)-1],Tabela["inds"][len(Tabela)-1],Tabela["kiedyskl"][len(Tabela)-1], Tabela["procentdyw"][len(Tabela)-1])
                            st.markdown(f'<p style= "text-align:center; font-weight:600; font-size:18px;">{"Wykres ilustruje kapitał kredytowy oraz wartość Twojej regularnej inwestycji"}</p>', unsafe_allow_html=True)
                            
                            #----------------------Wykres bilansowanie-----------------------------------------------------
                            b = kredyt1.Oszczednosc_na_Bilansowaniu_wykres()

                            fig, ax = plt.subplots()
                            fig.patch.set_facecolor('#00E175')
                            fig.patch.set_alpha(0) 
                                
                            x = b.DataKalendarzowa
                            y = b.Wartość_Środków
                            y1 = b.KapitałDoSpłaty
                            line = ax.plot(x, y, color = '#00E175', linewidth=0.5)
                            ax.plot(x,y1, color = 'white', linewidth=0.5)
                                
                            ax.set_facecolor('#0E1117')
                            ax.patch.set_alpha(0)
                            ax.spines['top'].set_alpha(0)
                            ax.spines['right'].set_alpha(0)
                            ax.spines['bottom'].set_color('white')
                            ax.spines['left'].set_color('white')
                            ax.tick_params(colors='white', which='both')
                            ax.grid(axis='y',linestyle='--',linewidth=0.3)

                            y_value=['{:,.0f}'.format(x).replace(",", " ") + 'PLN' for x in ax.get_yticks()]
                            ax.set_yticklabels(y_value)

                            plt.xticks(fontsize=5)
                            plt.yticks(fontsize=5)

                            line = plt.fill_between(x, y, 0, color='#00E175', alpha=0.07)
                            st.pyplot(plt)   
                            
                            
                            st.write("")
                            st.write("")
                            
                            #-------------------------------OUTPUT dla bilansowania kredytu---------------------------
                            col1, col2, = st.beta_columns([1,1])
                            
                            dfB = kredyt1.Oszczednosc_na_Bilansowaniu_dane()

                            x = "Koszt kredytu normalnie"
                            x1 = "Zysk z inwestycji"
                            x2 = "Oszczędność na spłacie"
                            x3 = "Oszczędność całkowita"

                            y = "Dzień spłaty normalnie"
                            y1 = "Dzień spłaty bilansowanie"
                            y2 = "Oszczędność czasu"
                            

                            with col1:
                                
                                a = "{:,.2f} PLN".format(dfB.iloc[0,0]).replace(",", " ")
                                st.markdown(f'<p class ="bilansowanie-contenery"><b>{x}</b></br>{a}</p>', unsafe_allow_html=True)
                                b = "{:,.2f} PLN".format(dfB.iloc[0,1]).replace(",", " ")
                                st.markdown(f'<p class ="bilansowanie-contenery"><b>{x1}</b></br>{b}</p>', unsafe_allow_html=True)
                                c = "{:,.2f} PLN".format(dfB.iloc[0,2]).replace(",", " ")
                                st.markdown(f'<p class ="bilansowanie-contenery"><b>{x2}</b></br>{c}</p>', unsafe_allow_html=True)
                                d = "{:,.2f} PLN".format(dfB.iloc[0,3]).replace(",", " ") 
                                st.markdown(f'<p class ="bilansowanie-contenery"><b>{x3}</b></br>{d}</p>', unsafe_allow_html=True)
                                    
                            with col2:
                                e = dfB.iloc[2,0].strftime('%d-%m-%Y')
                                st.markdown(f'<p class ="bilansowanie-contenery"><b>{y}</b></br>{e}</p>', unsafe_allow_html=True)
                                f = dfB.iloc[2,1].strftime('%d-%m-%Y')
                                st.markdown(f'<p class ="bilansowanie-contenery"><b>{y1}</b></br>{f}</p>', unsafe_allow_html=True)
                                g = dfB.iloc[2,2]
                                h = dfB.iloc[2,3]
                                st.markdown(f'<p class ="bilansowanie-contenery""><b>{y2}</b></br>{g} lat i {h} ms.</p>', unsafe_allow_html=True)
                                    

                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")

                            left = "1. Nadpłacamy kiedy chcemy.<br> 2. Oszczędność jest równa oprocentowaniu kredytu.<br> 3. Nadpłaty możemy rozpocząć dopiero w momencie zaciągnięcia kredytu. Bywa również, że banki obarczają nadpłaty dodatkową prowizją w pierwszym roku kredytu.<br> <br>4. Nie mamy możliwości odzyskania nadpłat. "
                            right = "1. Odkładamy regularnie, co miesiąc lub kwartał. <br> <br> 2. Oszczędność jest wypadkową stopy zwrotu portfela <br> i czasu spłaty kredytu. <br> <br> 3. Możemy rozpocząć inwestowanie jeszcze przed zaciągnięciem kredytu. <br><br> 4. Zbierane środki mogą ostatecznie zmienić swoje przeznaczenie."
                            col1, col2 = st.beta_columns(2)
                            with col1:
                                st.markdown("<h1 style='text-align: center; color: white;'>Nadpłacanie</h1>", unsafe_allow_html=True)
                                st.write("")
                                st.markdown(f'<p class ="bilansowanie-left_cont">{"1. Nadpłacamy kiedy chcemy.<br><br> 2. Oszczędność jest równa oprocentowaniu kredytu.<br><br> 3. Nadpłaty możemy rozpoacząć dopiero w momencie zaciągnięcia kredytu. Bywa również, że banki obarczają nadpłaty dodatkową prowizją w pierwszym roku kredytu. <br> <br> 4. Nie mamy możliwości odzyskania nadpłat. "}</p>', unsafe_allow_html=True)
                            with col2:
                                st.markdown("<h1 style='text-align: center; color: white;'>Bilansowanie</h1>", unsafe_allow_html=True)
                                st.write("")
                                st.markdown(f'<p style="background-color:rgba(0, 225, 117, 0.15);color:#fffff;font-size:16px;border-radius:20px;text-align:left;padding: 27.5px 15px 27.5px 35px;">{right}</p>', unsafe_allow_html=True)
                            
                            st.write("")
                            st.write("")
                            st.write("")

                            down = "Dzięki dodatkowej elastyczności jaką daje nam bilanoswanie w postaci <b>dowolnego wykorzystania uzbieranych środków</b> otwieramy sobie drzwi do jednej z najlepszych form optymalizacji kredytu. </br><b>Sparwdź punkt 5. Kredyt spałca się sam?<b>"

                            st.markdown(f'<p style="background-color:rgba(225, 225, 225, 0.1);\
                                                        color:#fffff;font-size:16px;border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 15px 30px 15px 30px;\
                                                            ">{down}</p>', unsafe_allow_html=True)

                #-------------------------------------------------------------------------------SEKCJA nr. 5 -----------------------------------------------------------------------------------        
                elif choice == 'Kredyt spłaca sie sam?':

                    link = "https://financialmill.pl/posts/readpageKredytyHipoteczneDywidenda/readpage.html"
                    st.markdown(f'<a role="button" class="btn-primary" href={link}>Lekcja nr. 6 GOTOWY NA WSZYSTKO</a>', unsafe_allow_html=True)
                    
                    up = "Ostatnią ciekawą formą optymalizacji kredytu jest możliwość zbudowania poduszki<br>finansowej z pasywnym przychodem inwestycyjnym, którego dywidenda pokryje ratę Twojego kredytu"
                    st.markdown(f'<h2 style="background-color:rgba(0, 255, 117, 0.1);\
                                                        color:#fffff;\
                                                        border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 15px 30px 15px 30px;\
                                                            ">{up}</h2>', unsafe_allow_html=True)
                        
                    st.markdown(f'<p class="nazwyParametrow">{"Parametry kredytu"}</p>', unsafe_allow_html=True)
                    col1, col2, col3, col4, col5 =  st.beta_columns([1.2,0.9,0.8,0.9,0.9])
                    
                    with col1:
                        wielkosc = st.number_input('Kwota kredytu*', min_value=0, step=50000,value = Tabela['wielkosc'][len(Tabela)-1],help='Podaj kwotę kredytu, o którą chciałbyś wnioskować (wnioskowałeś). Chodzi o część pożyczoną z banku, nie uwzględniaj wkładu własnego.')
                    with col2:
                        okres = st.number_input('Na ile lat?*', min_value=0, step=10, max_value=30,value = Tabela['okres'][len(Tabela)-1], help = 'Określ czas trwania kredytu, wyrażony w latach.')
                    with col3:
                        kiedy = st.date_input('Kiedy kredyt?', min_value=datetime.today(), help='Nie zdecydowałeś się jeszcze na zaciągnięcie kredytu? Podaj szcunkową datę jego startu. Jeśli już jesteś kredytobiorcą, wybierz dzisiejszą datę. W polu "Kwota kredytu" wpisz kapitał pozostały do spłaty, a w "Na ile lat?" wpisz ile lat pozostało Ci do spłaty.')
                    with col4:
                        marza = st.number_input('Marża banku*', min_value=0.00, format="%.2f", step=0.5,value = Tabela['marza'][len(Tabela)-1], help="Podaj marżę banku wyrażoną w procentach. Przykład: Marza = 2,5% wpisz do kalkulatora 2.5")
                    with col5:
                        wibor = st.number_input('WIBOR 3M', min_value=0.1, format="%.2f",value = Tabela['wibor'][len(Tabela)-1], help="Domyślnie ustawiony jest aktualny poziom WIBOR 3M. Pamiętaj, że możesz go zmienić według własnych potrzeb.")
                    
                    st.write("")
                    st.markdown(f'<p class="nazwyParametrow">Parametry systematycznego inwestowania</p>', unsafe_allow_html=True)

                    col1, col2, col3, col4 =  st.beta_columns(4)

                    with col1:
                        skladka = st.number_input('Składka*',min_value=0, step=50,value = Tabela['skladka'][len(Tabela)-1], help="Wpisz ile złotych jesteś w stanie odłożyc miesięcznie w celu oszczędzania długoterminowego (10-30lat)?")
                    with col2:
                        kiedyskl = st.number_input('Od kiedy?',min_value=0, step=1,value = Tabela['kiedyskl'][len(Tabela)-1], help='Zdecyduj od kiedy zaczniesz bilansowanie. 0 - od teraz, 1 - za rok, 2 - za 2 lata itd.')      
                    with col3:
                        procent = st.number_input('Oprocentowanie składki*',min_value=0.00,value = Tabela['procent'][len(Tabela)-1], step=0.5, help="Podaj średnie oprocentowanie netto twoich oszczędności. Pamiętaj, że zależy ono od wielu czynników, m.in. akcpetowalnego poziomu ryzyka, horyzontu czasowego czy posiadanych instrumentów finansowych. Aby bilansowanie mogło być efektywne powinieneś przyjąć oprocentowanie składek na poziomie zbliżonym do oprocentowania kredytu (WIBOR 3M + marża).")    
                    with col4:
                        inds = st.number_input('Indeksacja',min_value=0.00, step=0.5,value = Tabela['inds'][len(Tabela)-1], help="Indeksacja to coroczny, procentowy wzrost nadpłat. Zazwyczaj zależy on od wysokości pensji. Polacy średniorocznie zwiększają swoje przychody o 6%. Każdy przypadek jest jednak nieco inny.  Zalecamy przyjąc poziom indeksacji między 4%, a 8%.")
                    
                    st.markdown("<h2 style='text-align: left; color: white; font-size:25px; font-weight:600;'>Parametr dywidendy</h2>", unsafe_allow_html=True)
                    
                    col1, col2 = st.beta_columns([0.5,1.5])
                    
                    with col1:
                        procentdyw = st.number_input('Oczekiwana dywidenda*', min_value=0.00, step=0.5, value = Tabela['procentdyw'][len(Tabela)-1], help="Dywidenda to inaczej udział w zysku. Na dywidendę możesz liczyć inwestując w akcje, a w szczególności spółki dywidendowe. Możesz zainwestować również w nieruchomość, a zysk z najmu będzie Twoją dywidendą. Jeśli masz jeszcze więcej czasu możesz zainwestować we własny biznes, który również może przynieść Ci solidną dywidendę. Na potrzeby kalkulacji zalecamy przyjąć dywidendę na poziomie od 4% do 8%.")
                    
                        
                    if st.button("Oblicz"):
                        get_data().append({'wielkosc':  wielkosc,'okres': okres, 'marza' :marza, 'wibor' :wibor, "kiedy": kiedy,'nadplata':Tabela['nadplata'][len(Tabela)-1],'kiedynad':Tabela['kiedynad'][len(Tabela)-1],'indn':Tabela['indn'][len(Tabela)-1],'skladka':skladka,'kiedyskl':kiedyskl,'procent':procent,'inds':inds,'procentdyw':procentdyw})
                        
                        lister = get_data()
                        Tabela = pd.DataFrame(lister)

                        if Tabela['skladka'][len(Tabela)-1]>0 and Tabela['procentdyw'][len(Tabela)-1]>0.00 and Tabela['procent'][len(Tabela)-1]>0.00: 
                            kredyt1 = Parametry_kredytu(Tabela["wielkosc"][len(Tabela)-1],Tabela["kiedy"][len(Tabela)-1], Tabela["okres"][len(Tabela)-1], Tabela["wibor"][len(Tabela)-1], Tabela["marza"][len(Tabela)-1],Tabela["nadplata"][len(Tabela)-1],Tabela["indn"][len(Tabela)-1],Tabela["kiedynad"][len(Tabela)-1],Tabela["skladka"][len(Tabela)-1],Tabela["procent"][len(Tabela)-1],Tabela["inds"][len(Tabela)-1],Tabela["kiedyskl"][len(Tabela)-1], Tabela["procentdyw"][len(Tabela)-1])
                            #wykres

                            check = kredyt1.Czy_kredyt_moze_sie_splacic_sam()

                            if check > 0:  
                                
                                st.markdown(f'<p style= "text-align:center; font-weight:600; font-size:18px;">{"Wykres ilustruje kapitał pozostały do spłaty oraz wartość środków"}</p>', unsafe_allow_html=True)
                            
                                b = kredyt1.Kiedy_Kredyt_Splaca_Sie_Sam_Wykres() 

                                fig, ax = plt.subplots()
                                fig.patch.set_facecolor('#00E175')
                                fig.patch.set_alpha(0) 
                                    
                                x = b.DataKalendarzowa
                                y = b.WartośćŚrodków 
                                y1 = b.KapitałDoSpłaty
                                y2 = b.linia
                                line = ax.plot(x, y, color = '#00E175', linewidth=0.5)
                                ax.plot(x,y2, color = '#00FF75', linewidth=0.5)

                                ax.plot(x,y1, color = 'white', linewidth=0.5)
                                
                                    
                                ax.set_facecolor('#0E1117')  
                                ax.patch.set_alpha(0)
                                ax.spines['top'].set_alpha(0)
                                ax.spines['right'].set_alpha(0)
                                ax.spines['bottom'].set_color('white')
                                ax.spines['left'].set_color('white')
                                ax.tick_params(colors='white', which='both')
                                ax.grid(axis='y',linestyle='--',linewidth=0.3)

                                y_value=['{:,.0f}'.format(x).replace(",", " ") + 'PLN' for x in ax.get_yticks()]
                                ax.set_yticklabels(y_value)
                        
                                plt.xticks(fontsize=5)
                                plt.yticks(fontsize=5)

                                line = plt.fill_between(x, y, 0, color='#00E175', alpha=0.07)
                                plt.fill_between(x, y2, 0, color='#00E175', alpha=0.07)
                                st.pyplot(plt)

                                st.write("")
                                st.write("")
                                st.write("")

                                #-------------------Kredyt spłąca sie sam OUTPUT dane---------------------------
                                dfD = kredyt1.Kiedy_Kredyt_Splaca_Sie_Sam_Dane()
                                x = "Koszt kredytu normalnie"
                                x1 = "Zysk z inwestycji"
                                x2 = "Ilość rat pokrytych przez dywidendę"
                                x3 = "Wielkość rat pokrytych"

                                y = "Dzień spłaty normalnie"
                                y1 = "Kiedy dywidenda pokryje raty?"  
                                y2 = "Ile lat kredyt będzie spłacał się sam?"

                                

                                col1, col2 = st.beta_columns([1,1])    
                                    
                                with col1:
                                    
                                    a = "{:,.2f} PLN".format(dfD.iloc[0,0]).replace(",", " ")
                                    st.markdown(f'<p class ="sam-contenery"><b>{x}</b></br>{a}</p>', unsafe_allow_html=True)
                                    b = "{:,.2f} PLN".format(dfD.iloc[0,1]).replace(",", " ")
                                    st.markdown(f'<p class ="sam-contenery"><b>{x1}</b></br>{b}</p>', unsafe_allow_html=True)
                                    c = dfD.iloc[0,2]
                                    st.markdown(f'<p class ="sam-contenery"><b>{x2}</b></br>{c}</p>', unsafe_allow_html=True)
                                    d = "{:,.2f} PLN".format(dfD.iloc[0,3]).replace(",", " ") 
                                    st.markdown(f'<p class ="sam-contenery"><b>{x3}</b></br>{d}</p>', unsafe_allow_html=True)
                        
                                with col2: 
                                    e = dfD.iloc[1,0].strftime('%d-%m-%Y')
                                    st.markdown(f'<p class ="sam-contenery"><b>{y}</b></br>{e}</p>', unsafe_allow_html=True)
                                    f = dfD.iloc[1,1].strftime('%d-%m-%Y')
                                    st.markdown(f'<p class ="sam-contenery"><b>{y1}</b></br>{f}</p>', unsafe_allow_html=True)
                                    g = dfD.iloc[1,2]
                                    h = dfD.iloc[1,3]
                                    st.markdown(f'<p class ="sam-contenery"><b>{y2}</b></br>{g} lat i {h.astype(int)} ms.</p>', unsafe_allow_html=True)
                                
                    
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")

                                srodki = kredyt1.WartoscSrodkow()
                                srodki = "{:,.2f} PLN".format(dfD.iloc[0,1]).replace(",", " ")

                                up = f"Dzięki zaplanowanej strategii dywidendowej uda Ci się zaoszczędzić: <b>{srodki}</b> Dywidenda z tej kwoty pozwoli na opłacanie rat kredytu. Od tej chwili uwalniasz dodatkowe środki domowego budrzetu w postaci: <b>raty kredytu</b> oraz <b>comiesięcznych składek inwestycyjnych</b>, których dokonywałeś na poczet budowy portfela inwestycyjnego. "

                                st.markdown(f'<h2 style="background-color:rgba(255, 255, 255, 0.1);\
                                                        color:#fffff;border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 15px 25px 15px 25px;\
                                                            ">{up}</h2>', unsafe_allow_html=True)

                                
                                
                                st.markdown('<h1 style="position: relative; text-align: center; font-size: 50px; opacity:0.8; line-height: 100%;">Co dalej?</h2>', unsafe_allow_html=True)
                                
                                
                                left = "Możesz wynagrodzić się za lata oszczędzania, a wolne środki przeznaczyć na <b>koszty życia lub pasje</b>, na które wcześniej nie miałeś czasu."
                                right = "Możesz kontynuwać oszczędzanie np. do czasu w którym dywidenda <b>pokryje wszystkie Twoje wydatki</b>, co pozwoli Ci na spokojną emeryturę. "
                                col1, col2, = st.beta_columns(2)
                                with col1:
                                    st.markdown(f'<p style="font-size:100px; font-weight:900; text-align: center; background-color: rgba(0, 255, 117, 0.1); margin-bottom: -24px; border-radius: 20px 20px 0px 0px;">{"1"}</p>', unsafe_allow_html=True)
                                
                                    st.markdown(f'<h2 style="background-color:rgba(0, 255, 117, 0.1);font-size:17px;color:#fffff;border-radius:0px 0px 20px 20px;text-align:center;padding: 0px 15px 27.5px 15px;">{left}</h2>', unsafe_allow_html=True)
                                
                                with col2:
                                    st.markdown(f'<p style="font-size:100px; font-weight:900; text-align: center; background-color: rgba(0, 255, 117, 0.1); margin-bottom: -24px; border-radius: 20px 20px 0px 0px;">{"2"}</p>', unsafe_allow_html=True)
                                    st.markdown(f'<h2 style="background-color:rgba(0, 255, 117, 0.1);font-size:17px;color:#fffff;border-radius:0px 0px 20px 20px;text-align:center;padding: 0px 15px 27.5px 15px;">{right}</h2>', unsafe_allow_html=True)
                                
                                
                                
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")
                                down = "Nie jesteśmy w stane zaplanować wszystkiego w długim terminie z dokładnością do 1 PLN..."
                                st.markdown(f'<h2 style="background-color:rgba(255, 255, 255, 0.1);\
                                                        color:#fffff;border-radius:5px;\
                                                        text-align:center;\
                                                        padding: 15px 30px 15px 30px;\
                                                            ">{down}</h2>', unsafe_allow_html=True)
                                st.write("")
                                st.write("")
                                st.markdown(f'<p class="first_last-coment">Możemy jednak przyjąć pewną strategie</br>i zacząć ją realizować!</p>', unsafe_allow_html=True)

                            else:

                                st.write("")
                                
                                st.warning("Twoje parametry są zbyt niskie, żeby skorzystać z dywidendowej opcji. Zastanów się nad zwiększeniem parametrów. W szczególności wielkość składki lub wielkość indeksacji")
                                # st.markdown(f'<h2 style="background-color:rgba(255, 126, 126, 0.42);\
                                #                         border: 2px solid #FF0000;\
                                #                         color:#fffff; border-radius:5px;\
                                #                         text-align:center;\
                                #                         padding: 15px 30px 15px 30px;\
                                #                             ">{error}</h2>', unsafe_allow_html=True)
            else:
                
                ers = "Kod aktywacyjny jest nieprawidłowy lub wygasł. Zaloguj się i sprawdź kod lub jeśli jeszcze tego nie zrobiłeś zarejestruj się i korzystaj w pełni z naszych narzędzi premium."
                st.markdown(f'<h2 style="background-color:rgba(204, 229, 255, 0.70);\
                                                    color:#004085;\
                                                    border-radius:5px;\
                                                    text-align:center;\
                                                    padding: 20px 20px 10px 20px;\
                                                        ">{ers}<h2>', unsafe_allow_html=True)
                
                linktofm = "https://financialmill.pl/premium/index.php"
                st.markdown(f'<div style="text-align: center; margin-top:20px;"><a role="button" class="btn-primary" target="_blank" style="font-family: "Montserrat" href={linktofm}>Przejdź do strony</a></div>', unsafe_allow_html=True) 
                
if __name__ =='__main__':
                
    main()
    
    
    