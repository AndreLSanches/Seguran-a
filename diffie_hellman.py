from random import randint
if __name__ == "__main__":
  from large_prime import get_random_large_prime
else:
	from large_prime import get_random_large_prime

MAX_PRIVATE_VALUE = 1000

def __computes_value_to_send(alpha: int, private: int, p: int) -> int:
	return pow(alpha, private, p)

def __calculate_psk(received_value: int, private: int, p: int) -> int:
	return pow(received_value, private, p)

def get_value_to_send(alpha: int, p: int) -> tuple[int, int]:
	private = randint(2, MAX_PRIVATE_VALUE)
	to_send = __computes_value_to_send(alpha, private, p)

	return private, to_send

def generate_psk(received_value: int, private: int, p: int) -> int:
	psk = __calculate_psk(received_value, private, p)

	return psk

if __name__ == "__main__":
	alpha, p = [get_random_large_prime() for i in range(2)]
	private_a, a_to_send = get_value_to_send(alpha, p)
	private_b, b_to_send = get_value_to_send(alpha, p)

	psk_a = generate_psk(b_to_send, private_a, p)
	psk_b = generate_psk(a_to_send, private_b, p)
 
	print("Chaves geradas são iguais: %s" % ("Sim" if psk_a == psk_b else "Não"))
	print(psk_a)
	print(psk_b)
