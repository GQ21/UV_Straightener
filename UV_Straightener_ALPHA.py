######################################
#####         UV Straightener    #####
#####         ALPHA              #####      
######################################
  ###                            ###
######################################
##### Authored and Maintained by #####
#####          Gin               #####      
######################################
 

import maya.cmds as mc

#Global vertical marked lists
gridTxs_V=[]
placeTxs_V=[]
vmarkMainList=[]
vmarkMainListCord=[]
#Global horizontal marked lists
gridTxs_U=[]
placeTxs_U=[]
umarkMainList=[]
umarkMainListCord=[]

#Function to create shader
def createstrUVMat():
    
    if 'strUVMat' not in mc.ls(mat=True):
        mc.shadingNode('blinn', asShader=True, n='strUVMat')
        if 'strUVMatSG' in mc.ls(type='shadingEngine'):
            mc.connectAttr ( 'strUVMat.outColor', 'strUVMatSG.surfaceShader', f=True)            
    if 'strUVMatSG' not in mc.ls(type='shadingEngine'):
        mc.sets (renderable=True, noSurfaceShader=True, empty=True, name='strUVMatSG')
        mc.connectAttr ( 'strUVMat.outColor', 'strUVMatSG.surfaceShader', f=True)         

#Function to create new texture for vertical marked uvs and connect it to the main shader.
def createTx_V():    

    #Create grid and place textures          
    mc.shadingNode('grid', asTexture=True, n='strUVgrid_V_01')      
    gridTxs_V.append(mc.ls(sl=True))      
    mc.shadingNode('place2dTexture', asUtility=True, n='strUVplaceTx_V_01')
    placeTxs_V.append(mc.ls(sl=True))
    mc.connectAttr (str(placeTxs_V[len(placeTxs_V)-1][0])+'.outUV', str(gridTxs_V[len(gridTxs_V)-1][0])+'.uv')    
    mc.connectAttr ( str(placeTxs_V[len(placeTxs_V)-1][0])+'.outUvFilterSize', str(gridTxs_V[len(gridTxs_V)-1][0])+'.uvFilterSize')
   
    #Change grid color and coverage
    slider_value=mc.floatSlider('textures_width_slider', q=True, v=True)
    mc.setAttr (str(gridTxs_V[len(gridTxs_V)-1][0])+'.lineColor', 1, 0, 0, type='double3', )
    mc.setAttr (str(gridTxs_V[len(gridTxs_V)-1][0])+'.fillerColor', 1, 0, 0, type='double3', )
    mc.setAttr (str(placeTxs_V[len(placeTxs_V)-1][0])+'.coverageU', slider_value)
     
    #Check if texture is first    
    if len(gridTxs_V)==1 and len(gridTxs_U)==0 :        
        mc.connectAttr (str(gridTxs_V[0][0])+'.outColor', 'strUVMat.color', f=True)
    #If textures is not the first then connect it with the last texture
    if len(gridTxs_V)>1 or len(gridTxs_U)>=1:
        object='strUVMat'        
        while 'strUVgrid' in mc.listConnections(object, d=False)[-1]:                
            object=mc.listConnections(object, d=False)[-1]                              
        mc.connectAttr(str(gridTxs_V[len(gridTxs_V)-1][0])+'.outColor', str(object)+'.defaultColor', f=True)    
              
#Function to create new texture for horizontal marked uvs and connect it to the main shader        
def createTx_U():    

    #Create grid and place texture          
    mc.shadingNode('grid', asTexture=True, n='strUVgrid_U_01')      
    gridTxs_U.append(mc.ls(sl=True))      
    mc.shadingNode('place2dTexture', asUtility=True, n='strUVplaceTx_U_01')
    placeTxs_U.append(mc.ls(sl=True))
    mc.connectAttr (str(placeTxs_U[len(placeTxs_U)-1][0])+'.outUV', str(gridTxs_U[len(gridTxs_U)-1][0])+'.uv')    
    mc.connectAttr ( str(placeTxs_U[len(placeTxs_U)-1][0])+'.outUvFilterSize', str(gridTxs_U[len(gridTxs_U)-1][0])+'.uvFilterSize')
   
    #Change grid color and coverage
    slider_value=mc.floatSlider('textures_width_slider', q=True, v=True)
    mc.setAttr (str(gridTxs_U[len(gridTxs_U)-1][0])+'.lineColor', 0, 0, 1, type='double3', )
    mc.setAttr (str(gridTxs_U[len(gridTxs_U)-1][0])+'.fillerColor', 0, 0, 1, type='double3', )
    mc.setAttr (str(placeTxs_U[len(placeTxs_U)-1][0])+'.coverageV', slider_value)
     
    #Check if texture is first    
    if len(gridTxs_U)==1 and len(gridTxs_V)==0 :        
        mc.connectAttr (str(gridTxs_U[0][0])+'.outColor', 'strUVMat.color', f=True)
    #If textures is not the first then connect it with last texture
    if len(gridTxs_U)>1 or len(gridTxs_V)>=1:
        object='strUVMat'        
        while 'strUVgrid' in mc.listConnections(object, d=False)[-1]:                
            object=mc.listConnections(object, d=False)[-1]              
        mc.connectAttr(str(gridTxs_U[len(gridTxs_U)-1][0])+'.outColor', str(object)+'.defaultColor', f=True)                             

#Function to check if one of selected uvs are in vertical marked uv list. If answer is positive function adds rest of selected uvs on the same partition as selected uvs where in
def checkSimUV_V(vmarkMainList,vmarkUvList):  

    suv=[]
    mpart=0
    u=0    
    p=0                      
    while len(vmarkUvList)>p:
        for e in vmarkMainList:
            #Check if selected uvs is in main vertical marked uv list                      
            if vmarkUvList[p] in e:
                #Add same uvs in temp list                                
                suv.append(vmarkUvList[p])
                mpart=e                                                                                                                        
        p=p+1        
    #Check if there are similar uvs
    if len(suv)>0:
        #Seperate same uvs from not same uvs
        vmarkUvList=list(set(vmarkUvList)-set(suv))
        for n in vmarkMainList:            
            for i in mpart:
                if i in n:                    
                    nmpar=u                  
            u=u+1
        #Add not same uvs to same uvs main list partition                          
        vmarkMainList[nmpar]=vmarkMainList[nmpar]+vmarkUvList
       
    #Check if there are no simmilar uvs
    if len(suv)<1:
        #Check if uv is not one. If it is write an error
        if len(vmarkUvList)==1:
            mc.error('There is only one uv selected')
        #Add selected uvs in main list
        vmarkMainList.append(vmarkUvList)  
        
