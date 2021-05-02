class Stack: 
    # LI FO
    
    def __init__(self):
        self.array = []
    
    # Return true/false wheter the stack is empty or not
    def isEmpty(self):
        return len(self.array) == 0
    
    # Look last element of the stack
    def peek(self):  
        if len(self.array) > 0: 
            return self.array[-1]
        return None

    # Retrieve and deletes last element of the stack
    # Return null if the stack is empty
    def pop(self):
        if len(self.array) > 0: 
            last = self.array[-1]
            del self.array[-1]
            return last
        return None
    
    # Add an element to the stack
    def add(self, element):
        self.array.append(element)

    # Return the index of the element inside the stack
    # return None if the element is not
    def search(self, search_object):
        index = 0
        for element in self.array:
            if search_object == element:
                return index
            index += 1
        return None

    # Method to print all the stack
    def print(self):
        print(self.array)
    
