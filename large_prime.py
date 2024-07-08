# Código adaptado do site GeeksForGeeks
# Disponível em https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
import random

# Primos pré-gerados
FIRST_PRIMES_LIST = [
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
  31, 37, 41, 43, 47, 53, 59, 61, 67, 
  71, 73, 79, 83, 89, 97, 101, 103, 107, 
  109, 113, 127, 131, 137, 139, 149, 151, 
  157, 163, 167, 173, 179, 181, 191, 193, 
  197, 199, 211, 223, 227, 229, 233, 239, 
  241, 251, 257, 263, 269, 271, 277, 281, 
  283, 293, 307, 311, 313, 317, 331, 337, 
  347, 349
]
# Total de iterações para o teste de Miller Rabin
NUMBER_OF_RABIN_TRAILS = 20
# Total de bits que o primo gerado deve ter por padrão
DEFAULT_PRIME_BITS = 1024
 
def __n_bit_random(n: int) -> int:
	"""Sorteia um número com n bits.

	Args:
			n (int): total de bits do número a ser sorteado

	Returns:
			int: número sorteado
	"""
	return random.randrange(2**(n-1)+1, 2**n - 1)

def __get_low_level_prime_candidate(n: int) -> int:
	"""Gera um candidato a primo que, seja divisível por um dos primos na lista 
	`FIRST_PRIMES_LIST`.

	Um número aleatório de n bits é sorteado, então sua divisibilidade pelos primos 
	na lista é testada para verificar se é um bom candidato a primo.

	Args:
			n (int): número de bits que o candidato de primo terá

	Returns:
			int: candidato a primo
	"""
	while True:
		prime_candidate = __n_bit_random(n)

		for divisor in FIRST_PRIMES_LIST:
			if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate: break
		else:
			return prime_candidate
 
def __is_miller_rabin_passed(prime_candidate: int) -> bool:
	"""Roda 20 iterações do teste de primaridade de Rabin Miller.

	Args:
			prime_candidate (int): candidato a primo selecionado

	Returns:
			bool: o candidato a primo é, confirmadamente, primo
	"""
	max_divisions_by_two = 0
	ec = prime_candidate - 1
	while ec % 2 == 0:
		ec >>= 1
		max_divisions_by_two += 1
	assert(2**max_divisions_by_two * ec == prime_candidate-1)

	def trial_composite(round_tester):
		if pow(round_tester, ec, prime_candidate) == 1:
			return False
		for i in range(max_divisions_by_two):
			if pow(round_tester, 2**i * ec, prime_candidate) == prime_candidate-1:
				return False
		return True

	for i in range(NUMBER_OF_RABIN_TRAILS):
		round_tester = random.randrange(2, prime_candidate)
		if trial_composite(round_tester):
			return False
	return True
 
def get_random_large_prime(bits: int = DEFAULT_PRIME_BITS) -> int:
	"""Sorteia um número primo qualquer com a quantidade de bits especificada.

	Args:
			bits (int, optional): total de bits do número a ser gerado. Defaults to DEFAULT_PRIME_BITS.

	Returns:
			int: número primo gerado
	"""
	while True:
		prime_candidate = __get_low_level_prime_candidate(bits)
		if not __is_miller_rabin_passed(prime_candidate):
			continue
		else:
			break

	return prime_candidate