#Function to check if one of selected uvs are in horizontal marked uv list. If answer is positive function adds rest of selected uvs on the same partition as selected uvs where in          
def checkSimUV_U(umarkMainList,umarkUvList):  

    suv=[]
    mpart=0
    u=0    
    p=0                      
    while len(umarkUvList)>p:
        for e in umarkMainList:
            #Check if selected uvs is in main horizontal marked uv list                      
            if umarkUvList[p] in e:
                #Add same uvs in temp list                                
                suv.append(umarkUvList[p])
                mpart=e                                                                                                                        
        p=p+1        
    #Check if there are similar uvs
    if len(suv)>0:
        #Seperate same uvs from not same uvs
        umarkUvList=list(set(umarkUvList)-set(suv))
        for n in umarkMainList:            
            for i in mpart:
                if i in n:                    
                    nmpar=u                  
            u=u+1
        #Add not same uvs to same uvs main list partition                          
        umarkMainList[nmpar]=umarkMainList[nmpar]+umarkUvList
       
    #Check if there are no simmilar uvs
    if len(suv)<1:
        #Check if uv is not one. If it is write an error
        if len(umarkUvList)==1:
            mc.error('There is only one uv selected')
        #Add selected uvs in main list
        umarkMainList.append(umarkUvList)      
                                                                                                                                                             
#Function which translates and scales textures that represents uvs which marked in a vertical manner
def txtrans_V(list_V,placeTxs_V,uaverage):
   
    #Calculate textures size  
    arrayCord=mc.polyEditUV(list_V, q=True  )
    maxVval=max(arrayCord[::-2])
    minVval=min(arrayCord[::-2])
    markLen=maxVval-minVval    
    #Transalte and scale texture
    slider_value=mc.floatSlider('textures_width_slider', q=True, v=True)
    mc.setAttr (str(placeTxs_V[0])+'.coverageV', markLen)
    mc.setAttr (str(placeTxs_V[0])+'.translateFrameU', (uaverage-(slider_value/0.01)*0.005))
    mc.setAttr (str(placeTxs_V[0])+'.translateFrameV', minVval)   
    
#Function which translates and scales textures that represents uvs which marked in a horizontal manner  
def txtrans_U(list_U,placeTxs_U,vaverage):
   
    #Calculate textures size  
    arrayCord=mc.polyEditUV(list_U, q=True)    
    maxUval=max(arrayCord[::2])
    minUval=min(arrayCord[::2])
    markLen=maxUval-minUval        
    #Transalte and scale texture
    slider_value=mc.floatSlider('textures_width_slider', q=True, v=True)
    mc.setAttr (str(placeTxs_U[0])+'.coverageU', markLen)
    mc.setAttr (str(placeTxs_U[0])+'.translateFrameU', minUval)
    mc.setAttr (str(placeTxs_U[0])+'.translateFrameV', (vaverage-(slider_value/0.01)*0.005))    
    
#Function for sliding textures width 
def width_slider(slider_value):  
       
    #Change horizontal  marked textures width
    for e in placeTxs_U:
        current_tr_value=mc.getAttr (str(e[0])+'.translateFrameV')        
        current_cov_value=mc.getAttr (str(e[0])+'.coverageV')              
        change_tr_value=current_tr_value+(current_cov_value-slider_value)/2.0                
        mc.setAttr (str(e[0])+'.coverageV', slider_value)
        mc.setAttr (str(e[0])+'.translateFrameV', change_tr_value)
    #Change vertical  marked textures width    
    for i in placeTxs_V:
        current_tr_value=mc.getAttr (str(i[0])+'.translateFrameU')        
        current_cov_value=mc.getAttr (str(i[0])+'.coverageU')              
        change_tr_value=current_tr_value+(current_cov_value-slider_value)/2.0                
        mc.setAttr (str(i[0])+'.coverageU', slider_value)
        mc.setAttr (str(i[0])+'.translateFrameU', change_tr_value)  
                
#Function to straighten uvs in a vertical manner    
def straigtenUVs_V(uvarray):
   
    #Calculate average uvs array position in horizontal manner      
    arrayCord = mc.polyEditUV(uvarray, q=True  )        
    uaverage = sum(arrayCord[::2]) / len(arrayCord[::2])
    #Translate uvs accordingly    
    for uv in uvarray:        
        oneUvCord = mc.polyEditUV(uv, r=False, u=uaverage)
    return uaverage  
    
#Function to straighten uvs in a horizontal manner     
def straigtenUVs_U(uvarray):
   
    #Calculate average uvs array position in horizontal manner      
    arrayCord = mc.polyEditUV(uvarray, q=True  )        
    vaverage = sum(arrayCord[::-2]) / len(arrayCord[::-2])
    #Translate uvs accordingly    
    for uv in uvarray:        
        oneUvCord = mc.polyEditUV(uv, r=False, v=vaverage)
    return vaverage      

#Function to recalculate vertical marked uvs    
def recalculateUVs_V():
   
    #Create list for marked uv current coordinates
    vmarkMainListCordRec=convertionToCord(vmarkMainList)
    u=0
    n=0    
    sluv=mc.ls(sl=True, fl=1)          
    while len(vmarkMainList)>u:
        #Check if selected uvs are in the main vertical marked uvs list
        for e in sluv:          
            if e in vmarkMainList[u]:                          
                uvposition=vmarkMainList[u].index(e)
                #Check if current selected uvs coordinates are same as was before and if they aren`t recalculate vertical marked uvs list
                if vmarkMainListCord[u][uvposition]!=vmarkMainListCordRec[u][uvposition]:                    
                    while len(vmarkMainList)>n:
                        #unfold marked uvs in vertical manner if checkbox is selected
                        if mc.checkBox('AutoUnfoldVertical',q=True, v=True):                            
                            unfoldAlong_V(vmarkMainList[n])
                        #Recalculate vertical textures
                        txtrans_V(vmarkMainList[n],placeTxs_V[n],straigtenUVs_V(vmarkMainList[n]))
                        n=n+1
                        #Recalculate horizontal textures                           
                        if len(umarkMainList)>0:
                            num=0                            
                            for uv in umarkMainList:                                                        
                                txtrans_U(umarkMainList[num],placeTxs_U[num],mc.polyEditUV(umarkMainList[num][0],q=True)[1])
                                num=num+1
                    #recalculate global vertical marked uv coordinates list                          
                    recalculateMainCord_V()                                                                                                          
        u=u+1 
         
