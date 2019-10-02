import numpy as np
from stl import mesh

def computeSketch(specs, depths):
    x = [0]
    y = [0]
    for i in range(specs["pinNumber"]):
        x.append(specs["tfc"] + i*specs["spacing"] - specs["rootCut"]/2)
        y.append(-specs["increment"]*depths[i])
        x.append(specs["tfc"] + i*specs["spacing"] + specs["rootCut"]/2)
        y.append(-specs["increment"]*depths[i])

    #Bottom part
    x.append(specs["tfc"] + (specs["pinNumber"])*specs["spacing"] + specs["rootCut"]/2)
    y.append(-(specs["maxDepth"]+1)*specs["increment"])
    #Need this to for mesh design
    for i in range(specs["pinNumber"]):
        x.append(specs["tfc"] + (specs["pinNumber"]-1-i)*specs["spacing"] + specs["rootCut"]/2)
        y.append(-(specs["maxDepth"]+1)*specs["increment"])
        x.append(specs["tfc"] + (specs["pinNumber"]-1-i)*specs["spacing"] - specs["rootCut"]/2)
        y.append(-(specs["maxDepth"]+1)*specs["increment"])

    x.append(0)
    y.append(-(specs["maxDepth"]+1)*specs["increment"])

    x.append(0)
    y.append(-specs["keyHeight"] + .1)
    x.append(specs["tfc"]+(specs["pinNumber"]-1)*specs["spacing"])
    y.append(-specs["keyHeight"] + .1)
    x.append(specs["tfc"]+(specs["pinNumber"]-1)*specs["spacing"])
    y.append(-specs["keyHeight"])
    x.append(0)
    y.append(-specs["keyHeight"])

    #Handle
    x.append(0)
    y.append(y[-1]-.1)
    x.append(-.3)
    y.append(y[-1])
    x.append(-1.5)
    y.append(y[-1])
    x.append(-1.5)
    y.append(0.7)
    x.append(-.3)
    y.append(0.7)
    x.append(-.3)
    y.append(0.1)
    x.append(0)
    y.append(0.1)
    x.append(0)
    y.append(0)

    return x,y

