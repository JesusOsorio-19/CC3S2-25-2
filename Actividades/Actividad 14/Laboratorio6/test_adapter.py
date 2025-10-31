#!/usr/bin/env python3
"""
Test simple del patrón Adapter
Demuestra cómo convertir null_resource a mock_cloud_bucket
"""

import json
import os
from iac_patterns.factory import NullResourceFactory
from iac_patterns.adapter import MockBucketAdapter
from iac_patterns.composite import CompositeModule
from iac_patterns.builder import InfrastructureBuilder


def test_basic_adapter():
    """Test básico: null_resource -> mock_cloud_bucket"""
    print("=== Test básico: Adapter simple ===\n")
    
    # Crear un null_resource normal
    null_res = NullResourceFactory.create(
        "storage_bucket",
        triggers={"region": "us-east-1", "versioning": "true"}
    )
    
    print("Null resource original:")
    print(json.dumps(null_res, indent=2))
    print()
    
    # Adaptarlo a bucket
    adapter = MockBucketAdapter(null_res)
    bucket = adapter.to_bucket()
    
    print("Mock bucket adaptado:")
    print(json.dumps(bucket, indent=2))
    print()
    
    return bucket


def test_adapter_in_composite():
    """Test: Usar adapter en un módulo compuesto"""
    print("=== Test: Adapter en Composite ===\n")
    
    composite = CompositeModule()
    
    # Crear varios null_resources y adaptarlos
    for i in range(3):
        null_res = NullResourceFactory.create(
            f"bucket_{i}",
            triggers={"environment": "dev", "index": i}
        )
        bucket = MockBucketAdapter(null_res).to_bucket()
        composite.add(bucket)
    
    result = composite.export()
    
    print("Módulo con buckets adaptados:")
    print(json.dumps(result, indent=2))
    print()
    
    return result


def test_adapter_in_builder():
    """Test: Integrar adapter en el Builder (requisito del desafío 3.2)"""
    print("=== Test: Adapter integrado en Builder ===\n")
    
    # Crear builder y agregar recursos normales
    builder = InfrastructureBuilder(env_name="adapter-demo")
    builder.build_null_fleet(count=2)
    
    # Agregar recursos adaptados usando el adapter
    for i in range(2):
        null_res = NullResourceFactory.create(
            f"data_lake_{i}",
            triggers={"tier": "hot", "zone": i}
        )
        bucket = MockBucketAdapter(null_res).to_bucket()
        builder._module.add(bucket)
    
    result = builder._module.export()
    
    print("Builder con recursos mixtos (null + adapted):")
    print(json.dumps(result, indent=2))
    print()
    
    # Contar recursos por tipo
    resource_types = {}
    for res_block in result.get("resource", []):
        for res_type in res_block.keys():
            resource_types[res_type] = resource_types.get(res_type, 0) + 1
    
    print("Resumen de recursos:")
    for res_type, count in resource_types.items():
        print(f"  {res_type}: {count}")
    print()
    
    return builder


def generate_files():
    """Genera archivos de salida"""
    print("=== Generando archivos ===\n")
    
    os.makedirs("terraform", exist_ok=True)
    
    # Test 1: Básico
    bucket = test_basic_adapter()
    with open("terraform/adapter_basic.tf.json", "w") as f:
        json.dump(bucket, f, indent=2)
    print("Generado: terraform/adapter_basic.tf.json\n")
    
    # Test 2: Composite
    composite = test_adapter_in_composite()
    with open("terraform/adapter_composite.tf.json", "w") as f:
        json.dump(composite, f, indent=2)
    print("Generado: terraform/adapter_composite.tf.json\n")
    
    # Test 3: Builder (cumple requisito del desafío)
    builder = test_adapter_in_builder()
    builder.export("terraform/adapter_builder.tf.json")

if __name__ == "__main__":
    generate_files()