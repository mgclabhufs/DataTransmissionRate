'''
HashChaning algorithm for MAC Address matching user name
format--> MAC OUI:MAC UUA:User count
|  0|  -> None
|  1| 1:3:User 1 -> None
|  2|  -> None
|  3|  -> None
|  4| 4:5:User 2 -> None
|  5|  -> None
|  6| 6:5:User 3 -> None
|  7|  -> None
|  8|  -> None
|  9|  -> None


input --> mac address OUI before 4(int), UUA front 4(int)

ex)input: set_name 45 45

If you want to see all HashChaining List, press enter 'print'

ex)input: print


**you can change hashsize & hash function
'''

class Node:
	def __init__(self, OUI, UUA, name=None):
		self.OUI = OUI
		self.UUA = UUA
		self.next = None
		self.name = name
		self.Umsg = []

	def __str__(self):
		return str(self.OUI)

class SinglyLinkedList:
	def __init__(self):
		self.head = None
	def __iter__(self):
		v = self.head
		while v != None:
			yield v
			v = v.next
	def __str__(self):
		return " -> ".join(str(v.OUI)+':'+str(v.UUA)+':'+str(v.name) for v in self) + " -> None"

	def pushFront(self, OUI, UUA, name=None, msg=None):
		new_node = Node(OUI,UUA,name)
		new_node.Umsg.append(msg)
		new_node.next = self.head
		self.head = new_node

	def popFront(self):
		if self.head == None: # empty list
			return None
		else:
			OUI = self.head.OUI
			self.head = self.head.next
			return OUI

	def search(self, UUA):
		v = self.head
		while v != None:
			if v.UUA == UUA:
				return v
			v = v.next
		return v

	def remove(self, v):
		if v == None or self.head == None:
			return None
		OUI = v.OUI
		if v == self.head:
			return self.popFront()
		else:
			prev, curr = None, self.head
			while curr != None and curr != v:
				prev = curr
				curr = curr.next
				if curr == v:
					prev.next = curr.next
			return OUI

class HashChaining:
	def __init__(self, size=10):
		self.size = size
		self.H = [SinglyLinkedList() for x in range(self.size)]
		self.user_count = 0
		
	def __str__(self):
		s = ""
		i = 0
		for k in self:
			s += "|{0:-3d}| ".format(i) + str(k) + "\n"
			i += 1
		return s
	def __iter__(self):
		for i in range(self.size):
			yield self.H[i]

	def hash_function(self, OUI):
		return OUI % self.size

	def find_slot(self, OUI):
		return self.hash_function(OUI)

	def set(self, OUI, UUA,name=None,msg=None):
		i=self.find_slot(OUI)
		v= self.H[i].search(UUA)
		if v==None:
			self.user_count+=1
			name = "User "+str(self.user_count)
			self.H[i].pushFront(OUI,UUA,name,msg)       
								
		else:
			v.Umsg.append(msg)
			v.UUA=UUA
			

	def remove(self, OUI,UUA):
		i=self.find_slot(OUI)
		v=self.H[i].search(UUA)
		if v==None:
			return None
		else:
			return self.H[i].remove(v)

	def search(self, OUI, UUA):
		i=self.find_slot(OUI)
		v=self.H[i].search(UUA)
			
		if v==None:
			return None
		else:
			return v

	def set_name(self, OUI, UUA,name = None, msg=None):
		k = self.search(OUI,UUA)
		if k==None:
			self.set(OUI,UUA,msg=msg)
			k=self.search(OUI,UUA)
			return k.name
		else:
			k.Umsg.append(msg)
			k.name

'''				
H = HashChaining(10)
while True:
	cmd = input().split()
	if cmd[0] == 'set':
		OUI = H.set(int(cmd[1]),int(cmd[2]))
		print("+ {0} : {1} is set into H".format(cmd[1],cmd[2]))
	elif cmd[0] == 'search':
		OUI = H.search(int(cmd[1]), int(cmd[2]))
		if OUI == None:
			print("* {0} is not found!".format(cmd[1]))
		else:
			print(" * {0} is found!".format(cmd[1]))
	elif cmd[0] == 'remove':
		OUI = H.remove(int(cmd[1]))
		if OUI == None:
			print("- {0} is not found, so nothing happens".format(cmd[1]))
		else:
			print("- {0} is removed".format(cmd[1]))
	elif cmd[0] == 'print':
		print(H)
	elif cmd[0] == 'exit':
		break
	elif cmd[0] == 'set_name':
		H.set_name(int(cmd[1]), int(cmd[2]))
	else:
		print("* not allowed command. enter a proper command!")
'''