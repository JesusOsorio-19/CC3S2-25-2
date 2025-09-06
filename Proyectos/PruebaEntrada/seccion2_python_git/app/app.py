# Implementa la función summarize y el CLI.
# Requisitos:
# - summarize(nums) -> dict con claves: count, sum, avg
# - Valida que nums sea lista no vacía y elementos numéricos (acepta strings convertibles a float).
# - CLI: python -m app "1,2,3" imprime: sum=6.0 avg=2.0 count=3

def summarize(nums):  # TODO: tipado opcional
    if not isinstance(nums, list):
        raise TypeError("El input debe ser una lista.")
    
    if len(nums) == 0:
        raise ValueError("La lista no debe estar vacía.")
    
    # Convertir elementos a float y validar
    converted_nums = []
    for i, item in enumerate(nums):
        try:
            if isinstance(item, str):
                converted_nums.append(float(item))
            elif isinstance(item, (int, float)):
                converted_nums.append(float(item))
            else:
                raise ValueError(f"El elemento en la posición {i} no es convertible a número: {item}")
    
        except ValueError:
            raise ValueError(f"El elemento en la posición {i} no es convertible a número: {item}")
    
    count = len(converted_nums)
    total_sum = sum(converted_nums)
    avg = total_sum / count 

    return {
        "count": count,
        "sum": total_sum, 
        "avg": avg
    }

if __name__ == "__main__":
    import sys

    # Validar argumentos
    if len(sys.argv) != 2:
        print("Uso: python -m app \"1,2,3\"")
        sys.exit(1)

    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    items = [p.strip() for p in raw.split(",") if p.strip()]

    # TODO: validar items y llamar summarize, luego imprimir el formato solicitado
    
    try:
        # validar items y llamar summarize
        result = summarize(items)

        # imprimir el formato solicitado
        print(f"sum={result['sum']} avg={result['avg']} count={result['count']}")
    
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
