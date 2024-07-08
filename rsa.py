import base64
from random import randint
if __name__ == "__main__":
  from large_prime import get_random_large_prime
else:
  from large_prime import get_random_large_prime


MAX_NTH_E_CANDIDATE = 20

def __mdc(a: int, b: int) -> int:
  """Cálculo do máximo divisor comum.

  Args:
      a (int): Valor de A
      b (int): Valor de B

  Returns:
      int: Máximo divisor comum
  """
  if not b: return a
  
  return __mdc(b, a % b)

def __select_e(phi: int, n: int, e_candidate: int = 2, nth_candidate: int = 1) -> int:
  """Seleciona um número adequeado para ser o e.
  
  O e não pode ser fator de n e o mdc com φ(n) é 1.

  Args:
      phi (int): Valor de φ(n)
      n (int): Valor de n
      e_candidate (int, optional): Valor do candidato de e para a recursão atual. Defaults to 2.
      nth_candidate (int, optional): qual candidato de e escolher. Defaults to 1.

  Returns:
      int: Valor de e selecionado
  """
  if(n % e_candidate == 0 or __mdc(phi, e_candidate) != 1): return __select_e(phi, n, e_candidate+1, nth_candidate)
  
  return e_candidate if nth_candidate == 1 else __select_e(phi, n, e_candidate+1, nth_candidate-1)

def __get_d(e: int, phi: int, k: int = 2) -> int:
  """Irá calcular a congruência entre e^-1 e φ(n).
  
  d ≅ e^-1 mod(φ(n))
  
  O cálculo do congruente pode ser reescrito na forma d = k*e^-1 + φ(n).
  
  Para o cálculo ser realizado de maneira direta o valor de d ou k deveriam ser conhecidos
  para encontrar apenas o desconhecido, mas nesse caso ambos são desconhecidos.
  
  Como k pode ser definido como {k ∈ N | k > 1}, então uma estratégia é tentar todos os 
  valores possíveis para k até que a expressão [(phi*k + 1) / e] seja um número natural 
  e não um real.
  
  Como os resultados podem crescer absurdamente ao trabalhar com primos muito largos, na 
  faixa de 128 bytes, operações envolvendo floats disparam o erro OverflowError uma vez que 
  Python não suporta operações para floats tão largos, porém suporta para ints, então é 
  realizada a divisão inteira, ou floor division e posteriormente o cálculo do resto 
  para verificar se essa operação resultou um um natural ou real. Caso um real, o cálculo 
  é refeito incrementando o valor de k em 1 via recursão.

  Args:
      e (int): Valor de e selecionado
      phi (int): valor de φ(n) calculado
      k (int, optional): Valor de k para a recursãoa atual. Defaults to 2.
  
  Returns:
      int: Valor de d
  """
  d_candidate = (phi*k + 1) // e
  remainder = (phi*k + 1) % e
  if not remainder == 0: return __get_d(e, phi, k+1)
  
  return int(d_candidate)

def generate_keys() -> tuple[tuple[int, int], tuple[int, int]]:
  """Gerador de chaves RSA.
  
  Sorteia primos aleatórios e opera em cima deles para geração de 
  pares de chave pública e chave privativa.

  Returns:
      tuple[tuple[int, int], tuple[int, int]]: Conjunto de chaves pública e privada, respectivamente
  """
  p, q = [get_random_large_prime() for i in range(2)]
  n = p*q
  phi = (p - 1) * (q - 1)
  e = __select_e(phi, n, nth_candidate=randint(1, MAX_NTH_E_CANDIDATE))
  d = __get_d(e, phi)

  puk = (e, n)
  prk = (d, n)

  return puk, prk

def __get_number_of_digits(n: int) -> int:
  if n != 0: return __get_number_of_digits(n // 10) + 1

  return 0

def __zero_fill_int_as_str(n: int, fill: int) -> str:
  total_zeros = fill - __get_number_of_digits(n)
  zeros = "".join(["0" for i in range(total_zeros)])
  return zeros + str(n)

def encrypt(message: str, puk: tuple[int, int]) -> str:
  e, n = puk
  digits = __get_number_of_digits(n)
  encrypted_bytes = list()
  for byte in base64.b64encode(message.encode('utf-8')):
    encrypted_bytes.append(__zero_fill_int_as_str(pow(byte, e, n), digits))
  
  encrypted = "".join(encrypted_bytes)
  
  return encrypted

def decrypt(message: str, prk: tuple[int, int]) -> str:
  d, n = prk
  digits = __get_number_of_digits(n)
  decrypted_bytes = list()
  for i in range(0, len(message), digits):
    byte = int(message[i:i+digits])
    decrypted_bytes.append(pow(byte, d, n))
  
  decrypted = base64.b64decode(bytearray(decrypted_bytes) + b"==").decode('utf-8')
  
  return decrypted

if __name__ == "__main__":
  puk, prk = generate_keys()
  print(puk, prk)
  encrypted = encrypt("Hi", puk)
  print("Mensagem cifrada: %s" % encrypted)
  decrypted = decrypt(encrypted, prk)
  print("Mensagem decifrada: %s" % decrypted)
