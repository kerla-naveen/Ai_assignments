import copy
class state:
    def __init__(self,List,side,cost):
        """self.ayansh=ayansh
        self.ananya=ananya
        self.grandma=grandma
        self.grandpa=grandpa"""
        self.side=side
        self.List=List
        self.cost=cost
        
    def testGoal(self):
        if self.List[0][1]==self.List[1][1]==self.List[2][1]==self.List[3][1]=='r' and self.cost<=65:
            return True
        else:
            return False

    def genMoves(self):
        children=[]
        if self.side=='l':
            for i in range(0,len(self.List)-1):
                for j in range(i+1,len(self.List)):
                    a=self.List[i]
                    b=self.List[j]
                    if(a[1]==b[1]=='l'):
                        new_List = copy.deepcopy(self.List)
                        new_List[i][1]='r'
                        new_List[j][1]='r'
                        cost=a[2] if a[2]>b[2] else b[2]
                        children.append(state(new_List,'r',self.cost+cost))
        else:
            for i in range(0,len(self.List)):
                if(self.List[i][1]=='r'):
                    new_List = copy.deepcopy(self.List)
                    new_List[i][1]='l'
                    children.append(state(new_List,'l',self.cost+new_List[i][2]))
        return children
        
    def removeSeen(self,open,closed,children):
        open_n=[n for n,parent in open]
        closed_n=[n for n,parent in closed]
        unseen_nodes=[c for c in children if c not in open_n and c not in closed_n]
        return unseen_nodes

    def reconstructPath(self,closed,node_pair):
        path=[]
        parent_map={}
        for node,parent in closed:
            parent_map[node]=parent
            
        node,parent=node_pair
        parent_map[node]=parent
        while node:
            path.append(node)
            node=parent_map[node]
        path.reverse()
        return path
        
    def BFS(self):
        open=[]
        closed=[]
        open.append((self,None))
        while open:
            node_pair=open.pop(0)
            node,parent=node_pair
            if node.testGoal():
                res=(self.reconstructPath(closed,node_pair),node.cost)
                return res
            else:
                closed.append(node_pair)
                children=node.genMoves()
                unseen_nodes=self.removeSeen(open,closed,children)
                node_pairs=[(c,node) for c in unseen_nodes]
                open=open+node_pairs
    
    def __eq__(self,other):
        return self.side == other.side and all(p1 == p2 for p1, p2 in zip(self.List, other.List))
        
    def __hash__(self):
       return hash(tuple(tuple(person) for person in self.List))
        
    def __str__(self):
        return "ayansh:"+self.List[0][1]+" ananya:"+self.List[1][1]+" grandma:"+self.List[2][1]+" grandpa:"+self.List[3][1]
        
obj=state([["ayansh",'l',5],["ananya",'l',10],["grandma",'l',20],["grandpa",'l',25]],'l',0)
children=obj.genMoves()
"""for c in children:
    print(c)
    print(c.cost,c.side)
    print("\n")"""
res=obj.BFS()
for node in res[0]:
    print(node)
    print("\n")
print("the required time to cross the bridge is:",res[1])
