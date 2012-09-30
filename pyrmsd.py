#!/usr/bin/python

import sys

def read(name):
	f=open(name,'r')
	lines=f.readlines()
	f.close()
	lig={'elem':[],'pos':[],'matrix':[],'count':0}
	connect=[x.split() for x in lines if len(x.split())==7]
	coord=[x.split() for x in lines if len(x.split())==16]
	lig['pos']=[]
	lig['elem']=[]
	lig['count']=len(coord)
	lig['neib']=[]
	for one in coord:
		lig['pos'].append([float(x) for x in one[0:3]])
		lig['elem'].append(filter(str.isalpha,one[3]).upper())
	lig['matrix']=[[0 for col in range(lig['count'])] for row in range(lig['count'])]
	for one in connect:
		if int(one[2])!=0:
			lig['matrix'][int(one[0])-1][int(one[1])-1]=1
			lig['matrix'][int(one[1])-1][int(one[0])-1]=1
	for i in range(lig['count']):
		lig['neib'].append(''.join(sorted([lig['elem'][x] for x in range(lig['count']) if lig['matrix'][i][x]!=0])))
	return lig

def findCand(lig, native):
	if (lig['count']!=native['count']):
		return -1
	count=lig['count']
	candidate=[[i] for i in range(count)]
	for i in range(lig['count']):
		for j in range(lig['count']):
			if (lig['neib'][i]==native['neib'][j]):
				flag=True
				for x in [t for t in range(count) if (lig['matrix'][i][t]!=0)]:
					inflag=False
					for y in [t for t in range(count) if (native['matrix'][j][t]!=0)]:
						if (lig['neib'][x]==native['neib'][y]):
							inflag=True
							break
					if (inflag==False):
						flag=False
						break
				if (flag):
					candidate[i].append(j)
	return candidate
	#return sorted(candidate,key=lambda x:len(x))

def calcRMSD(lig,native,map):
	sum=0.0;
	for i in range(len(map)):
		j=map[i]
		sum+=(lig['pos'][i][0]-native['pos'][j][0])**2+(lig['pos'][i][1]-native['pos'][j][1])**2+(lig['pos'][i][2]-native['pos'][j][2])**2
	return (sum/len(map))**0.5
		

def tryMap(l,map,visited,candidate,log,lig,native):
	if (l>=len(candidate)):
		x=calcRMSD(lig,native,map)
		if x<log:
			log=x
		return log
	else:
		for i in range(len(candidate[l])-1):
			if (visited[candidate[l][1+i]]==False):
				map[candidate[l][0]]=candidate[l][1+i]
				visited[candidate[l][1+i]]=True
				log=tryMap(l+1,map,visited,candidate,log,lig,native)
				map[candidate[l][0]]=-1
				visited[candidate[l][1+i]]=False
		return log
	pass
	
	
def getRMSD(lig_name, native_name):
	lig=read(lig_name)
	native=read(native_name)
	if (lig['count']!=native['count']):
		return -1
	count=lig['count']
	candidate=findCand(lig,native)
	map=[-1]*count
	visited=[False]*count
	need2try=[]
	for one in candidate:
		if len(one)==2:
			map[one[0]]=one[1]
			visited[one[1]]=True
		else:
			need2try.append(one)
	log=1e9
	log=tryMap(0,map,visited,sorted(need2try,key=lambda x:len(x)),log,lig,native)
	return log

if __name__=='__main__':
	lig_name=sys.argv[1]
	native_name=sys.argv[2]
	print getRMSD(lig_name,native_name)
