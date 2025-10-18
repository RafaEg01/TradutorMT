
f = open('teste.in','r', encoding="utf-8")


transitionType = (f.readline())[1]
allStates = []
newTransitionshash =[]
newTransitionShift = []
newStatesItoS = []
newTransitionsRigth = []
semiFilteredStates = []
filteredStates = []
aux = []
aux1 = []
aux2 = []
aux3 = []
transitionsSpring = [('0','_','_','l','!SymbolMarker'),('0','1','1','l','!SymbolMarker'),('0','0','0','l','!SymbolMarker'),('!SymbolMarker','_','#','r','!NewInitial'),]
transitionDelimiters = [
    ('0', '1', '#', 'r', '!shift1'),
    ('0', '0', '#', 'r', '!shift0'),

    ('!shift1', '1', '1', 'r', '!shift1'),
    ('!shift1', '0', '1', 'r', '!shift0'),
    ('!shift1', '_', '1', 'r', '!shift$'),

    ('!shift0', '0', '0', 'r', '!shift0'),
    ('!shift0', '1', '0', 'r', '!shift1'),
    ('!shift0', '_', '0', 'r', '!shift$'),
    
    ('!shift$', '_', '$', 'l', '!shiftbackInicial'),

    ('!shiftbackInicial', '0', '0', 'l', '!shiftbackInicial'),
    ('!shiftbackInicial', '1', '1', 'l', '!shiftbackInicial'),
    ('!shiftbackInicial', '_', '_', 'l', '!shiftbackInicial'),
    ('!shiftbackInicial', '#', '#', 'r', '!NewInitial'),

   
    
]
transitionModel = [
    ('', '#', '#', 'r', '!shiftRigth'),

    ('!shiftRigth', '1', '_', 'r', '!shift1'),
    ('!shiftRigth', '0', '_', 'r', '!shift0'),
    ('!shiftRigth', '_', '_', 'r', '!shiftRigth'),
    ('!shiftRigth', '$', '_', 'r', '!shift$'),

    ('!shift1', '1', '1', 'r', '!shift1'),
    ('!shift1', '0', '1', 'r', '!shift0'),
    ('!shift1', '_', '1', 'r', '!shift$'),
    ('!shift1', '$', '1', 'r', '!shiftRigth$'),

    ('!shift0', '0', '0', 'r', '!shift0'),
    ('!shift0', '1', '0', 'r', '!shift1'),
    ('!shift0', '_', '0', 'r', '!shift$'),

    ('!shift0', '$', '0', 'r', '!shiftRigth$'),

    ('!shiftRigth$', '_', '$', 'l', '!position'),

    ('!position', '0', '0', 'l', '!position'),
    ('!position', '1', '1', 'l', '!position'),
    ('!position', '_', '_', '*', '')
]
def leituraEstados(file):
  for line in file:
      if(line[0] != ';' and line[0] != '\n' ):
       allStates.append(tuple(line.split()))
  return(allStates)    

def filtroEstados(allStates):
  for i in range(len(allStates)):
    aux = list(allStates[i])
    if(aux[0] == '!NewInitial'):
      aux[0] = '0'
    if(aux[4] == '!NewInitial'):      
      aux[4] = '0'
    semiFilteredStates.append(tuple(aux))  
  for i in range(len(semiFilteredStates)):
    aux1 = list(semiFilteredStates[i])
    if(aux1[0][0] != '!' and aux1[4][0] != '!'):
      filteredStates.append(tuple(aux1))
      
  return(filteredStates)


def renomearEstadosIniciais(filteredStates):
  aux = []
  for i in range(len(filteredStates)):
    aux = list(filteredStates[i])
    if(aux[0] == '0'):
      aux[0] = '!NewInitial'
    if(aux[4] == '0'):      
      aux[4] = '!NewInitial'
    newStatesItoS.append(tuple(aux))
  return(newStatesItoS)

def estadosIparaS(newStatesItoS):
  for i in range(len(newStatesItoS)):
    if(newStatesItoS[i][3] == 'l'):
      aux.append(newStatesItoS[i][4])
  aux2 = set(aux)
  aux2 = list(aux2)
  for i in range(len(aux2)):
    newTransitionshash.append((aux2[i],'#','#','r',aux2[i]))
  for i in range(len(newTransitionshash)):
    newStatesItoS.append(newTransitionshash[i])
  return(newStatesItoS)

def estadosSparaI(renamedStates):
  for i in range(len(renamedStates)):
    if(renamedStates[i][3] == 'l'):
      aux.append(renamedStates[i][4])
    if(renamedStates[i][3] == 'r'):
      aux1.append(renamedStates[i][4])
  aux2 = set(aux)
  aux2 = list(aux2)
  aux3 = set(aux1)
  aux3 = list(aux3)
  for i in range(len(aux2)):
      for j in range(len(transitionModel)):
       newTransitionShift.append((transitionModel[j][0] + aux2[i],transitionModel[j][1],transitionModel[j][2],transitionModel[j][3], transitionModel[j][4] + aux2[i]))
  for i in range(len(aux3)):
    newTransitionsRigth.append((aux3[i],'$','_','r','!$' + aux3[i]))
    newTransitionsRigth.append(('!$' + aux3[i],'_','$','l',aux3[i]))      
  for i in range(len(newTransitionShift)):
    renamedStates.append(newTransitionShift[i])
  for i in range(len(newTransitionsRigth)):
    renamedStates.append(newTransitionsRigth[i])
  return(renamedStates)

def escritaArq(newStates,Model,transitionType):
  with open("teste.out", "w") as out:
    if(transitionType == 'S' or transitionType == 's'):
      out.write(";I\n")
    if(transitionType == 'I' or transitionType == 'i'):
      out.write(";S\n")
    for i in range(len(Model)):
      for j in range(5):
        out.write(Model[i][j] +' ')
      out.write("\n")
    for i in range(len(newStates)):
        for j in range(5):
          out.write(str(newStates[i][j]) +' ')
        out.write("\n")

if(transitionType == 'S' or transitionType == 's'):
   escritaArq(estadosSparaI(renomearEstadosIniciais(filtroEstados(leituraEstados(f)))),transitionDelimiters,transitionType)
elif(transitionType == 'I' or transitionType == 'i'):
 escritaArq(estadosIparaS(renomearEstadosIniciais(filtroEstados(leituraEstados(f)))),transitionsSpring,transitionType)
else:
  print("Informação sobre o tipo de arquivo invalida, verifique o arquivo de entrada!")
    


    


