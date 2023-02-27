class Linked_List:
    
    class __Node:
        
        def __init__(self, val):
            # Declare and initialize the public attributes for objects of the
            # Node class. TODO replace pass with your implementation
            self.get_value=val
            self.next=None
            self.prev=None

           

    def __init__(self):
        # Declare and initialize the private attributes for objects of the
        # sentineled Linked_List class TODO replace pass with your
        # implementation
        self.__header=self.__Node(None)
        self.__trailer=self.__Node(None)
        self.__header.next=self.__trailer
        self.__trailer.prev=self.__header
        self.__size=0
        

    def __len__(self):
        # Return the number of value-containing nodes in this list. TODO replace
        # pass with your implementation
        return self.__size
        

    def append(self, val):
        # Increase the size of the list by one, and add a node containing val at
        # the new tail position. this is the only way to add items at the tail
        # position. TODO replace pass with your implementation
        new=self.__Node(val)
        self.__trailer.prev.next=new
        new.prev=self.__trailer.prev
        self.__trailer.prev=new
        new.next=self.__trailer
        self.__size=self.__size+1

    def insert_element_at(self, val, index):
        if index>=self.__size or index<0:
            raise IndexError
        else:
            new=self.__Node(val)
            cur=self.__header
            for i in range(index):
                cur=cur.next
            cur.next.prev=new
            new.next=cur.next
            cur.next=new
            new.prev=cur
        self.__size=self.__size+1

    def remove_element_at(self, index):
        if index>=self.__size or index<0:
            raise IndexError
        elif index+1==self.__size:
            val=self.__trailer.prev.get_value
            self.__trailer.prev=self.__trailer.prev.prev
            self.__trailer.prev.next=self.__trailer
        else:
            cur=self.__header
            for i in range(index):
                cur=cur.next
            val=cur.next.get_value
            cur.next=cur.next.next
            cur.next.prev=cur
        self.__size=self.__size-1
        return val

    def get_element_at(self, index):
        if index>=self.__size or index<0:
            raise IndexError
        cur=self.__header
        for i in range(index):
            cur=cur.next
        val=cur.next.get_value
        return val

        

    def rotate_left(self):
        if self.__size<=1:
            pass
        else:
            mover=self.__header.next
            mover.next.prev=self.__header
            self.__header.next=mover.next
            self.__trailer.prev.next=mover
            mover.prev=self.__trailer.prev
            mover.next=self.__trailer
            self.__trailer.prev=mover
        
    def __str__(self):
        if self.__size==0:
            return ''
        else:
            stuff=''
            for item in self:
                stuff=stuff+'|'+str(item)
            return stuff


    def __iter__(self):
        self.__iter=self.__header.next
        return self

    def __next__(self):
        if self.__iter==self.__trailer:
            raise StopIteration
        to_return=self.__iter.get_value
        self.__iter=self.__iter.next
        return to_return
        

    def __reversed__(self):
        flip=Linked_List()
        cur=self.__trailer.prev
        for i in range(self.__size):
            flip.append_element(cur.get_value)
            cur=cur.prev
        return flip

if __name__ == '__main__':
    # Your test code should go here. Be sure to look at cases when the list is
    # empty, when it has one element, and when it has several elements. Do the
    # indexed methods raise exceptions when given invalid indices? Do they
    # position items correctly when given valid indices? Does the string
    # representation of your list conform to the specified format? Does removing
    # an element function correctly regardless of that element's location? Does
    # a for loop iterate through your list from head to tail? Does a for loop
    # iterate through your reversed list from tail to head? Your writeup should
    # explain why you chose the test cases. Leave all test cases in your code
    # when submitting. TODO replace pass with your tests
    my_list=Linked_List()
    my_list.append_element(6)
    my_list.insert_element_at(4,0)
    my_list.insert_element_at(7,1)
    my_list.insert_element_at(8,1)
    my_list.remove_element_at(2)
    print(len(my_list))
    try:
        my_list.insert_element_at(12,3)
    except IndexError:
        print('goteem')
    try:
        my_list.remove_element_at(4)
    except IndexError:
        print('goteem')
    try:
        my_list.insert_element_at(-2,-2)
    except IndexError:
        print('goteem')
    

    for item in my_list:
        print(item)
    print(my_list)
    print(reversed(my_list))
    my_list.rotate_left()
    print(my_list)

    
  