#Function to recalculate horizontal marked uvs
def recalculateUVs_U():
   
    #Create list for marked uv current coordinates
    umarkMainListCordRec=convertionToCord(umarkMainList)
    u=0
    n=0    
    seluv=mc.ls(sl=True, fl=1)          
    while len(umarkMainList)>u:
        #Check if selected uvs are in the main horiztonal marked uvs list
        for e in seluv:          
            if e in umarkMainList[u]:                          
                uvposition=umarkMainList[u].index(e)
                #Check if current selected uvs coordinates are same as was before and if they aren`t recalculate horizontal marked uvs list
                if umarkMainListCord[u][uvposition]!=umarkMainListCordRec[u][uvposition]:                    
                    while len(umarkMainList)>n:
                        #unfold marked uvs in horizontal manner if checkbox is selected
                        if mc.checkBox('AutoUnfoldHorizontal',q=True, v=True):                            
                            unfoldAlong_U(umarkMainList[n])
                        #Recalculate textures
                        txtrans_U(umarkMainList[n],placeTxs_U[n],straigtenUVs_U(umarkMainList[n]))
                        n=n+1
                        #Recalculate vertical textures
                        if len(vmarkMainList)>0:        
                            num=0                            
                            for uv in vmarkMainList:                                                        
                                txtrans_V(vmarkMainList[num],placeTxs_V[num],mc.polyEditUV(vmarkMainList[num][0],q=True)[0])
                                num=num+1 
                    #recalculate global horizontal marked uv coordinates list                          
                    recalculateMainCord_U()                                                                                                      
        u=u+1  
   
#Function to mark selected uvs in vertical manner                                                      
def vmark():    

    p=0  
    u=0  
    vmarkUvList = mc.ls (sl=True, fl=1)                
    #If just one uv selected write and error
    if len(vmarkUvList)==1:                
            mc.error('There is only one uv selected')  
    #If no uv selected write an error
    if  len(vmarkUvList)==0 or vmarkUvList[0].find('.map')<0:
        mc.error('No uvs selected')            
    tmpvmarkMainList=len(vmarkMainList)    
   
    #Check if uvs is in the main list and if so add those uvs
    if len(vmarkMainList)>0:        
        switch=0
        #Check if all selected uvs are under same object
        for n in vmarkUvList:            
            for v in vmarkMainList:
                for h in v:                    
                    if h.find(n[:n.find('.')])==-1:
                        switch=1
        #If selected uvs is on different object, ask if user want to switch and delete all textures              
        if switch==1:                        
            confirmSwtich=mc.confirmDialog( title='Switching Confirm', message='You are switching on editing other object uvs. All previous uv constrains will be deleted', button=['Okay','No'], defaultButton='okay', cancelButton='No', dismissString='No' )
            if confirmSwtich=='Okay':                                              
                #Clear all list and delete textures
                listcount=0
                h=len(gridTxs_V)
                while h>listcount:
                    del vmarkMainList[0]
                    mc.delete(gridTxs_V[0])
                    gridTxs_V.remove(gridTxs_V[0])                    
                    mc.delete(placeTxs_V[0])
                    placeTxs_V.remove(placeTxs_V[0])
                    listcount=listcount+1
                listcount=0    
                h=len(gridTxs_U)
                while h>listcount:
                    del umarkMainList[0]
                    mc.delete(gridTxs_U[0])
                    gridTxs_U.remove(gridTxs_U[0])                    
                    mc.delete(placeTxs_U[0])
                    placeTxs_U.remove(placeTxs_U[0])
                    listcount=listcount+1                                                            
                listcount=0
                #Reasign to default material
                shadingGroup = cmds.listConnections('strUVMat', type='shadingEngine')
                componentsWithMaterial = cmds.sets(shadingGroup, q=True)
                mc.sets (componentsWithMaterial, e=True, forceElement='initialShadingGroup')                            
        else:            
            checkSimUV_V(vmarkMainList, vmarkUvList)                
            if tmpvmarkMainList<len(vmarkMainList):            
                #Straighten uvs and recalculate textures
                diff=len(vmarkMainList)-tmpvmarkMainList
                while diff>u:                
                    createTx_V()
                    u=u+1
                while len(vmarkMainList)>p:                                        
                    txtrans_V(vmarkMainList[p],placeTxs_V[p],straigtenUVs_V(vmarkMainList[p]))
                    p=p+1            
               
            if tmpvmarkMainList==len(vmarkMainList):                                
                #Straighten uvs and recalculate textures
                while len(vmarkMainList)>p:                                                
                    txtrans_V(vmarkMainList[p],placeTxs_V[p],straigtenUVs_V(vmarkMainList[p]))
                    p=p+1
            recalculateMainCord_V()
            #Recalculate horizontal textures  
            if len(umarkMainList)>0:
                            num=0                            
                            for uv in umarkMainList:                                                        
                                txtrans_U(umarkMainList[num],placeTxs_U[num],mc.polyEditUV(umarkMainList[num][0],q=True)[1])
                                num=num+1
    #Check if there are no uvs marked.If there are mark selected
    if len(vmarkMainList)==0:              
        vmarkMainList.append(vmarkUvList)
        #Convert string uv list to cordinate list
        recalculateMainCord_V()
        #Create shader and apply texture
        selObj=mc.ls(sl=True)
        if len(umarkMainList)==0:
            createstrUVMat()        
            mc.select (selObj[0][:selObj[0].find('.')] )
            mc.sets (e=True,  forceElement='strUVMatSG')        
        createTx_V()
        txtrans_V(vmarkMainList[0],placeTxs_V[0],straigtenUVs_V(vmarkMainList[0]))
        #Recalculate  horizontal textures  
        if len(umarkMainList)>0:
                        num=0                            
                        for uv in umarkMainList:                                                        
                            txtrans_U(umarkMainList[num],placeTxs_U[num],mc.polyEditUV(umarkMainList[num][0],q=True)[1])
                            num=num+1
        #ScriptJob to recalculate textures after moving uvs
        jobNum_V = cmds.scriptJob( ac= [vmarkMainList[0][0],'recalculateUVs_V()'], protected=True)        
        #Reselect object
        mc.select (selObj[0][:selObj[0].find('.')] ) 
        
