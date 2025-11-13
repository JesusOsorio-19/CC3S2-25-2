import pytest
from pathlib import Path

import main as iac_generator

@pytest.fixture
def base_name():
    """Base de prueba para los módulos."""
    return "test-project-bucket"

@pytest.fixture
def bucket_mod(base_name):
    """Retorna una instancia del módulo de bucket."""
    return iac_generator.StorageBucketModule(base_name)

@pytest.fixture
def access_mod(bucket_mod):
    """Retorna una instancia del módulo de acceso."""
    bucket_facade = bucket_mod.outputs()
    return iac_generator.StorageBucketAccessModule(
        bucket_facade, "test-entity", "TESTER"
    )

def test_bucket_resource_exists(bucket_mod):
    """
    Valida que 'bucket.tf.json' tiene 'resource.null_resource.storage_bucket'.
    """
    resources = bucket_mod.resource()
    
    assert "null_resource" in resources
    assert "storage_bucket" in resources["null_resource"]
    assert resources["null_resource"]["storage_bucket"] is not None

def test_bucket_access_dependency(access_mod):
    """
    Valida que 'bucket_access.tf.json' incluye 'depends_on' 
    apuntando a 'null_resource.storage_bucket'.
    """
    resources = access_mod.resource()
    
    assert "null_resource" in resources
    assert "bucket_access" in resources["null_resource"]
    
    bucket_access_resource = resources["null_resource"]["bucket_access"]
    
    assert "depends_on" in bucket_access_resource
    assert "null_resource.storage_bucket" in bucket_access_resource["depends_on"]

def test_bucket_triggers_match_facade(bucket_mod, base_name):
    """
    Valida que el trigger 'name' en el recurso bucket coincide
    con el 'name' expuesto en el facade (outputs).
    """
    facade_name = bucket_mod.outputs()["name"]
    trigger_name = bucket_mod.resource()["null_resource"]["storage_bucket"]["triggers"]["name"]
    
    assert trigger_name == facade_name
    assert base_name in facade_name # Verifica que el nombre base se usó

def test_access_triggers_match_facade(access_mod, bucket_mod):
    """
    Valida que el trigger 'bucket' en el recurso de acceso
    usa el 'name' proveído por el facade.
    """
    facade_name = bucket_mod.outputs()["name"]
    trigger_name = access_mod.resource()["null_resource"]["bucket_access"]["triggers"]["bucket"]
    
    assert trigger_name == facade_name