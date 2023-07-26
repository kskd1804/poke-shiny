from constants import PokemonConstants

class Pokemon:
    
    def __init__(self, poke_content):
        self.contents = poke_content

    def get_contents(self):
        return self.contents

    def get_personality_value(self):
        return self.read(PokemonConstants.personality_value_offset, PokemonConstants.personality_value_size)
    
    def get_original_trainer_id(self):
        return self.read(PokemonConstants.original_trainer_id_offset, PokemonConstants.original_trainer_id_size)

    def get_data(self):
        return self.read(PokemonConstants.data_offset, PokemonConstants.data_size)

    def set_data(self, new_bytes):
        self.overwrite(PokemonConstants.data_offset, PokemonConstants.data_size, new_bytes)

    def read(self, address, num_bytes):
        start = address - 0x0000
        end = start + num_bytes
        return self.contents[start:end]

    def overwrite(self, address, num_bytes, new_bytes):
        start = address - 0x0000
        end = start + num_bytes
        self.contents = self.contents[:start] + new_bytes + self.contents[end:]

    def set_personality_value(self):
        personality_value = self.get_original_trainer_id()
        new_shuffle_order = int.from_bytes(personality_value, byteorder='little') % 24
        new_shuffle_blocks = PokemonConstants.substructure_order[new_shuffle_order]
        old_shuffle_blocks = PokemonConstants.substructure_order[self.shuffle_order]
        block_data = { "G": None, "A": None, "E": None, "M": None }
        for i, block in enumerate(old_shuffle_blocks):
            block_data[block] = self.read(PokemonConstants.data_offset + (i * PokemonConstants.subsection_block_size), PokemonConstants.subsection_block_size)
        for i, block in enumerate(new_shuffle_blocks):
            self.overwrite(PokemonConstants.data_offset + (i * PokemonConstants.subsection_block_size), PokemonConstants.subsection_block_size, block_data[block])
        self.overwrite(PokemonConstants.personality_value_offset, PokemonConstants.personality_value_size, personality_value)

    def get_key(self, bytes1, bytes2):
        result = bytearray()
        for b1, b2 in zip(bytes1, bytes2):
            result.append(b1 ^ b2)
        return result

    def calculate_checksum(self, data):
        checksum = 0x0
        for i in range(0, len(data), 2):
            checksum += int.from_bytes(data[i:i+2], byteorder='little')
        return checksum

    def crypt_data(self):
        key = self.get_key(self.get_original_trainer_id(), self.get_personality_value())
        new = bytearray()
        data = self.get_data()
        self.shuffle_order = int.from_bytes(self.get_personality_value(), byteorder='little') % 24
        for i in range(0, len(data), 4):
            bytes_4 = data[i:i+4]
            for b, k in zip(bytes_4, key):
                new.append(b ^ k)
        self.set_data(new)
        
    