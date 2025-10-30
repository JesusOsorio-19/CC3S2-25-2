from iac_patterns.singleton import ConfigSingleton

def test_reset():
    # Primera instancia
    c1 = ConfigSingleton("dev")
    created = c1.created_at
    
    # Agregamos configuración
    c1.set("x", 1)
    c1.set("y", 2)
    
    # Verificamos que se guardó
    assert c1.get("x") == 1
    assert c1.get("y") == 2
    
    # Reset
    c1.reset()
    
    # Validaciones
    assert c1.settings == {}, "Settings debe estar vacío"
    assert c1.created_at == created, "created_at debe mantenerse"
    assert c1.env_name == "dev", "env_name debe mantenerse"
    
    # Verificar que sigue siendo singleton
    c2 = ConfigSingleton("prod")  # Este parámetro se ignora
    assert c2 is c1, "Debe ser la misma instancia"
    assert c2.settings == {}, "La segunda referencia también debe ver settings vacío"
    
    print("Todas las pruebas pasaron")

if __name__ == "__main__":
    test_reset()