#Function to mark selected uvs in horizontal manner                
def umark():  
    
    p=0  
    u=0  
    umarkUvList = mc.ls (sl=True, fl=1)              
    #If just one uv selected write and error
    if len(umarkUvList)==1:                
            mc.error('There is only one uv selected')  
    #If no uv selected write an error
    if  len(umarkUvList)==0 or umarkUvList[0].find('.map')<0:
        mc.error('No uvs selected')            
    tmpumarkMainList=len(umarkMainList)
   
    if len(umarkMainList)>0:                    
        switch=0
        #Check if all selected uvs are under same object
        for n in umarkUvList:            
            for v in umarkMainList:
                for h in v:                    
                    if h.find(n[:n.find('.')])==-1:
                        switch=1
        #If selected uvs is on different object, ask if user want to switch and delete all textures              
        if switch==1:                        
            confirmSwtich=mc.confirmDialog( title='Switching Confirm', message='You are switching on editing other object uvs. All previous uv constrains will be deleted', button=['Okay','No'], defaultButton='okay', cancelButton='No', dismissString='No' )
            if confirmSwtich=='Okay':                                              
                #Clear all list and delete textures
                listcount=0
                h=len(gridTxs_V)
                while h>listcount:
                    del vmarkMainList[0]
                    mc.delete(gridTxs_V[0])
                    gridTxs_V.remove(gridTxs_V[0])                    
                    mc.delete(placeTxs_V[0])
                    placeTxs_V.remove(placeTxs_V[0])
                    listcount=listcount+1
                listcount=0    
                h=len(gridTxs_U)
                while h>listcount:
                    del umarkMainList[0]
                    mc.delete(gridTxs_U[0])
                    gridTxs_U.remove(gridTxs_U[0])                    
                    mc.delete(placeTxs_U[0])
                    placeTxs_U.remove(placeTxs_U[0])
                    listcount=listcount+1                                                            
                listcount=0
                #Reasign to default material
                shadingGroup = cmds.listConnections('strUVMat', type='shadingEngine')
                componentsWithMaterial = cmds.sets(shadingGroup, q=True)
                mc.sets (componentsWithMaterial, e=True, forceElement='initialShadingGroup')                            
        else:              
            checkSimUV_U(umarkMainList, umarkUvList)                        
            if tmpumarkMainList<len(umarkMainList):            
               #Straighten uvs and recalculate textures
               diff=len(umarkMainList)-tmpumarkMainList
               while diff>u:                
                   createTx_U()
                   u=u+1
               while len(umarkMainList)>p:                                        
                   txtrans_U(umarkMainList[p],placeTxs_U[p],straigtenUVs_U(umarkMainList[p]))
                   p=p+1                    
            if tmpumarkMainList==len(umarkMainList):                                
                #Straighten uvs and recalculate textures
                while len(umarkMainList)>p:                                                
                   txtrans_U(umarkMainList[p],placeTxs_U[p],straigtenUVs_U(umarkMainList[p]))
                   p=p+1
            recalculateMainCord_U() 
            #Recalculate vertical textures
            if len(vmarkMainList)>0:        
                num=0                            
                for uv in vmarkMainList:                                                        
                    txtrans_V(vmarkMainList[num],placeTxs_V[num],mc.polyEditUV(vmarkMainList[num][0],q=True)[0])
                    num=num+1      
    #Check if there are no uvs marked.If there are mark selected       
    if len(umarkMainList)==0:              
        umarkMainList.append(umarkUvList)
        #Convert string uv list to cordinate list
        recalculateMainCord_U()                  
        #Create shader and apply texture
        selObj=mc.ls(sl=True)
        if len(vmarkMainList)==0:
            createstrUVMat()        
            mc.select (selObj[0][:selObj[0].find('.')] )
            mc.sets (e=True,  forceElement='strUVMatSG')        
        createTx_U()       
        txtrans_U(umarkMainList[0],placeTxs_U[0],straigtenUVs_U(umarkMainList[0]))
        #Recalculate vertical textures
        if len(vmarkMainList)>0:        
            num=0                            
            for uv in vmarkMainList:                                                        
                txtrans_V(vmarkMainList[num],placeTxs_V[num],mc.polyEditUV(vmarkMainList[num][0],q=True)[0])
                num=num+1 
        #ScriptJob to recalculate textures after moving uvs
        jobNum_U = cmds.scriptJob( ac= [umarkMainList[0][0],'recalculateUVs_U()'], protected=True)        
        #Reselect object
        mc.select (selObj[0][:selObj[0].find('.')])
             
#Function to convert string uv list to uv cord list
def convertionToCord(strlist):
   
    p=0
    convertedList=[]
    subUVCord=[]
    while len(strlist)>p:
        for e in strlist[p]:
            uvCord=mc.polyEditUV(e, q=True)
            subUVCord.append(uvCord)            
        convertedList.append(subUVCord)
        subUVCord=[]                
        p=p+1          
    return convertedList
   
#Function to recalculate global vertical marked uv coordinates list    
def recalculateMainCord_V():              
   
    vmarkMainListCordRec=convertionToCord(vmarkMainList)
    del vmarkMainListCord[:]
    for z in vmarkMainListCordRec:
        vmarkMainListCord.append(z)          
        
#Function to recalculate global horizontal marked uv coordinates list    
def recalculateMainCord_U():              
   
    umarkMainListCordRec=convertionToCord(umarkMainList)
    del umarkMainListCord[:]
    for z in umarkMainListCordRec:
        umarkMainListCord.append(z)  
                
