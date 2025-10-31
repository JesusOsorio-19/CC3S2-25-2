#!/usr/bin/env python3

import json
import os
from iac_patterns.factory import TimestampedNullResourceFactory

def test_timestamped_factory():
    """Genera recursos con diferentes formatos de timestamp"""
    
    # Test 1: Formato por defecto (YYYYMMDD)
    resource1 = TimestampedNullResourceFactory.create("daily_backup")
    print("=== Recurso con formato por defecto (%Y%m%d) ===")
    print(json.dumps(resource1, indent=2))
    print()
    
    # Test 2: Formato con fecha y hora
    resource2 = TimestampedNullResourceFactory.create(
        "hourly_snapshot", 
        fmt="%Y-%m-%d_%H:%M:%S"
    )
    print("=== Recurso con formato fecha-hora ===")
    print(json.dumps(resource2, indent=2))
    print()
    
    # Test 3: Formato solo año-mes
    resource3 = TimestampedNullResourceFactory.create(
        "monthly_report",
        fmt="%Y%m"
    )
    print("=== Recurso con formato año-mes ===")
    print(json.dumps(resource3, indent=2))
    print()
    
    # Test 4: Generar Terraform válido
    terraform_config = {
        "resource": []
    }
    
    # Agregar múltiples recursos con diferentes formatos
    for res in [resource1, resource2, resource3]:
        terraform_config["resource"].extend(res["resource"])
    
    # Guardar en directorio terraform
    os.makedirs("terraform", exist_ok=True)
    output_path = "terraform/timestamped_test.tf.json"
    
    with open(output_path, "w") as f:
        json.dump(terraform_config, f, indent=2)
    
    print(f"Archivo generado: {output_path}")

if __name__ == "__main__":
    test_timestamped_factory()