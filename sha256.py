import hashlib

def sha256_hash(message: str) -> str:
    """Gera o hash SHA-256 da mensagem fornecida."""
    sha_signature = hashlib.sha256(message.encode()).hexdigest()
    return sha_signature

def sha256_verify(message: str, hash_value: str) -> bool:
    """Verifica se o hash da mensagem fornecida corresponde ao hash fornecido."""
    return sha256_hash(message) == hash_value

if __name__ == "__main__":
    plain_text = "Exemplo de mensagem"
    generated_hash = sha256_hash(plain_text)
    
    print(f"Mensagem original: {plain_text}")
    print(f"Hash SHA-256 gerado: {generated_hash}")

    # Verificação
    is_valid = sha256_verify(plain_text, generated_hash)
    print(f"A verificação do hash corresponde? {'Sim' if is_valid else 'Não'}")

    # Teste com uma mensagem diferente
    different_text = "Mensagem diferente"
    is_valid = sha256_verify(different_text, generated_hash)
    print(f"A verificação do hash com uma mensagem diferente corresponde? {'Sim' if is_valid else 'Não'}")