#Function to unfold uvs
def uvunfold():  
   
    p=0
    multiShelluvs_V=[]
    multiShelluvs_U=[]
    flatmarkMainlist_V=[]
    flatmarkMainlist_U=[]
    #Unfold all marked shells uvs
    if mc.radioCollection('selTypeunfoldCollection', q=True, select=True)=='sel_All_unfold':
        #List all uvs shells with vertical marking
        while len(vmarkMainList)>p:
            for x in vmarkMainList[p]:
                #Flatten vertical marked uv list
                flatmarkMainlist_V.append(x)
                #List selected uv shell uvs                
                mc.select(x)
                mel.eval ('polySelectBorderShell 0')
                shelluvs=mc.ls(sl=True, fl=1)                
                multiShelluvs_V=multiShelluvs_V+shelluvs                
            p=p+1
        p=0
        #Remove duplicates    
        cleanList_V=list(dict.fromkeys(multiShelluvs_V))                       
        #List all uvs shells with horizontal marking
        while len(umarkMainList)>p:
            for t in umarkMainList[p]:
                #Flatten horizontal marked uv list
                flatmarkMainlist_U.append(t)
                #List selected uv shell uvs                
                mc.select(t)
                mel.eval ('polySelectBorderShell 0')
                shelluvs=mc.ls(sl=True, fl=1)                
                multiShelluvs_U=multiShelluvs_U+shelluvs                      
            p=p+1
        #Remove duplicates    
        cleanList_U=list(dict.fromkeys(multiShelluvs_U))
        cleanList_V= list(dict.fromkeys(multiShelluvs_V))
        cleanList_UV=list(dict.fromkeys(cleanList_U+cleanList_V))
        #Select uvs which is not marked
        all_unfolduvs=list(set(cleanList_UV)-set(dict.fromkeys(flatmarkMainlist_V+flatmarkMainlist_U)))
        #Unfold uvs with legacy algorithm
        if mc.radioCollection('unfoldCollection', q=True, select=True)== 'unLegacy':                          
            mc.unfold(all_unfolduvs, i=5000, ss=0.001,gb=0,gmb=0.5,pub=0, ps=0,oa=0, us=False)
        #Unfold uvs with unfold3d algorithm  
        if mc.radioCollection('unfoldCollection', q=True, select=True)== 'unUnfold3D':                  
            mc.u3dUnfold(all_unfolduvs, ite=1,p=0,bi=1,tf=1,ms=1024,rs=0)
        mc.select(d=True)
    #Unfold uvs on selected uvs
    if mc.radioCollection('selTypeunfoldCollection', q=True, select=True)=='sel_unfold':  
        sel_UV=mc.ls(sl=True, fl=1)
        while len(vmarkMainList)>p:
            for x in vmarkMainList[p]:
                #Flatten vertical marked uv list
                flatmarkMainlist_V.append(x)
            p=p+1
        p=0
        while len(umarkMainList)>p:
            for t in umarkMainList[p]:
                #Flatten horizontal marked uv list
                flatmarkMainlist_U.append(t)
            p=p+1
        combine_marked=list(dict.fromkeys(flatmarkMainlist_U+flatmarkMainlist_V))
        sel_unfolduvs=list(set(sel_UV)-set(combine_marked))
        #Unfold uvs with legacy algorithm
        if mc.radioCollection('unfoldCollection', q=True, select=True)== 'unLegacy':                          
            mc.unfold(sel_unfolduvs, i=5000, ss=0.001,gb=0,gmb=0.5,pub=0, ps=0,oa=0, us=False)
        #Unfold uvs with unfold3d algorithm  
        if mc.radioCollection('unfoldCollection', q=True, select=True)== 'unUnfold3D':                  
            mc.u3dUnfold(sel_unfolduvs, ite=1,p=0,bi=1,tf=1,ms=1024,rs=0)      
            
#Function to optimize uvs
def optimize():  
   
    p=0
    multiShelluvs_V=[]
    multiShelluvs_U=[]
    flatmarkMainlist_V=[]
    flatmarkMainlist_U=[] 
    #Optimize all marked shells uvs   
    if mc.radioCollection('optimize_Collection', q=True, select=True)=='optimize_All':
        #List all uvs shells with vertical marking
        while len(vmarkMainList)>p:
            for x in vmarkMainList[p]:
                #Flatten vertical marked uv list
                flatmarkMainlist_V.append(x)
                #List selected uv shell uvs                
                mc.select(x)
                mel.eval ('polySelectBorderShell 0')
                shelluvs=mc.ls(sl=True, fl=1)                
                multiShelluvs_V=multiShelluvs_V+shelluvs                
            p=p+1
        p=0
        #Remove duplicates    
        cleanList_V=list(dict.fromkeys(multiShelluvs_V))      
           
        #List all uvs shells with horizontal marking
        while len(umarkMainList)>p:
            for t in umarkMainList[p]:
                #Flatten horizontal marked uv list
                flatmarkMainlist_U.append(t)
                #List selected uv shell uvs                
                mc.select(t)
                mel.eval ('polySelectBorderShell 0')
                shelluvs=mc.ls(sl=True, fl=1)                
                multiShelluvs_U=multiShelluvs_U+shelluvs                      
            p=p+1
        #Remove duplicates    
        cleanList_U=list(dict.fromkeys(multiShelluvs_U))
        cleanList_V= list(dict.fromkeys(multiShelluvs_V))
        cleanList_UV=list(dict.fromkeys(cleanList_U+cleanList_V))
        #Select uvs which is not marked
        all_optuvs=list(set(cleanList_UV)-set(dict.fromkeys(flatmarkMainlist_V+flatmarkMainlist_U)))        
        mc.u3dOptimize(all_optuvs, ite=1, pow=1, sa=1, bi=False, tf=True, ms=1024, rs=0)                
        mc.select(d=True)
    #Optimize selected uvs 
    if mc.radioCollection('optimize_Collection', q=True, select=True)=='optimize_Selected':  
        sel_UV=mc.ls(sl=True, fl=1)
        while len(vmarkMainList)>p:
            for x in vmarkMainList[p]:
                #Flatten vertical marked uv list
                flatmarkMainlist_V.append(x)
            p=p+1
        p=0
        while len(umarkMainList)>p:
            for t in umarkMainList[p]:
                #Flatten horizontal marked uv list
                flatmarkMainlist_U.append(t)
            p=p+1
        combine_marked=list(dict.fromkeys(flatmarkMainlist_U+flatmarkMainlist_V))
        sel_optuvs=list(set(sel_UV)-set(combine_marked))
        #Optimize uvs with legacy algorithm
        mc.u3dOptimize(sel_optuvs, ite=1, pow=1, sa=1, bi=False, tf=True, ms=1024, rs=0)  
       
