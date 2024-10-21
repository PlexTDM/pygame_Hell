class HashTable():
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        
    def hash_function(self, key):
        return hash(key) % self.size
    def insert(self, key, value):
        self.table[self.hash_function(key)] = value
    
    def get(self, key):
        return self.table[self.hash_function(key)]
    
hashTable = HashTable(10)
hashTable.insert("name","Anar")
# print(hashTable.get("name"))

print(hashTable.hash_function('name'))
            