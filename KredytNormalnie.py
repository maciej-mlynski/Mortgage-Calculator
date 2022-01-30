import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import numpy_financial as nf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from datetime import date, timedelta, datetime
import pickle as pkle
import os.path
import toml
import streamlit.components.v1 as components
import matplotlib.animation as animation
from dateutil.relativedelta import relativedelta






class Parametry_kredytu:
    def __init__(self,wielkosc,kiedy,okres,wibor,marza,nadplata,indn,kiedynad,skladka,procent,inds,kiedyskl, procentdyw):
        self.wielkosc = wielkosc #wielkość kredytu
        self.kiedy = kiedy #Kiedy brany jest kredyt, format: '01-01-2022'
        self.okres = okres #Na jak długo kredyt (w latach)
        self.wibor = wibor #Wibor w postaci ułamka = 0.021
        self.marza = marza #Marża banku w postaci ułamka
        #------------nadpłaty--------------
        
        self.nadplata = nadplata #Wielkość nadpłat
        self.indn = indn #Indeksacja nadpłat w skali roku - Ułamek
        self.kiedynad = kiedynad #Od kiedy zaczynamy nadpłaty. 0 - od początku, 1 - za rok, 2-za 2 lata...
        #----------bilansowanie-------- ----
        self.skladka = skladka #Wielkość comiesięcznej składki
        self.procent = procent #Średnioroczne oprocentowanie lokaty
        self.inds = inds #Indeksacja składek w skali roku - Ułamek
        self.kiedyskl = kiedyskl #Od kiedy zaczynamy składki, liczac od dnia bierzącego. 0 - Teraz, 1 - za rok...
        
        #---------dywidenda----------------
        self.procentdyw = procentdyw #Roczne oprocentowanie dywidendy

        #PARAMETRY KREDYTU
    
    def Oprocentowanie(self):
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        return "{:,.2f} %".format(oprocentowanie*100)

    def Rata_kredytu(self):
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        return "{:,.2f} PLN".format(rata).replace(",", " ")
    
    def Koszt_kredytu(self):
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        koszt = rata * self.okres * 12 - self.wielkosc
        
        return "{:,.2f} PLN".format(koszt).replace(",", " ")
    
    def Dzien_splaty_normalnie(self): 
        idx = pd.date_range(self.kiedy, periods=self.okres * 12+1, freq="M")
        fmt = "%d-%m-%Y"
        dzien = idx[-1].strftime(fmt)
        return dzien
    
        
    def Kapital_do_splaty(self):
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        
        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc

        miesiące = np.arange(self.okres*12)+1
        idx = pd.date_range(self.kiedy, periods=self.okres * 12, freq="M")
        
        
        df = pd.DataFrame(
        {
            'DataKalendarzowa':idx, 'Miesiąc' : miesiące, 'Rata' : rata
        })

        df.loc[0, 'RataOdsetkowa'] = rata1_odsetkowa
        df.loc[0, 'RataKapitałowa'] = rata - rata1_odsetkowa
        df.loc[0, 'KapitałDoSpłaty'] = self.wielkosc - df.loc[0, 'RataKapitałowa']
        


        for i in range(1, len(df)):
            df.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * df.loc[i-1, 'KapitałDoSpłaty']
            df.loc[i, 'RataKapitałowa'] = df.loc[i, 'Rata'] - df.loc[i, 'RataOdsetkowa']
            df.loc[i, 'KapitałDoSpłaty'] = df.loc[i-1, 'KapitałDoSpłaty'] - df.loc[i, 'RataKapitałowa'].cumsum()


        df = df['KapitałDoSpłaty'].round(2)
        #df = df[['DataKalendarzowa', 'KapitałDoSpłaty']]
        #df = df.rename(columns={'DataKalendarzowa':'index'}).set_index('index')
        
        return df
    def Kapital_do_splaty_daty(self):
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        
        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc

        miesiące = np.arange(self.okres*12)+1
        idx = pd.date_range(self.kiedy, periods=self.okres * 12, freq="M")
        
        
        df = pd.DataFrame(
        {
            'DataKalendarzowa':idx, 'Miesiąc' : miesiące, 'Rata' : rata
        })

        df.loc[0, 'RataOdsetkowa'] = rata1_odsetkowa
        df.loc[0, 'RataKapitałowa'] = rata - rata1_odsetkowa
        df.loc[0, 'KapitałDoSpłaty'] = self.wielkosc - df.loc[0, 'RataKapitałowa']
        


        for i in range(1, len(df)):
            df.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * df.loc[i-1, 'KapitałDoSpłaty']
            df.loc[i, 'RataKapitałowa'] = df.loc[i, 'Rata'] - df.loc[i, 'RataOdsetkowa']
            df.loc[i, 'KapitałDoSpłaty'] = df.loc[i-1, 'KapitałDoSpłaty'] - df.loc[i, 'RataKapitałowa'].cumsum()


        
        dfd = df['DataKalendarzowa']
        #df = df.rename(columns={'DataKalendarzowa':'index'}).set_index('index')
        
        return dfd

    def wykres_wibor(self):
        dfS = pd.read_csv('./wibor3m.csv', sep=',', usecols=['Data', 'Zamkniecie'])
        dfS['Zamkniecie'] = dfS['Zamkniecie']/100
        idx = pd.date_range('2000-01-31', periods=dfS['Zamkniecie'].count(), freq="M")
        dfS['idx'] = idx
        dfS = dfS[['idx','Zamkniecie']]
        
        return dfS

    def Warianty_rat_i_kosztow_kredytowych_wykres(self):
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        
        rata_dzis = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        rata_optym = -nf.pmt(0.0428/12, self.okres*12, self.wielkosc)
        rata_bazowa = -nf.pmt(0.0562/12, self.okres*12, self.wielkosc)
        rata_pesym = -nf.pmt(0.0696/12, self.okres*12, self.wielkosc)
        
        left = [rata_dzis, rata_optym, rata_bazowa, rata_pesym]
        data = [['Dzis', rata_dzis], ['w. optymistyczny', rata_optym], ['w. bazowy', rata_bazowa], ['w. pesymistyczny', rata_pesym]]
        df = pd.DataFrame(data, columns= ['Wariant', 'Rata'])

        return left

    def Warianty_rat_i_kosztow_kredytowych_tabela(self):
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        
        rata_dzis = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        rata_optym = -nf.pmt(0.0448/12, self.okres*12, self.wielkosc)
        rata_bazowa = -nf.pmt(0.0582/12, self.okres*12, self.wielkosc)
        rata_pesym = -nf.pmt(0.0716/12, self.okres*12, self.wielkosc)
        
        koszt_dzis = rata_dzis * self.okres *12 - self.wielkosc
        koszt_optym = rata_optym * self.okres *12 - self.wielkosc
        koszt_bazowy = rata_bazowa * self.okres *12 - self.wielkosc
        koszt_pesym = rata_pesym * self.okres *12 - self.wielkosc

        data = [['Dzis', oprocentowanie, rata_dzis, koszt_dzis], ['w.optymistyczny', '4.48%', rata_optym, koszt_optym], ['w.bazowy', '5.82%', rata_bazowa, koszt_bazowy], ['w.pesymistyczny', '7.16%',rata_pesym, koszt_pesym]]
        df = pd.DataFrame(data, columns= ['Wariant','Oprocentowanie', 'Rata', 'Koszt'])
        df = df.set_index('Wariant')
        
        return df
    
    
    #-------------------------Wykres nadpłaty i klasycznie----------------------------------------------------------------------


    def Oszczednosc_nadplaty_wykres(self):
        
        #---------------------wariant z nadpłatami------------------------------------------
        self.kiedy =self.kiedy.strftime('%d-%m-%Y')
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        
        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k
        współczynnik_kredytowy = rata1_odsetkowa/self.wielkosc
        


        miesiace = np.arange(self.okres*12+ile_ms_do_kredytu)+1
        idx = pd.date_range(date.today(), periods=self.okres*12+ile_ms_do_kredytu, freq="M")
        
        dfN = pd.DataFrame(
        {
            'DataKalendarzowa':idx, 'Miesiąc' : miesiace
        })
        
        mnożniki = np.arange(0,len(dfN))
        for i in range(0,29):
            dfN.loc[i*12:((i*12)+12), 'Mnożnik'] = mnożniki[i]
        dfN['Mnożnik'].values[dfN['Mnożnik'].values < 0] = 0
        
        dfN['MiesiąceKredyt'] = dfN['Miesiąc'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        
        dfN['Nadpłata'] = self.nadplata*(1+self.indn/100)**dfN['Mnożnik']
        dfN['Nadpłata'] = dfN['Nadpłata'].shift(self.kiedynad*12+ile_ms_do_kredytu)
        dfN['Rata'] = rata
        dfN['Rata'] = dfN['Rata'].shift(ile_ms_do_kredytu)
        
        dfN.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfN.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfN.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfN.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        if self.kiedynad == 0:

            for i in range(ile_ms_do_kredytu+1, len(dfN)):
                dfN.loc[i, 'RataOdsetkowa'] = współczynnik_kredytowy * dfN.loc[i-1, 'KapitałDoSpłaty']
                dfN.loc[i, 'RataKapitałowa'] = dfN.loc[i, 'Rata'] - dfN.loc[i, 'RataOdsetkowa']
                dfN.loc[i, 'KapitałDoSpłaty'] = dfN.loc[i-1, 'KapitałDoSpłaty'] - dfN.loc[i, 'RataKapitałowa'].cumsum() - dfN.loc[i, 'Nadpłata']

        else:    

            for i in range(ile_ms_do_kredytu+1, self.kiedynad*12+ile_ms_do_kredytu):
                dfN.loc[i, 'RataOdsetkowa'] = współczynnik_kredytowy * dfN.loc[i-1, 'KapitałDoSpłaty']
                dfN.loc[i, 'RataKapitałowa'] = dfN.loc[i, 'Rata'] - dfN.loc[i, 'RataOdsetkowa']
                dfN.loc[i, 'KapitałDoSpłaty'] = dfN.loc[i-1, 'KapitałDoSpłaty'] - dfN.loc[i, 'RataKapitałowa'].cumsum()

            for i in range(self.kiedynad*12+ile_ms_do_kredytu, len(dfN)):
                dfN.loc[i, 'RataOdsetkowa'] = współczynnik_kredytowy * dfN.loc[i-1, 'KapitałDoSpłaty']
                dfN.loc[i, 'RataKapitałowa'] = dfN.loc[i, 'Rata'] - dfN.loc[i, 'RataOdsetkowa']
                dfN.loc[i, 'KapitałDoSpłaty'] = dfN.loc[i-1, 'KapitałDoSpłaty'] - dfN.loc[i, 'RataKapitałowa'].cumsum() - dfN.loc[i, 'Nadpłata']

        
        #---------------------wariant klasyczny------------------------------------------
        
        df = pd.DataFrame(
        {
            'DataKalendarzowa':idx, 'Miesiąc' : miesiace, 'Rata' : rata
        })

        df.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        df.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        df.loc[ile_ms_do_kredytu, 'KapitałDoSpłatyNormalnie'] = self.wielkosc - df.loc[ile_ms_do_kredytu, 'RataKapitałowa']
        


        for i in range(ile_ms_do_kredytu+1, len(df)):
            df.loc[i, 'RataOdsetkowa'] = współczynnik_kredytowy * df.loc[i-1, 'KapitałDoSpłatyNormalnie']
            df.loc[i, 'RataKapitałowa'] = df.loc[i, 'Rata'] - df.loc[i, 'RataOdsetkowa']
            df.loc[i, 'KapitałDoSpłatyNormalnie'] = df.loc[i-1, 'KapitałDoSpłatyNormalnie'] - df.loc[i, 'RataKapitałowa'].cumsum()

                
        #---------------------porównanie nadplat i klasycznie----------------------------
        
        pozycja_splaty_indx = dfN.index[dfN['KapitałDoSpłaty']>0][-1]+1
        
        
        dfNadplaty = pd.concat([dfN[['DataKalendarzowa', 'KapitałDoSpłaty']],df['KapitałDoSpłatyNormalnie']], axis=1, join='inner')
        dfNadplaty['KapitałDoSpłaty'] = dfNadplaty['KapitałDoSpłaty'].iloc[:pozycja_splaty_indx]

        return dfNadplaty


    def Oszczednosc_nadplaty_dane(self):
        
        #---------------------wariant z nadpłatami------------------------------------------
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)
        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        
        
        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k
        współczynnik_kredytowy = rata1_odsetkowa/self.wielkosc

        miesiace = np.arange(self.okres*12+ile_ms_do_kredytu)+1
        idx = pd.date_range(date.today(), periods=self.okres*12+ile_ms_do_kredytu, freq="M")
        
        dfN = pd.DataFrame(
        {
            'DataKalendarzowa':idx, 'Miesiąc' : miesiace
        })
        
        mnożniki = np.arange(0,len(dfN))
        for i in range(0,29):
            dfN.loc[i*12:((i*12)+12), 'Mnożnik'] = mnożniki[i]
        dfN['Mnożnik'].values[dfN['Mnożnik'].values < 0] = 0
        
        dfN['MiesiąceKredyt'] = dfN['Miesiąc'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        
        dfN['Nadpłata'] = self.nadplata*(1+self.indn/100)**dfN['Mnożnik']
        dfN['Nadpłata'] = dfN['Nadpłata'].shift(self.kiedynad*12+ile_ms_do_kredytu)
        dfN['Rata'] = rata
        dfN['Rata'] = dfN['Rata'].shift(ile_ms_do_kredytu)
        
        dfN.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfN.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfN.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfN.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        if self.kiedynad == 0:

            for i in range(ile_ms_do_kredytu+1, len(dfN)):
                dfN.loc[i, 'RataOdsetkowa'] = współczynnik_kredytowy * dfN.loc[i-1, 'KapitałDoSpłaty']
                dfN.loc[i, 'RataKapitałowa'] = dfN.loc[i, 'Rata'] - dfN.loc[i, 'RataOdsetkowa']
                dfN.loc[i, 'KapitałDoSpłaty'] = dfN.loc[i-1, 'KapitałDoSpłaty'] - dfN.loc[i, 'RataKapitałowa'].cumsum() - dfN.loc[i, 'Nadpłata']

        else:    

            for i in range(ile_ms_do_kredytu+1, self.kiedynad*12+ile_ms_do_kredytu):
                dfN.loc[i, 'RataOdsetkowa'] = współczynnik_kredytowy * dfN.loc[i-1, 'KapitałDoSpłaty']
                dfN.loc[i, 'RataKapitałowa'] = dfN.loc[i, 'Rata'] - dfN.loc[i, 'RataOdsetkowa']
                dfN.loc[i, 'KapitałDoSpłaty'] = dfN.loc[i-1, 'KapitałDoSpłaty'] - dfN.loc[i, 'RataKapitałowa'].cumsum()

            for i in range(self.kiedynad*12+ile_ms_do_kredytu, len(dfN)):
                dfN.loc[i, 'RataOdsetkowa'] = współczynnik_kredytowy * dfN.loc[i-1, 'KapitałDoSpłaty']
                dfN.loc[i, 'RataKapitałowa'] = dfN.loc[i, 'Rata'] - dfN.loc[i, 'RataOdsetkowa']
                dfN.loc[i, 'KapitałDoSpłaty'] = dfN.loc[i-1, 'KapitałDoSpłaty'] - dfN.loc[i, 'RataKapitałowa'].cumsum() - dfN.loc[i, 'Nadpłata']

    
        #porównanie nadplat i klasycznie
        
        koszt_kredytu = rata * self.okres *12 - self.wielkosc
        idx = pd.date_range(self.kiedy, periods=self.okres * 12+1, freq="M")
        data_splaty_normalnie = idx[-1]
        
        pozycja_splaty_indx = dfN.index[dfN['KapitałDoSpłaty']>0][-1]+1
        data_splaty_nadplaty = dfN['DataKalendarzowa'].iloc[pozycja_splaty_indx]
        koszt_kredytu_nadplaty = dfN['RataOdsetkowa'][:pozycja_splaty_indx].sum()
        reszta = -dfN['KapitałDoSpłaty'][pozycja_splaty_indx]
        oszczednosc_nadplaty=  koszt_kredytu - koszt_kredytu_nadplaty + reszta
        lat_oszczedzonych = (relativedelta(data_splaty_normalnie, data_splaty_nadplaty)).years
        mies_oszczedzonych = (relativedelta(data_splaty_normalnie, data_splaty_nadplaty)).months
        

        
        

        data = [["Kredyt bez nadpłacania", koszt_kredytu, data_splaty_normalnie,""], ["Kredyt z nadpłatami", koszt_kredytu_nadplaty, data_splaty_nadplaty,""], ["Oszczędność", oszczednosc_nadplaty, lat_oszczedzonych, mies_oszczedzonych]]
        dfNd = pd.DataFrame(data, columns=['x', "Koszt", "Dzień spłaty",""])
        dfNd = dfNd.set_index('x')

          
        return dfNd

        #BILANSOWANIE KREDYTU
    
    def Oszczednosc_na_Bilansowaniu_dane(self):
        
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        #wariant z bilansowanie
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)

        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc
        
        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k

        idx2 = pd.date_range(date.today(), periods = self.okres*12+ile_ms_do_kredytu, freq="M")
        miesiace2 = np.arange(self.okres*12+ile_ms_do_kredytu )+1
        
        dfI = pd.DataFrame({'DataKalendarzowa':idx2, 'Miesiące' : miesiace2 })
        Mnożniki = np.arange(0,len(dfI))
        for i in range(0,29):
            dfI.loc[i*12:((i*12)+12), 'Mnożnik'] = Mnożniki[i]
        dfI['Mnożnik'].values[dfI['Mnożnik'].values < 0] = 0
        
        dfI['MiesiąceKredyt'] = dfI['Miesiące'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        dfI['Rata'] = rata
        dfI['Rata'] = dfI['Rata'].shift(ile_ms_do_kredytu)
        
        dfI['Wplaty'] = self.skladka*(1+self.inds/100)**dfI['Mnożnik']
        dfI['Wplaty'] = dfI['Wplaty'].shift(self.kiedyskl*12)
        
        dfI.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfI.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfI.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfI.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        for i in range(ile_ms_do_kredytu+1, len(dfI)):
            dfI.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * dfI.loc[i-1, 'KapitałDoSpłaty']
            dfI.loc[i, 'RataKapitałowa'] = dfI.loc[i, 'Rata'] - dfI.loc[i, 'RataOdsetkowa']
            dfI.loc[i, 'KapitałDoSpłaty'] = dfI.loc[i-1, 'KapitałDoSpłaty'] - dfI.loc[i, 'RataKapitałowa'].cumsum()

        dfI.loc[self.kiedyskl*12, 'Wartość Środków'] = dfI.loc[self.kiedyskl*12, 'Wplaty']
        for i in range(self.kiedyskl*12+1, len(dfI)):
            dfI.loc[i, 'Wartość Środków'] = (dfI.loc[i-1, 'Wartość Środków'].cumsum()+dfI.loc[i,'Wplaty'])*(1+(self.procent/100)/12)

        #Zestawienie bilans i klasycznie
        
        
        koszt_kredytu = rata * self.okres *12 - self.wielkosc
        PozycjaSplatyIndeks = dfI.index[dfI['Wartość Środków'] > dfI['KapitałDoSpłaty']][0]
        ZaplaconychOdsetek = dfI['RataOdsetkowa'][:PozycjaSplatyIndeks+1].sum()
        WplatyDoMomentuSplatyKredytu = dfI['Wplaty'][:PozycjaSplatyIndeks].sum()
        WartoscRachunkuWDniuSplaty = dfI['Wartość Środków'][PozycjaSplatyIndeks]
        

        Dzien_splaty_bilans = dfI['DataKalendarzowa'][PozycjaSplatyIndeks]
        
        idx = pd.date_range(self.kiedy, periods=self.okres * 12+1, freq="M")
        Data_splaty_normalnie = idx[-1]
        
        ZyskZInwestycji = WartoscRachunkuWDniuSplaty - WplatyDoMomentuSplatyKredytu
        
        OszczednoscNaRatach = koszt_kredytu - ZaplaconychOdsetek
        OszczednoscnaKredycieBilans = OszczednoscNaRatach + ZyskZInwestycji
        
        lata_oszczedzone_bilans = (relativedelta(Data_splaty_normalnie, Dzien_splaty_bilans)).years
        ms_oszczedzone_bilans = (relativedelta(Data_splaty_normalnie, Dzien_splaty_bilans)).months
        

        data= [["",koszt_kredytu, ZyskZInwestycji, OszczednoscNaRatach, OszczednoscnaKredycieBilans], ["",'Dzień spłaty normalnie', 'Dzień spłaty z bilansowaniem', 'Oszczędność czasu', ""], ["",Data_splaty_normalnie, Dzien_splaty_bilans, lata_oszczedzone_bilans, ms_oszczedzone_bilans]]
        dfB = pd.DataFrame(data, columns=["x",'Koszt kredytu normalnie', "Zysk z inwestycji", "Oszczędność na ratach","Oszczędność całkowita"])
        dfB = dfB.set_index('x')
        
        return dfB
    
    
    #bilansowanie wykres
    
    def Oszczednosc_na_Bilansowaniu_wykres(self):
        self.kiedy =self.kiedy.strftime('%d-%m-%Y')
        oprocentowanie =  round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)

        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc
        
        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k

        idx2 = pd.date_range(date.today(), periods = self.okres*12+ile_ms_do_kredytu, freq="M")
        miesiace2 = np.arange(self.okres*12+ile_ms_do_kredytu )+1
        
        dfI = pd.DataFrame({'DataKalendarzowa':idx2, 'Miesiące' : miesiace2 })
        
        mnożniki = np.arange(0,len(dfI))
        for i in range(0,29):
            dfI.loc[i*12:((i*12)+12), 'Mnożnik'] = mnożniki[i]
        
        
        dfI['Mnożnik'].values[dfI['Mnożnik'].values < 0] = 0
        
        dfI['MiesiąceKredyt'] = dfI['Miesiące'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        dfI['Rata'] = rata
        dfI['Rata'] = dfI['Rata'].shift(ile_ms_do_kredytu)
        
        dfI['Wplaty'] = self.skladka*(1+self.inds/100)**dfI['Mnożnik']
        dfI['Wplaty'] = dfI['Wplaty'].shift(self.kiedyskl*12)
        
        dfI.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfI.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfI.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfI.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        for i in range(ile_ms_do_kredytu+1, len(dfI)):
            dfI.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * dfI.loc[i-1, 'KapitałDoSpłaty']
            dfI.loc[i, 'RataKapitałowa'] = dfI.loc[i, 'Rata'] - dfI.loc[i, 'RataOdsetkowa']
            dfI.loc[i, 'KapitałDoSpłaty'] = dfI.loc[i-1, 'KapitałDoSpłaty'] - dfI.loc[i, 'RataKapitałowa'].cumsum()

        dfI.loc[self.kiedyskl*12, 'Wartość_Środków'] = dfI.loc[self.kiedyskl*12, 'Wplaty']
        
        for i in range(self.kiedyskl*12+1, len(dfI)):
            dfI.loc[i, 'Wartość_Środków'] = (dfI.loc[i-1, 'Wartość_Środków'].cumsum()+dfI.loc[i,'Wplaty'])*(1+(self.procent/100)/12)
            
        PozycjaSplatyIndeks = dfI.index[dfI['Wartość_Środków'] > dfI['KapitałDoSpłaty']][0]
        
        dfIndeksacja = dfI[['DataKalendarzowa','KapitałDoSpłaty', 'Wartość_Środków']]
        dfIndeksacja['Wartość_Środków'] = dfIndeksacja['Wartość_Środków'][:PozycjaSplatyIndeks]
        
        return dfIndeksacja



#-------------------------------------SEKCJA nr. 5 Kredyt spłaca się sam?-------------------------------------------------------

    def Czy_kredyt_moze_sie_splacic_sam(self):

        self.kiedy =self.kiedy.strftime('%d-%m-%Y')
        oprocentowanie = round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)

        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc


        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k
        

        idx3 = pd.date_range(date.today(), periods = self.okres*12+ile_ms_do_kredytu, freq="M")
        miesiace3 = np.arange(self.okres*12+ile_ms_do_kredytu )+1

        dfD = pd.DataFrame({'DataKalendarzowa':idx3, 'Miesiące' : miesiace3 })
        mnożniki = np.arange(0,len(dfD))
        for i in range(0,29):
            dfD.loc[i*12:((i*12)+12), 'Mnożnik'] = mnożniki[i]

        dfD['Mnożnik'].values[dfD['Mnożnik'].values < 0] = 0

        dfD['MiesiąceKredyt'] = dfD['Miesiące'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        dfD['Rata'] = rata
        dfD['Rata'] = dfD['Rata'].shift(ile_ms_do_kredytu)

        dfD['Wplaty'] = self.skladka*(1+self.inds/100)**dfD['Mnożnik']
        dfD['Wplaty'] = dfD['Wplaty'].shift(self.kiedyskl*12)

        dfD.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        for i in range(ile_ms_do_kredytu+1, len(dfD)):
                dfD.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * dfD.loc[i-1, 'KapitałDoSpłaty']
                dfD.loc[i, 'RataKapitałowa'] = dfD.loc[i, 'Rata'] - dfD.loc[i, 'RataOdsetkowa']
                dfD.loc[i, 'KapitałDoSpłaty'] = dfD.loc[i-1, 'KapitałDoSpłaty'] - dfD.loc[i, 'RataKapitałowa'].cumsum()

        dfD.loc[self.kiedyskl*12, 'WartośćŚrodków'] = dfD.loc[self.kiedyskl*12, 'Wplaty']

        for i in range(self.kiedyskl*12+1, len(dfD)):
            dfD.loc[i, 'WartośćŚrodków'] = (dfD.loc[i-1, 'WartośćŚrodków'].cumsum()+dfD.loc[i,'Wplaty'])*(1+(self.procent/100)/12)
        
        
        dfD['Dywidenda'] = dfD['WartośćŚrodków'] * self.procentdyw/1200
        iloscRatPokrytych = len(dfD.index[dfD['Dywidenda'] > dfD['Rata']])

        return iloscRatPokrytych
    
    
    
    def Kiedy_Kredyt_Splaca_Sie_Sam_Wykres(self):

        oprocentowanie = round(self.marza/100 + self.wibor/100, 4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)

        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc

        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k

        idx3 = pd.date_range(date.today(), periods = self.okres*12+ile_ms_do_kredytu, freq="M")
        miesiace3 = np.arange(self.okres*12+ile_ms_do_kredytu )+1

        dfD = pd.DataFrame({'DataKalendarzowa':idx3, 'Miesiące' : miesiace3 })
        mnożniki = np.arange(0,len(dfD))
        for i in range(0,29):
            dfD.loc[i*12:((i*12)+12), 'Mnożnik'] = mnożniki[i]

        dfD['Mnożnik'].values[dfD['Mnożnik'].values < 0] = 0

        dfD['MiesiąceKredyt'] = dfD['Miesiące'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        dfD['Rata'] = rata
        dfD['Rata'] = dfD['Rata'].shift(ile_ms_do_kredytu)

        dfD['Wplaty'] = self.skladka*(1+self.inds/100)**dfD['Mnożnik']
        dfD['Wplaty'] = dfD['Wplaty'].shift(self.kiedyskl*12)

        dfD.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        for i in range(ile_ms_do_kredytu+1, len(dfD)):
                dfD.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * dfD.loc[i-1, 'KapitałDoSpłaty']
                dfD.loc[i, 'RataKapitałowa'] = dfD.loc[i, 'Rata'] - dfD.loc[i, 'RataOdsetkowa']
                dfD.loc[i, 'KapitałDoSpłaty'] = dfD.loc[i-1, 'KapitałDoSpłaty'] - dfD.loc[i, 'RataKapitałowa'].cumsum()

        dfD.loc[self.kiedyskl*12, 'WartośćŚrodków'] = dfD.loc[self.kiedyskl*12, 'Wplaty']

        for i in range(self.kiedyskl*12+1, len(dfD)):
            dfD.loc[i, 'WartośćŚrodków'] = (dfD.loc[i-1, 'WartośćŚrodków'].cumsum()+dfD.loc[i,'Wplaty'])*(1+self.procent/1200)
        
        
        dfD['Dywidenda'] = dfD['WartośćŚrodków'] * self.procentdyw/1200
        

        PozycjaSplaty_dywideda = dfD.index[dfD['Dywidenda'] > dfD['Rata']][0]

        WartoscRachunku_do_czas_uzbierania_kwoty = dfD['WartośćŚrodków'][PozycjaSplaty_dywideda]
        dfD['Wplaty Skumulowane'] = dfD['Wplaty'].cumsum()

        dfD['Wplaty Skumulowane'] = dfD['Wplaty Skumulowane'][:PozycjaSplaty_dywideda]
        dfD['WartośćŚrodków'] = dfD['WartośćŚrodków'][:PozycjaSplaty_dywideda+1]
        dfD['linia'] = WartoscRachunku_do_czas_uzbierania_kwoty 
        dfD['linia'] = dfD['linia'].shift(PozycjaSplaty_dywideda)

        return dfD

    def Kiedy_Kredyt_Splaca_Sie_Sam_Dane(self):

        
        oprocentowanie = round(self.marza/100 + self.wibor/100,4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)

        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
       
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc

        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k

        idx3 = pd.date_range(date.today(), periods = self.okres*12+ile_ms_do_kredytu, freq="M")
        miesiace3 = np.arange(self.okres*12+ile_ms_do_kredytu )+1

        dfD = pd.DataFrame({'DataKalendarzowa':idx3, 'Miesiące' : miesiace3 })
        mnożniki = np.arange(0,len(dfD))

        for i in range(0,29):
            dfD.loc[i*12:((i*12)+12), 'Mnożnik'] = mnożniki[i]

        dfD['Mnożnik'].values[dfD['Mnożnik'].values < 0] = 0

        dfD['MiesiąceKredyt'] = dfD['Miesiące'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        dfD['Rata'] = rata
        dfD['Rata'] = dfD['Rata'].shift(ile_ms_do_kredytu)

        dfD['Wplaty'] = self.skladka*(1+self.inds/100)**dfD['Mnożnik']
        dfD['Wplaty'] = dfD['Wplaty'].shift(self.kiedyskl*12)

        dfD.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        for i in range(ile_ms_do_kredytu+1, len(dfD)):
                dfD.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * dfD.loc[i-1, 'KapitałDoSpłaty']
                dfD.loc[i, 'RataKapitałowa'] = dfD.loc[i, 'Rata'] - dfD.loc[i, 'RataOdsetkowa']
                dfD.loc[i, 'KapitałDoSpłaty'] = dfD.loc[i-1, 'KapitałDoSpłaty'] - dfD.loc[i, 'RataKapitałowa'].cumsum()

        dfD.loc[self.kiedyskl*12, 'Wartość Środków'] = dfD.loc[self.kiedyskl*12, 'Wplaty']

        for i in range(self.kiedyskl*12+1, len(dfD)):
            dfD.loc[i, 'Wartość Środków'] = (dfD.loc[i-1, 'Wartość Środków'].cumsum()+dfD.loc[i,'Wplaty'])*(1+self.procent/1200)
        
        #Nowe obliczenia pod dywidende
        
        dfD['Dywidenda'] = dfD['Wartość Środków'] * self.procentdyw/1200
        iloscRatPokrytych = len(dfD.index[dfD['Dywidenda'] > dfD['Rata']])
        koszt_kredytu = self.okres*12 * rata - self.wielkosc

        PozycjaSplaty_dywideda = dfD.index[dfD['Dywidenda'] > dfD['Rata']][0]
        SumaWplat_do_czasu_uzbierania_odpowieniej_kwoty = dfD['Wplaty'][:PozycjaSplaty_dywideda].sum()

        WartoscRachunku_do_czas_uzbierania_kwoty = dfD['Wartość Środków'][PozycjaSplaty_dywideda]
        Zysk_do_dywidendy = WartoscRachunku_do_czas_uzbierania_kwoty - SumaWplat_do_czasu_uzbierania_odpowieniej_kwoty

        SumaRatSplaconyPrzezDywidende = iloscRatPokrytych * rata
        Kiedy_kredyt_splaca_sie_sam_data = dfD['DataKalendarzowa'][PozycjaSplaty_dywideda]
        idx = pd.date_range(self.kiedy, periods=self.okres * 12+1, freq="M")
        data_splaty_normalnie = idx[-1] 

        lata_oszczedzone_dywidenda = (relativedelta(data_splaty_normalnie, Kiedy_kredyt_splaca_sie_sam_data)).years
        ms_oszczedzone_dywidenda = (relativedelta(data_splaty_normalnie, Kiedy_kredyt_splaca_sie_sam_data)).months
        

        data= [["",koszt_kredytu, Zysk_do_dywidendy, iloscRatPokrytych, SumaRatSplaconyPrzezDywidende], ["",data_splaty_normalnie, Kiedy_kredyt_splaca_sie_sam_data, lata_oszczedzone_dywidenda, ms_oszczedzone_dywidenda]]
        dfD = pd.DataFrame(data, columns=["x",'Koszt kredytu normalnie', "Zysk z inwestycji", "Ilość pokrytych rat","Wartość pokrytych rat"])
        dfD = dfD.set_index('x')

        return dfD

    def WartoscSrodkow(self):

        
        oprocentowanie = round(self.marza/100 + self.wibor/100,4)
        rata = -nf.pmt(oprocentowanie/12, self.okres*12, self.wielkosc)

        rata1_odsetkowa = -nf.ipmt(oprocentowanie/12, 1, self.okres*12, self.wielkosc)
    
        wspolczynnik_kredytowy = rata1_odsetkowa/self.wielkosc

        lata_do_k = (datetime.strptime(self.kiedy, "%d-%m-%Y").year - datetime.today().year ) *12
        miesiace_do_k = datetime.strptime(self.kiedy, "%d-%m-%Y").month - datetime.today().month
        ile_ms_do_kredytu = lata_do_k + miesiace_do_k

        idx3 = pd.date_range(date.today(), periods = self.okres*12+ile_ms_do_kredytu, freq="M")
        miesiace3 = np.arange(self.okres*12+ile_ms_do_kredytu )+1

        dfD = pd.DataFrame({'DataKalendarzowa':idx3, 'Miesiące' : miesiace3 })
        mnożniki = np.arange(0,len(dfD))

        for i in range(0,29):
            dfD.loc[i*12:((i*12)+12), 'Mnożnik'] = mnożniki[i]

        dfD['Mnożnik'].values[dfD['Mnożnik'].values < 0] = 0

        dfD['MiesiąceKredyt'] = dfD['Miesiące'].shift(ile_ms_do_kredytu).fillna(0).astype(int)
        dfD['Rata'] = rata
        dfD['Rata'] = dfD['Rata'].shift(ile_ms_do_kredytu)

        dfD['Wplaty'] = self.skladka*(1+self.inds/100)**dfD['Mnożnik']
        dfD['Wplaty'] = dfD['Wplaty'].shift(self.kiedyskl*12)

        dfD.loc[ile_ms_do_kredytu, 'RataOdsetkowa'] = rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa'] = rata - rata1_odsetkowa
        dfD.loc[ile_ms_do_kredytu, 'KapitałDoSpłaty'] = self.wielkosc - dfD.loc[ile_ms_do_kredytu, 'RataKapitałowa']

        for i in range(ile_ms_do_kredytu+1, len(dfD)):
                dfD.loc[i, 'RataOdsetkowa'] = wspolczynnik_kredytowy * dfD.loc[i-1, 'KapitałDoSpłaty']
                dfD.loc[i, 'RataKapitałowa'] = dfD.loc[i, 'Rata'] - dfD.loc[i, 'RataOdsetkowa']
                dfD.loc[i, 'KapitałDoSpłaty'] = dfD.loc[i-1, 'KapitałDoSpłaty'] - dfD.loc[i, 'RataKapitałowa'].cumsum()

        dfD.loc[self.kiedyskl*12, 'Wartość Środków'] = dfD.loc[self.kiedyskl*12, 'Wplaty']

        for i in range(self.kiedyskl*12+1, len(dfD)):
            dfD.loc[i, 'Wartość Środków'] = (dfD.loc[i-1, 'Wartość Środków'].cumsum()+dfD.loc[i,'Wplaty'])*(1+self.procent/1200)
        
        #Nowe obliczenia pod dywidende
        
        dfD['Dywidenda'] = dfD['Wartość Środków'] * self.procentdyw/1200
       

        PozycjaSplaty_dywideda = dfD.index[dfD['Dywidenda'] > dfD['Rata']][0]
        
        WartoscRachunku = dfD['Wartość Środków'][PozycjaSplaty_dywideda]
        
        return WartoscRachunku

        


        

        

    