#Function to unfold uvs on vertical axies            
def unfoldAlong_V(vmarkedList):
    
    #Flatten list      
    for e in vmarkedList:
            if e.find(':')>0:
                vmarkedList=vmarkedList+mc.ls(e, fl=1)
                vmarkedList.remove(e)            
    #Unfold vertical
    mc.unfold(vmarkedList, i=5000, ss=0.001,gb=0,gmb=0.5,pub=0, ps=0,oa=1, us=False)
           
    #Check if there are horizontal marked uvs in the list    
    list_num=0
    for i in umarkMainList:        
        for n in vmarkedList:
            if n in i:
                #If there are horizontal uvs intercrossing, move vertical uvs array corresponding to intercrossing uv horizontal coordinates
                v_Cord=mc.polyEditUV(n, q=True)
                for uv in i:        
                    move_U_UVs = mc.polyEditUV(uv, r=False, v=v_Cord[0])
                #Unfold horizontal uvs intercrossing array                              
                mc.unfold(i, i=5000, ss=0.001,gb=0,gmb=0.5,pub=0, ps=0,oa=1, us=False)
                #Update horizontal uvs textures
                txtrans_U(umarkMainList[list_num],placeTxs_U[list_num],straigtenUVs_U(umarkMainList[list_num]))
        list_num=list_num+1
        
#Function to unfold uvs on horizontal axies 
def unfoldAlong_U(umarkedList): 
 
    #Flatten list
    for e in umarkedList:
            if e.find(':')>0:
                umarkedList=umarkedList+mc.ls(e, fl=1)
                umarkedList.remove(e)           
    #Unfold horizontal
    mc.unfold(umarkedList, i=5000, ss=0.001,gb=0,gmb=0.5,pub=0, ps=0,oa=2, us=False)
       
    #Check if there are vertical marked uvs in the list    
    list_num=0
    for i in vmarkMainList:        
        for n in umarkedList:
            if n in i:
                #If there are vertical uvs intercrossing, move vertical uvs array corresponding to intercrossing uv horizontal coordinates
                u_Cord=mc.polyEditUV(n, q=True)                
                for uv in i:        
                    move_V_UVs = mc.polyEditUV(uv, r=False, u=u_Cord[0])
                #Unfold vertical uvs intercrossing array                              
                mc.unfold(i, i=5000, ss=0.001,gb=0,gmb=0.5,pub=0, ps=0,oa=1, us=False)
                #Update vertical uvs textures
                txtrans_V(vmarkMainList[list_num],placeTxs_V[list_num],straigtenUVs_V(vmarkMainList[list_num]))
        list_num=list_num+1 
                       
#Function to reconnect textures into strUVMat
def reconnectTxs():
    i=0
    s=0
    #Disconnect all gridTxs_V    
    for e in gridTxs_V:
        #Check if there is out going connection          
        destinationAttr=cmds.listConnections(e, plugs=True, source=False)
        sourceAttrs = str(e[0])+'.outColor'        
        if len(destinationAttr)>1:                                                      
            #Disconnect connection            
            mc.disconnectAttr(sourceAttrs,destinationAttr[-1])
    #Disconnect all gridTxs_U          
    for t in gridTxs_U:
        #Check if there is out going connection          
        destinationAttr=cmds.listConnections(t, plugs=True, source=False)
        sourceAttrs = str(t[0])+'.outColor'        
        if len(destinationAttr)>1:                                                      
            #Disconnect connection            
            mc.disconnectAttr(sourceAttrs,destinationAttr[-1])            
           
    #Connect all gridTxs_V
    while len(gridTxs_V)>i:
        #Connect first texture to shader        
        if i==0:
            mc.connectAttr (str(gridTxs_V[0][i])+'.outColor', 'strUVMat.color', f=True)
        #If textures is not the first then connect it with last texture    
        else:
            mc.connectAttr(str(gridTxs_V[i][0])+'.outColor', str(gridTxs_V[i-1][0])+'.defaultColor', f=True)              
        i=i+1  
    #Connect all gridTxs_U
    while len(gridTxs_U)>s:        
        #If there is no gridTxs_V connect first texture to shader.Otherwise connect to last gridTxs_V      
        if s==0:
            if len(gridTxs_V)==0:
                mc.connectAttr (str(gridTxs_U[0][s])+'.outColor', 'strUVMat.color', f=True)
            else:
                mc.connectAttr (str(gridTxs_U[0][s])+'.outColor', str(gridTxs_V[-1][0])+'.defaultColor', f=True)
        #Otherwise connect to last gridTxs_U  texture    
        else:
            mc.connectAttr(str(gridTxs_U[s][0])+'.outColor', str(gridTxs_U[s-1][0])+'.defaultColor', f=True)              
        s=s+1
       
#Function to remove vertical marking
def removeUvs_V():
    
    k=0
    n=0
    z=0
    #List selected uvs
    seluv=mc.ls(sl=True, fl=1)      
    #Check if selected uvs is in main vertical marked uvs list                
    for e in seluv:        
        while len(vmarkMainList)>k and n==0 :
            if e in vmarkMainList[k]:
                #If uv is in the list, then delete that element                              
                vmarkMainList[k].remove(e)
                #If after deletion list has one uv, then empty list and delete it
                if len(vmarkMainList[k])==1:
                    vmarkMainList[k].remove(vmarkMainList[k][0])                    
                    #Delete corresponing textures
                    mc.delete(gridTxs_V[k])
                    gridTxs_V.remove(gridTxs_V[k])                    
                    mc.delete(placeTxs_V[k])
                    placeTxs_V.remove(placeTxs_V[k])
                    #Reconnect textures                  
                    if len(gridTxs_V)>0 or len(gridTxs_U)>0 :                        
                        reconnectTxs()      
                    #Delete empty list                                                      
                    del vmarkMainList[k]
                    n=1                                                
            k=k+1
        k=0
        n=0
    #Recalculate textures sizes    
    while len(vmarkMainList)>z:
        txtrans_V(vmarkMainList[z],placeTxs_V[z],straigtenUVs_V(vmarkMainList[z]))        
        z=z+1
        
