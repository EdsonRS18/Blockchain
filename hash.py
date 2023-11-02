import math
import random
import datetime

def custom_hash(input_str):
    ascii_values = [ord(char) for char in input_str]
    seed = sum(ascii_values) % 1000000
    seed = ''.join(str(value) for value in ascii_values)
    random.seed(seed)
    
    def custom_seno(char):
        return math.sin(ord(char) + random.random())
    
    def custom_cosseno(char):
        return math.cos(ord(char) + random.random())
    
    def custom_transform(char):
        return (ord(char) ** 2) + random.random()
    
    transformed_values = []
    for char in input_str:
        transformed = custom_seno(char) + custom_cosseno(char) + custom_transform(char)
        transformed_values.append(int(transformed * 1000))
    
    while len(transformed_values) < 32:
        random_value = random.randint(0, 15)
        transformed_values.append(random_value)
    
    transformed_values = transformed_values[:32]
    hex_hash = ''.join(format(value, 'x') for value in transformed_values)
    
    if len(hex_hash) > 32:
        hex_hash = hex_hash[:32]
    
    return hex_hash
class Block:
    def __init__(self, index, data, previous_hash, timestamp, hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash = hash
        self.valid = True

def calculate_hash(index, data, previous_hash, timestamp):
    hash_string = f"{index}{data}{previous_hash}{timestamp}"
    return custom_hash(hash_string)

def create_genesis_block(data):
    return Block(0, data, "0", datetime.datetime.now(), calculate_hash(0, data, "0", datetime.datetime.now()))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = datetime.datetime.now()
    hash = calculate_hash(index, data, previous_block.hash, timestamp)
    return Block(index, data, previous_block.hash, timestamp, hash)

def create_or_add_block(data, blockchain, genesis_created):
    if not genesis_created:
        blockchain.append(create_genesis_block(data))
        print("Bloco de Gênese criado com sucesso!")
        return True
    else:
        if all(block.valid for block in blockchain):
            new_block = create_new_block(blockchain[-1], data)
            blockchain.append(new_block)
            print(f"Novo bloco adicionado! Hash: {new_block.hash}")
            return True
        else:
            print("Há blocos inválidos. Não é possível adicionar novos blocos.")
            return False

def save_blocks_to_file(filename, blocks):
    with open(filename, 'w', encoding='utf-8') as file:
        for block in blocks:
            file.write(f"Índice: {block.index}\n")
            file.write(f"Timestamp: {block.timestamp}\n")
            file.write(f"Data: {block.data}\n")
            file.write(f"Hash: {block.hash}\n")
            file.write(f"Hash Anterior: {block.previous_hash}\n")
            file.write(f"Validação: {'Válido' if block.valid else 'Inválido'}\n")
            file.write("=" * 40 + "\n\n")  # Linha separadora

def load_blocks_from_file(filename):
    blocks = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        index = None
        data = None
        previous_hash = None
        timestamp = None
        hash = None
        valid = None

        for line in lines:
            if line.startswith("Índice:"):
                index = int(line.split(":")[1].strip())
            elif line.startswith("Timestamp:"):
                timestamp = datetime.datetime.strptime(line.split(":", 1)[1].strip(), "%Y-%m-%d %H:%M:%S.%f")
            elif line.startswith("Data:"):
                data = line.split(":", 1)[1].strip()
            elif line.startswith("Hash:"):
                hash = line.split(":", 1)[1].strip()
            elif line.startswith("Hash Anterior:"):
                previous_hash = line.split(":", 1)[1].strip()
            elif line.startswith("Validação:"):
                valid = line.split(":", 1)[1].strip() == "Válido"
            elif line.strip() == "=" * 40:
                blocks.append(Block(index, data, previous_hash, timestamp, hash))
                blocks[-1].valid = valid

    return blocks

blockchain = []
genesis_created = False

while True:
    print("\nMenu:")
    print("1. Criar/Adicionar Bloco")
    print("2. Listar Blocos")
    print("3. 2 Blockchain")
    print("0. Sair")

    choice = input("Escolha uma opção: ")

    if choice == '1':
        data = input("Digite os dados para o bloco: ")
        genesis_created = create_or_add_block(data, blockchain, genesis_created)
            
    elif choice == '2':
        print("\nLista de Blocos:")
        for block in blockchain:
            print(f"Índice: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Hash Anterior: {block.previous_hash}")
            print(f"Validação: {'Válido' if block.valid else 'Inválido'}\n")
        
        # Salvando as informações dos blocos em um arquivo
        save_blocks_to_file("blockchain.json", blockchain)
        print("Informações dos blocos foram salvas no arquivo 'blockchain.json'.")
            
            
    elif choice == '3':
        existing_file = input("Digite o caminho do arquivo da blockchain existente: ")
        blockchain = load_blocks_from_file(existing_file)
        genesis_created = True
        print("Blockchain carregada com sucesso!")
        
    else:
        print("Opção inválida. Escolha novamente.")