class Queue: 
    # FI FO
    
    def __init__(self):
        self.array = []
    
    # Return true/false wheter the queue is empty or not
    def isEmpty(self):
        return len(self.array) == 0
    
    # Look last first element of the queue
    def peek(self): 
        if len(self.array) > 0: 
            return self.array[0]
        return None

    # Retrieve and deletes first element of the queue
    # Return null if the queue is empty
    def pop(self):
        if len(self.array) > 0: 
            head = self.array[0]
            del self.array[0]
            return head
        return None
    
    # Add an elemente to the queue
    def add(self, element):
        self.array.append(element)
    