#Function to remove horizontal marking        
def removeUvs_U():
    
    k=0
    n=0
    z=0
    #List selected uvs
    seluv=mc.ls(sl=True, fl=1)      
    #Check if selected uvs is in main horizontal marked uvs list                
    for e in seluv:        
        while len(umarkMainList)>k and n==0 :            
            if e in umarkMainList[k]:
                #If uv is in the list, then delete that element                              
                umarkMainList[k].remove(e)                
                #If after deletion list has one uv, then empty list and delete it
                if len(umarkMainList[k])==1:
                    umarkMainList[k].remove(umarkMainList[k][0])                    
                    #Delete corresponing textures
                    mc.delete(gridTxs_U[k])
                    gridTxs_U.remove(gridTxs_U[k])                    
                    mc.delete(placeTxs_U[k])
                    placeTxs_U.remove(placeTxs_U[k])
                    #Reconnect textures                  
                    if len(gridTxs_V)>0 or len(gridTxs_U)>0 :                        
                        reconnectTxs()      
                    #Delete empty list                                                      
                    del umarkMainList[k]
                    n=1                                                
            k=k+1
        k=0
        n=0
    #Recalculate textures sizes    
    while len(umarkMainList)>z:
        txtrans_U(umarkMainList[z],placeTxs_U[z],straigtenUVs_U(umarkMainList[z]))        
        z=z+1  
         
#Function to reset scriptJob and textures
def reset():
    
    #Reset scriptJobs     
    jobNum_V = cmds.scriptJob( ac= [vmarkMainList[0][0],'recalculateUVs_V()'], protected=True)
    jobNum_U = cmds.scriptJob( ac= [umarkMainList[0][0],'recalculateUVs_U()'], protected=True) 
    n=0    
    #Recalculate vertical marked textures
    while len(vmarkMainList)>n:            
        txtrans_V(vmarkMainList[n],placeTxs_V[n],straigtenUVs_V(vmarkMainList[n]))
        n=n+1
    n=0
    #Recalculate horizontal marked textures
    while len(umarkMainList)>n:            
        txtrans_U(umarkMainList[n],placeTxs_U[n],straigtenUVs_U(umarkMainList[n]))
        n=n+1
    #Reconnect textures     
    reconnectTxs()
    
#Function to delete all lists,textures and material        
def clear_all():    

    n=0
    combine_marked=umarkMainList+vmarkMainList
    #If lists are not clear then clear them and delete textures    
    if umarkMainList>0:            
        while len(umarkMainList)!=n:
            del umarkMainList[0]                
            gridTxs_U.remove(gridTxs_U[0])                
            placeTxs_U.remove(placeTxs_U[0])      
    if vmarkMainList>0:              
        while len(vmarkMainList)!=n:
            del vmarkMainList[0]               
            gridTxs_V.remove(gridTxs_V[0])                
            placeTxs_V.remove(placeTxs_V[0])                     
    grid_V_Tx=cmds.ls(['strUVgrid_V_0%s' % n for n in range(1,10000)])
    if len(grid_V_Tx)>0:
        mc.delete(grid_V_Tx)
    grid_U_Tx=cmds.ls(['strUVgrid_U_0%s' % n for n in range(1,10000)])
    if len(grid_U_Tx)>0:
        mc.delete(grid_U_Tx)
    place_V_Tx=cmds.ls(['strUVplaceTx_V_0%s' % n for n in range(1,10000)])
    if len(place_V_Tx)>0:
        mc.delete(place_V_Tx)
    place_U_Tx=cmds.ls(['strUVplaceTx_U_0%s' % n for n in range(1,10000)])
    if len(place_U_Tx)>0:
        mc.delete(place_U_Tx)  
    if mc.objExists('strUVMat'):                                        
        #Check if there are any objects connected to strUVMat
        object_strUVMat = mc.listConnections('strUVMatSG',type='mesh')
        if object_strUVMat>0:
            mc.select(object_strUVMat)
            mc.sets (e=True, forceElement='initialShadingGroup')
            mc.select(d=True)      
        #Delete strUVMat material                              
        mc.delete('strUVMat')
        mc.delete('strUVMatSG')
    #Clear all scriptJobs
    cmds.scriptJob( killAll=True, force=True)
    
#Function to select whole marked uv array     
def sel_Array():
   
    #If no uv selected write an error
    if  len(mc.ls(sl=True, fl=1))==0:
        mc.error('No uvs selected')
    #Check if sel uvs are in horizontal marked uvs list
    sel_uvs=mc.ls(sl=True, fl=1)
    for e in umarkMainList:
        for i in sel_uvs:
            if i in e:
                mc.select(sel_uvs, d=True)
                mc.select(e, add=True)                  
    #Check if sel uvs are in vertical marked uvs list    
    for n in vmarkMainList:
        for u in sel_uvs:
            if u in n:
                mc.select(sel_uvs, d=True)
                mc.select(n, add=True)       
                      
