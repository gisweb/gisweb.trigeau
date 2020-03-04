# -*- coding: utf-8 -*-

from gisweb.trigeau import _
from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from gisweb.trigeau.content.mappa_simulazione import IMappaSimulazione
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from swmm5.swmm5tools import SWMM5Simulation

import os
import psycopg2
from os.path import isfile
from datetime import datetime
import random
import string


def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



class testView(BrowserView):
    """
    """

    def calcoloArea(self,imp,tipo,areaS):
        imp=int(imp)
        areaS=float(areaS)
        area=0
        params={"pp":[0.05,0.2],"tv":[0.8,0.667]}
        coeff=params[tipo][0] if imp<45 else params[tipo][0]
        area=imp*coeff
        return area

    def parseRow(self,line,sezione):
        """
        fa il parse della riga

        """
        conf={
            'RG':[0,17,30,43,56,75,330,343,356],
            'SC':[0,17,34,51,68,81,98,115,149],
            'LD':[0,17,34,47,66,79,92,105,118,131]
        }
        row=[]
        if sezione not in conf:
            return []

        v=conf[sezione]
        for i in range (0,len(v)-1):
            start=v[i]
            end=v[i+1]
            s=line[start:end]
            if s not in["","\n"]:
                row.append(s)
        return row
    
    def simulazione(self,rete='CS',schema='H',imp='15',regime='CAM',anni='2',convpp='',convtv='',callback='',_=''):

        #apro il file di base e sostituisco i valori
        filePath = "/apps/trigeau/data"
        fileName = "%s/%s_%s.inp" %(filePath,rete,schema)
        fileName = "%s/%s_%s.inp" %(filePath,rete,schema)

        zona="Chicago"

        rsRandom = randomString()

        sxInpFile = "/tmp/%s_%s_%s_sx.inp" %(rete,schema,rsRandom)
        dxInpFile = "/tmp/%s_%s_%s_dx.inp" %(rete,schema,rsRandom)

        sxInpFile = "/tmp/%s_%s_sx.inp" %(rete,schema)
        dxInpFile = "/tmp/%s_%s_dx.inp" %(rete,schema)

        llsx=[]
        lldx=[]
        leadUsage=[]#array co i leadusage calcolati

        html=''

        fileInp = open(fileName, 'r') 
        lines = fileInp.readlines()
        index=0
        for line in lines:
            if line.strip()=='[RAINGAGES]':
                idxRainGages = index
            if line.strip()=='[SUBCATCHMENTS]':
                idxSubCatchments = index
            if line.strip()=='[LID_USAGE]':
                idxLidUsage = index
            if line.strip()=='[ADJUSTMENTS]':
                idxAdjustments = index


            llsx.append(line)
            index=index+1


        #cambio le righe a sx
        v=self.parseRow(lines[idxRainGages+3],'RG')
        s='"%s/%s-%s%sY.txt"'%(filePath,regime,zona,anni)
        s=s.ljust(255,' ')
        v[5]=str(s)
        s="%s-RG"%regime
        s=s.ljust(13,' ')
        v[6]=str(s)
        llsx[idxRainGages+3]="".join(v)

        index = idxSubCatchments+3
        v=self.parseRow(lines[index],'SC')
        summArea=0
        while v!=[]:
            if v[0][:1] == "S":
                #cambio la riga su file sx                        
                s="%s.0000"%imp
                s=s.ljust(13,' ')
                v[4]=str(s)

                #genero i dati per LID_USAGE
                if convpp:
                    area=self.calcoloArea(imp,"pp",v[3])*float(convpp)
                    summArea=summArea+area
                    area='{:.4f}'.format(area)
                    lid=[
                        v[0],
                        "PP".ljust(17,' '),
                        "2".ljust(13,' '),
                        area.ljust(19,' '),
                        "5.0000".ljust(13,' '),
                        "10.0000".ljust(13,' '),                                
                        "0.0000".ljust(13,' '),
                        "0".ljust(13,' '),
                        " ".ljust(13,' ')
                    ]
                    leadUsage.append(lid)

                if convtv:
                    area=self.calcoloArea(imp,"tv",v[3])*float(convtv)
                    summArea=summArea+area
                    area='{:.4f}'.format(area)
                    lid=[
                        v[0],
                        "TV".ljust(17,' '),
                        "1".ljust(13,' '),
                        area.ljust(19,' '),
                        "11.0000".ljust(13,' '),
                        "30.0000".ljust(13,' '),
                        "0.0000".ljust(13,' '),
                        "0".ljust(13,' '),
                        " ".ljust(13,' ')
                    ]
                    leadUsage.append(lid)

            llsx[index]="".join(v)+"\n"
            index=index+1
            v=self.parseRow(lines[index],'SC')

        fsx = open(sxInpFile, 'w')
        fsx.writelines(llsx)
        fsx.close() 

        #FILE DI DX
        #genero le righe di dx partendo dalle modifiche a sx
        #copio iol file di sx fino a LID_USAGE
        for i in range(0,idxLidUsage+3):
            lldx.append(llsx[i])

        #cambio le righe subcatchment
        index = idxSubCatchments+3
        v=self.parseRow(lines[index],'SC')
        while v!=[]:
            if v[0][:1] == "S":
                #cambio la riga su file dx       
                area=float(v[3])*pow(10,4)
                impdx=66#(area*imp-summArea)/(area-summArea)                
                s="%s.0000"%impdx
                s=s.ljust(13,' ')
                v[4]=str(s)

            lldx[index]="".join(v)+"\n"
            index=index+1
            v=self.parseRow(lines[index],'SC')
 
        
        #aggiungo LID_USAGE nuovo calcolato
        for row in leadUsage:
            lldx.append("".join(row)+"\n")

        #copio le ultime righe da 2 righe prima di adjusteents alla fine
        for i in range(idxAdjustments-2,len(lines)-1):
            lldx.append(lines[i])

        fdx = open(dxInpFile, 'w')
        fdx.writelines(lldx)
        fdx.close() 


        result=dict(success=0)

        st=SWMM5Simulation(str(sxInpFile))
        files=st.getFiles()
        if isfile(files[1]):
            print files[1]
            result["sx"]=self.parseReport(files[1])

        st=SWMM5Simulation(str(dxInpFile))
        files=st.getFiles()
        if isfile(files[1]):
            print files[1]
            result["dx"]=self.parseReport(files[1])


    def parseReport(self,reportfile="/tmp/CS_H_dxlbijUu.rpt"):

        fileRep = open(reportfile, 'r') 
        lines = fileRep.readlines()
        index = 0 
        for line in lines:
            if line.strip()=='Subcatchment Runoff Summary':
                idxRunoff = index
            index=index+1


        ll=[]
        index=idxRunoff+8
        v=self.parseRow(lines[index],'SC')
        while v!=[]:
            ll.append(v)
            index=index+1
            v=self.parseRow(lines[index],'SC')
 

        return str(ll)

    def __call__(self):
        # Implement your own actions:
        self.msg = _(u'A small message')
        return self.index()


class MyView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('my_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.msg = _(u'A small message')
        return self.index()


class ProgramView(BrowserView):

    def sessions(self):
        """Return a catalog search result of sessions to show."""

        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        self.start = datetime.date.today()
        self.end = datetime.date.today()


        return catalog(
            object_provides=IMappaSimulazione.__identifier__,
            path='/'.join(context.getPhysicalPath()),
            sort_on='sortable_title')


    def __call__(self):
        # Implement your own actions:
        #self.start = datetime.date.today()
    	#self.end = datetime.date.today()
        #self.msg = _(u'A small message')
        return self.index()