def computeMeshData(x, y, pinNumber, depths, extrudedHeight = 0.1):
    #pinNumber can be calculated from length of x or y but it's easier to take it as an argument.
    #This is super messy, really. Might want to change this.
    pointsBase = list(zip(x,y,[0]*len(x)))
    pointsExtruded = list(zip(x,y,[extrudedHeight]*len(x)))

    #sides
    data = np.zeros((2*(len(x)-1),3,3))
    for i in range(len(x)-1):
        data[2*i,0] = pointsBase[i]
        data[2*i,2] = pointsBase[i+1]
        data[2*i,1] = pointsExtruded[i]
        data[2*i + 1,0] = pointsBase[i+1]
        data[2*i + 1,2] = pointsExtruded[i+1]
        data[2*i + 1,1] = pointsExtruded[i]

    #handle + bottom
    data = np.insert(data,len(data),[pointsBase[-2],pointsBase[-8],pointsBase[-7]], axis=0)
    data = np.insert(data,len(data),[pointsBase[-2],pointsBase[-7],pointsBase[-3]], axis=0)
    data = np.insert(data,len(data),[pointsExtruded[-2],pointsExtruded[-7],pointsExtruded[-8]], axis=0)
    data = np.insert(data,len(data),[pointsExtruded[-2],pointsExtruded[-3],pointsExtruded[-7]], axis=0)
    data = np.insert(data,len(data),[pointsBase[-7],pointsBase[-6],pointsBase[-4]], axis=0)
    data = np.insert(data,len(data),[pointsBase[-6],pointsBase[-5],pointsBase[-4]], axis=0)
    data = np.insert(data,len(data),[pointsExtruded[-7],pointsExtruded[-4],pointsExtruded[-6]], axis=0)
    data = np.insert(data,len(data),[pointsExtruded[-6],pointsExtruded[-4],pointsExtruded[-5]], axis=0)
    data = np.insert(data,len(data),[pointsBase[-9],pointsBase[-12],pointsBase[-10]], axis=0)
    data = np.insert(data,len(data),[pointsBase[-10],pointsBase[-12],pointsBase[-11]], axis=0)
    data = np.insert(data,len(data),[pointsExtruded[-9],pointsExtruded[-10],pointsExtruded[-12]], axis=0)
    data = np.insert(data,len(data),[pointsExtruded[-10],pointsExtruded[-11],pointsExtruded[-12]], axis=0)

    #bitting
    prevDepth = 0
    for i in range(pinNumber):
        if prevDepth == depths[i]:
            data = np.insert(data,len(data),[pointsBase[2*i],pointsBase[2*i+2],pointsBase[2+4*pinNumber-2*i]], axis=0)
            data = np.insert(data,len(data),[pointsBase[2*i+2],pointsBase[4*pinNumber-2*i],pointsBase[2+4*pinNumber-2*i]], axis=0)
            data = np.insert(data,len(data),[pointsExtruded[2*i+2],pointsExtruded[2*i],pointsExtruded[2+4*pinNumber-2*i]], axis=0)
            data = np.insert(data,len(data),[pointsExtruded[2*i+2],pointsExtruded[2+4*pinNumber-2*i],pointsExtruded[4*pinNumber-2*i]], axis=0)
        else:
            data = np.insert(data,len(data),[pointsBase[2*i+1],pointsBase[2*i+2],pointsBase[4*pinNumber-2*i]], axis=0)
            data = np.insert(data,len(data),[pointsBase[2*i+1],pointsBase[4*pinNumber-2*i],pointsBase[1+4*pinNumber-2*i]], axis=0)
            data = np.insert(data,len(data),[pointsExtruded[2*i+2],pointsExtruded[2*i+1],pointsExtruded[4*pinNumber-2*i]], axis=0)
            data = np.insert(data,len(data),[pointsExtruded[2*i+1],pointsExtruded[1+4*pinNumber-2*i],pointsExtruded[4*pinNumber-2*i]], axis=0)
            if prevDepth < depths[i]:
                midPointBase = [pointsBase[2*i][0],pointsBase[2*i+1][1],0]
                midPointExtruded = [pointsBase[2*i][0],pointsBase[2*i+1][1],extrudedHeight]
                data = np.insert(data,len(data),[pointsBase[2*i],pointsBase[2*i+1],midPointBase], axis=0)
                data = np.insert(data,len(data),[pointsBase[2+4*pinNumber-2*i],midPointBase,pointsBase[2*i+1]], axis=0)
                data = np.insert(data,len(data),[pointsBase[1+4*pinNumber-2*i],pointsBase[2+4*pinNumber-2*i],pointsBase[2*i+1]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2*i],midPointExtruded,pointsExtruded[2*i+1]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2+4*pinNumber-2*i],pointsExtruded[2*i+1],midPointExtruded], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2+4*pinNumber-2*i],pointsExtruded[1+4*pinNumber-2*i],pointsExtruded[2*i+1]], axis=0)

            else:
                midPointBase = [pointsBase[2*i+1][0],pointsBase[2*i][1],0]
                midPointExtruded = [pointsBase[2*i+1][0],pointsBase[2*i][1],extrudedHeight]
                data = np.insert(data,len(data),[pointsBase[2*i],pointsBase[2*i+1],midPointBase], axis=0)
                data = np.insert(data,len(data),[pointsBase[2+4*pinNumber-2*i],pointsBase[2*i],midPointBase], axis=0)
                data = np.insert(data,len(data),[pointsBase[2+4*pinNumber-2*i],midPointBase,pointsBase[1+4*pinNumber-2*i]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2*i],midPointExtruded,pointsExtruded[2*i+1]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2+4*pinNumber-2*i],midPointExtruded,pointsExtruded[2*i]], axis=0)
                data = np.insert(data,len(data),[pointsExtruded[2+4*pinNumber-2*i],pointsExtruded[1+4*pinNumber-2*i],midPointExtruded], axis=0)
        prevDepth = depths[i]
    data = np.insert(data,len(data),[pointsBase[2*pinNumber],pointsBase[2*pinNumber+1],pointsBase[2*pinNumber+2]], axis=0)
    data = np.insert(data,len(data),[pointsExtruded[2*pinNumber],pointsExtruded[2*pinNumber+2],pointsExtruded[2*pinNumber+1]], axis=0)
    return data

def generateSTL(data, name="key.stl"):
    if data is None:
        print("No Mesh, can't save STL")
        return
    key = mesh.Mesh(np.zeros(data.shape[0], dtype=mesh.Mesh.dtype))
    key.vectors = data
    key.save(name)