#Function to create UI 
def UI():
    
    #check to see if window exists
    if mc.window('uv_straigtenerUI', exists = True):
        mc.deleteUI('uv_straigtenerUI')
    
    #create window
    uvstr = mc.window('uv_straigtenerUI', title = 'UV Straightener ALPHA', mnb = False, mxb = False, sizeable = False, widthHeight=(200,260))
    #create main layout
    mainLayout = mc.formLayout ()
    #Vertical uvs edit buttons
    txt_V=mc.text(label = 'Vertical',font='fixedWidthFont')
    addBtn_V=mc.button(label = 'Add', height=45, width = 57, c = 'vmark()')
    removeBtn_V=mc.button(label = 'Remove', height=45, width = 60, c = 'removeUvs_V()')
    unAlong_V=mc.button(label = 'Unfold_V', height=25, width = 85, c = 'unfoldAlong_V(mc.ls(sl=True))')
    unAlong_V_Auto= mc.checkBox('AutoUnfoldVertical', label = 'auto', v=True)
    #Horizontal uvs edit buttons
    txt_U=mc.text(label = 'Horizontal',font='fixedWidthFont')
    addBtn_U=mc.button(label = 'Add', height=45, width = 57, c = 'umark()')
    removeBtn_U=mc.button(label = 'Remove', height=45, width = 60, c = 'removeUvs_U()')
    unAlong_U=mc.button(label = 'Unfold_H', height=25, width = 85, c = 'unfoldAlong_U(mc.ls(sl=True))')
    unAlong_U_Auto= mc.checkBox('AutoUnfoldHorizontal', label = 'auto', v=True)
    #Seperator A
    seperator_A = mc.separator(height=10,width=200,style='in')
    #Select array button
    sel_Array_Btn=mc.button(label = 'Select Marked Arrays', height=35, width = 200, c = 'sel_Array()')
    #Seperator B
    seperator_B = mc.separator(height=10,width=200,style='in')
    #unfold button
    unfoldBtn=mc.button(label = 'Unfold', height=45, width = 200, c = 'uvunfold()')
    #unfold checkboxes
    unCollection=mc.radioCollection('unfoldCollection')
    unLegacy = mc.radioButton('unLegacy', label = 'Legacy')
    unUnfold3D = mc.radioButton('unUnfold3D', label = 'Unfold3D')
    mc.radioCollection(unCollection, edit=True, select=unLegacy)
    sel_unCollection=mc.radioCollection('selTypeunfoldCollection')
    sel_All_unBtn = mc.radioButton('sel_All_unfold', label = 'All Marked')
    sel_unBtn = mc.radioButton('sel_unfold', label = 'Selected')
    mc.radioCollection(sel_unCollection, edit=True, select=sel_All_unBtn)
    #Optimize button
    optBtn=mc.button(label = 'Optimize', height=45, width = 200, c = 'optimize()')
    optCollection=mc.radioCollection('optimize_Collection')
    opt_All_Btn = mc.radioButton('optimize_All', label = 'All Marked')
    opt_sel_Btn = mc.radioButton('optimize_Selected', label = 'Selected')
    mc.radioCollection(optCollection, edit=True, select=opt_All_Btn)
    #Seperator C
    seperator_C = mc.separator(height=10,width=200,style='in')
    #Textures width slider
    txt_slider=mc.text(label = 'Marked Lines Width Slider',font='fixedWidthFont')
    tx_width_Slider=mc.floatSlider('textures_width_slider',height=30, width = 190, min=0, max=0.03, value =0.01, dc=width_slider )
    #Seperator D
    seperator_D = mc.separator(height=10,width=200,style='in')
    #Reset button
    reset=mc.button(label = 'Reset', height=45, width = 200, c = 'reset()')
    #Clear all button
    clear=mc.button(label = 'Clear All', height=45, width = 200, c = 'clear_all()')
    #Buttons layout
    buttonsLayout  = mc.formLayout (mainLayout , edit=True, attachForm=[(txt_V, 'top', 15),
                                                                           (addBtn_V, 'top', 0),
                                                                           (removeBtn_V, 'top', 0),
                                                                           (unAlong_V, 'top', 50),
                                                                           (unAlong_V_Auto, 'top', 55),
                                                                           
                                                                           (txt_U, 'top', 100),
                                                                           (addBtn_U, 'top', 85),
                                                                           (removeBtn_U, 'top', 85),
                                                                           (unAlong_U, 'top', 135),
                                                                           (unAlong_U_Auto, 'top', 140),
                                                                           
                                                                           (seperator_A, 'top', 170),                                                                        
                                                                           (sel_Array_Btn, 'top', 188),                                                                      
                                                                           (seperator_B, 'top', 230),
                                                                           
                                                                                                                                                                                                                         
                                                                           (unfoldBtn, 'top', 250),                                                                      
                                                                           (unLegacy, 'top', 305),
                                                                           (unUnfold3D, 'top',305),
                                                                           (sel_All_unBtn, 'top', 325),
                                                                           (sel_unBtn, 'top', 325),
                                                                           
                                                                           (optBtn, 'top', 355),
                                                                           (opt_All_Btn, 'top', 410),
                                                                           (opt_sel_Btn, 'top', 410),
                                                                           
                                                                           (seperator_C, 'top', 440),                                                                      
                                                                           (txt_slider, 'top', 460),
                                                                           (tx_width_Slider, 'top', 480),                                                                        
                                                                           (seperator_D, 'top', 515),                                                                                                                    
                                                                             
                                                                           
                                                                           (reset, 'top', 545),
                                                                           (clear, 'top', 595)
    
                                                                           
                                                                           ],
    
                                                            attachPosition=[(txt_V, 'left', 0,2),
                                                                            (addBtn_V, 'left', 0,40),
                                                                            (removeBtn_V, 'left', 0,70),
                                                                            (unAlong_V, 'left', 0,2),
                                                                            (unAlong_V_Auto, 'left', 0,50),
                                                                           
                                                                            (txt_U, 'left', 0,2),
                                                                            (addBtn_U, 'left', 0,40),
                                                                            (removeBtn_U, 'left', 0,70),
                                                                            (unAlong_U, 'left', 0,2),
                                                                            (unAlong_U_Auto, 'left', 0,50),
                                                                           
                                                                            (unfoldBtn, 'left', 0,0),                                                                        
                                                                            (unLegacy, 'left', 0,2),
                                                                            (unUnfold3D, 'left', 0,45),
                                                                            (sel_All_unBtn, 'left', 0,2),
                                                                            (sel_unBtn, 'left', 0,45),
                                                                           
                                                                            (optBtn, 'left', 0,0),
                                                                            (opt_All_Btn, 'left', 0,2),
                                                                            (opt_sel_Btn, 'left', 0,45),
                                                                           
                                                                            (txt_slider, 'left', 0,5),
                                                                            (tx_width_Slider,  'left', 0,2),
                                                                           
                                                                           
                                                                            (reset, 'left', 0,0),
                                                                            (clear, 'left', 0,0)
                                                                           
                                                                            ])
    
    
    mc.showWindow(uvstr)
    #Update window size
    mc.window('uv_straigtenerUI', e=True, widthHeight=(200,645))

UI()            